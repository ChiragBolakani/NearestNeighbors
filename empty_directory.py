import os 
import shutil

shutil.rmtree("setup_json_data")
os.mkdir("setup_json_data")

shutil.rmtree("setup_columns_extracted_data_with_reason")
os.mkdir("setup_columns_extracted_data_with_reason")

shutil.rmtree("setup_data_column_encoded")
os.mkdir("setup_data_column_encoded")

shutil.rmtree("x_data")
os.mkdir("x_data")

shutil.rmtree("validated_setup_data_for_vectorizing")
os.mkdir("validated_setup_data_for_vectorizing")

if os.path.exists("setup.csv"):
    os.remove("setup.csv")
else:
    pass