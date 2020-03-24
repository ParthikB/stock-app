import yfinance as yf

import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button

from binance.client import Client

import os
from datetime import datetime
import numpy as np

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

		self.cols = 3
		self.rows = 4
		'''
		------------------------------------------
		|Security		| Yes Bank | Ripple (XRP)|
		------------------------------------------
		|Current price	|		   |			 |
		|Total shares	|		   |			 |
		|Buy Price		|		   |			 |
		|Investment		|		   |			 |
		|Returns		|		   |			 |
		------------------------------------------
		|Net Security	|		   | 			 |
		------------------------------------------
		|Last Updated   | 		NET EMOTION      |
		------------------------------------------
		'''

		self.security = Label(text='Security')
		self.details  = Label(text='''Current Price

Total shares

Buy Price

Investment

Returns''')
		self.net_security     = Label(text='Net Security')
		self.yes_bank         = Label(text='YESBANK.NS (INR)')
		self.ripple           = Label(text='XRP (INR)')
		self.yes_bank_details = Label()
		self.ripple_details   = Label()
		self.yes_bank_net     = Label(bold=True)
		self.ripple_net       = Label(bold=True)
		self.misc             = Label(text='Tap anywhere to update', color=[0.2, 0.2, 1, 1])
		self.total_net_info   = Label(text='Total Net :', color=[1, 1, 0, 1], font_size='25dp')
		self.total_net 		  = Label(bold=True, font_size='35dp')


		self.add_widget(self.security)
		self.add_widget(self.yes_bank)
		self.add_widget(self.ripple)	
		self.add_widget(self.details)
		self.add_widget(self.yes_bank_details)
		self.add_widget(self.ripple_details)
		self.add_widget(self.net_security)
		self.add_widget(self.yes_bank_net)
		self.add_widget(self.ripple_net)
		self.add_widget(self.misc)
		self.add_widget(self.total_net_info)
		self.add_widget(self.total_net)




		# with self.info.text:
		#     Color(0, 1, 0)


	def update_share(self):
		stock 		   = yf.Ticker('YESBANK.NS')
		cur_price 	   = stock.history('max')["Close"][-1]


		total_shares   = [71, 79]
		buy_price      = [27, 35]

		investement    = round(sum([x*y for x, y in zip(total_shares, buy_price)]), 2)
		returns        = round(sum(total_shares)*cur_price, 2)
		net            = round(returns - investement, 2)

		emotion        = 'PROFIT' if net > 0 else 'LOSS'
		
		self.yes_bank_details.text = f'''{cur_price}

{total_shares}

{buy_price}

{investement}

{returns}'''
		
		self.yes_bank_net.text  = f'{net}'
		self.yes_bank_net.color =[0, 1, 0, 1] if emotion == 'PROFIT' else [1, 0, 0, 1]


	def update_binance(self):

		API = os.environ.get('BINANCE_API')
		KEY = os.environ.get('BINANCE_SECRET_KEY')

		client = Client(API, KEY)

		COIN = 'XRP'

		# Getting the balance of the COIN
		total_shares = client.get_asset_balance(asset=COIN)
		total_shares = round(float(total_shares['free']), 2)

		# Getting the average price of the COIN in $
		cur_price    = client.get_avg_price(symbol=f'{COIN}USDT')
		cur_price    = round(float(cur_price['price']) * 72, 2)

		investement  = 6500
		returns      = round(total_shares * cur_price, 2)

		net          = round(returns - investement, 2)
		buy_price    = '--'
		emotion      = 'PROFIT' if net > 0 else 'LOSS'

		self.ripple_details.text = f'''{cur_price}

{total_shares}

{buy_price}

{investement}

{returns}'''
		
		self.ripple_net.text  = f'{net}'
		self.ripple_net.color =[0, 1, 0, 1] if emotion == 'PROFIT' else [1, 0, 0, 1]


		# orders = client.get_all_orders(symbol='XRPBTC', limit=10)

		# Orders
		# for i in orders:
		#     if i['status'] == 'FILLED':
		#         print(i['symbol'], i['price'], i['origQty'])


		# converting the binance-api time to readable format
		#from datetime import datetime
		#t = TIMESTAMP
		#time = datetime.fromtimestamp(t/1000)
		# human_readable = time.strftime('%Y : %m : %d')

	def update_net(self):
		net = float(self.ripple_net.text) + float(self.yes_bank_net.text)
		self.total_net.text = f'{round(np.abs(net), 2)}'

		emotion      = 'PROFIT' if net > 0 else 'LOSS'
		self.total_net.color =[0, 1, 0, 1] if emotion == 'PROFIT' else [1, 0, 0, 1]



	def on_touch_up(self, touch):
		cur_time       = datetime.now().strftime('%H:%M:%S')

		self.update_share()
		self.update_binance()
		self.update_net()
		self.misc.text = f'''
Last Updated 
---------------
   {cur_time}'''

		#### IMPORTANT
		# Saving the details for future use
		# with open('prev_details.txt', 'w') as f:
		# 	f.write(f'{total_shares},{buy_price}')




class StockApp(App):
	
	def build(self):
		return HomePage()


if __name__ == "__main__":
	StockApp().run()
