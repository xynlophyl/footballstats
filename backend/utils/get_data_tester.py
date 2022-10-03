from scrape_fbref_data import StatsScraper
from scrape_fpl_data import FPLScraper
import pandas as pd
import time

def scrape_fbref_data():
  t = time.time()
  path = 'static/2022-2023/'

  # df = pd.read_csv(path+"2022_2023_outfield.csv")

  s = StatsScraper('epl')
  matches, outfielders, goalkeepers = s.get_season_stats()  
  matches.to_csv(path+'2022_2023_matches.csv')
  outfielders.to_csv(path+'2022_2023_outfield.csv')
  goalkeepers.to_csv(path+'2022_2023_gk.csv')

scrape_fbref_data()
