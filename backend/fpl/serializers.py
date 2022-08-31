from rest_framework import serializers
from fpl.models import UserSquad

class UserSquadSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserSquad
    fields = ('squad_id', 'user', 'gameweek', 'player', 'starter', 'is_captain', 'is_vice_captain')
    