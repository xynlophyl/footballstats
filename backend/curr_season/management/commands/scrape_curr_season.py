from operator import index
from django.core.management.base import BaseCommand
from curr_season.models import Matches, Players
from scraping.scrape import StatsScraper
from datetime import date
import pandas as pd
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

    matches.to_sql(Matches._meta.db_table, if_exists='replace', con=engine, index= True)
    goalkeepers.to_sql(Players._meta.db_table, if_exists='replace', con=engine, index= True)
    outfielders.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= True)
  
  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')
    path = 'data/2021-2022/EPL_'

    goalkeepers = pd.read_csv(path+'Goalkeepers_21_22.csv')
    outfielders = pd.read_csv(path+'Outfielders_21_22.csv')
    matches = pd.read_csv(path+'Matches_21_22.csv')

    goalkeepers = goalkeepers.loc[:, ~goalkeepers.columns.str.contains('^Unnamed')]
    outfielders = outfielders.loc[:, ~outfielders.columns.str.contains('^Unnamed')]
    matches = matches.loc[:, ~matches.columns.str.contains('^Unnamed')]
    
    goalkeepers.to_sql(Players._meta.db_table, if_exists='replace', con=engine, index= False)
    outfielders.to_sql(Players._meta.db_table, if_exists='append', con=engine, index= False)
    matches.to_sql(Matches._meta.db_table, if_exists='append', con=engine, index= False)

    print('done scraping')

