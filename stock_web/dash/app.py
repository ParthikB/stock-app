import yfinance as yf
from binance.client import Client

import dash, dash_table
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Output, Input, State
from dash.exceptions import PreventUpdate

import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

def update_val(data, security):
    
    if security == 'XRP':
        api_key    = 'jfdgMTk4LEnYl54Lto18zWAvyYS2GEOfvfwfnifaQawFE9TIMUlZnjCPqubWKWoP'
        secret_key = 'H0UfJS8hCj13a3StI3IgZ46C0AfkaUS6zwf7s0bK8bDv1cqP8x49kHe4M4phVfnI'
        
        client = Client(api_key, secret_key)

        # Getting the average price of the COIN in $ and then converting into INR
        cur_price    = client.get_avg_price(symbol=f'{security}USDT')
        cur_price    = round(float(cur_price['price']) * 72, 2)

        # Getting the balance of the security
        total_shares = client.get_asset_balance(asset=security)
        total_shares = round(float(total_shares['free']), 2) - 52 - 41 - 41 # 52:Pranay, 41:Aman, 41:Mayank

        buy_price    = '--'
        
        investement  = 3500
          
    elif security == 'YESBANK.NS':
        stock          = yf.Ticker(security)
        cur_price      = stock.history('max')["Close"][-1]

        total_shares   = [71, 26]
        buy_price      = [27, 35]

        investement    = round(sum([x*y for x, y in zip(total_shares, buy_price)]), 2)
    
    ##########################################################    
    temp_total_shares = total_shares
    if type(total_shares) == list:
        temp_total_shares = sum(total_shares)
        
    returns         = round(temp_total_shares * cur_price, 2)
        
    net             = round(returns - investement, 2)
    emotion_percent = round((returns/investement)*100)

    emotion         = 'PROFIT' if net > 0 else 'LOSS'
        
   
    data[security]['Current Price'] = str(cur_price)
    data[security]['Total Shares']  = str(total_shares)
    data[security]['Buy Price']     = str(buy_price)
    data[security]['Investment']    = str(investement)
    data[security]['Returns']       = str(returns)
    data[security]['Net']           = str(net)
    
    return data



# df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/solar.csv')

def create_dummy_df():
	df = pd.DataFrame(columns=['Info','YESBANK.NS', 'XRP'])
	df['Info'] = ['Current Price', 'Total Shares', 'Buy Price', 'Investment', 'Returns', 'Net']
	df.index = df.Info
	return df
data = create_dummy_df()


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


app.layout = html.Div([
    # The memory store reverts to the default on every page refresh
    dcc.Store(id='database', storage_type='session'),

    html.Div([

				dash_table.DataTable(
				    id='table',
				    columns=[{"name": i, "id": i} for i in data.columns],
				    data=data.to_dict('records'),
				),
			
			    html.Button('Refresh', id='button'),

			    html.Div(id='output-container-button',
             			 children='Refresh to update values..!'),

			    

						])
])

store = 'database'

@app.callback(Output(store, 'data'),
                  [Input('button', 'n_clicks')],
                  [State(store, 'data')])
def on_click(n_clicks, data):
    if n_clicks is None:
        raise PreventUpdate

    # Give a default data dict with 0 clicks if there's no data.
    data = create_dummy_df()
    
    for security in ['YESBANK.NS', 'XRP']:
    	data = update_val(data, security)

    data = data.to_dict('records')
    print(type(data))
    return data


# output the stored clicks in the table cell.
@app.callback(Output('table', 'data'),
              # Since we use the data prop in an output,
              # we cannot get the initial data on load with the data prop.
              # To counter this, you can use the modified_timestamp
              # as Input and the data as State.
              # This limitation is due to the initial None callbacks
              # https://github.com/plotly/dash-renderer/pull/81
              [Input(store, 'modified_timestamp')],
              [State(store, 'data')])
def on_data(ts, data):
    if ts is None:
        raise PreventUpdate

    return data


# @app.callback(
# 	dash.dependencies.Output('table', 'data'),
#     [dash.dependencies.Input('button', 'n_clicks')],
#     [dash.dependencies.State('database', 'data')])
# def on_click(data, securities=['YESBANK.NS', 'XRP']):
# 	print(type(data))
# 	for security in securities:
# 		df = update_val(df, security)

# 	return df.to_dict('records')


if __name__ == '__main__':
    app.run_server(port=2222, debug=True)
