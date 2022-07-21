from tkinter import CASCADE
from turtle import ondrag
from django.db import models

# Create your models here.

# General Information

# class LeagueInfo(models.Model):
  # pass

class TeamInfo(models.Model):
  team_id = models.CharField('id', max_length=3, primary_key=True)
  team_name = models.CharField('name', max_length=255)
  fbref = models.CharField('fbref link', max_length=255)


class PlayerInfo(models.Model):
  player_name = models.CharField('name', max_length=255)
  team_name = models.CharField('team', max_length=255)
  dob = models.DateField('date of birth')

# Statistical information
class TeamStats(models.Model):
  team_id = models.ForeignKey('id', TeamInfo, on_delete=models.CASCADE)


class MatchStats(models.Models):
  pass

class PlayerStats(models.Model):
  id = models.ForeignKey(PlayerInfo, on_delete=models.CASCADE)