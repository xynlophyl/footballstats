from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PlayerSerializer, TeamSerializer, FixtureSerializer, UserSquadSerializer
from .models import Player, Team, Fixture, UserSquad

# Create your views here.
class PlayerView(viewsets.ModelViewSet):
  serializer_class = PlayerSerializer
  queryset = Player.objects.all()

class TeamView(viewsets.ModelViewSet):
  serializer_class = TeamSerializer
  queryset = Team.objects.all()

class FixtureView(viewsets.ModelViewSet):
  serializer_class = FixtureSerializer
  queryset = Fixture.objects.all()

class SquadView(viewsets.ModelViewSet):
  serializer_class = UserSquadSerializer
  queryset = UserSquad.objects.all()