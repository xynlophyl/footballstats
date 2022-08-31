from django.core.management.base import BaseCommand
from fpl.models import UserSquad, Gameweek
from utils.scrape_fpl_data import FPLScraper
from sqlalchemy import create_engine

class Command(BaseCommand):
  
  help = "Uses the Fantasy Premier League API (https://fantasy.premierleague.com/api/) to get the season's fixtures"

  def __init__(self):
    self.scraper = FPLScraper()

  def add_arguments(self, parser) -> None:
    parser.add_argument(
      '--user', 
      nargs=1,
      help = 'id of the user you wish to retrieve the squad from'
    )

  def handle(self, *args, **kwargs):
    engine = create_engine('sqlite:///db.sqlite3')
    gw = 1

    if not kwargs['user']:
      print('please enter a user id')
      return 
      
    user = kwargs['user'][0]

    while True:
      if Gameweek.objects.filter(gameweek=gw).exists():
        print(f'statistics for {gw} season already exists in database')
        gw += 1
        continue

      squad = self.scraper.get_user_squad(user, gw)
      if squad.empty:
        break

      squad.to_sql(UserSquad._meta.db_table, if_exists='append', con=engine, index= False)

      gw_model = Gameweek(gameweek=gw)
      gw_model.save()

      gw += 1
