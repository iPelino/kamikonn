import logging
from datetime import timedelta

from celery import shared_task
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import send_mail

from apps.events.models import RSVP

User = get_user_model()

logger = logging.getLogger(__name__)


@shared_task
def send_rsvp_confirmation_email(user_id: int, event_title: str, status: str):
    try:
        user = User.objects.get(id=user_id)
        subject = f"RSVP Confirmation: {event_title}"
        if status == "ATTENDING":
            message = (
                f"Hi {user.username},\n\n"
                f"You have successfully RSVP'd to {event_title}. "
                "We look forward to seeing you there!"
            )
        else:
            message = (
                f"Hi {user.username},\n\n"
                f"You have been placed on the waitlist for {event_title}. "
                "We will notify you if a spot opens up."
            )

        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        logger.info(f"RSVP confirmation email sent to {user.email}")
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for RSVP email.")
    except Exception as e:
        logger.error(f"Failed to send RSVP email: {str(e)}")


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
        logger.info(f"Reminder email sent to {user.email}")
    except User.DoesNotExist:
        logger.error(f"User {user_id} not found for reminder email.")
    except Exception as e:
        logger.error(f"Failed to send reminder email: {str(e)}")


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

    logger.info(f"Scheduled reminders for {upcoming_events.count()} events.")
