from rest_framework import serializers
from fpl.models import Player, Team, Fixture, UserSquad, Gameweek

class PlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Player
    fields = '__all__'

class TeamSerializer(serializers.ModelSerializer):
  class Meta:
    model = Team
    fields = '__all__'

class FixtureSerializer(serializers.ModelSerializer):
  class Meta:
    model = Fixture
    fields = '__all__'

class UserSquadSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserSquad
    fields = ('squad_id', 'user', 'gameweek', 'player', 'starter', 'is_captain', 'is_vice_captain')
