from rest_framework import serializers
from .models import PlayerStat, MatchStat

class PlayerSerializer(serializers.ModelSerializer):
  class Meta:
    model = PlayerStat
    fields = '__all__'

class MatchSerializer(serializers.ModelSerializer):
  class Meta:
    model = MatchStat
    fields = '__all__'