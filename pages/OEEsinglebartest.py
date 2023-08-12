import dash
from dash import Dash, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pyodbc
import array
from datetime import date as dte
import plotly.graph_objects as go
import dbcon

# cnxn = pyodbc.connect(driver='{SQL Server}', server='ANIKETKADIYAN-P\AKSERVER',
#                       database='ProefficientDB', trusted_connection='yes')

# cursor = cnxn.cursor()
tablename1 = "Shift"
df1 = dbcon.tbl_Shift
# pd.read_sql("SELECT * from {}".format(tablename1), cnxn)
# print(df1.columns)
tablename2 = "StopageReason"
df2 = dbcon.tbl_StopageReason
# pd.read_sql("SELECT * from {}".format(tablename2), cnxn)
# print(df2)
tablename3 = "ProductionEntry"
df3 = dbcon.tbl_ProductionEntry
# pd.read_sql("SELECT * from {}".format(tablename3), cnxn)
# print(df3)
tablename4 = "MasterProduct"
df4 = dbcon.tbl_MasterProduct
# pd.read_sql("SELECT * from {}".format(tablename4), cnxn)
print(df4.columns)
tablename5 = "BreakDownEntry"
df5 = dbcon.tbl_BreakDownEntry
# pd.read_sql("SELECT * from {}".format(tablename5), cnxn)
# print(df5)
df6 = pd.merge(df5, df2, how="inner", on=["ReasonId"])
# print(df4)
df = pd.merge(df6, df1, how="inner", on=["ShiftId"])
tablename7 = "MasterMachine"
df7 = dbcon.tbl_MasterMachine
# pd.read_sql("SELECT * from {}".format(tablename7), cnxn)
df6 = pd.merge(df6, df7, how="inner", on=["MachineID"])
df3 = pd.merge(df3, df7, how="inner", on=["MachineID"])


colors = {
    'background': '#111111',
    'text': 'rgb(0,0,0)'
}
dash.register_page(__name__, external_stylesheets=[dbc.themes.DARKLY],src="/OEE")
# server = app.server
machinelist = df7.MachineName.unique()
layout = dbc.Container(
    [
        dcc.Markdown(
            "OEE",
           style={'fontSize': 40,
                       'textAlign': 'center',
                       'color': 'white'},
            className="my-4",
        ),
        dbc.Row(
            [
                dbc.Col(
                    [
                        dcc.DatePickerSingle(
                            id="datepicker1",
                            min_date_allowed=min(df3["ProductionDateOnly"]),
                            max_date_allowed=max(df3["ProductionDateOnly"]),
                            date=max(df3["ProductionDateOnly"]),
                            initial_visible_month=max(
                                df3["ProductionDateOnly"]),
                            clearable=False,
                        ),
                    ],
                    width=4,
                ),
                dbc.Col(
                    [
                        dcc.Dropdown(
                            machinelist, 
                            machinelist[0], 
                            id='dropdown-selection',
                            style = {
                                "color" : "black"
                            }
                            ),
                    ],
                    width=4,
                ),

            ]
        ),
        dbc.Row(
            [
                dcc.Graph(id='graph-content',
                        #   figure={
                        #       'layout': {
                        #           'plot_bgcolor': colors['background'],
                        #           'paper_bgcolor': colors['background'],
                        #           'font': {
                        #               'color': colors['text']
                        #           }
                        #       }
                        #   }
                          )
            ]
        ),
    ], 
    fluid=True,
    # style={'textAlign': 'center',
    #        'color': colors["text"],
    #        'background-color': colors["background"]
    #        }
)


