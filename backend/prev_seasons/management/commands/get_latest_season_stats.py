from django.core.management.base import BaseCommand
from prev_seasons.models import Matches, Players, Seasons
from utils.scrape_fbref_data import StatsScraper
from datetime import date
from sqlalchemy import create_engine

class Command(BaseCommand):
  
  help = 'Scrapes statistics from last finished season'

  def __init__(self):
    self.scraper = StatsScraper('epl')

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')
   
    curr_date = str(date.today())
    year, month, day = curr_date.split('-')
    y = int(year)
    season = f'{y-1}-{y}' if int(month) >= 8 else f'{y-1}-{y-2}'

    if Seasons.objects.filter(season=season).exists():
      print(f'{season} season is already in database')
      return

    print(f'scraping data for {season} season')
    matches, outfielders, goalkeepers = self.scraper.get_season_stats(season)

    goalkeepers.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= False)
    outfielders.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= False)
    matches.to_sql(Matches._meta.db_table, if_exists='append', con=engine, index= False)

    s_model = Seasons(season=season)
    s_model.save()
  