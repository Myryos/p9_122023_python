"""Litrevu URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path


import authentication.views

import reviewsys.views


urlpatterns = [
    path("admin/", admin.site.urls),
    path("login/", authentication.views.login_page, name="login"),
    path("signup/", authentication.views.signup, name="signup"),
    path("home/", reviewsys.views.flow, name="home"),
    path("posts/", reviewsys.views.posts, name="posts"),
    path("logout/", authentication.views.logout_view, name="logout"),
    path("new_ticket/", reviewsys.views.ticket_create, name="new_ticket"),
    path(
        "new_review/<int:ticket_id>/", reviewsys.views.review_create, name="new_review"
    ),
    path(
        "update_ticket/<int:ticket_id>/",
        reviewsys.views.ticket_update,
        name="update_ticket",
    ),
    path(
        "update_review/<int:review_id>/",
        reviewsys.views.review_update,
        name="update_review",
    ),
    path(
        "delete_ticket/<int:ticket_id>",
        reviewsys.views.ticket_delete,
        name="delete_ticket",
    ),
    path(
        "delete_review/<int:review_id>",
        reviewsys.views.review_delete,
        name="delete_review",
    ),
    path(
        "tikectreview/", reviewsys.views.ticket_review_create, name="new_ticket_review"
    ),
    path("abonnements/", reviewsys.views.abonnements_view, name="abonnements"),
    path("follow/<str:username>/", reviewsys.views.follow_user, name="follow_user"),
    path(
        "unfollow/<str:username>/", reviewsys.views.unfollow_user, name="unfollow_user"
    ),
    path(
        "search_not_followed_user/<str:input_string>",
        reviewsys.views.search_not_followed_user,
        name="search not followed user",
    ),
]
