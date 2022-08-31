import pandas as pd
import requests
from datetime import date

'''
gameweek  = 2
general_info = '/bootstrap-static/' # get player general information
my_gameweek_picks = f'/entry/{user}/event/{gameweek}/picks/' # get my team information
player_information = f'/element-summary/' # get player detailed information
fixtures = '/fixtures/' # get fixtures list

my_team = requests.get(base_url+my_gameweek_picks).json()
'''

class FPLScraper:
  def __init__(self):
    self.base_url = 'https://fantasy.premierleague.com/api'

  def get_user_squad(self, user, gw):

    link = f'{self.base_url}/entry/{user}/event/{gw}/picks/'
    data = requests.get(link).json()

    if 'detail' in data:
      return pd.DataFrame()

    squad = pd.DataFrame({
      'squad_id': pd.Series(dtype='str'),
      'user': pd.Series(dtype='int'),
      'gameweek': pd.Series(dtype='int'),
      'player': pd.Series(dtype='int'),
      'starter': pd.Series(dtype='bool'),
      'is_captain': pd.Series(dtype='str'),
      'is_vice_captain': pd.Series(dtype='str'),
    })

    for el in data['picks']:
      starter = el['position'] < 12
      squad.loc[len(squad)] = [
        f"{user}_{gw}_{el['element']}", 
        user, 
        gw, el['element'], 
        starter, el['is_captain'], el['is_vice_captain']
      ]
    
    return squad

  def get_players_information(self):
    link = f'{self.base_url}/bootstrap-static/'
    data = requests.get(link).json()

    players = pd.DataFrame({
      'player_id': pd.Series(dtype='int'),
      'first_name': pd.Series(dtype='str'),
      'second_name': pd.Series(dtype='str'),
      'known_as': pd.Series(dtype='str'),
      'image': pd.Series(dtype='str'),
      'team_id': pd.Series(dtype='int'),
      'position': pd.Series(dtype='int'),
      'fpl_cost': pd.Series(dtype='float'),
      'fpl_total_points': pd.Series(dtype='float'),
      'fpl_form': pd.Series(dtype='float'),
    })
    
    photo_base_link = 'https://resources.premierleague.com/premierleague/photos/players/110x140/p'

    for el in data['elements']:
      players.loc[len(players)] = [
        el['id'], el['first_name'], el['second_name'], el['web_name'], 
        f"{photo_base_link}{el['code']}.png", 
        el['team'], el['element_type'],
        el['now_cost'], el['total_points'], el['form']]
 
    return players
  
  def get_team_information(self):
    link = f'{self.base_url}/bootstrap-static/'
    data = requests.get(link).json()
    teams = pd.DataFrame({
      'team_id': pd.Series(dtype='int'),
      'name': pd.Series(dtype='str'),
      'short_name': pd.Series(dtype='str'),
      'strength': pd.Series(dtype='int'),
      'strength_overall_home': pd.Series(dtype='int'),
      'strength_overall_away': pd.Series(dtype='int'),
      'strength_attack_home': pd.Series(dtype='int'),
      'strength_attack_away': pd.Series(dtype='int'),
      'strength_defence_home': pd.Series(dtype='int'),
      'strength_defence_away': pd.Series(dtype='int'),
    })

    for el in data['teams']:

      teams.loc[len(teams)] = [
        el['code'], el['name'], el['short_name'], 
        el['strength'], el['strength_overall_home'], el['strength_overall_away'], el['strength_attack_home'], el['strength_attack_away'], el['strength_defence_home'], el['strength_defence_away'],
      ]
    
    return teams
  
  def get_fixtures(self):
    link = f'{self.base_url}/fixtures/'
    data = requests.get(link).json()

    fixtures = pd.DataFrame({
      'match_id': pd.Series(dtype='int'),
      'season': pd.Series(dtype='str'),
      'gw': pd.Series(dtype='int'),
      'home_id': pd.Series(dtype='str'),
      'away_id': pd.Series(dtype='str'),
      'finished': pd.Series(dtype='bool')
    })

    curr_season = self.get_season()

    for el in data:
      fixtures.loc[len(fixtures)] = [el['code'], curr_season, el['event'], el['team_h'], el['team_a'], el['finished']]
    
    return fixtures
  
  def get_season(self):
    curr_date = str(date.today())
    year, month, day = curr_date.split('-')
    y = int(year)
    season = f'{y}_{y+1}' if int(month) >= 8 else f'{y-1}-{y}'

    return season

'''
resources used:
  https://resources.premierleague.com/
  https://fantasy.premierleague.com/api/
'''