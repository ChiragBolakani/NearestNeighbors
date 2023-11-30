pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                bat """
                    call %python_venv%
                    python get_setup_names.py
                    python get_setup_data_json.py
                    python get_input_data.py
                    python label_encoding.py
                    python fit_knn.py
                    python fit_dct.py
                    python fit_svc.py
                    python result_analysis.py
                    python empty_directory.py
                """
            }
        }
        stage('Test') {
            steps {
                bat """
                    call %python_venv%
                    python result_analysis.py
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