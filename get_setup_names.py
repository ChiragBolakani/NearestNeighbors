import mysql.connector
from mysql.connector.errors import DatabaseError, ProgrammingError
import pandas as pd
import sys
from utils import create_logger

log = create_logger()

args = sys.argv
args_valid = True

try:
    if args[1] == "chn": 
        database = "regression_db"
    elif args[1] == "ant":
        database = "regression_db_ant"
    else:
        raise Exception
except Exception as e:
    args_valid = False
    if len(args) < 2:
        # print("Location argument missing : python get_setup_names.py <location>")
        log.error("Location argument missing : python get_setup_names.py <location>")
    else:
        log.error("invalid arguments passed")
    sys.exit(1)


if args_valid == True:
    try:
        connection = mysql.connector.connect(user = "root", host = "localhost", password = "r@ndom06", database = database)

        cursor = connection.cursor()

        sql = '''select name from setup'''
        cursor.execute(sql)

        setups = []

        for row in cursor.fetchall():
            setups.append(row[0])

        connection.close()
        setup_df = pd.DataFrame({"setups" : setups})
        setup_df.to_csv("setup.csv")
        log.info("setup names stored in setup.csv")
    except ProgrammingError as e:
        # print(e.msg)
        log.error(e.msg)
    except DatabaseError as e:
        # print(e.msg)
        log.error(e.msg)
    except mysql.connector.Error as e:
        # print(e.msg)
        log.error(e.msg)
    except Exception as e:
        # print(e)
        log.error(e)
else:
    # print("Invalid Arguments passed")
    log.error("Invalid Arguments passed")
    sys.exit(1)
