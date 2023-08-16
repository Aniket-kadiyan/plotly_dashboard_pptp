from dash import html
import dash

dash.register_page(__name__, title="Dashboard")

layout = html.H1("Welcome to Dashboard, please navigate using top bar")