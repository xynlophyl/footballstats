from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import requests

def scrape_team_urls(league_site, year):
  data = requests.get(league_site)
  soup = bs(data.text, 'html.parser')
  standings = soup.select('table.stats_table')[0]

  links = [l.get('href') for l in standings.find_all('a')]
  team_urls = [f'https://fbref.com{l}' for l in links if '/squads/' in l]
  team_urls = {url.split('/')[-1].replace('-Stats', '').replace('-', ' '): url for url in team_urls}

  # time.sleep(1)
  
  return team_urls


def scrape_match_data(urls):
  all_matches = []
  
  for team, url in urls.items():
    print(team, url)
    # getting general stats
    data = requests.get(url)
    matches = pd.read_html(data.text, match= "Scores & Fixtures")[0]

    time.sleep(3)

    # getting shooting stats
    soup = bs(data.text, 'html.parser')
    links = [l.get('href') for l in soup.find_all('a')]
    shooting_stats_url = [l for l in links if l and 'all_comps/shooting/' in l][0]
    data = requests.get(f'https://fbref.com{shooting_stats_url}')
    shooting_stats = pd.read_html(data.text, match="Shooting")[0]
    shooting_stats.columns = shooting_stats.columns.droplevel()
    time.sleep(3)

    # getting defending stats


    try:
      team_data = matches.merge(shooting_stats[["Date", "Sh", "SoT", "Dist", "FK", "PK", "PKatt"]], on="Date")
    except ValueError:
      print('error')
      continue
    
    # formatting
    team_data = team_data.drop(['Result', 'Day', 'Match Report', 'Notes'], axis=1)
    team_data = team_data[team_data["Comp"] == "Premier League"]
    team_data["Team"] = team
    # print(team_data.head())
    # print(team_data.shape)

    all_matches.append(team_data)

    time.sleep(3)
  return all_matches

def scrape_team_data(base_site, year):
  team_urls = scrape_team_urls(base_site, year)
  matches = scrape_match_data(team_urls)
  for m in matches:
    m["Season"] = year
  
  df = pd.concat(matches)
  df.columns = [c.lower() for c in df.columns]
  season, team = df.pop('Season'), df.pop('Team')
  df.insert(0, "Season", season)
  df.insert(1, "Team", team)
  
  return df
dataframe = scrape_team_data(base_site="https://fbref.com/en/comps/9/Premier-League-Stats", year="2022")

for i in dataframe:
  print(i)
  


# source: https://fbref.com/en/comps/9/Premier-League-Stats