import yfinance as yf

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import os
from datetime import datetime

from kivy.graphics import Color, Rectangle


# def update_rect(instance, value):
#     instance.rect.pos = instance.pos
#     instance.rect.size = instance.size
   
# self.bind(pos=update_rect, size=update_rect)

kivy.require('1.11.1')

print('Fetching Details...')
# stock = yf.Ticker('YESBANK.NS')
# cur_price = stock.history('max')["Close"][-1]


class HomePage(GridLayout):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)

		self.cols = 2

		# if os.path.isfile('prev_details.txt'):
		# 	with open('prev_details.txt', 'r') as f:
		# 		details = f.read().split(',')

		# 		total_shares     = details[0]
		# 		buy_price       = details[1]
		# else:
		# 	total_shares     = ''
		# 	buy_price       = ''


		# self.add_widget(Label()) # Empty label to move the Button toward right
		# self.submit = Button(text='Submit!')
		# self.submit.bind(on_press=self.submit_button) # Button Action

		# self.add_widget(self.submit)

		self.info = Label(text='Net Change : ')
		self.add_widget(self.info)
		self.net = Label()
		self._ = Label()
		self.time = Label()
		self.add_widget(self.net)
		self.add_widget(self._)	
		self.add_widget(self.time)

		# with self.info.text:
		#     Color(0, 1, 0)


	def update(self):
		stock 		   = yf.Ticker('YESBANK.NS')
		cur_price 	   = stock.history('max')["Close"][-1]

		cur_time       = datetime.now().strftime('%H : %M : %S')

		total_shares   = [71, 26]
		buy_price      = [27, 35]

		invested       = sum([x*y for x, y in zip(total_shares, buy_price)])
		cur_amount     = sum(total_shares)*cur_price
		balance        = round(cur_amount - invested, 2)

		emotion        = 'PROFIT' if balance > 0 else 'LOSS'
		
		self.net.text  = str(f'Rs. {balance}')
		self.time.text =\
str(f'''
-------------------------
Last Updated : {cur_time}''')

		self.net.color=[0, 1, 0, 1] if emotion == 'PROFIT' else [1, 0, 0, 1]



	def on_touch_up(self, touch):
		self.update()
		#### IMPORTANT
		# Saving the details for future use
		# with open('prev_details.txt', 'w') as f:
		# 	f.write(f'{total_shares},{buy_price}')




class StockApp(App):
	
	def build(self):
		return HomePage()


if __name__ == "__main__":
	StockApp().run()
