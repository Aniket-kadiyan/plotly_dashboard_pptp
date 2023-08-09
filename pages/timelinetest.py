import dash
from dash import Dash, dcc, Input, Output, callback
import plotly.express as px
import dash_bootstrap_components as dbc
import pandas as pd
import pyodbc
import array
from datetime import date as dte

cnxn = pyodbc.connect(driver='{SQL Server}', server='ANIKETKADIYAN-P\AKSERVER',
                      database='ProefficientDB', trusted_connection='yes')

cursor = cnxn.cursor()

tablename1 = "ProductionEntry"
df1 = pd.read_sql("SELECT * from {}".format(tablename1), cnxn)
print(df1.columns)
tablename2 = "BreakDownEntry"
df2 = pd.read_sql("SELECT MachineID,StartTime,EndTime from {}".format(tablename2), cnxn)
tablename3 = "MasterMachine"
df3 = pd.read_sql("SELECT MachineID,MachineName from {}".format(tablename3), cnxn)
print(df3.columns)
df4 = pd.merge(df2, df3, how="inner", on=["MachineID"])
print(df4)
# df = pd.DataFrame([
#     dict(Task="Job A", Start='2009-01-01',
#          Finish='2009-02-28', Resource="Idle"),
#         dict(Task="Job A", Start='2009-02-28',
#          Finish='2009-05-30', Resource="Working"),
#         dict(Task="Job B", Start='2009-01-01',
#          Finish='2009-03-05', Resource="Idle"),
#     dict(Task="Job B", Start='2009-03-05',
#          Finish='2009-04-15', Resource="Breakdown"),
#     dict(Task="Job C", Start='2009-01-01',
#          Finish='2009-02-28', Resource="Idle"),
#         dict(Task="Job C", Start='2009-02-28',
#          Finish='2009-05-30', Resource="Working")
# ])
df = pd.DataFrame(columns=["MachineID","StartTime","EndTime"])

# colors = {"Breakdown": "red", "Idle": "orange", "Working": "green"}
colors = ["orange","green", "red"]

fig = px.timeline(df4, x_start="StartTime", x_end="EndTime",y="MachineName", color="MachineName")
fig.update_yaxes(autorange="reversed")
fig.show()
