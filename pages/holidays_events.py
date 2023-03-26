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

columns = ['type', 'locale', 'locale_name', 'description', 'transferred']

def list_options(column):
	# Returns list of unique values in given column of table

	statement = """SELECT DISTINCT {} FROM holidays_events""".format(column)
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

dash.register_page(__name__, path='/holidays_events')

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
							dcc.RadioItems(['date'] + columns, 'date', id='order_by', labelStyle={'display': 'block'})
						])
					])		
				])
			])
		]),
		dbc.Row([
			dbc.Col([
				html.Div(id='statement')
			])
		]),
		dbc.Row([
			dbc.Col([
				html.Div(id='holidays_table')
			])
		]),
	], fluid=True)
)

@callback(
	Output('holidays_table', 'children'),
	Output('statement', 'children'),
	Input('select_type', 'value'),
	Input('select_locale', 'value'),
	Input('select_locale_name', 'value'),
	Input('select_description', 'value'),
	Input('select_transferred', 'value'),
	Input('order_by', 'value'),
)

def render_table(select_type, select_locale, select_locale_name, select_description, select_transferred, order_by):

	# Create dictionary with selected filters
	dict_keys = columns
	dict_values = [select_type, select_locale, select_locale_name, select_description, select_transferred]
	selections = dict(zip(dict_keys, dict_values))

	# Create SQL statement
	if all((item is None) or (not item) for item in selections.values()):
		statement = """SELECT * FROM holidays_events"""
	else:
		statement = """SELECT * FROM holidays_events WHERE """
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