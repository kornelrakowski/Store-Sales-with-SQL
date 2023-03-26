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
	# Returns Pandas Datataframe containing results of SQL query

	database = mysql.connector.connect(**config)
	cursor = database.cursor()
	cursor.execute('USE {}'.format(DB_NAME))

	result = pd.read_sql(statement, database)

	cursor.close()
	database.close()

	return result

columns = ['city', 'state', 'type', 'cluster']

def list_options(column):
	# Returns list of unique values in given column of table

	statement = """SELECT DISTINCT {} FROM stores""".format(column)
	df = query(statement)
	output = pd.Series(df[column]).tolist()

	return output

def generate_item(column):
	# Returns NavItem for given column

	item = dbc.NavItem([
		dbc.DropdownMenu(label=column, children=[
			dcc.Checklist(list_options(column), id='select_{}'.format(column), labelStyle={'display': 'block'})
		])
	])

	return item

dash.register_page(__name__, path='/stores')

layout = html.Div(
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dbc.Nav([
					generate_item(column) for column in columns
				])
			]),
			dbc.Col([
				dbc.Nav([
					dbc.NavItem([
						dbc.DropdownMenu(label='ORDER BY', children=[
							dcc.RadioItems(['store_nbr'] + columns, 'store_nbr', id='order_by', labelStyle={'display': 'block'})
						])
					])		
				])
			])
		]),
		dbc.Row([
			dbc.Col([
				html.Div(id='stores_statement')
			])
		]),
		dbc.Row([
			dbc.Col([
				html.Div(id='stores_table')
			])
		]),
	], fluid=True)
)

@callback(
	Output('stores_table', 'children'),
	Output('stores_statement', 'children'),
	Input('select_city', 'value'),
	Input('select_state', 'value'),
	Input('select_type', 'value'),
	Input('select_cluster', 'value'),
	Input('order_by', 'value'),
)

def render_table(select_city, select_state, select_type, select_cluster, order_by):

	# Create dictionary with selected filters
	dict_keys = columns
	dict_values = [select_city, select_state, select_type, select_cluster]
	selections = dict(zip(dict_keys, dict_values))

	# Create SQL statement
	if all((item is None) or (not item) for item in selections.values()):
		statement = """SELECT * FROM stores"""
	else:
		statement = """SELECT * FROM stores WHERE """
		partial_statements = []
		for key in dict_keys:
			if (selections[key]):
				partial_statement = """ OR """.join(['{}="{}"'.format(key, item) for item in selections[key]])
				partial_statement	= '({})'.format(partial_statement)
				partial_statements.append(partial_statement)
		statement += ' AND '.join(partial_statements)

	statement += ' ORDER BY {}'.format(order_by)

	print(statement)

	df = query(statement)
	table = DataTable(df.to_dict('records'), [{"name": i, "id": i} for i in df.columns])

	return table, statement