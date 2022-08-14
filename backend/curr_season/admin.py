from django.contrib import admin
from .models import Matches, Players

# Register your models here.
@admin.register(Matches)
class MatchesAdmin(admin.ModelAdmin):
  list_display = ('match_id', 'team', 'season', 'date', 'time','gameweek', 'result','gf','ga',)
  search_fields = ('match_id', 'team', 'season', 'date', 'gameweek', 'result',)

@admin.register(Players)
class PlayersAdmin(admin.ModelAdmin):
  list_display = ('player', 'team', 'pos',)
  search_fields = ('player', 'team', 'pos',)