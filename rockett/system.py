from WordProcessor import *
from WebScraper2 import *
import pandas as pd 
import math, time, sys, os, csv

def ProcessWords(text):
	processor = WordProcessor(text)
	results = processor.run()
	return results


def filter_commas(arr):
	arr = [x for x in arr]
	if ',' in arr:
		arr.remove(',')
	return ''.join(arr)

def get_common_ingredients(results, ingreds):
	common_ingreds = []
	for x in ingreds:
		if x in results:
			common_ingreds.append(x)
	return common_ingreds             

def sort_num_ingreds(arr):
	copy_arr = arr.copy()
	sorted_arr = []
	for x in copy_arr:
		smallest = arr[0]
		for compare in arr:
			if compare[1] < smallest[1]:
				smallest = compare
		sorted_arr.append(smallest)
		arr.pop(arr.index(smallest))
	return sorted_arr

def sort_time_taken(arr):
	new_arr = []
	for x in arr:
		lowest = arr[0]
		for compare in arr:
			if compare[4] < lowest[4]:
				lowest = compare
		#print(lowest, ': ', arr)
		new_arr.append(lowest) 
		arr.remove(lowest)
	new_arr.append(arr[0])

	return new_arr

def get_foods(main_item, AnyOtherIngreds, links):
	print('WORD PROCESSOR RESULTS: ', main_item, AnyOtherIngreds)

	TRL = [get_links(link) for link in links] # TRL acronym for total_recipe_links
	total_recipe_links = []
	for arr in TRL:					# this part is just for getting all the links
		for link in arr:			# out of separate lists inside TRL. 
			total_recipe_links.append(link)

	data = run_links(total_recipe_links)

	###
	return data
	###

	commonVals = []
	common = []
	common_recipes = []
	true_common_recipes = []
	for x in data:
		results_ingredients = ' '.join(x[2])
		result_ingreds = ProcessWords(results_ingredients)
		common_ingreds = []
		for ingred in result_ingreds:
			if ingred == main_item or ingred in AnyOtherIngreds:
				if ingred not in common_ingreds:
					common_ingreds.append(ingred)
		x.append(len(common_ingreds))
		commonVals.append(len(common_ingreds))
		common_recipes.append(x)
		common.append(common_ingreds)
		common_recipes.append(x)


	for x in common_recipes:
		if x not in true_common_recipes:
			true_common_recipes.append(x)
	true_common_recipes = sort_num_ingreds(true_common_recipes)
	#true_common_recipes = sort_time_taken(true_common_recipes)
	print('TRUE COMMON RECIPES: ', true_common_recipes)
	return true_common_recipes