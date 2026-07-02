from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import BlogPost


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 1.0

    def items(self):
        return ["home", "blog_list"]

    def location(self, item):
        return reverse(item)


class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.7

    def items(self):
        return BlogPost.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at
