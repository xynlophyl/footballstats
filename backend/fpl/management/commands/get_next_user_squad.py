from django.core.management.base import BaseCommand
from fpl.models import UserSquad, Gameweek
from utils.scrape_fpl_data import FPLScraper
from sqlalchemy import create_engine
from django.db.models import Max

class Command(BaseCommand):
  
  help = "Uses the Fantasy Premier League API (https://fantasy.premierleague.com/api/) to get the latest (unscraped) user squad"

  def __init__(self):
    self.scraper = FPLScraper()

  def add_arguments(self, parser) -> None:
    parser.add_argument(
      '--user', 
      nargs=1,
      help = 'id of the user you wish to retrieve the squad from'
    )

  def handle(self, *args, **kwargs):
    user = kwargs['user'][0]
    engine = create_engine('sqlite:///db.sqlite3')

    last_gw = Gameweek.objects.all().aggregate(Max('gameweek'))['gameweek__max']

    print(last_gw)

    gw = last_gw + 1 if last_gw else 1

    squad = self.scraper.get_user_squad(user, gw)
    if squad.empty:
      err = f'squads for the latest gameweek: gw {gw} have not been released yet'
      print(err)
      return 
    
    squad.to_sql(UserSquad._meta.db_table, if_exists='append', con=engine, index= False)
    gw_model = Gameweek(gameweek=gw)
    gw_model.save()


