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


class ExtraScraper(object):
    def cookpreptime(self, URL, preporcook):
        page = str(list(requests.get(URL)))

        print(page)

        span = re.search(preporcook, page).span()
        find_range = page[span[1]:span[1]+16]
        print(find_range)
        if re.search('b', find_range) != None:
            span = re.search(preporcook, page[span[1]+16:len(page)]).span()
        find_range = page[span[0]:span[1]+16]
        print('FINAL FIND RANGE: ', find_range)
        if re.search('PT', find_range) != None:
            for index in range(len(find_range)):
                if find_range[index] == 'T' and find_range[index-1] == 'P':
                    break 
            if 'H' in find_range and 'M' not in find_range:
                time = int(find_range[index+1:find_range.index('H')])*60
            if 'H' in find_range and 'M' in find_range:
                time = find_range[find_range.index('H')-1]*60 + find_range[find_range.index('M')]
            if 'H' not in find_range and 'M' in find_range:
                time = find_range[index+1:find_range.index('M')]
        return time


def get_links(arr):
    links = []
    for x in range(len(arr)):
        if arr[x] == 'h' and arr[x+1] == 't' and arr[x+2] == 't' and arr[x+3] == 'p' and arr[x+8] == 'w':
            if x+80 > len(arr):
                addon = len(arr)-x-1
            else:
                addon = 80
            for extension in range(x, x+addon):
                if x+1 < len(arr):
                    if arr[extension] == '}':
                        links.append(str(arr[x:extension-1]))
    return links

def run_scraper(alpha):
    #alpha = input("What is your main ingredient you've wasted:  ")
    data = pd.read_csv('RecipeData.csv')  
    found_links = []
    for x in range(len(data)):
      food_data = data.iloc[x]["Wasted Food"]
      found = re.search(alpha, str(food_data))
      if found != None:
        found_links.append(data.iloc[x]["BBCGoodFood link"])
        


    def download_url(url):
        resp = requests.get(url)
        title = "Content"
        with open(title, "wb") as fh:
            fh.write(resp.content)

    download_url(found_links[0])

    list_content = []
    file1 = open("Content", encoding='utf-8') 
    list_content.append(file1.read())
    search_list = []
    content = str(list_content)

    for y in range(1000):
      try:
        #list.append(re.search("(?P<url>https?://[^\s]+)", content).group("url"))
        x = re.search("(?P<url>https?://[^\s]+)", content).group("url")
        search_list.append(x)
        content = content.replace(str(x),"")
      except:
        break

    list_recipes = []
    for n in range(len(search_list)):
        #a = re.search("recipes/", str(search_list[n]))
        #b = re.search("https", str(search_list[n]))
        #c = re.search("collection", str(search_list[n]))
        #if a != None and b != None and c == None and n%2 == 0:
            #list_recipes.append(search_list[n])
        if 'recipes/' in search_list[n] and 'https' in search_list[n] and 'collection' in search_list[n]:
            if search_list[n][-4:len(search_list)] == 'link':
                list_recipes.append(search_list[n][0:-8])

    print('LIST RECIPES: ', list_recipes)

    thread_local = threading.local()
    def get_session():
        if not hasattr(thread_local, "session"):
            thread_local.session = requests.Session()
        return thread_local.session

    def download_site(url):
        session = get_session()
        recipe = str(url)
        scrape = scrape_me(recipe)
        extrascraper = ExtraScraper()

        print('RETURNED RECIPE LINK: ', recipe)
        print('Scrape function: ', scrape)
        title = scrape.title()
        #total_time = extrascraper.cookpreptime(recipe, 'prepTime')+extrascraper.cookpreptime(recipe, 'cookTime')
        #print('TOTAL TIME: ', total_time)
        ingredients = scrape.ingredients()
        print('ingredients: ', ingredients)
        instructions = scrape.instructions()
        return [title, len(ingredients), ingredients, instructions] #, total_time

    def download_all_sites(sites):
        global title_links
        title_links = []
        title_names = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=13) as executor:
            for url in sites:
                title_links.append(executor.submit(download_site, url))
            for task in as_completed(title_links):
                title_names.append(task.result())

            return title_links, title_names


    title_links, data = download_all_sites(list_recipes)

    print('TITLE LINKS: ', title_links)
    print('data: ', data)
    sys.exit()
    return title_links, data
