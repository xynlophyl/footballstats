from django.shortcuts import render
from rest_framework import viewsets
from .serializers import PlayerSerializer, MatchSerializer
from .models import PlayerStat, MatchStat

# Create your views here.
class PlayerView(viewsets.ModelViewSet):
  serializer_class = PlayerSerializer
  queryset = PlayerStat.objects.all()

class MatchView(viewsets.ModelViewSet):
  serializer_class = MatchSerializer
  queryset = MatchStat.objects.all()