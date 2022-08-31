from django.contrib import admin
from .models import MatchStat, PlayerStat

# Register your models here.
@admin.register(MatchStat)
class MatchStatAdmin(admin.ModelAdmin):
  list_display = ('match_id', 'team', 'season', 'date', 'time','gameweek', 'result','gf','ga',)
  search_fields = ('match_id', 'team', 'season', 'date', 'gameweek', 'result',)

@admin.register(PlayerStat)
class PlayerStatAdmin(admin.ModelAdmin):
  list_display = ('player', 'team', 'pos',)
  search_fields = ('player', 'team', 'pos',)