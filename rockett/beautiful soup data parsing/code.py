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
from googlesearch import search
url = 'https://www.bbcgoodfood.com/recipes/collection/cheesy-pasta-recipes'


def get_links(url)
    results = []
    for r in search(url, tld="co.in", num=30, stop=30, pause=2):
        #print(r)
        if re.search('https://www.bbcgoodfood.com/recipes/', str(r)) != None:
            if re.search('collection/', str(r)) == None:
               results.append(str(r))
    return results