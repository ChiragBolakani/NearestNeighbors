import os 

# Database config values
CHENNAI_DB = "regression_db"
ANTWERP_DB = "regression_db_ant"
HOST = os.environ['DB_HOST']
USER = os.environ['DB_USER']
PASSWORD = os.environ['DB_PASSWORD']

# KNN training config values
K_VALUE = 7
ALGORITHM_FOR_NEIGHBORS = 'ball_tree'