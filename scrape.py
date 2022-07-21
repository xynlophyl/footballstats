from re import M
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests

class StatsScraper():
  def __init__(self, league) -> None:
    fbref_links = {'epl': 'https://fbref.com/en/comps/9/Premier-League-Stats', 'efl': 'https://fbref.com/en/comps/10/Championship-Stats'}
    if league not in fbref_links:
      raise Exception('SCRAPE ERROR: League does not exist in our database')
    
    self.link = fbref_links[league]
    self.team_urls = self.get_team_urls()
    self.stat_types = ["att", "def", "gk", "pass", "gsc", "poss", "misc"]
    # self.stat_types = ["gsc", "misc", "poss", "att", "def", "gk", "pass"]

    self.advanced_stats = {
      "att":("Shooting", ["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]), # shooting
      "def": ("Defensive Actions", ["Date", "Tkl", "TklW", "TklvsDrb", "AttvsDrb", "Press", "Succ", "Blocks", "Int", "Err"]), # defending
      "gk": ("Goalkeeping", ["Date", "SoTA", "Saves", "PSxG", "PSxG+/-"]), # goalkeeping
      "pass": ("Passing", ["Date", "PassCmp", "PassAtt", "PassTotDist", "PassPrgDist"]), # passing
      "gsc": ("Goal and Shot Creation", ['Date','SCA','SCAPassLive','SCAPassDead','SCADrib','SCASh','SCAFld','SCADef','GCA','GCAPassLive','GCAPassDead','GCADrib','GCASh','GCAFld','GCADef']), # gca: merge on whole table
      "poss": ("Possession", ["Date", "Touches", "Def Pen", "Att Pen", "Carries", "TotDist", "PrgDist", "ProgCarries", "ProgPass"]), # possession
      "misc": ("Miscellaneous Stats", ["Date", "CrdY", "CrdR", "2CrdY", "Fls", "Fld", "Off", "Recov", "ArlWon", "ArlLost"]), # misc
    }

    self.advanced_stats_cols = {
      "att": [],
      "def": [("", "vsDrb", 14, 19)],
      "gk": [],
      "pass": [("Pass","", 10, 15)], 
      "gsc": [("SCA", "", 11, 17), ("GCA", "", 18, 24)],
      "poss": [("", "Carries", 26, 27), ("","Pass", 34, 35)],
      "misc": [("Arl", "", 23, 25)],

    }
    self.stats_urls = {t: '' for t in self.stat_types}

  def get_team_urls(self):
    data = requests.get(self.link)
    time.sleep(5)

    soup = bs(data.text, 'html.parser')
    standings = soup.select('table.stats_table')[0]
  
    links = [l.get('href') for l in standings.find_all('a')]
    team_urls = [f'https://fbref.com{l}' for l in links if '/squads/' in l]
    team_urls = {url.split('/')[-1].replace('-Stats', '').replace('-', ' '): url for url in team_urls}

    return team_urls

  def get_advanced_stats(self, link, stat_type):

    data = requests.get(f'https://fbref.com{link}')
    time.sleep(5)

    stats = pd.read_html(data.text, match=stat_type)[0]
    stats.columns = stats.columns.droplevel()

    return stats
    
  def merge_match_stats(self, advanced_stats):
    pass

  def rename_col_names(self, cols, fields):
    new_cols = []
    exp_before, exp_after, low, high = fields
    for i, col in enumerate(cols):
      if i >= low and i < high:
        col = exp_before + col + exp_after
      new_cols.append(col)
    return new_cols
      
  def reformat_season(self, season):
    yrs = season.split('-')
    return yrs[0][-2:]+'/'+yrs[1][:-2]

  def get_matches_info(self, season):
    s = self.reformat_season(season)
    all_matches = []
    for team, url in self.team_urls.items():
      print(team, url)
      # getting general stats
      data = requests.get(url)
      time.sleep(5)

      team_matches = pd.read_html(data.text, match= "Scores & Fixtures")[0]
      soup = bs(data.text, 'html.parser')
      links = [l.get('href') for l in soup.find_all('a')]
      links = [l for l in links if l and 'all_comps/' in l]

      for l in links:
        if 'all_comps/shooting/' in l:
          self.stats_urls["att"] = l
        elif 'all_comps/defense/' in l:
          self.stats_urls["def"] = l
        elif 'all_comps/keeper/' in l:
          self.stats_urls["gk"] = l
        elif 'all_comps/passing/' in l:
          self.stats_urls["pass"] = l
        elif 'all_comps/gca/' in l:
          self.stats_urls["gsc"] = l
        elif 'all_comps/possession/' in l:
          self.stats_urls["poss"] = l
        elif 'all_comps/misc/' in l:
          self.stats_urls["misc"] = l

      # getting advanced stats
      for t in self.stat_types:
        title, fields = self.advanced_stats[t]
        url = self.stats_urls[t]
        if not url:
          continue

        stats = self.get_advanced_stats(url, title)

        stats_cols = stats.columns.values
        for f in self.advanced_stats_cols[t]:
          stats_cols = self.rename_col_names(stats_cols, f)
        stats.columns = stats_cols
        
        try:
            team_matches = team_matches.merge(stats[fields], on="Date")
        except ValueError:
          print('error: no stats')
          continue
      
      # adding new columns and removing excess columns
      team_matches = team_matches.drop(['Result', 'Day', 'Match Report', 'Notes'], axis=1)
      team_matches = team_matches[team_matches["Comp"] == "Premier League"]
      team_matches["Team"] = team
      team_matches["Season"] = s
      all_matches.append(team_matches)
    
    # formatting
    df = pd.concat(all_matches)
    df.columns = [''.join(c.split(" ")) for c in df.columns]
    season, team = df.pop("Season"), df.pop("Team")
    df.insert(0, "Season", season)
    df.insert(1, "Team", team)

    return df


premScraper = StatsScraper('epl')
df = premScraper.get_matches_info("2021-2022")
df.to_csv("EPL_21_22.txt")