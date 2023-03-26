from dash import Dash, dcc, html, callback, Input, Output, State
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from dash.exceptions import PreventUpdate

import mysql.connector

import pandas as pd

config = {
	'user': 'root', 
	'password': 'Supreme',
	'host': '127.0.0.1',
	'allow_local_infile': True,
	'get_warnings': True
}

DB_NAME = 'store_sales'

def query(statement):

	database = mysql.connector.connect(**config)
	cursor = database.cursor()
	cursor.execute('USE {}'.format(DB_NAME))

	result = pd.read_sql(statement, database)

	cursor.close()
	database.close()

	return result

statement = """SELECT DISTINCT store_nbr FROM transactions"""
stores = pd.Series(query(statement)['store_nbr']).tolist()

dash.register_page(__name__, path='/transactions')

layout = html.Div(
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dbc.Nav([
					dbc.NavItem([
						dbc.DropdownMenu(label='Store', children=[
							dcc.RadioItems(stores, stores[0], id='select_store', labelStyle={'display': 'block'})
						])
					])
				])
			])
		]),
		dbc.Row([
			dbc.Col([
				dcc.Graph(id='graph')
			])
		]),
	], fluid=True)
)

@callback(
	Output('graph', 'figure'),
	Input('select_store', 'value'),
	prevent_initial_call=True
)

def display_graph(select_store):

	# Plot transactions in selected store
	statement = """SELECT * FROM transactions WHERE store_nbr={}""".format(select_store)
	df = query(statement)
	fig = go.Figure(go.Scatter(x=df['date'], y=df['transactions']))

	return fig
