from django.conf import settings
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path, re_path
from django.views.static import serve

from core.sitemaps import BlogSitemap, StaticSitemap

sitemaps = {"static": StaticSitemap, "blog": BlogSitemap}

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("core.urls")),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    # Media served by Django in all environments — fine at portfolio scale.
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
]
