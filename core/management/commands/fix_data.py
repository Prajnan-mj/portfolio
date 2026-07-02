"""
One-time data fix: reorder projects, fix timeline title.
Safe to run multiple times.
"""
from django.core.management.base import BaseCommand
from core.models import Project, TimelineEntry


class Command(BaseCommand):
    help = "Fix existing DB records: project order, timeline title."

    def handle(self, *args, **options):
        n1 = Project.objects.filter(title="Producty — AI productivity tool").update(order=1)
        n2 = Project.objects.filter(title="Traffic Violation Detector").update(order=2)
        n3 = TimelineEntry.objects.filter(title="MSc Mathematics (Integrated)").update(
            title="MSc Mathematics"
        )
        self.stdout.write(self.style.SUCCESS(
            f"Updated: Producty order={n1}, Traffic order={n2}, timeline title={n3}"
        ))
