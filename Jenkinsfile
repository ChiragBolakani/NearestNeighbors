pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    call %python_venv%
                    // commands.bat
                    python get_setup_names.py %Location%
                    python get_setup_data_json.py %Location%
                    python get_input_data_with_reason.py
                    python label_encoding.py
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
    // post {
    //     success{

    //         script{
    //             currentBuild.description = """<img src='C:\ProgramData\Jenkins\.jenkins\workspace\ML_pipeline\accuracy_bar_plot.png' alt='accuracy_bar_plot' width='500' height='600'>"""
    //         } 
    //     }
    // }
} 