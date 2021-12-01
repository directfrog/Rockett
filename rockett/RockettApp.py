from system import *
from WordProcessor import *
import kivy
from kivy.app import App 
from kivy.uix.widget import Widget 
from kivy.lang import Builder 
from kivy.core.window import Window 
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.list import OneLineListItem, MDList, TwoLineListItem, ThreeLineListItem
from kivymd.uix.list import ThreeLineIconListItem, IconLeftWidget
from kivymd.uix.label import MDLabel
from kivymd.icon_definitions import md_icons
from kivy.properties import ObjectProperty
from functools import partial
from kivy.uix.scrollview import ScrollView

def get_used_links(link):
	data = pd.read_csv('RecipeData.csv')
	links = []
	for x in range(len(data)):
		row = data.iloc[x, :]
		for i in link: # loops through list of ingredients given in params
			if re.search(i, row[0]) != None: # checks if it is in the row
				if len(row[0]) == len(i):
					if row[1] not in links:
						links.append(row[1])
	return links



def change_screens(self, result):
	wm.current = 'third'
	global selecected_result 
	selecected_result = results[md_index_matrix[str(result)]]


class TextEnterWindow(Screen):
	def button_on(self):
		self.ids.button_image.source = 'button1.png'

	def button_off(self):
		self.ids.button_image.source = 'button2.png' 

	def run_system(self):
		global links
		main_ingreds = ProcessWords(self.ids.main_ingred.text) # main ingred word processor results
		print(main_ingreds)

		for _ in range(5):
			print(' ') 

		links_used = get_used_links(main_ingreds)
		print(links_used)
		other_ingreds = ProcessWords(filter_commas(self.ids.other_ingred.text)) # other ingred word processor results

		self.ids.main_ingred.text = ''
		self.ids.other_ingred.text = '' 

		global results # making sure results can be raed in ResultsWindow
		results = get_foods(main_ingreds, other_ingreds, links_used) # creating results
		global md_index_matrix
		md_index_matrix = {} # this is a dict which matches kivymd.uix.list.ThreeLineListItem object with index in the data list

		##### Just some console stuff #####
		for _ in range(3):
			print(' ')
		print(f'RESULTS: {results}')
		for _ in range(3):
			print(' ')



class ResultsWindow(Screen):
	def on_enter(self): # this on_enter function is self explanatory
		list_view = MDList()
		scroll = ScrollView()
		for x, result in enumerate(results):
			items = ThreeLineListItem(text=f"{result[0]}",
										secondary_text=f'number of ingredients: {result[1]}',
										tertiary_text=f'time taken to cook: {result[-2]} minutes',
										bg_color=(60/255, 188/255, 66/255, 1),
										on_press=partial(change_screens, str(result)))
			md_index_matrix[str(items)] = x
			print(str(items), x)
			list_view.add_widget(items)
		scroll.add_widget(list_view)
		self.add_widget(scroll)


class RecipeWindow(Screen):
	def on_enter(self):
		print(f'SELECTED RESULT: ', selecected_result)
		Label = MDLabel(text=selecected_result[0], halign='center')
		self.add_widget(Label)
		

class WindowManager(ScreenManager):
    pass


#kv = Builder.load_file('RockettApp.kv')
Builder.load_file('RockettApp.kv')

class TheApp(MDApp):
	def build(self):
		global wm
		self.title = 'App'
		#return kv
		wm = WindowManager()
		return wm

if __name__ == '__main__':
	TheApp().run()
