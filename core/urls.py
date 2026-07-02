from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
    path("writing/", views.blog_list, name="blog_list"),
    path("writing/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("robots.txt", views.robots_txt, name="robots_txt"),
]
