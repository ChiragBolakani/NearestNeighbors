import mysql.connector
import pandas as pd
import json
import sys
from utils import validate_date, create_logger

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
    
    from_date = args[2]
    date_valid, error = validate_date(from_date)
    if not date_valid:
        raise error
    
    to_date = args[3]
    date_valid, error = validate_date(to_date)
    if not date_valid:
        raise error

except ValueError as e:
    log.error("Error while validating date." + e.__str__())
    # print("Error while validating date. " + e.__str__())
    sys.exit()
except Exception as e:
    args_valid = False
    if len(args) < 4:
        log.error("Some arguments missing : python get_setup_names.py <location> <from_data> <to_date>")
        # print("Some arguments missing : python get_setup_names.py <location> <from_data> <to_date>")
    else:
        log.error("invalid arguments passed")
        # print("invalid arguments passed")
    sys.exit(1)

connection = mysql.connector.connect(user = "root", host = "localhost", password = "r@ndom06", database = database)
cursor = connection.cursor(buffered=True)

setup_df = pd.read_csv("setup.csv")
setups = setup_df["setups"].tolist()

for setup in setups:

    sql = '''
SELECT 
    functional_test.id,
    functional_test.testrun_id,
    functional_test.comments,
    functional_test.result_per_step,
    functional_test.fr,
    functional_testcase.mnemonic
FROM
    functional_test
        INNER JOIN
    testrun ON functional_test.testrun_id = testrun.id
        INNER JOIN
    setup ON testrun.setup_id = setup.id
        INNER JOIN
    functional_testcase ON functional_testcase.id = functional_test.testcase_id
WHERE
    setup.name = %s
        AND testrun.date between %s and %s
        AND LENGTH(functional_test.comments) != 0
        AND (functional_test.nb_steps_fail > 0
        OR functional_test.nb_steps_not_run > 0)
ORDER BY testrun.date DESC
'''
    val = (setup,from_date, to_date)
    cursor.execute(sql,val)
    if(cursor.rowcount > 0):
    
        rows_json = [dict((cursor.description[i][0], value) \
                for i, value in enumerate(row)) for row in cursor.fetchall()]
        
        json_output = json.dumps(rows_json, default=str)

        with open("setup_json_data/"+setup+".json", "w") as jsonf:
            jsonf.write(json_output)
            log.info("created json file at {setup}.".format(setup="setup_json_data/"+setup+".json"))

    else:
        # print("No data found for setup : {setup}".format(setup=setup))
        log.info("no data found for setup : {setup}".format(setup=setup))

connection.close()
