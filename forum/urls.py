"""XRoads URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('forum/', views.show_posts, name='forums'),
    path('post/', views.show_post, name='post'),
    path('create-post/', views.create_post, name='create_post'),
    # path('forum/<str: name>', views.spec_forum, name='spec_forum'),
    # path('forum/<str: name>/post/<int: id>', views.forum_post, name='forum_post'),
    path('tos/', views.terms_of_service, name='tos'),
    path('privacy/', views.privacy_policy, name='pp'),
    # TODO add easier to read urls
]
