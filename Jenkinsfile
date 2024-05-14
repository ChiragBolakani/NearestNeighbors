pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    call %python_venv%
                    // commands.bat
		    python check_and_create_directory.py
                    python empty_directory.py
                    python get_setup_names.py %Location% 
                    python get_setup_data_json.py %Location% %From% %To%
                    python get_input_data_with_reason.py
                    python label_encoding.py
                    python validate_failure_reason_before_vectorizing.py
                    python vectorizer.py
                    python fit_knn_vectorized.py
                """
            }
        }
        stage('post-build-steps'){
            steps {
                bat """
                    call %python_venv%
                    python empty_directory.py
                """
            }
        }
    }
} 
