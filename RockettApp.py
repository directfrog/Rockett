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
from kivymd.icon_definitions import md_icons
from kivy.properties import ObjectProperty
from functools import partial
from kivy.uix.scrollview import ScrollView



#WindowManager = ScreenManager()

def showresults(self, item):
	for x in range(3):
		print(' ')
	print('the data of what you selected: ')
	print(' ')
	print(result_matrix[self])

def recieve_select(self, index):
    print('selected: ', index.text)

class TextEnterWindow(Screen):
	def button_on(self):
		self.ids.button_image.source = 'button1.png'

	def button_off(self):
		self.ids.button_image.source = 'button2.png' 

	def run_system(self):
		main_ingred = ProcessWords(self.ids.main_ingred.text)
		other_ingreds = ProcessWords(filter_commas(self.ids.other_ingred.text))

		# above here we are getting our main_ingred and other ingred results

		self.ids.main_ingred.text = ''
		self.ids.other_ingred.text = '' 

		global results # making sure results can be raed in ResultsWindow
		results = get_foods(main_ingred, other_ingreds) # creating results
		global result_matrix
		result_matrix = {}
		for result in results:
			result_matrix[result[0]] = result


class ResultsWindow(Screen):
	def on_enter(self): # this on_enter function is self explanatory
		list_view = MDList()
		scroll = ScrollView()

		for x, result in enumerate(results):
			items = ThreeLineListItem(text=f"{result[0]}",
										secondary_text=f'number of ingredients: {result[1]}',
										tertiary_text=f'time taken to cook: {result[-2]} minutes',
										bg_color=(60/255, 188/255, 66/255, 1),
										on_press=partial(showresults, result[0]))
			list_view.add_widget(items)
		scroll.add_widget(list_view)
		self.add_widget(scroll)

class RecipeWindow(Screen):
	pass


class WindowManager(ScreenManager):
    pass

kv = Builder.load_file('RockettApp.kv')
	

class TheApp(MDApp):
	def build(self):
		self.title = 'App'
		return kv

if __name__ == '__main__':
	TheApp().run()