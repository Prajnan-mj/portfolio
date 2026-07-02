from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class SiteProfile(models.Model):
    """Single row holding everything editable about the site owner."""

    BACKGROUND_CHOICES = [
        ("a", "Breathing (A)"),
        ("b", "Drift (B)"),
        ("c", "Journey (C)"),
    ]

    name = models.CharField(max_length=100, default="Prajnan MJ")
    site_name = models.CharField(max_length=100, default="prajnan.dev")
    eyebrow = models.CharField(
        max_length=200,
        default="Applied AI · Full-stack engineering",
        help_text="Small mono label above the hero headline.",
    )
    intro = models.TextField(
        default=(
            "I build computer-vision and LLM systems that hold up in "
            "production — detection pipelines, AI assistants, and the "
            "full stack around them."
        )
    )
    about = models.TextField(
        default=(
            "Software developer specializing in applied AI and full-stack "
            "engineering. YOLOv8, LLMs, FastAPI, React — building things "
            "that work in production."
        ),
        help_text="Large serif statement in the About section.",
    )
    currently = models.CharField(
        max_length=250,
        blank=True,
        default="MSc Mathematics @ BITS Pilani, K K Birla Goa Campus (2025–2030)",
        help_text="One-line 'currently' note under the About statement.",
    )
    email = models.EmailField(default="mj.prajnan@gmail.com")
    github_url = models.URLField(default="https://github.com/Prajnan-mj")
    linkedin_url = models.URLField(
        default="https://www.linkedin.com/in/prajnan-m-j-82798630b/"
    )
    resume = models.FileField(
        upload_to="resume/",
        blank=True,
        help_text="Upload a PDF. Note: on Render's free tier uploaded files "
        "reset on redeploy — a resume URL below is more durable.",
    )
    resume_url = models.URLField(
        blank=True,
        help_text="Alternative to uploading: link to a hosted resume "
        "(Google Drive, GitHub, etc.). Used if no file is uploaded.",
    )
    availability = models.CharField(
        max_length=250,
        default="Open to roles and collaborations in applied AI and full-stack engineering.",
    )
    background_theme = models.CharField(
        max_length=1, choices=BACKGROUND_CHOICES, default="a",
        help_text="Which neural-mesh background strip to use site-wide.",
    )
    meta_description = models.CharField(
        max_length=300,
        default=(
            "Prajnan MJ — software developer specializing in applied AI and "
            "full-stack engineering. YOLOv8, LLMs, FastAPI, React, Django."
        ),
    )

    class Meta:
        verbose_name = "site profile"
        verbose_name_plural = "site profile"

    def __str__(self):
        return self.name

    @property
    def resume_href(self):
        if self.resume:
            return self.resume.url
        return self.resume_url or ""


class Skill(models.Model):
    name = models.CharField(max_length=80)
    category = models.CharField(
        max_length=80,
        default="Other",
        help_text="Group label, e.g. 'AI / ML', 'Backend', 'Frontend', 'Tools'.",
    )
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.name


class Project(models.Model):
    title = models.CharField(max_length=200)
    tag = models.CharField(
        max_length=100,
        blank=True,
        help_text="Mono label in the left column, e.g. 'Computer vision · 2025'.",
    )
    description = models.TextField()
    stack = models.CharField(
        max_length=300,
        blank=True,
        help_text="Comma-separated technologies, e.g. 'YOLOv8, Python, OpenCV'.",
    )
    github_url = models.URLField(blank=True)
    live_url = models.URLField(blank=True)
    image = models.ImageField(
        upload_to="projects/",
        blank=True,
        help_text="Optional preview image, revealed on hover. On Render's "
        "free tier uploads reset on redeploy; the static path below survives.",
    )
    image_static = models.CharField(
        max_length=200,
        blank=True,
        help_text="Path under static/, e.g. 'img/projects/producty.webp'. "
        "Used when no image is uploaded.",
    )
    featured = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def stack_list(self):
        return [s.strip() for s in self.stack.split(",") if s.strip()]

    @property
    def primary_url(self):
        return self.live_url or self.github_url or ""


class TimelineEntry(models.Model):
    KIND_CHOICES = [
        ("education", "Education"),
        ("experience", "Experience"),
        ("project", "Project"),
        ("award", "Award"),
    ]

    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default="experience")
    period = models.CharField(
        max_length=60, help_text="e.g. '2025 — 2030' or '2025 — Present'."
    )
    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=200, blank=True)
    description = models.TextField(blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name_plural = "timeline entries"

    def __str__(self):
        return f"{self.period} — {self.title}"


class BlogPost(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    excerpt = models.TextField(
        blank=True, help_text="Short summary shown in lists and meta tags."
    )
    body = models.TextField(help_text="Plain text; blank lines start new paragraphs.")
    published = models.BooleanField(default=True)
    published_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:250]
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog_detail", kwargs={"slug": self.slug})

    @property
    def reading_minutes(self):
        return max(1, round(len(self.body.split()) / 200))


class ContactMessage(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} <{self.email}> — {self.created_at:%Y-%m-%d %H:%M}"
