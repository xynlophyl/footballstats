from django.db import models

# Create your models here.
class Player(models.Model):
  player_id = models.IntegerField(primary_key=True)
  first_name = models.CharField(max_length=255)
  second_name = models.CharField(max_length=255)
  known_as = models.CharField(max_length=255)
  image = models.URLField()
  team_id = models.IntegerField()
  position = models.IntegerField()
  fpl_cost = models.IntegerField()
  fpl_total_points = models.IntegerField()
  fpl_form = models.IntegerField()

class Team(models.Model):
  team_id = models.IntegerField(primary_key=True)
  name = models.CharField(max_length=255)
  short_name = models.CharField(max_length=255)
  strength = models.IntegerField()
  strength_overall_home = models.IntegerField()
  strength_overall_away = models.IntegerField()
  strength_attack_home= models.IntegerField()
  strength_attack_away = models.IntegerField()
  strength_defence_home = models.IntegerField()
  strength_defence_away = models.IntegerField()

class Fixture(models.Model):
  match_id = models.IntegerField(primary_key=True)
  season = models.CharField(max_length=255)
  gw = models.IntegerField()
  home_id = models.IntegerField()
  away_id = models.IntegerField()
  finished = models.BooleanField()

class UserSquad(models.Model):
  squad_id = models.CharField(max_length=255, primary_key=True)
  user = models.IntegerField()
  gameweek = models.IntegerField()
  player = models.IntegerField()
  starter = models.BooleanField()
  is_captain = models.BooleanField()
  is_vice_captain = models.BooleanField()

class Gameweek(models.Model):
  gameweek = models.IntegerField()
  
  

  
  