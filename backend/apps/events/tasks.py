import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives, send_mail

from apps.events.models import RSVP

User = get_user_model()

logger = logging.getLogger(__name__)


def _build_ics(event) -> str:
    """Build a minimal iCalendar string for an event."""
    # Event model uses start_time / end_time
    dt_start = event.start_time.strftime("%Y%m%dT%H%M%SZ") if event.start_time else ""
    dt_end = event.end_time.strftime("%Y%m%dT%H%M%SZ") if event.end_time else dt_start
    location = getattr(event, "location", "") or ""
    frontend_url = getattr(settings, "FRONTEND_URL", "https://kamikonn.rw")
    return (
        "BEGIN:VCALENDAR\r\n"
        "VERSION:2.0\r\n"
        "PRODID:-//KamiKonn//EN\r\n"
        "BEGIN:VEVENT\r\n"
        f"SUMMARY:{event.title}\r\n"
        f"DTSTART:{dt_start}\r\n"
        f"DTEND:{dt_end}\r\n"
        f"LOCATION:{location}\r\n"
        f"DESCRIPTION:View event: {frontend_url}/events/{event.slug}\r\n"
        "END:VEVENT\r\n"
        "END:VCALENDAR\r\n"
    )


@shared_task
def send_rsvp_confirmation_email(user_id: int, event_id: int, status: str):
    """Send an RSVP confirmation email with an .ics calendar attachment."""
    from apps.events.models import Event
    from apps.notifications.models import NotificationPreference

    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        logger.error("User %s not found for RSVP email.", user_id)
        return

    prefs, _ = NotificationPreference.objects.get_or_create(user=user)
    if not prefs.rsvp_confirmation:
        logger.info("RSVP confirmation email suppressed for user %s (preference off).", user_id)
        return

    try:
        event = Event.objects.get(id=event_id)
    except Event.DoesNotExist:
        logger.error("Event %s not found for RSVP email.", event_id)
        return

    frontend_url = getattr(settings, "FRONTEND_URL", "https://kamikonn.rw")
    subject = f"RSVP Confirmation: {event.title}"

    if status == "ATTENDING":
        plain_body = (
            f"Hi {user.username},\n\n"
            f"You have successfully RSVP'd to {event.title}. "
            "We look forward to seeing you there!\n\n"
            f"View event: {frontend_url}/events/{event.slug}"
        )
        html_body = (
            f"<p>Hi {user.username},</p>"
            f"<p>You have successfully RSVP'd to <strong>{event.title}</strong>. "
            "We look forward to seeing you there!</p>"
            f'<p><a href="{frontend_url}/events/{event.slug}">View event details</a></p>'
        )
    else:
        plain_body = (
            f"Hi {user.username},\n\n"
            f"You have been placed on the waitlist for {event.title}. "
            "We will notify you if a spot opens up.\n\n"
            f"View event: {frontend_url}/events/{event.slug}"
        )
        html_body = (
            f"<p>Hi {user.username},</p>"
            f"<p>You have been placed on the waitlist for <strong>{event.title}</strong>. "
            "We will notify you if a spot opens up.</p>"
            f'<p><a href="{frontend_url}/events/{event.slug}">View event details</a></p>'
        )

    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=plain_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[user.email],
        )
        email.attach_alternative(html_body, "text/html")

        # Attach .ics calendar file
        ics_content = _build_ics(event)
        email.attach(
            filename=f"{event.slug}.ics",
            content=ics_content,
            mimetype="text/calendar",
        )

        email.send(fail_silently=False)
        logger.info("RSVP confirmation email sent to %s", user.email)
    except Exception as exc:
        logger.error("Failed to send RSVP email: %s", exc)


@shared_task
def send_event_reminder_email(user_id: int, event_title: str):
    try:
        user = User.objects.get(id=user_id)
        subject = f"Reminder: {event_title} is tomorrow!"
        message = (
            f"Hi {user.username},\n\n"
            f"This is a reminder that {event_title} is happening tomorrow. "
            "Don't miss it!"
        )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info("Reminder email sent to %s", user.email)
    except User.DoesNotExist:
        logger.error("User %s not found for reminder email.", user_id)
    except Exception as exc:
        logger.error("Failed to send reminder email: %s", exc)


@shared_task
def schedule_event_reminders():
    from django.utils import timezone

    from apps.events.models import Event, RSVPStatus

    now = timezone.now()
    start_window = now + timedelta(hours=23, minutes=30)
    end_window = now + timedelta(hours=24, minutes=30)

    upcoming_events = Event.objects.filter(
        start_time__gte=start_window,
        start_time__lt=end_window,
    )

    for event in upcoming_events:
        attendees = RSVP.objects.filter(event=event, status=RSVPStatus.ATTENDING)
        for rsvp in attendees:
            send_event_reminder_email.delay(rsvp.user.id, event.title)

    logger.info("Scheduled reminders for %s events.", upcoming_events.count())


@shared_task
def notify_followers_new_event(event_id: int):
    """Notify all followers of an event's organizer about a new event.

    Requires the FollowedOrganizer model in apps.organizers.models.
    If the model does not exist (not yet migrated), the task exits silently.
    """
    from apps.events.models import Event
    from apps.notifications.models import NotificationPreference

    try:
        from apps.organizers.models import FollowedOrganizer
    except ImportError:
        logger.warning("notify_followers_new_event: FollowedOrganizer model not found. Skipping.")
        return

    try:
        event = Event.objects.select_related("organizer").get(id=event_id)
    except Event.DoesNotExist:
        logger.error("notify_followers_new_event: Event %s not found.", event_id)
        return

    organizer = event.organizer
    frontend_url = getattr(settings, "FRONTEND_URL", "https://kamikonn.rw")

    followers = FollowedOrganizer.objects.filter(organizer=organizer).select_related("user")

    notified = 0
    for follow in followers:
        follower = follow.user
        prefs, _ = NotificationPreference.objects.get_or_create(user=follower)
        if not prefs.new_from_followed:
            continue

        subject = f"New event from {organizer.get_full_name() or organizer.username}: {event.title}"
        message = (
            f"Hi {follower.username},\n\n"
            f"{organizer.get_full_name() or organizer.username} has published a new event: "
            f"{event.title}.\n\n"
            f"View event: {frontend_url}/events/{event.slug}"
        )
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[follower.email],
                fail_silently=False,
            )
            notified += 1
        except Exception as exc:
            logger.error("Failed to notify follower %s: %s", follower.email, exc)

    logger.info(
        "notify_followers_new_event: notified %s followers for event %s.", notified, event_id
    )
