from django.contrib import admin
from .models import Player, Team, Fixture, UserSquad, Gameweek

# Register your models here.
@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
  list_display = ('player_id', 'first_name', 'second_name', 'known_as', 'team_id', 'image', 'position')
  search_fields = ('player_id', 'first_name', 'second_name', 'known_as', 'team_id', 'position')

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
  list_display = ('team_id', 'name', 'short_name',)
  search_fields = ('team_id', 'name', 'short_name',)

@admin.register(Fixture)
class FixtureAdmin(admin.ModelAdmin):
  list_display = ('match_id', 'season', 'gw', 'home_id', 'away_id', 'finished',)
  search_fields = ('match_id', 'season', 'gw', 'home_id', 'away_id', 'finished',)

@admin.register(UserSquad)
class SquadAdmin(admin.ModelAdmin):
  list_display = ('squad_id', 'user', 'gameweek', 'player',)
  search_fields = ('squad_id', 'user', 'gameweek', 'player',)

@admin.register(Gameweek)
class GameweekAdmin(admin.ModelAdmin):
  list_display = ('gameweek',)
  search_fields = ('gameweek',)