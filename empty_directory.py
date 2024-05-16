import os 
import shutil

shutil.rmtree("setup_json_data")
os.mkdir("setup_json_data")

shutil.rmtree("setup_data_column_encoded")
os.mkdir("setup_data_column_encoded")

shutil.rmtree("x_data")
os.mkdir("x_data")

if os.path.exists("setup.csv"):
    os.remove("setup.csv")
else:
    pass