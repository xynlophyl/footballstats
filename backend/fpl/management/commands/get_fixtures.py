from django.core.management.base import BaseCommand
from fpl.models import Fixture
from utils.scrape_fpl_data import FPLScraper
from sqlalchemy import create_engine

class Command(BaseCommand):
  
  help = "Uses the Fantasy Premier League API (https://fantasy.premierleague.com/api/) to get the season's fixtures"

  def __init__(self):
    self.scraper = FPLScraper()

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')

    print(f'getting fixtures for the current season')

    fixtures = self.scraper.get_fixtures()

    fixtures.to_sql(Fixture._meta.db_table, if_exists='replace', con=engine, index= True)


