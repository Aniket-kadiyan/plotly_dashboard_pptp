import pyodbc
import pandas as pd


servername = "ANIKETKADIYAN-P\AKSERVER"
dbname = "ProefficientDB"
cnxn = pyodbc.connect(driver='{SQL Server}', server=servername,
                      database=dbname, trusted_connection='yes')

tablename1 = "MasterMachine"
tbl_MasterMachine = pd.read_sql("SELECT * from {}".format(tablename1), cnxn)
tablename2 = "StopageReason"
tbl_StopageReason = pd.read_sql("SELECT * from {}".format(tablename2), cnxn)
tablename3 = "BreakDownEntry"
tbl_BreakDownEntry = pd.read_sql("SELECT * from {}".format(tablename3), cnxn)
tablename4 = "Shift"
tbl_Shift = pd.read_sql("SELECT * from {}".format(tablename4), cnxn)
tablename5 = "ProductionEntry"
tbl_ProductionEntry = pd.read_sql("SELECT * from {}".format(tablename5), cnxn)
tablename6 = "MasterProduct"
tbl_MasterProduct = pd.read_sql("SELECT * from {}".format(tablename6), cnxn)
tablename7 = "ProductionRejectReasonMapping"
tbl_ProductionRejectReasonMapping = pd.read_sql("SELECT * from {}".format(tablename7), cnxn)
tablename8 = "RejectionReason"
tbl_RejectionReason = pd.read_sql("SELECT * from {}".format(tablename8), cnxn)