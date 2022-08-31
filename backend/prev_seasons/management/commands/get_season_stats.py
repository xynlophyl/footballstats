from django.core.management.base import BaseCommand
from prev_seasons.models import MatchStat, PlayerStat, Season
from utils.scrape_fbref_data import StatsScraper
from sqlalchemy import create_engine
from datetime import date
import time

class Command(BaseCommand):
  
  help = 'Scrapes statistics from inputted seasons (YYYY-YYYY)'

  def __init__(self):
    self.scraper = StatsScraper('epl')

  def add_arguments(self, parser) -> None:
    parser.add_argument(
      '--season', 
      nargs='*',
      help = 'the seasons you wish to get data on (if blank -> scrapes most recently finished season'
    )

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
      if Season.objects.filter(season=season).exists():
        print(f'statistics for {season} season already exists in database')
        continue
      
      print(f'scraping data for {season} season')
      matches, outfielders, goalkeepers = self.scraper.get_season_stats(season)
     
      formatted_season = self.scraper.format_season(season)
      outfielders['player_id'] = outfielders['player_team'].astype(str) + '_' + formatted_season
      goalkeepers['player_id'] = goalkeepers['player_team'].astype(str) + '_' + formatted_season
      
      matches.to_sql(MatchStat._meta.db_table, if_exists='append', con=engine, index= False)
      goalkeepers.to_sql(PlayerStat._meta.db_table, if_exists='append', con=engine, index= False)
      outfielders.to_sql(PlayerStat._meta.db_table, if_exists='append', con=engine, index= False)

      s_model = Season(season=season)
      s_model.save()

      time.sleep(10)

