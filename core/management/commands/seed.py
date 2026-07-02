"""
Seed the database with initial content.

Idempotent and non-destructive: uses get_or_create only, so anything
edited later in the admin is never overwritten by a redeploy.
"""
import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from core.models import BlogPost, Project, SiteProfile, Skill, TimelineEntry


class Command(BaseCommand):
    help = "Seed initial portfolio content (safe to run repeatedly)."

    def handle(self, *args, **options):
        created = []

        if not SiteProfile.objects.exists():
            SiteProfile.objects.create()
            created.append("site profile")

        projects = [
            dict(
                title="Producty — AI productivity tool",
                tag="Applied AI · 2025",
                description=(
                    "Task management, calendar sync, habit tracking and highly "
                    "stylized notes, with an AI assistant that plans your day, "
                    "analyzes documents and drafts emails. Built with FastAPI, "
                    "React, NVIDIA NIM (LLaMA 3.3 70B) and PostgreSQL."
                ),
                stack="FastAPI, React 19, NVIDIA NIM, LLaMA 3.3, PostgreSQL, Docker",
                github_url="https://github.com/Prajnan-mj/Producty-AI-Based-Productivity-tool",
                live_url="https://producty-web.onrender.com",
                image_static="img/projects/producty.webp",
                order=1,
            ),
            dict(
                title="Traffic Violation Detector",
                tag="Computer vision · 2025",
                description=(
                    "A modular traffic-violation pipeline that eliminates false "
                    "positives with geometric gating — a COCO pass finds vehicles, "
                    "then helmet and triple-riding detections are validated against "
                    "vehicle 'rider zones' before a violation is logged. Detected "
                    "coordinates are reused to crop and OCR license plates. Ships "
                    "with a Streamlit UI and Docker setup."
                ),
                stack="YOLOv8, Python, OpenCV, OCR, Streamlit, Docker",
                github_url="https://github.com/Prajnan-mj/Traffic-Violation-Detector",
                image_static="img/projects/traffic.webp",
                order=2,
            ),
        ]
        for data in projects:
            _, was_created = Project.objects.get_or_create(
                title=data["title"], defaults=data
            )
            if was_created:
                created.append(f"project: {data['title']}")

        skills = [
            ("AI / ML", ["YOLOv8", "OpenCV", "LLM integration", "NVIDIA NIM", "OCR pipelines"]),
            ("Backend", ["Python", "FastAPI", "Django", "PostgreSQL", "REST APIs"]),
            ("Frontend", ["React", "JavaScript", "HTML / CSS", "Streamlit"]),
            ("Tools", ["Docker", "Git", "Linux"]),
        ]
        order = 0
        for category, names in skills:
            for name in names:
                order += 10
                _, was_created = Skill.objects.get_or_create(
                    name=name, category=category, defaults={"order": order}
                )
                if was_created:
                    created.append(f"skill: {name}")

        timeline = [
            dict(
                kind="education",
                period="2025 — 2030",
                title="MSc Mathematics",
                organization="BITS Pilani, K K Birla Goa Campus",
                description=(
                    "Five-year integrated Master of Science in Mathematics, "
                    "building the theoretical foundation behind the applied-AI work."
                ),
                order=1,
            ),
            dict(
                kind="project",
                period="2025",
                title="Traffic Violation Detector",
                organization="Personal project",
                description=(
                    "Computer-vision pipeline for helmet and triple-riding "
                    "violations with geometric gating and license-plate OCR."
                ),
                order=2,
            ),
            dict(
                kind="project",
                period="2025",
                title="Producty",
                organization="Personal project",
                description=(
                    "AI-powered productivity suite — planning assistant, document "
                    "analysis and email drafting on NVIDIA NIM (LLaMA 3.3 70B)."
                ),
                order=3,
            ),
        ]
        for data in timeline:
            _, was_created = TimelineEntry.objects.get_or_create(
                title=data["title"], period=data["period"], defaults=data
            )
            if was_created:
                created.append(f"timeline: {data['title']}")

        if not BlogPost.objects.exists():
            BlogPost.objects.create(
                title="Hello, world",
                excerpt="Why this site exists and what I'll write about here.",
                body=(
                    "This is the first post on prajnan.dev — a place to write "
                    "about applied AI, computer vision and the full-stack "
                    "engineering around it.\n\n"
                    "Expect notes on YOLOv8 detection pipelines, working with "
                    "LLMs in production, and the occasional deep dive into the "
                    "mathematics underneath.\n\n"
                    "This post is a seeded placeholder — edit or delete it from "
                    "the Django admin."
                ),
            )
            created.append("blog post: Hello, world")

        # Optional superuser from environment (useful on Render).
        User = get_user_model()
        su_name = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        su_pass = os.environ.get("DJANGO_SUPERUSER_PASSWORD")
        if su_name and su_pass and not User.objects.filter(username=su_name).exists():
            User.objects.create_superuser(
                username=su_name,
                email=os.environ.get("DJANGO_SUPERUSER_EMAIL", ""),
                password=su_pass,
            )
            created.append(f"superuser: {su_name}")

        if created:
            self.stdout.write(self.style.SUCCESS("Seeded: " + ", ".join(created)))
        else:
            self.stdout.write("Nothing to seed — all content already exists.")
