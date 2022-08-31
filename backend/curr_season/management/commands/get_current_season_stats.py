from django.core.management.base import BaseCommand
from curr_season.models import MatchStat, PlayerStat
from utils.scrape_fbref_data import StatsScraper
from datetime import date
from sqlalchemy import create_engine

class Command(BaseCommand):
  
  help = 'Scrapes statistics from inputted seasons, if season argument is not input, then scrape current season'

  def __init__(self):
    self.scraper = StatsScraper('epl')

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')
    
    curr_date = str(date.today())
    year, month, day = curr_date.split('-')
    y = int(year)
    season = f'{y}-{y+1}' if int(month) >= 8 else f'{y-1}-{y}'

    print(f'scraping data for {season} season')
    matches, outfielders, goalkeepers = self.scraper.get_season_stats(season)

    matches.to_sql(MatchStat._meta.db_table, if_exists='replace', con=engine, index= False)

    goalkeepers.to_sql(PlayerStat._meta.db_table, if_exists='replace', con=engine, index= False)
    outfielders.to_sql(PlayerStat._meta.db_table, if_exists='append', con=engine, index= False)
