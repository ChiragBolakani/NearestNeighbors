import os

directories = os.listdir(os.getcwd())

if "label_encoders" not in directories:
    os.mkdir("label_encoders")
if "models" not in directories:
    os.mkdir("models")
if "setup_columns_extracted_data_with_reason" not in directories:
    os.mkdir("setup_columns_extracted_data_with_reason")
if "setup_data_column_encoded" not in directories:
    os.mkdir("setup_data_column_encoded")
if "setup_json_data" not in directories:
    os.mkdir("setup_json_data")
if "validated_setup_data_for_vectoring" not in directories:
    os.mkdir("validated_setup_data_for_vectoring")
if "x_data" not in directories:
    os.mkdir("x_data")
