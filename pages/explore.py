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

dash.register_page(__name__, path='/explore')

def query(statement):

	database = mysql.connector.connect(**config)
	cursor = database.cursor()
	cursor.execute('USE {}'.format(DB_NAME))

	result = pd.read_sql(statement, database)

	cursor.close()
	database.close()

	return result

layout = html.Div(
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dbc.Nav([
					dbc.NavItem(
						dbc.Input(id="statement", placeholder="SQL statement", type="text"),
					),
					dbc.NavItem(
    				dbc.Button("Query", id="query-button", className="me-2", n_clicks=0),
					),
				])
			])
		]),
		dbc.Row([
			dbc.Col([
				html.Div(id='table')
			])
		]),
	], fluid=True)
)

@callback(
	Output('table', 'children'),
	Input('query-button', 'n_clicks'),
	State('statement', 'value'),
	prevent_initial_call=True
)

def render_table(query_button, statement):

	df = query(statement)
	table = DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

	return table