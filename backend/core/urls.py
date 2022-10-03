"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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

from rest_framework import routers
from curr_season import views as curr_view
from fpl import views as fpl_view

router = routers.DefaultRouter()
# router.register(r'curr', curr_view.PlayerView, 'curr')

# CURRENT SEASON API URLS
router.register(r'curr_season/player', curr_view.PlayerView, 'curr_season/player')
router.register(r'curr_season/match', curr_view.MatchView, 'curr_season/match')


# PREVIOUS SEASON API URLS

# FPL API URLS
router.register(r'fpl/player', fpl_view.PlayerView, 'fpl/player')
router.register(r'fpl/team', fpl_view.TeamView, 'fpl/team')
router.register(r'fpl/fixture', fpl_view.FixtureView, 'fpl/fixture')
router.register(r'fpl/squad', fpl_view.SquadView, 'fpl/squad')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