@callback(
    Output('graph-content', 'figure'),
    Input("datepicker1", "date"),
    Input('dropdown-selection', 'value'),
)
def update_graph(date, value):
    print(date, "\n", value)
    dff6 = df6[(df6["StartTime"].dt.date <= dte.fromisoformat(date))
               & (df6["EndTime"].dt.date >= dte.fromisoformat(date)) & (df6["MachineName"] == value)]
    # print(dff6.size, "\n", dff6, "\n")
    dff3 = df3[df3["ProductionDate"].dt.date == dte.fromisoformat(date)]
    dff3 = dff3[dff3["MachineName"] == value]
    # print(dff3.size, "\n", dff3, "\n")
    QRDF = dff3[["ShiftId", "TotalProduction", "Rejection"]]
    QRDF = QRDF.groupby(QRDF["ShiftId"]).sum().reset_index()
    QRDF.loc[len(QRDF)] = {"ShiftId": 3, "TotalProduction": dff3["TotalProduction"].sum(
    ), "Rejection": dff3["Rejection"].sum()}
    ARDF = pd.DataFrame(
        columns=["ShiftId", "unscheduled loss", "scheduled loss"])
    PRDF = pd.DataFrame(columns=["ShiftId", "CTxTP"])
    print(QRDF)
    # print(ARDF)
    for sid in df1.ShiftId.unique():
        dfg3 = dff3[dff3["ShiftId"] == sid]
        prods = dfg3.ProductID.unique()
        dfg3 = dfg3[["ProductID", "TotalProduction"]]
        # print(dfg3)
        dfg3 = dfg3.groupby(["ProductID"]).sum().reset_index()
        dfg3 = pd.merge(dfg3, df4, how="inner", left_on=[
                        "ProductID"], right_on=["ProductId"])
        dfg3 = dfg3[["ProductID", "TotalProduction", "CycleTime"]]
        # print(sid,":\n",dfg3)
        cttp = 0
        for id in prods:
            if len(dfg3.loc[dfg3["ProductID"] == id, "TotalProduction"]) == 1:
                cttp = cttp + (dfg3.loc[dfg3["ProductID"] == id, "TotalProduction"].iloc[0]
                               * dfg3.loc[dfg3["ProductID"] == id, "CycleTime"].iloc[0])
        PRDF.loc[(len(PRDF))] = {"ShiftId": sid, "CTxTP": cttp}
        # print(dfg3)
        # print("product IDs:\n", prods)
        dfg6 = dff6[dff6["ShiftId"] == sid]
        dfg6 = dfg6[["TotalStoppageTime", "IsSchLoss"]]
        dfg6 = dfg6.groupby(["IsSchLoss"]).sum().reset_index()
        schtime = 0
        unschtime = 0
        if len(dfg6.loc[dfg6["IsSchLoss"] == True, "TotalStoppageTime"]) == 1:
            schtime = dfg6.loc[dfg6["IsSchLoss"] ==
                               True, "TotalStoppageTime"].iloc[0]

        if len(dfg6.loc[dfg6["IsSchLoss"] == False, "TotalStoppageTime"]) == 1:
            unschtime = dfg6.loc[dfg6["IsSchLoss"] ==
                                 False, "TotalStoppageTime"].iloc[0]
        ARDF.loc[len(ARDF)] = {
            "ShiftId": sid, "unscheduled loss": unschtime, "scheduled loss": schtime}
    ARDF = pd.merge(ARDF, df1, how="inner", on=["ShiftId"])
    ARDF = ARDF[["ShiftId", "unscheduled loss",
                 "scheduled loss", "DurationMin"]]
    prdfsum = PRDF["CTxTP"].sum()
    PRDF.loc[len(PRDF)] = {"ShiftId": 3, "CTxTP": prdfsum}
    tul = ARDF["unscheduled loss"].sum()
    tsl = ARDF["scheduled loss"].sum()
    td = ARDF["DurationMin"].sum()
    ARDF.loc[len(ARDF)] = {"ShiftId": 3, "unscheduled loss": tul,
                           "scheduled loss": tsl, "DurationMin": td}
    print(ARDF)
    print(PRDF)
    OEEDF = pd.DataFrame(columns=["ShiftId", "AR", "PR", "QR", "OEE"])
    for sid in ARDF.ShiftId.unique():
        print(sid, "debug chk1")
        shifttime = ARDF.loc[ARDF["ShiftId"] == sid, "DurationMin"].iloc[0]
        print(sid, "debug chk1.1")
        schdloss = ARDF.loc[ARDF["ShiftId"] == sid, "scheduled loss"].iloc[0]
        print(sid, "debug chk1.2")
        unschdloss = ARDF.loc[ARDF["ShiftId"]
                              == sid, "unscheduled loss"].iloc[0]
        print(sid, "debug chk2")
        AR = (shifttime-schdloss-unschdloss)/(shifttime-schdloss)
        if (shifttime-schdloss-unschdloss) <= 0:
            AR = 0
        cttp = PRDF.loc[PRDF["ShiftId"] == sid, "CTxTP"].iloc[0]
        print(sid, "debug chk3")
        PR = cttp/(shifttime-schdloss-unschdloss)
        QR = 0
        if len(QRDF.loc[QRDF["ShiftId"] == sid, "Rejection"]) == 1:
            tp = QRDF.loc[QRDF["ShiftId"] == sid, "TotalProduction"].iloc[0]
            rp = QRDF.loc[QRDF["ShiftId"] == sid, "Rejection"].iloc[0]
            QR = (tp-rp)/tp
        print(sid, "debug chk4")
        OEE = AR*PR*QR
        OEEDF.loc[len(OEEDF)] = {"ShiftId": sid,
                                 "AR": AR, "PR": PR, "QR": QR, "OEE": OEE}
    print("\n\tOEE1\n",OEEDF)
    dff1 = df1[["ShiftId", "ShiftName"]]
    print(dff1)
    dff1.loc[len(dff1)] = {"ShiftId": 3, "ShiftName": "total"}
    print(dff1)
    OEEDF = pd.merge(OEEDF, dff1, how="inner", on=["ShiftId"])
    print(OEEDF)
    OEEBar = px.bar(OEEDF, x='ShiftName', y='OEE')
    trace1 = go.Scatter(
        x=OEEDF["ShiftName"],
        y=OEEDF["OEE"],
        showlegend=False
    )
    OEEBar.add_trace(trace1)
    # OEEBar.update_layout(plot_bgcolor: colors['background'],'paper_bgcolor': colors['background'],'font': {'color': colors['text']})
    OEEBar.update_layout({"plot_bgcolor": colors["text"], "paper_bgcolor": colors["text"], "font_color": "white"})
    return OEEBar


# if __name__ == '__main__':
#     app.run(debug=True)
