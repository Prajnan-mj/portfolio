from django.contrib import admin

from .models import (
    BlogPost,
    ContactMessage,
    Project,
    SiteProfile,
    Skill,
    TimelineEntry,
)

admin.site.site_header = "Prajnan MJ — Portfolio Admin"
admin.site.site_title = "prajnan.dev admin"
admin.site.index_title = "Content"


@admin.register(SiteProfile)
class SiteProfileAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Keep it a singleton: allow adding only when no profile exists yet.
        return not SiteProfile.objects.exists()


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "order")
    list_editable = ("category", "order")
    list_filter = ("category",)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ("title", "tag", "featured", "order")
    list_editable = ("featured", "order")


@admin.register(TimelineEntry)
class TimelineEntryAdmin(admin.ModelAdmin):
    list_display = ("period", "title", "organization", "kind", "order")
    list_editable = ("order",)
    list_filter = ("kind",)


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "published", "published_at", "reading_minutes")
    list_filter = ("published",)
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_at"


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "created_at", "is_read")
    list_editable = ("is_read",)
    list_filter = ("is_read",)
    readonly_fields = ("name", "email", "message", "created_at")

    def has_add_permission(self, request):
        return False
