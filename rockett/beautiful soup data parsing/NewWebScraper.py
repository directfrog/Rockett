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

test_collections = ['https://www.bbcgoodfood.com/recipes/collection/skirt-steak-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/steak-salad-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/steak-sauce-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/healthy-steak-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/beer-cocktail-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/john-torode-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/healthy-butternut-squash-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/brunch-egg-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/vegetarian-camping-recipes',
			  'https://www.bbcgoodfood.com/recipes/collection/ham-hock-recipes']

def get_total_time(page):
	req = Request(page)
	html_page = urlopen(req)
	soup = str(BeautifulSoup(html_page, "lxml"))
	span = re.search('totalTime', soup).span()
	section = soup[span[0]:span[1]+15]
	time_span = re.search('PT', section).span()
	time_section = str(section[time_span[0]:time_span[1]+4])
	time_in_mins = 0
	if 'H' in time_section:
		H_index = time_section.index('H')
		hours = int(time_section[H_index-1])
		time_in_mins += hours*60
		if time_section[H_index+1].isdigit():
			try:
				mins = int(f'{time_section[H_index+1]}{time_section[H_index+2]}') 
				time_in_mins += mins 
			except:
				time_in_mins += int(f'{time_section[H_index+1]}')
	else:
		try:
			mins = int(f'{time_section[2]}{time_section[3]}') 
			time_in_mins += mins 
		except:
			time_in_mins += int(f'{time_section[2]}')
	return time_in_mins



def get_links(collection):
	req = Request(collection)
	html_page = urlopen(req)
	soup = BeautifulSoup(html_page, "lxml")
	links = []
	for link in soup.findAll('a'):
		if re.search('recipes/', str(link)) != None:
			if re.search('collection', str(link)) == None:
				if re.search('category', str(link)) == None:
					if re.search('/search/', str(link)) == None:
						found_link = link.get('href')
						formatted_link = f'https://www.bbcgoodfood.com/{found_link}'#just adding  the https://www.bbcgoodfood.com/ to the start
						links.append(formatted_link)
	return links

def run_links(results):
	data = []
	for link in results:
		scrape = scrape_me(link)
		title = scrape.title()
		total_time = get_total_time(link)
		ingredients = scrape.ingredients()
		instructions = scrape.instructions()
		data.append([title, len(ingredients), total_time])
	return data 


##### HOW TO USE WebScraper 2 ####
results = get_links('https://www.bbcgoodfood.com/recipes/collection/ham-hock-recipes')
data = run_links(results)
print(data)

