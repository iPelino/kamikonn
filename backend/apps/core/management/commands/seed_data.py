import os
import random
import string
from datetime import timedelta

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.events.models import Category, Event
from apps.universities.models import University

User = get_user_model()


class Command(BaseCommand):
    help = "Seed database with initial data for development"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting to seed data...")

        admin_password = os.getenv("KAMIKONN_SEED_PASSWORD")
        if not admin_password:
            admin_password = "".join(random.choices(string.ascii_letters + string.digits, k=12))

        admin, created = User.objects.get_or_create(
            email="admin@kamikonn.com",
            defaults={
                "first_name": "Kami",
                "last_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
            },
        )
        if created:
            admin.set_password(admin_password)
            admin.save()
            self.stdout.write(
                self.style.WARNING(f"Created Admin user: admin@kamikonn.com / {admin_password}")
            )

        organizer_password = os.getenv("KAMIKONN_SEED_PASSWORD")
        if not organizer_password:
            organizer_password = "".join(random.choices(string.ascii_letters + string.digits, k=12))

        organizer, created = User.objects.get_or_create(
            email="organizer@kamikonn.com",
            defaults={
                "first_name": "Demo",
                "last_name": "Organizer",
            },
        )
        if created:
            organizer.set_password(organizer_password)
            organizer.save()
            self.stdout.write(
                self.style.WARNING(
                    f"Created Organizer user: organizer@kamikonn.com / {organizer_password}"
                )
            )

        # 2. Create Universities
        universities_data = [
            {"name": "University of Rwanda", "short_name": "UR", "domain": "ur.ac.rw"},
            {
                "name": "African Leadership University",
                "short_name": "ALU",
                "domain": "alueducation.com",
            },
            {
                "name": "Carnegie Mellon University Africa",
                "short_name": "CMU",
                "domain": "africa.cmu.edu",
            },
            {
                "name": "Kigali Independent University",
                "short_name": "ULK",
                "domain": "ulk.ac.rw",
            },
            {
                "name": "Adventist University of Central Africa",
                "short_name": "AUCA",
                "domain": "auca.ac.rw",
            },
            {"name": "University of Kigali", "short_name": "UoK", "domain": "uok.ac.rw"},
            {
                "name": "Mount Kenya University Rwanda",
                "short_name": "MKUR",
                "domain": "mku.ac.rw",
            },
            {"name": "Davis College / Akilah", "short_name": "Davis", "domain": "daviscollege.com"},
            {"name": "Kepler", "short_name": "Kepler", "domain": "kepler.org"},
            {"name": "IPRC Kigali", "short_name": "IPRC", "domain": "iprckigali.rp.ac.rw"},
        ]
        universities = []
        for u_data in universities_data:
            univ, _ = University.objects.get_or_create(**u_data)
            universities.append(univ)

        # 3. Create Categories
        categories_data = [
            {"name": "Technology", "slug": "technology", "icon": "cpu"},
            {"name": "Business", "slug": "business", "icon": "briefcase"},
            {"name": "Arts", "slug": "arts", "icon": "palette"},
        ]
        categories = []
        for c_data in categories_data:
            cat, _ = Category.objects.get_or_create(**c_data)
            categories.append(cat)

        # 4. Create Events
        now = timezone.now()
        events_data = [
            {
                "title": "Tech Symposium 2026",
                "description": "Annual technology gathering for students across Kigali.",
                "start_time": now + timedelta(days=5),
                "end_time": now + timedelta(days=5, hours=8),
                "location": "Kigali Convention Centre",
                "status": "APPROVED",
                "category": categories[0],
            },
            {
                "title": "Startup Pitch Night",
                "description": "Watch student entrepreneurs pitch their latest startups.",
                "start_time": now + timedelta(days=10),
                "end_time": now + timedelta(days=10, hours=4),
                "location": "Norrsken House Kigali",
                "status": "APPROVED",
                "category": categories[1],
            },
            {
                "title": "Design Workshop",
                "description": "Learn the basics of UI/UX design with industry experts.",
                "start_time": now + timedelta(days=2),
                "end_time": now + timedelta(days=2, hours=3),
                "location": "ALU Bumbogo Campus",
                "status": "APPROVED",
                "category": categories[2],
            },
        ]

        for e_data in events_data:
            event, created = Event.objects.get_or_create(
                title=e_data["title"],
                defaults={
                    "description": e_data["description"],
                    "start_time": e_data["start_time"],
                    "end_time": e_data["end_time"],
                    "location": e_data["location"],
                    "status": e_data["status"],
                    "category": e_data["category"],
                    "organizer": organizer,
                },
            )
            if created:
                event.universities.add(random.choice(universities))

        self.stdout.write(self.style.SUCCESS("Successfully seeded demo data!"))
