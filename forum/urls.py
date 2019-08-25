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
from django.urls import path, re_path

from forum.views import CreatePostView, HomeView, ListPosts, PostDetails
from . import views

# for passing context into class views
from forum.models import SubForum

app_name = 'forumsapp'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('forum/<str:forum_name>/', ListPosts.as_view(), name='forum'),
    path('forum/<str:forum_name>/<int:post_id>/', PostDetails.as_view(), name='forum_post'),
    path('post/<int:post_id>/', PostDetails.as_view(), name='post'),
    path('create-post/', CreatePostView.as_view(), name='create_post'),
]
