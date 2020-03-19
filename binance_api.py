from binance.client import Client

api_key    = 'jfdgMTk4LEnYl54Lto18zWAvyYS2GEOfvfwfnifaQawFE9TIMUlZnjCPqubWKWoP'
secret_key = 'H0UfJS8hCj13a3StI3IgZ46C0AfkaUS6zwf7s0bK8bDv1cqP8x49kHe4M4phVfnI'

client = Client(api_key, secret_key)

COIN = 'XRP'

# Getting the balance of the COIN
balance = client.get_asset_balance(asset=COIN)
balance = float(balance['free'])

# Getting the average price of the COIN in $
avg_price = client.get_avg_price(symbol=f'{COIN}USDT')
avg_price = float(avg_price['price'])


net_value = balance * avg_price


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

