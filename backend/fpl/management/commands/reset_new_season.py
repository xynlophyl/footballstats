from django.core.management.base import BaseCommand
from fpl.models import UserSquad, Gameweek
class Command(BaseCommand):
  
  help = "Clears data from User Squad and Gameweek models"

  def handle(self, *args, **kwargs):
    print(f'clearing data from User Squad and Gameweek models')
    
    UserSquad.objects.all().delete()
    Gameweek.objects.all().delete()
    
