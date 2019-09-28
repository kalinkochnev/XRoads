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

from forum.views import HomeView, ListPosts, PostDetails, QuerySchoolClass, CreatePostView
from . import views

# for passing context into class views
from forum.models import SubForum

app_name = 'forumsapp'
urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('forum/<str:forum_name>/', ListPosts.as_view(), name='forum'),
    path('forum/<str:forum_name>/<int:post_id>/', PostDetails.as_view(), name='forum_post'),
    path('post/<int:post_id>/', PostDetails.as_view(), name='post'),
    path('forum/post/create/', CreatePostView.as_view(), name="post/create"),
    path('tos/', views.terms_of_service, name='tos'),
    path('privacy/', views.privacy_policy, name='pp'),
    path('query/classes', QuerySchoolClass.as_view(), name="query/classes")
]
