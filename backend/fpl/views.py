from django.shortcuts import render

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status

from fpl.serializers import ratingsSerializer, songsSerializer
from fpl.models import UserSquad

# Create your views here.
