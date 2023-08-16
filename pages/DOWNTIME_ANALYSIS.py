import dash
from dash import Dash, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pyodbc
import dbcon

# cnxn = pyodbc.connect(driver='{SQL Server}', server='ANIKETKADIYAN-P\AKSERVER',
#                       database='ProefficientDB', trusted_connection='yes')

# tablename7 = "MasterMachine"
# machinedata = pd.read_sql("SELECT * from {}".format(tablename7), cnxn)
# tablename2 = "StopageReason"
# reasondata = pd.read_sql("SELECT * from {}".format(tablename2), cnxn)
# tablename5 = "BreakDownEntry"
# breakdowndata = pd.read_sql("SELECT * from {}".format(tablename5), cnxn)
breakdowndata = dbcon.tbl_BreakDownEntry
machinedata = dbcon.tbl_MasterMachine
reasondata = dbcon.tbl_StopageReason
df1 = pd.merge(breakdowndata, machinedata, how="inner", on=["MachineID"])
df = pd.merge(df1, reasondata, how="inner", on=["ReasonId"])

df["StartTime"] = pd.to_datetime(df["StartTime"])
df["EndTime"] = pd.to_datetime(df["EndTime"])

dash.register_page(__name__, external_stylesheets=[dbc.themes.DARKLY], src="/DOWNTIME_ANALYSIS",title="Dashboard", meta_tags=[
                   {'name': 'viewport', 'content': 'width=device-width , initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
# dash.register_page
# dash.register_page(__name__)
colors = {
    'background': '#111111',
    'text': 'rgb(0,0,0)'
}
tabs_styles = {
    'height': '44px'
}
tab_style = {
    'borderBottom': '1px solid #d6d6d6',
    'padding': '6px',
    'fontWeight': 'bold',
    "color": "white",
    "backgroundColor": "black"

}

tab_selected_style = {
    'borderTop': '3px solid #d6d6d6',
    'borderBottom': '2px solid #d6d6d6',
    "borderLeft": "2px solid #d6d6d6",
    "borderRight": "2px solid #d6d6d6",
    "borderColor": "blue",
    'backgroundColor': 'black',
    'color': 'white',
    'padding': '6px'
}
layout = dbc.Container(
    [
        dcc.Markdown(
            "DOWNTIME ANALYSIS",
            style={'fontSize': 40,
                   'textAlign': 'center',
                   'color': 'white'},
            className="my-4",
        ),
        dbc.Col(
            [
                dbc.Row(
                    [
                        dcc.DatePickerRange(
                            id="datepicker",
                            min_date_allowed=min(df["StartTime"]),
                            max_date_allowed=max(df["EndTime"]),
                            end_date=max(df["EndTime"]),
                            start_date=min(df["StartTime"]),
                            clearable=False,
                            style={
                                "color": "white",
                                "background-color": "black",
                                "border": "blue"
                            },
                        ),
                    ],
                ),
                dbc.Row(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-1",
                            children=[
                                dcc.Tab(
                                    label="Time",
                                    value="tab-1",
                                    children=[dcc.Loading(
                                        dcc.Graph(id="pie1"), type="cube")],
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Frequency",
                                    value="tab-2",
                                    children=[dcc.Loading(
                                        dcc.Graph(id="pie2"), type="cube")],
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                        ),
                    ],
                ),
            ]
        ),
    ], fluid=True, style={
        "background-color": "black"
    },
)


@callback(
    Output("pie1", "figure"),
    Output("pie2", "figure"),
    Input("datepicker", "start_date"),
    Input("datepicker", "end_date"),
)
def render_content(start_date, end_date):
    dff = df.query("StartTime > @start_date & EndTime < @end_date")
    dfg1 = dff.groupby(['ReasonName'])[
        'TotalStoppageTime'].sum().reset_index(name='sum')
    dfg2 = dff.groupby(['ReasonName'])[
        'ReasonName'].count().reset_index(name='count')
    print(dfg1)
    print(dfg2)
    pie1_fig = px.pie(dfg1, values="sum", names="ReasonName")
    pie1_fig.update_traces(textposition='inside')
    pie1_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    pie2_fig = px.pie(dfg2, values="count", names="ReasonName")
    pie2_fig.update_traces(textposition='inside')
    pie2_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    pie1_fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})
    pie2_fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})

    return (pie1_fig, pie2_fig)


# if __name__ == "__main__":
#     app.run_server(debug=True)
