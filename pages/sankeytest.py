import dash
from dash import Dash, dcc, Input, Output, html, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
import random
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
labellist = [*df.MachineName.unique(), *df.ReasonName.unique()]
machinelist = df.MachineName.unique()
reasonlist = df.ReasonName.unique()
sourcelist = []
destinationlist = []
valuelist = []
# print(machinelist, "\n\n", reasonlist)
colors = {
    'background': '#111111',
    'text': 'rgb(0,0,0)'
}


def populateGraph(mlist, rlist):
    # sourcelist = []
    # destinationlist = []
    # valuelist = []
    # print(mlist, rlist)
    for machine in mlist:
        dff = df[df.MachineName == machine]
        dfg = dff.groupby(['ReasonName'])[
            'ReasonName'].count().reset_index(name='count')
        # print("machine name:::", machine,
        #       "\nreasons::: ", dfg.ReasonName.unique())
        for reason in rlist:
            if (reason in dfg.ReasonName.unique()):
                sourcelist.append(labellist.index(machine))
                destinationlist.append(labellist.index(reason))
                # print("reason::: ",reason)
                val = dfg.loc[dfg['ReasonName'] == reason, 'count'].iloc[0]
                # print("val::: ",val)
                valuelist.append(val)


populateGraph(machinelist, reasonlist)
# print(px.colors.qualitative.Plotly)
# print(valuelist)

dash.register_page(__name__, external_stylesheets=[dbc.themes.DARKLY],src="/sankey")

layout = html.Div(
    [
        html.H2("Sankey graph test", style={"textAlign": "center"},),
        html.Br(),
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    id="machineselection",
                    value=machinelist,
                    options=machinelist,
                    multi=True,
                    style={
                        "color": "black",
                        "background-color": "black",
                        "border": "0px solid black"
                    },
                ),
            ], width="auto",align="Left",),
            dbc.Col([
                dcc.Dropdown(
                    id="reasonselection",
                    value=reasonlist,
                    options=reasonlist,
                    multi=True,
                    style={
                        "color": "black",
                        "background-color": "black",
                        "border": "0px solid black"
                    },
                ),
            ], width="auto",
                align="Right",),
        ]),

        dcc.Graph(id="graph"),
    ]
)


@callback(
    Output("graph", "figure"),
    Input("machineselection", "value"),
    Input("reasonselection", "value"),
)
def render_content(mlisti, rlisti):
    # populateGraph(mlisti,rlisti)
    sourcelist = []
    destinationlist = []
    valuelist = []
    # print(mlisti, rlisti)
    for machine in mlisti:
        dff = df[df.MachineName == machine]
        dfg = dff.groupby(['ReasonName'])[
            'ReasonName'].count().reset_index(name='count')
        # print("machine name:::", machine,
        #       "\nreasons::: ", dfg.ReasonName.unique())
        for reason in rlisti:
            if (reason in dfg.ReasonName.unique()):
                sourcelist.append(labellist.index(machine))
                destinationlist.append(labellist.index(reason))
                # print("reason::: ",reason)
                val = dfg.loc[dfg['ReasonName'] == reason, 'count'].iloc[0]
                # print("val::: ",val)
                valuelist.append(val)

    node = dict(
        pad=400000000000000,
        thickness=20,
        line=dict(
            color="red",
            width=0.5,
        ),
        label=labellist
    )
    link = dict(
        arrowlen=50,
        source=sourcelist,
        target=destinationlist,
        value=valuelist
    )
    fig = go.Figure(go.Sankey(link=link, node=node, arrangement='freeform'))
    fig.update_layout(font_size=10, autosize=True, width=1500, height=850,)
    fig.update_layout(uniformtext_minsize=12, uniformtext_mode='hide')
    fig.update_layout(
        {"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})

    return fig


# if __name__ == "__main__":
#     app.run_server(debug=True)

# import plotly.graph_objects as go

# fig = go.Figure(go.Sankey(
#     arrangement = "snap",
#     node = {
#         "label": ["A", "B", "C", "D", "E", "F"],
#         "x": [0.2, 0.1, 0.5, 0.7, 0.3, 0.5],
#         "y": [0.7, 0.5, 0.2, 0.4, 0.2, 0.3],
#         'pad':10},  # 10 Pixels
#     link = {
#         "source": [0, 0, 1, 2, 5, 4, 3, 5],
#         "target": [5, 3, 4, 3, 0, 2, 2, 3],
#         "value": [-1, 2, 1, 1, 1, 1, 1, 2]}))

# fig.show()
