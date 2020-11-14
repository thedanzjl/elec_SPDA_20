"""microservices URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from calendarapp import views as calendar_views
from themes import views as themes_views


urlpatterns = [

    path('themes/colors/', themes_views.colors),
    path('colors/', themes_views.colors),
    path('calendar/time/', calendar_views.time_view),
    path('calendar/date/', calendar_views.date_view),
    path('time/', calendar_views.time_view),
    path('date/', calendar_views.date_view),
]
