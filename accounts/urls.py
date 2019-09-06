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
from django.urls import path

from accounts.views import LoginClass, SignupClass, AccountView
from . import views

urlpatterns = [
    path('login/', LoginClass.as_view(), name='login'),
    path('logout/', views.view_logout, name='logout'),
    path('signup/', SignupClass.as_view(), name="signup"),
    path('account/', AccountView.as_view(), name='account'),
    path('chgpass/', views.chgpass, name='chgpass'),
    path('chgusername/', views.chgusername, name='chgusername'),
    path('chgtag/', views.chgtag, name='chgtag'),
]
