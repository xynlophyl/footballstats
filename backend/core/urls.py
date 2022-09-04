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
router.register(r'curr_season/players', curr_view.PlayerView, 'curr_season/players')
router.register(r'curr_season/matches', curr_view.MatchView, 'curr_season/matches')


# PREVIOUS SEASON API URLS

# FPL API URLS
router.register(r'fpl/players', fpl_view.PlayerView, 'fpl/players')
router.register(r'fpl/teams', fpl_view.TeamView, 'fpl/teams')
router.register(r'fpl/fixtures', fpl_view.FixtureView, 'fpl/fixtures')
router.register(r'fpl/squads', fpl_view.SquadView, 'fpl/squads')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

