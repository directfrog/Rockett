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
import urllib
from urllib.request import Request, urlopen
from concurrent.futures import ThreadPoolExecutor, as_completed
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_me


url = "https://www.bbcgoodfood.com/recipes/ultimate-spaghetti-carbonara-recipe"
file = urllib.request.urlopen(url)

for line in file:
	decoded_line = line.decode("utf-8")
	print(decoded_line)
