import mysql.connector
import pandas as pd
import numpy as np
import sys

args = sys.argv
args_valid = True

if args[1] == "chn": 
    database = "regression_db"
elif args[1] == "ant":
    database = "regression_db_ant"
else:
    exit()
    

if args_valid == True:
    connection = mysql.connector.connect(user = "root", host = "localhost", password = "r@ndom06", database = database)

    cursor = connection.cursor()

    sql = '''select name from setup'''
    cursor.execute(sql)

    setups = []

    for row in cursor.fetchall():
        setups.append(row[0])

    setup_df = pd.DataFrame({"setups" : setups})
    setup_df.to_csv("setup.csv")
    connection.close()
