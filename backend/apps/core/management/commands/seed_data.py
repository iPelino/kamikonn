# ruff: noqa: E501
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
            {"name": "Arts & Culture", "slug": "arts", "icon": "palette"},
            {"name": "Career & Networking", "slug": "career", "icon": "users"},
            {"name": "Science & Engineering", "slug": "science", "icon": "flask-conical"},
            {"name": "Sports & Wellness", "slug": "sports", "icon": "activity"},
            {"name": "Social Impact", "slug": "social-impact", "icon": "heart"},
        ]
        categories_dict = {}
        for c_data in categories_data:
            cat, _ = Category.objects.get_or_create(**c_data)
            categories_dict[cat.slug] = cat

        # 4. Create Events
        now = timezone.now()
        events_data = [
            {
                "title": "ALU Africa Industrialization Day Panel",
                "description": "Join industry leaders and ALU students for a panel discussion on the future of industrialization across the African continent. Networking session to follow.",
                "start_time": now + timedelta(days=3, hours=10),
                "end_time": now + timedelta(days=3, hours=13),
                "location": "ALU Bumbogo Campus, Main Auditorium",
                "status": "APPROVED",
                "category": categories_dict["business"],
            },
            {
                "title": "Fintech Revolution in Kigali: A Student's Perspective",
                "description": "Explore how mobile money and digital banking are transforming Rwanda. Featuring guest speakers from BK Techouse and MTN Mobile Money.",
                "start_time": now + timedelta(days=5, hours=14),
                "end_time": now + timedelta(days=5, hours=16),
                "location": "Kigali Heights, 4th Floor",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Kigali Founders Mixer",
                "description": "An exclusive networking event for student founders from ALU, UR, and CMU-Africa to meet, share ideas, and find co-founders.",
                "start_time": now + timedelta(days=7, hours=18),
                "end_time": now + timedelta(days=7, hours=21),
                "location": "Norrsken House Kigali",
                "status": "APPROVED",
                "category": categories_dict["career"],
            },
            {
                "title": "Rwanda Python Meetup: ALU Edition",
                "description": "Monthly Python developer meetup. This session focuses on Django and building REST APIs. Beginners welcome!",
                "start_time": now + timedelta(days=2, hours=17),
                "end_time": now + timedelta(days=2, hours=19),
                "location": "ALU Bumbogo Campus, Room 102",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Public Speaking for Aspiring Leaders",
                "description": "A hands-on workshop designed to help students overcome stage fright and deliver compelling presentations.",
                "start_time": now + timedelta(days=12, hours=15),
                "end_time": now + timedelta(days=12, hours=18),
                "location": "Kigali Public Library",
                "status": "APPROVED",
                "category": categories_dict["career"],
            },
            {
                "title": "AI & Machine Learning: Future of Work",
                "description": "CMU-Africa professors discuss the implications of GenAI on the global job market and how students can prepare.",
                "start_time": now + timedelta(days=15, hours=10),
                "end_time": now + timedelta(days=15, hours=13),
                "location": "CMU-Africa Campus, Kigali Innovation City",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Art of Storytelling Workshop",
                "description": "Learn narrative techniques for writing, filmmaking, and marketing. Led by local Rwandan filmmakers.",
                "start_time": now + timedelta(days=8, hours=14),
                "end_time": now + timedelta(days=8, hours=17),
                "location": "L'Espace Kigali",
                "status": "APPROVED",
                "category": categories_dict["arts"],
            },
            {
                "title": "Norrsken Kigali Hackathon 2026",
                "description": "A 48-hour coding marathon to solve local challenges. Cash prizes for the top 3 teams. Open to all university students.",
                "start_time": now + timedelta(days=20, hours=9),
                "end_time": now + timedelta(days=22, hours=18),
                "location": "Norrsken House Kigali",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Pan-African Healthcare Innovations",
                "description": "Symposium on digital health startups in East Africa. Connect with med-tech innovators and researchers.",
                "start_time": now + timedelta(days=11, hours=9),
                "end_time": now + timedelta(days=11, hours=16),
                "location": "University of Rwanda, Remera Campus",
                "status": "APPROVED",
                "category": categories_dict["science"],
            },
            {
                "title": "CMU-Africa Robotics Showcase",
                "description": "Experience live demonstrations of autonomous drones and robotic arms built by engineering master's students.",
                "start_time": now + timedelta(days=18, hours=10),
                "end_time": now + timedelta(days=18, hours=15),
                "location": "CMU-Africa Campus",
                "status": "APPROVED",
                "category": categories_dict["science"],
            },
            {
                "title": "ALU Wellness Day: Yoga & Mental Health",
                "description": "Take a break from academics! Free yoga sessions, mindfulness workshops, and mental health resources.",
                "start_time": now + timedelta(days=4, hours=8),
                "end_time": now + timedelta(days=4, hours=12),
                "location": "ALU Bumbogo Campus, Courtyard",
                "status": "APPROVED",
                "category": categories_dict["sports"],
            },
            {
                "title": "Agri-Tech Startup Pitch",
                "description": "Students pitch their agricultural technology solutions to a panel of investors from the Rwanda Innovation Fund.",
                "start_time": now + timedelta(days=25, hours=14),
                "end_time": now + timedelta(days=25, hours=17),
                "location": "Camp Kigali",
                "status": "APPROVED",
                "category": categories_dict["business"],
            },
            {
                "title": "Kigali Tech Summit: Student Day",
                "description": "Special student-focused day at the Kigali Tech Summit. Discounted tickets, career fairs, and tech talks.",
                "start_time": now + timedelta(days=30, hours=9),
                "end_time": now + timedelta(days=30, hours=18),
                "location": "Kigali Convention Centre",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Women in Tech Rwanda Mentorship Circle",
                "description": "Connect with female leaders in Rwanda's tech ecosystem for an evening of mentorship and guidance.",
                "start_time": now + timedelta(days=14, hours=18),
                "end_time": now + timedelta(days=14, hours=20),
                "location": "Westerwelle Startup Haus Kigali",
                "status": "APPROVED",
                "category": categories_dict["career"],
            },
            {
                "title": "Data Science for Social Good",
                "description": "A workshop on leveraging data analytics to track and solve SDGs in Rwanda.",
                "start_time": now + timedelta(days=9, hours=13),
                "end_time": now + timedelta(days=9, hours=16),
                "location": "ALU Bumbogo Campus",
                "status": "APPROVED",
                "category": categories_dict["social-impact"],
            },
            {
                "title": "African Art & Photography Exhibition",
                "description": "A curated gallery of student artwork and photography celebrating East African culture.",
                "start_time": now + timedelta(days=22, hours=17),
                "end_time": now + timedelta(days=24, hours=17),
                "location": "Inema Arts Center",
                "status": "APPROVED",
                "category": categories_dict["arts"],
            },
            {
                "title": "UR Engineering Expo",
                "description": "University of Rwanda engineering students showcase their final year projects to the public and industry partners.",
                "start_time": now + timedelta(days=28, hours=9),
                "end_time": now + timedelta(days=28, hours=16),
                "location": "UR CST Campus, Nyarugenge",
                "status": "APPROVED",
                "category": categories_dict["science"],
            },
            {
                "title": "Climate Change & Sustainability Forum",
                "description": "Student-led discussions on sustainable living, green energy startups, and climate advocacy in Rwanda.",
                "start_time": now + timedelta(days=6, hours=14),
                "end_time": now + timedelta(days=6, hours=17),
                "location": "Kepler Campus",
                "status": "APPROVED",
                "category": categories_dict["social-impact"],
            },
            {
                "title": "Venture Capital 101 for Students",
                "description": "Demystifying fundraising, term sheets, and valuations for early-stage student founders.",
                "start_time": now + timedelta(days=16, hours=16),
                "end_time": now + timedelta(days=16, hours=18),
                "location": "Norrsken House Kigali",
                "status": "APPROVED",
                "category": categories_dict["business"],
            },
            {
                "title": "Web3 and Blockchain Seminar",
                "description": "Introduction to smart contracts, decentralized finance, and the future of blockchain in Africa.",
                "start_time": now + timedelta(days=19, hours=15),
                "end_time": now + timedelta(days=19, hours=18),
                "location": "ALU Bumbogo Campus",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Kigali Inter-University Coding Championship",
                "description": "Competitive programming contest. Universities face off to solve complex algorithms. Bragging rights on the line!",
                "start_time": now + timedelta(days=35, hours=9),
                "end_time": now + timedelta(days=35, hours=14),
                "location": "University of Kigali",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "Entrepreneurship Bootcamp by ALU",
                "description": "An intensive 2-day bootcamp covering customer discovery, lean canvas, and go-to-market strategies.",
                "start_time": now + timedelta(days=26, hours=9),
                "end_time": now + timedelta(days=27, hours=17),
                "location": "ALU Bumbogo Campus",
                "status": "APPROVED",
                "category": categories_dict["business"],
            },
            {
                "title": "Future of African Fashion Design",
                "description": "Panel discussion with local designers and a mini runway show featuring student collections.",
                "start_time": now + timedelta(days=13, hours=18),
                "end_time": now + timedelta(days=13, hours=21),
                "location": "Kigali Cultural Village",
                "status": "APPROVED",
                "category": categories_dict["arts"],
            },
            {
                "title": "Cybersecurity Awareness Workshop",
                "description": "Protect yourself online! Learn about phishing, secure passwords, and ethical hacking basics.",
                "start_time": now + timedelta(days=21, hours=14),
                "end_time": now + timedelta(days=21, hours=16),
                "location": "IPRC Kigali",
                "status": "APPROVED",
                "category": categories_dict["technology"],
            },
            {
                "title": "ALU Alumni Networking Gala",
                "description": "Connect with ALU alumni working across various sectors in Kigali. Dinner and drinks included.",
                "start_time": now + timedelta(days=40, hours=19),
                "end_time": now + timedelta(days=40, hours=23),
                "location": "Kigali Marriott Hotel",
                "status": "APPROVED",
                "category": categories_dict["career"],
            },
            {
                "title": "Urban Agriculture & Smart Cities",
                "description": "Exploring hydroponics, vertical farming, and IoT solutions for urban food security.",
                "start_time": now + timedelta(days=32, hours=10),
                "end_time": now + timedelta(days=32, hours=13),
                "location": "Rwanda Institute for Conservation Agriculture (RICA)",
                "status": "APPROVED",
                "category": categories_dict["science"],
            },
            {
                "title": "Student Leadership Conference",
                "description": "Empowering the next generation of African leaders with workshops on governance, ethics, and community organizing.",
                "start_time": now + timedelta(days=17, hours=9),
                "end_time": now + timedelta(days=17, hours=17),
                "location": "ALU Bumbogo Campus",
                "status": "APPROVED",
                "category": categories_dict["social-impact"],
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
