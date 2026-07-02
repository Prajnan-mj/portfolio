from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ContactForm
from .models import BlogPost, Project, Skill, TimelineEntry


def home(request):
    skills = Skill.objects.all()
    skill_groups = {}
    for skill in skills:
        skill_groups.setdefault(skill.category, []).append(skill)

    context = {
        "projects": Project.objects.filter(featured=True),
        "skill_groups": skill_groups,
        "all_skills": skills,
        "timeline": TimelineEntry.objects.all(),
        "posts": BlogPost.objects.filter(published=True)[:3],
        "contact_form": ContactForm(),
    }
    return render(request, "core/home.html", context)


@require_POST
def contact(request):
    form = ContactForm(request.POST)
    if form.is_valid():
        message = form.save()
        try:
            send_mail(
                subject=f"[prajnan.dev] Message from {message.name}",
                message=f"From: {message.name} <{message.email}>\n\n{message.message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_TO_EMAIL],
                fail_silently=True,
            )
        except Exception:
            pass  # message is already stored in the database
        if request.headers.get("x-requested-with") == "fetch":
            return JsonResponse({"ok": True})
        return redirect("/#contact")

    if request.headers.get("x-requested-with") == "fetch":
        return JsonResponse({"ok": False, "errors": form.errors}, status=400)
    return redirect("/#contact")


def blog_list(request):
    posts = BlogPost.objects.filter(published=True)
    return render(request, "core/blog_list.html", {"posts": posts})


def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, published=True)
    return render(request, "core/blog_detail.html", {"post": post})


def robots_txt(request):
    lines = ["User-agent: *", "Allow: /", "Disallow: /admin/", ""]
    if request:
        lines.append(f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}")
    return HttpResponse("\n".join(lines), content_type="text/plain")
