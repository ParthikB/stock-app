import yfinance as yf

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

import os
from datetime import datetime

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



		# self.add_widget(Label(text='Total Shares :'))
		# self.total_shares = TextInput(text=total_shares, multiline=False)
		# self.add_widget(self.total_shares)

		# self.add_widget(Label(text='Buy Price :'))
		# self.buy_price = TextInput(text=buy_price, multiline=False)
		# self.add_widget(self.buy_price)

		# self.add_widget(Label()) # Empty label to move the Button toward right
		# self.submit = Button(text='Submit!')
		# self.submit.bind(on_press=self.submit_button) # Button Action

		# self.add_widget(self.submit)


		self.add_widget(Label(text='Net Change : '))
		self.net = Label()
		self.add_widget(self.net)


	def update(self):
		stock = yf.Ticker('YESBANK.NS')
		cur_price = stock.history('max')["Close"][-1]

		cur_time = datetime.now().strftime('%H : %M : %S')

		total_shares   = 150
		buy_price      = 29

		invested = total_shares*buy_price
		cur_amount = total_shares*cur_price
		balance = cur_amount - invested

		emotion = 'PROFIT' if balance > 0 else 'LOSS'
		
		self.net.text = str(f'''Rs.{balance} | {emotion}
-------------------------
Last Updated : {cur_time}''')


	def on_touch_up(self, touch):
		self.update()
		# total_shares   = int(self.total_shares.text)
		# buy_price      = int(self.buy_price.text)
		# # username = self.username.text

		# invested = total_shares*buy_price
		# cur_amount = total_shares*cur_price
		# balance = cur_amount - invested

		# net = 'PROFIT' if balance > 0 else 'LOSS'

		# print(f'Total Shares : {total_shares}')
		# print(f'Buy Price    : Rs.{buy_price}')
		# print(f'Current Price: Rs.{cur_price}')
		# print('------------------------------')
		# print(f'Investment   : Rs.{invested}')
		# print(f'Balance      : Rs.{balance}')
		# print(f'Net          : {net}')

		# print(port, ip, username)

		#### IMPORTANT
		# Saving the details for future use
		# with open('prev_details.txt', 'w') as f:
		# 	f.write(f'{total_shares},{buy_price}')




class StockApp(App):
	
	def build(self):
		return HomePage()


if __name__ == "__main__":
	StockApp().run()
