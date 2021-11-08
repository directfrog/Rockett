import datetime
import numpy as np
import pandas as pd
import re
import pandas as pd
import time
import csv
import concurrent.futures
import requests
import threading
import time
import sys 

from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me

req = Request('https://www.bbcgoodfood.com/recipes/collection/eggy-bread-recipes')
html_page = urlopen(req)

soup = BeautifulSoup(html_page, "lxml")

links = []
for link in soup.findAll('a'):
    text = str(link.get('href'))
    if re.search('recipes/', text) != None:
        if re.search('collection', text) == None:
             if re.search('search', text) == None:
                if re.search('category/', text) == None:
                    links.append(link.get('href'))

print(links)

