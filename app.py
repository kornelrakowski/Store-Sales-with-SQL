from dash import Dash, dcc, html, Input, Output, State
import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dash_bootstrap_components as dbc
from dash.dash_table import DataTable
from dash.exceptions import PreventUpdate

import pandas as pd

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True, suppress_callback_exceptions = True)

app.layout = html.Div(
	dbc.Container([
		dbc.Row([
			dbc.Col([
				dbc.Nav([
					dbc.NavItem(
						dbc.Button('Explore', href='/explore'),
					),
					dbc.NavItem(
						dbc.Button('Transactions', href='/transactions'),
					),
					dbc.NavItem(
						dbc.Button('Holidays Events', href='/holidays_events'),
					),
					dbc.NavItem(
						dbc.Button('Stores', href='/stores'),
					),
				])
			])
		]),
		dbc.Row([
			dbc.Col([
				dash.page_container
			])
		]),
	], fluid=True)
)

if __name__ == '__main__':
	app.run_server(debug=True, use_reloader=True)

