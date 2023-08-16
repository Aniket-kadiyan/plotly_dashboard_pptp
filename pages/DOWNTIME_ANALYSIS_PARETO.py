import dash
from dash import Dash, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dbcon

import pyodbc

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
machinelist = df.MachineName.unique()
df["StartTime"] = pd.to_datetime(df["StartTime"])
df["EndTime"] = pd.to_datetime(df["EndTime"])

dash.register_page(__name__, external_stylesheets=[dbc.themes.DARKLY], src="/DOWNTIME_ANALYSIS_PARETO",title="Dashboard", meta_tags=[
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
            "DOWNTIME ANALYSIS - PARETO",
            style={'fontSize': 40,
                   'textAlign': 'center',
                   'color': 'white'},
            className="my-4",
        ),
        dbc.Row(
            [
                dcc.Dropdown(
                    id='dropdown-selection',
                    value=machinelist,
                    options=machinelist,
                    multi=True,
                    style={
                        "color": "black",
                        "background-color": "black",
                        "border": "0px solid white",
                        
                    },
                ),
            ],
        ),
        dbc.Row(
            [

                dbc.Col(
                    [
                        dcc.Tabs(
                            id="tabs",
                            value="tab-1",
                            children=[
                                dcc.Tab(
                                    label="Time",
                                    value="tab-1",
                                    children=[dcc.Loading(dcc.Graph(id="bar1"),type="cube")],
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                                dcc.Tab(
                                    label="Frequency",
                                    value="tab-2",
                                    children=[dcc.Loading(dcc.Graph(id="bar2"),type="cube")],
                                    style=tab_style,
                                    selected_style=tab_selected_style,
                                ),
                            ],
                        ),
                    ],
                    style={
                        "color": "white",
                        "background-color": "black",
                        "border": "blue"
                    },
                ),
            ]
        ),
    ], fluid=True, style={
        "background-color": "black"
    },
)


@callback(
    Output("bar1", "figure"),
    Output("bar2", "figure"),
    Input('dropdown-selection', 'value'),
)
def render_content(value):
    dff = df[df["MachineName"].isin(value)]
    dfg1 = dff.groupby(['ReasonName'])[
        'TotalStoppageTime'].sum().reset_index(name='sum')
    dfg2 = dff.groupby(['ReasonName'])[
        'ReasonName'].count().reset_index(name='count')
    # print(dfg1)
    # print(dfg2)
    dfg1 = dfg1.sort_values(by=["sum"], ascending=False)
    dfg2 = dfg2.sort_values(by=["count"], ascending=False)
    dfg1["cumulative"] = dfg1["sum"].cumsum()
    dfg2["cumulative"] = dfg2["count"].cumsum()
    dfg1["cumulative%"] = (dfg1["cumulative"]/dfg1["sum"].sum())*100
    dfg2["cumulative%"] = (dfg2["cumulative"]/dfg2["count"].sum())*100
    # print(dfg1)
    trace1 = go.Bar(
        x=dfg1["ReasonName"],
        y=dfg1["sum"],
        showlegend=False
    )
    trace2 = go.Scatter(
        x=dfg1["ReasonName"],
        y=dfg1["cumulative%"],
        yaxis='y2',
        showlegend=False
    )
    bar1_fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar1_fig.add_trace(trace1)
    bar1_fig.add_trace(trace2, secondary_y=True)
    bar1_fig['layout'].update(height=800, width=1200, xaxis=dict(tickangle=90))
    bar1_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    bar1_fig['layout']['yaxis2']['showgrid'] = False
    # bar1_fig._config = dict({'scrollZoom': True})
    # bar1_fig.update_layout(yaxis_tickformat = '%' ,secondary_y=True)
    trace1 = go.Bar(
        x=dfg2["ReasonName"],
        y=dfg2["count"],
        showlegend=False
    )
    trace2 = go.Scatter(
        x=dfg2["ReasonName"],
        y=dfg2["cumulative%"],
        # range_y = [0,dfg2["count"].sum()],
        # color = dfg2["ReasonName"],
        yaxis='y2',
        showlegend=False
    )
    bar2_fig = make_subplots(specs=[[{"secondary_y": True}]])
    bar2_fig.add_trace(trace1)
    bar2_fig.add_trace(trace2, secondary_y=True)
    bar2_fig['layout'].update(height=800, width=1200, xaxis=dict(
        tickangle=90
    ))
    bar2_fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    bar1_fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})
    bar2_fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})
    bar2_fig['layout']['yaxis2']['showgrid'] = False
    return (bar1_fig, bar2_fig)


# if __name__ == "__main__":
#     app.run_server(debug=True)
