pipeline {
    agent any

    stages {
         stage('Checkout') {
             steps {
                 // Clone the repository
                 git 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
             }
         }

        stage('Set Up Environment') {
            steps {
                script {
                    // Create a virtual environment
                    sh 'python3 -m venv venv'
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    // Activate the virtual environment and install requirements
                    sh '''
                    source venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    // Run your tests here if applicable
                    // Uncomment the line below to run tests with pytest if you have tests
                    // sh 'source venv/bin/activate && pytest'
                    echo 'No tests to run in this setup. Customize as needed.'
                }
            }
        }

        stage('Run FastAPI Application') {
            steps {
                script {
                    // Start the FastAPI application
                    sh '''
                    source venv/bin/activate
                    nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
                    '''
                    echo 'FastAPI application started.'
                }
            }
        }
    }

    post {
        always {
            // Clean up and deactivate the virtual environment if necessary
            echo 'Cleaning up...'
            sh 'deactivate || true'  // Use || true to avoid errors if not activated
        }
    }
}
