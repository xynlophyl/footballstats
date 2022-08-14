from django.core.management.base import BaseCommand
from prev_seasons.models import Matches, Players, Seasons
from scraping.scrape import StatsScraper
import pandas as pd
from sqlalchemy import create_engine
from datetime import date

class Command(BaseCommand):
  
  help = 'Scrapes statistics from inputted seasons (YYYY-YYYY)'

  def __init__(self):
    self.scraper = StatsScraper('epl')

  def add_arguments(self, parser) -> None:
    parser.add_argument('season', nargs='*')

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')
    seasons = []
    if not kwargs['season']:
        curr_date = str(date.today())
        year, month, day = curr_date.split('-')
        y = int(year)
        seasons.append(f'{y-1}-{y}' if int(month) >= 8 else f'{y-1}-{y-2}')
    else:
      seasons = kwargs['season']

    for season in seasons:
      if Seasons.objects.filter(season=season).exists():
        print(f'statistics for {season} season already exists in database')
        continue
      
      print(f'scraping data for {season} season')
      matches, outfielders, goalkeepers = self.scraper.get_season_stats(season)
      
      matches.to_sql(Matches._meta.db_table, if_exists='append', con=engine, index= False)
      goalkeepers.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= False)
      outfielders.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= False)

      s_model = Seasons(season=season)
      s_model.save()

