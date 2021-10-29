import pandas as pd 
import sys, os, random

def get_split(arr):
	word_list = []
	for word in arr:
		count = 0 
		for x in word:
			if x == ' ':
				break 
			count += 1
		#word_list = []
		first = word[0:count]
		second = word[count+1:len(word)]
		if first != '' and second != '':
			word_list.append([first, second])
		if first == '' and second != '':
			word_list.append([second])
		if first != '' and second == '':
			word_list.append([first])
	return word_list 


def IntegratedMultipleFoods(results):
	final_results = []
	results = get_split(results)
	for result in results:
		for compare in results:
			#process multiples which is the main cause of the integrated double words problem
			if len(compare) > 1:
				for word in compare:
					word = [x for x in word]                      
					if word[-1] == 's':
						word.pop()
					if result[0] == ''.join(word):
						results.remove(result)
						for result in results:
							if len(result) < 2:
								final_results.append(result[0])
							if len(result) >=2:
								final_results.append(f'{result[0]} {result[1]}')
						return final_results
	

def MultipleFoods(results):
	data = pd.read_csv('RecipeData.csv')
	for x in range(len(data)):
		food_item = data.iloc[x, :][0]
		for result in results:
			for compare in results:
				if f'{result} {compare}' == food_item:
					results.remove(compare)
					results.remove(result)
					results.append(f'{result} {compare}')
				if f'{compare} {result}' == food_item:
					results.remove(compare)
					results.remove(result)
					results.append(f'{compare} {result}')
	return results



def check(check_list, row, results):
	check_results = []
	for word in check_list:
		if word.lower() in row:
			if word not in results:
				check_results.append(word)
	return check_results


class WordProcessor(object):
	def __init__(self, text):
		self.text = text 
		self.data = pd.read_csv('RecipeData.csv')

	def run(self):
		results = []
		text = self.text.split()
		for x in range(len(self.data)):
			row = self.data.iloc[x, :][0].lower().split()

			##### simple check #####
			check_results = check(text, row, results)
			if len(check_results) > 0:
				for result in check_results:
					results.append(result)


			##### es plurals check #####
			es_plurals = []
			for word in text:
				word = [x for x in word]
				if len(word) > 1:
					if word[-1] == 's' and word[-2] == 'e':
						if word[-3] == 'o':
							word.pop()
							word.pop()
						else:
							word.pop()
				es_plurals.append(''.join(word))
			#print(es_plurals, row)
			check_results = check(es_plurals, row, results)
			if len(check_results) > 0:
				for result in check_results:
					results.append(result)
		

			##### ies plurals #####
			ies_plurals = []
			for word in text:
				word = [x for x in word]
				if len(word) > 2:
					if word[-3] == 'i' and word[-2] == 'e' and word[-1] == 's':
						for _ in range(3):
							word.pop()
						word.append('y')
				ies_plurals.append(''.join(word))
			check_results = check(ies_plurals, row, results)
			if len(check_results) > 0:
				for result in check_results:
					results.append(result)


			##### s plurals #####
			s_plurals = []
			for word in text:
				word = [x for x in word]
				if len(word) > 1:
					if word[-1] == 's':
						word.pop()
				s_plurals.append(''.join(word))
			check_results = check(s_plurals, row, results)
			if len(check_results) > 0:
				for result in check_results:
					results.append(result)


		########## Avoids processing double word results with only one word ##########
		if len(results) == 1:
			return results

		##### Processes ies Results #####
		if len(results) >= 2:
			process = results.copy()
			for result in process: # eg ['raspberries', 'raspberry']
				for compare in process:
					if result[-1] == 'y' and ''.join(compare[-3:-1]) == 'ie' and compare[-1] == 's':
						result = [x for x in result]
						result.pop()
						result.append('i')
						result.append('e')
						result.append('s')
						if ''.join(result) == compare:
							results.pop(results.index(''.join(result)))

		results = MultipleFoods(results)
		return results
