python get_setup_names.py %1
python get_setup_data_json.py %1 %2 %3
python get_input_data_with_reason.py
python label_encoding.py
python validate_failure_reason_before_vectorizing.py
python vectorizer.py
python fit_knn_vectorized.py
python empty_directory.py
