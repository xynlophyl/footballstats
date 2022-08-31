from django.core.management.base import BaseCommand
from fpl.models import Player
from utils.scrape_fpl_data import FPLScraper
from sqlalchemy import create_engine

class Command(BaseCommand):
  
  help = "Uses the Fantasy Premier League API (https://fantasy.premierleague.com/api/) to get basic information for current football players"

  def __init__(self):
    self.scraper = FPLScraper()

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')

    print(f'getting player information')

    players = self.scraper.get_players_information()

    players.to_sql(Player._meta.db_table, if_exists='replace', con=engine, index= True)
