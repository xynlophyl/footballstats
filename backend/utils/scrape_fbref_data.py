from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests

class StatsScraper():
  """
  INITIALIZATION
  """
  def __init__(self, league: str) -> None:
    '''
    scraper is initialized with a target league
    league: YYYY-YYYY
    '''
    league_urls = {'epl': 'https://fbref.com/en/comps/9/Premier-League-Stats', 'efl': 'https://fbref.com/en/comps/10/Championship-Stats'}
    if league not in league_urls:
      raise Exception('SCRAPE ERROR: League does not exist in our database')
    
    self.league_url = league_urls[league]
    self.fbref_base_url = 'https://fbref.com'

    self.curr_season = "2022-2023"

    self.advanced_stats = {
      # stat_type: (Header, Columns, New Name Format)
      "att":("Shooting", ["Date", "Sh", "SoT", "Dist", "FK", "PKscored", "PKatt","Player"], ([("","scored", 18, 19)],[("","scored",15,16)])), # shooting
      "def":("Defensive Actions", ["Date", "Tkl", "TklW", "TklvsDrb", "AttvsDrb", "Press", "Succ", "Blocks", "Int", "Err", "Player"], ([("", "vsDrb", 14, 19)], [("", "vsDrb", 9, 14)])), # defending
      "gk":("Goalkeeping", ["Date", "SoTA", "Saves", "PSxG", "PSxG+/-", "Player"],([],[])), # goalkeeping
      "pass":("Passing", ["Date", "Pass_Cmp", "Pass_Att", "Pass_TotDist", "Pass_PrgDist", "Player"],([("Pass_","", 10, 15)],[("Pass_", "", 5, 10)])), # passing
      "gsc":("Goal and Shot Creation", ['Date','SCA','SCA_PassLive','SCA_PassDead','SCA_Drib','SCA_Sh','SCA_Fld','SCA_Def','GCA','GCA_PassLive','GCA_PassDead','GCA_Drib','GCA_Sh','GCA_Fld','GCA_Def', "Player"],([("SCA_", "", 11, 17), ("GCA_", "", 18, 24)],[("SCA_", "", 7, 13), ("GCA_", "", 15, 21)])), # gca
      "poss":("Possession", ["Date", "Touches", "Touches_Def 3rd", "Touches_Att 3rd", "Touches_Att Pen", "Carries", "Carries_TotDist", "Carries_PrgDist", "ProgCarries", "ProgPassRec", "Player"], ([("Touches_", "", 12, 18),("Carries_","",24,26), ("", "Carries", 26, 27), ("","PassRec", 34, 35)],[("Touches_", "", 6, 11),("Carries_","", 18, 20),("", "Carries", 20, 21), ("","PassRec", 28, 29)])), # possession
      "misc":("Miscellaneous Stats", ["Date", "CrdY", "CrdR", "2CrdY", "Fls", "Fld", "Off", "Recov", "ArlWon", "ArlLost", "Player"],([("Arl", "", 23, 25)],[("Arl", "", 18, 20)])), # misc
    }

    self.formatted_fields = {
      'round': 'gameweek',
      'g+a': 'goal_contrib', 'g-pk':'npg', 'g+a-pk':'np_goal_contrib', 'npxg+xa': 'np_xgoal_contrib', 'xg+xa': 'xgoal_contrib',
      'psxg+/-': 'psxg_pm', 
      '2crdy': 'twocrdy', '90s': 'ninetys', 'min': 'minutes', 'int': 'inter', 
      "touches_def 3rd": "touches_defthird", "touches_att pen": "touches_attpen", "touches_att 3rd": "touches_attthird"
    }

  """
  MAIN SCRAPING FUNCTIONS
  """

  def get_season_stats(self, season: str = ''):
    '''
    scrapes team and player stats from every match of each gameweek in a given season
    '''

    season = season if season else self.curr_season
    season_url = self.get_season_url(season)
    all_matches = []
    all_outfield_players = []
    all_goalkeepers = []

    for team, team_url in self.get_team_urls(season_url, season).items():
      print(team, team_url)
      data = requests.get(team_url)
      time.sleep(5)

      matches = self.get_season_match_stats(data)
      outfielders, goalkeepers = self.get_season_player_stats(data)

      formatted_season = self.format_season(season)

      matches = self.add_constant_field(matches, {"Team": team, "Season": formatted_season})
      outfielders = self.add_constant_field(outfielders, {"Team": team, "Season": formatted_season})
      goalkeepers = self.add_constant_field(goalkeepers, {"Team": team, "Season": formatted_season})

      all_matches.append(matches)
      all_outfield_players.append(outfielders)
      all_goalkeepers.append(goalkeepers)
    
    matches_df = self.format_df(all_matches)
    outfielders_df = self.format_df(all_outfield_players)
    goalkeepers_df = self.format_df(all_goalkeepers)

    matches_df = self.add_match_id(matches_df)
    outfielders_df = self.add_player_id(outfielders_df)
    goalkeepers_df = self.add_player_id(goalkeepers_df)

    outfielders_df = self.format_age(outfielders_df)
    goalkeepers_df = self.format_age(goalkeepers_df)


    return matches_df, outfielders_df, goalkeepers_df
    
  """
  AUX SCRAPING FUNCTIONS
  """
  # url helper functions
  def get_team_urls(self, url: str, season: str):
    '''
    gets all teams playing within target league at a particular season
    '''
    data = requests.get(url)
    time.sleep(5)

    soup = bs(data.text, 'html.parser')
    standings = soup.select('table.stats_table')[0]
  
    links = [l.get('href') for l in standings.find_all('a')]
    links = [l for l in links if '/squads/' in l]

    team_urls = {}
    for l in links:
      url_parts = l.split('/')
      team = url_parts[-1].replace('-Stats', '').replace('-', ' ')
      url = self.fbref_base_url + '/'.join(l.split('/')[:4] + [season])
      team_urls[team] = url
    return team_urls

  def get_season_url(self, season: str):
    '''
    retrieves the url of the target season
    '''

    if season == self.curr_season:
      return self.league_url
    
    curr, url = '', self.league_url
    while True:
      data = requests.get(url)
      time.sleep(3)

      soup = bs(data.text, 'html.parser')
      curr = soup.select('h1')[0].text

      if season in curr:
        return url

      url = self.fbref_base_url + soup.select('a.prev')[0].get('href')


  def get_advanced_stats_url(self, data):
    soup = bs(data.text, 'html.parser')
    links = [l.get('href') for l in soup.find_all('a')]
    links = [l for l in links if l and '/all_comps/' in l]
    stats_urls = {}

    for l in links:
      if 'all_comps/shooting/' in l:
        stats_urls["att"] = self.fbref_base_url+l
      elif 'all_comps/defense/' in l:
        stats_urls["def"] = self.fbref_base_url+l
      elif 'all_comps/keeper/' in l:
        stats_urls["gk"] = self.fbref_base_url+l
      elif 'all_comps/passing/' in l:
        stats_urls["pass"] = self.fbref_base_url+l
      elif 'all_comps/gca/' in l:
        stats_urls["gsc"] = self.fbref_base_url+l
      elif 'all_comps/possession/' in l:
        stats_urls["poss"] = self.fbref_base_url+l
      elif 'all_comps/misc/' in l:
        stats_urls["misc"] = self.fbref_base_url+l
    return stats_urls
  
  # statistic helper functions
  def get_season_match_stats(self, data):
    team_matches = pd.read_html(data.text, match= "Scores & Fixtures")[0]
    advanced_stats_urls = self.get_advanced_stats_url(data)

    for stat_type in self.advanced_stats:
      url = advanced_stats_urls.get(stat_type, None)
      if not url:
        continue
      header, merge_fields, field_formats = self.advanced_stats[stat_type]
      data = requests.get(url)
      time.sleep(5)

      stats = self.get_statistic(data, header)
      
      for f in field_formats[0]:
        stats = self.format_columns(stats,f)
  
      try:
        team_matches = team_matches.merge(stats[merge_fields[:-1]], on="Date")
      except ValueError:
        print(f'Scrape Error: No table for {stat_type}')
        continue
    
    team_matches = team_matches.drop(['Match Report', 'Notes'], axis=1)
    team_matches = team_matches[team_matches["Comp"] == "Premier League"]
    return team_matches
    
  def get_season_player_stats(self, data):
    player_stats = pd.read_html(data.text, match="Playing Time")[0]
    player_stats.columns = player_stats.columns.droplevel()

    player_stats = player_stats.loc[player_stats['Min'] >= 90]
    player_stats = self.remove_values(player_stats, {"Player": ["Squad Total", "Opponent Total"]})


    player_stats = player_stats.drop(player_stats.iloc[:, 11:15], axis=1)
    player_stats = player_stats.loc[:, ~player_stats.columns.duplicated()]
    player_stats = player_stats.drop(['G+A', 'G+A-PK', 'xG+xA'], axis = 1)

    outfielder_stats, goalkeeper_stats = self.filter_gk_outfield_stats(player_stats)

    for stat_type in self.advanced_stats:
      header, merge_fields, field_formats = self.advanced_stats[stat_type]
      stats = self.get_statistic(data, header)
      if stat_type == "gk":
        advanced_gk_stats = self.get_statistic(data, "Advanced Goalkeeping")
        stats = stats.merge(advanced_gk_stats, on="Player", suffixes=('','_DROP')).filter(regex='^(?!.*_DROP)')
        stats = self.remove_values(stats, {"Player": ["Squad Total", "Opponent Total"]})

      for f in field_formats[1]:
        stats = self.format_columns(stats, f)
      
      outfield, gk = self.filter_gk_outfield_stats(stats)

      try:
        goalkeeper_stats = goalkeeper_stats.merge(gk[merge_fields[1:]], on="Player")
        if stat_type != "gk":
          outfielder_stats = outfielder_stats.merge(outfield[merge_fields[1:]], on="Player")
      except ValueError:
        print(f'Scrape Error: No table for {stat_type}')
        continue
      
    outfielder_stats = outfielder_stats.drop(['Matches'], axis = 1)
    goalkeeper_stats = goalkeeper_stats.drop(['Matches'], axis = 1)

    return outfielder_stats, goalkeeper_stats


  def get_statistic(self, data, header):
    stats = pd.read_html(data.text, match=header)[0]
    stats.columns = stats.columns.droplevel()

    return stats

  # formatting functions
  def format_season(self, season):
    '''
    formats season from XXYY-XXYY to YY/YY
    '''

    yrs = season.split('-')
    return yrs[0]+'_'+yrs[1]

  def format_columns(self, stats, format):
    new_columns = []
    exp_before, exp_after, low, high = format

    for i, col in enumerate(stats.columns.values):
      if i >=low and i < high:
        col = exp_before + col + exp_after
      new_columns.append(col)

    stats.columns = new_columns
    return stats

  def format_df(self, df):
    df = pd.concat(df)
    df = df.reset_index(drop=True)
    
    season, team = df.pop("Season"), df.pop("Team")
    df.insert(0, "Season", season)
    df.insert(1, "Team", team)

    cols = []
    for c in df.columns:
      c = c.lower()
      c = self.formatted_fields.get(c, c)
      cols.append(c)
    df.columns = cols

    return df

  def format_age(self, df):
    ages = []
    for i in df['age']:
      ages.append(i.split('-')[0])
    df['age'] = ages
    return df

  def add_match_id(self, df):
    df['match_id'] = df['team'].astype(str) + '_' + df['opponent'].astype(str) + '_' + df['venue'].astype(str)+ '_' +df['season'].astype(str)
    return df

  def add_player_id(self, df):
    df['player_team'] = df['player'].astype(str) + '_' + df['team']
    return df

  def add_constant_field(self, df, fields: dict):
    for field, title in fields.items():
      df[field] = title
    
    return df

  def remove_values(self, df, fields: dict):
    for field, titles in fields.items():
      for t in titles:
        df = df.loc[df[field] != t] 
    return df
  
  def filter_gk_outfield_stats(self, df):
    return df.loc[df['Pos'] != 'GK'], df.loc[df['Pos'] == 'GK']