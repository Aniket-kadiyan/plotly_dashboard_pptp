import dash
from dash import Dash, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pyodbc
import array
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import dbcon

# cnxn = pyodbc.connect(driver='{SQL Server}', server='ANIKETKADIYAN-P\AKSERVER',database='ProefficientDB', trusted_connection='yes')

# cursor = cnxn.cursor()
tablename1 = "ProductionRejectReasonMapping"
df1 = dbcon.tbl_ProductionRejectReasonMapping
# pd.read_sql("SELECT * from {}".format(tablename1), cnxn)
# print(df1)
tablename2 = "RejectionReason"
df2 = dbcon.tbl_RejectionReason
# pd.read_sql("SELECT * from {}".format(tablename2), cnxn)
# print(df2)
tablename3 = "ProductionEntry"
df3 = dbcon.tbl_ProductionEntry
# pd.read_sql("SELECT * from {}".format(tablename3), cnxn)
# print(df3)
df4 = pd.merge(df1, df2, how="inner", on=["ReasonId"])
# print(df4)
df = pd.merge(df4, df3, how="inner", on=["ProductionId"])
# print(df)

dash.register_page(__name__, external_stylesheets=[dbc.themes.DARKLY], src="/REJECTION_ANALYSIS_PARETO",title="Dashboard", meta_tags=[
                   {'name': 'viewport', 'content': 'width=device-width , initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
# server = app.server
colors = {
    'background': '#111111',
    'text': 'rgb(0,0,0)'
}
layout = dbc.Container(
    [
        dcc.Markdown(
            "REJECTION ANALYSIS - Pareto",
            style={'fontSize': 40,
                   'textAlign': 'center',
                   'color': 'white'},
            className="my-4",
        ),
        dbc.Row(
            [
                dcc.DatePickerRange(
                    id="datepicker",
                    min_date_allowed=min(df["ProductionDateOnly"]),
                    max_date_allowed=max(df["ProductionDateOnly"]),
                    end_date=max(df["ProductionDateOnly"]),
                    start_date=min(df["ProductionDateOnly"]),
                    clearable=False,
                ),
            ]
        ),
        dbc.Row(
            [
                dcc.Loading(dcc.Graph(id='graph-content1'),type="cube")
            ]
        ),
    ], fluid=True, style={
        "background-color": "black"
    },
)


@callback(
    Output('graph-content1', 'figure'),
    Input("datepicker", "start_date"),
    Input("datepicker", "end_date"),
)
def update_graph(start_date, end_date):
    dff = df.query(
        "ProductionDateOnly >= @start_date & ProductionDateOnly <= @end_date")
    dfg = dff.groupby(['ReasonDescription'])[
        'RejectCount'].sum().reset_index(name='sum')
    print(dfg)
    dfg = dfg.sort_values(by=["sum"], ascending=False)
    print(dfg)
    dfg["csum"] = dfg["sum"].cumsum()
    dfg["pareto"] = (dfg["csum"]/dfg["sum"].sum())*100
    trace1 = go.Bar(
        x=dfg["ReasonDescription"],
        y=dfg["sum"],
        showlegend=False
    )
    trace2 = go.Scatter(
        x=dfg["ReasonDescription"],
        y=dfg["pareto"],
        yaxis='y2',
        showlegend=False
    )
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(trace1)
    fig.add_trace(trace2, secondary_y=True)
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})
    fig['layout']['yaxis2']['showgrid'] = False
    return fig


# if __name__ == '__main__':
#     app.run(debug=True)
