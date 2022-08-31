from scrape_fbref_data import StatsScraper
from scrape_fpl_data import FPLScraper
import time

def scrape_fbref_data():
  t = time.time()
  path = 'data/2021-2022/'
  s = StatsScraper('epl')

  s.get_gameweek_statistics('2022-2023', 1)

  # print(df)

scrape_fbref_data()
