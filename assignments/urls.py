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
from django.urls import path, include

from assignments.views import AllQuizzesView
from . import views

from django.conf.urls import url

# for passing context into class views

app_name = 'forumsapp'
urlpatterns = [
    path('my-assignments/', AllQuizzesView.as_view(), name='quizhome'),
    path('quiz/<int: quiz_id>', AllQuizzesView.as_view(), name='quiz'),
]
