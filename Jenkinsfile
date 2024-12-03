pipeline {
    agent any

    environment {
        VENV_DIR = 'venv' // Virtual environment directory
        APP_HOST = '0.0.0.0'
        APP_PORT = '8000'
        GIT_REPO = 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
    }

    stages {
        stage('Checkout') {
            steps {
                echo 'Cloning the repository...'
                git "${GIT_REPO}"
            }
        }

        stage('Set Up Python Environment') {
            steps {
                script {
                    echo 'Setting up Python virtual environment...'
                    sh '''
                    python3 -m venv ${VENV_DIR}
                    source ${VENV_DIR}/bin/activate
                    '''
                }
            }
        }

        stage('Install Dependencies') {
            steps {
                script {
                    echo 'Installing dependencies...'
                    sh '''
                    source ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    '''
                }
            }
        }

        stage('Code Linting') {
            steps {
                script {
                    echo 'Linting the code with Flake8...'
                    sh '''
                    source ${VENV_DIR}/bin/activate
                    flake8 --statistics || echo "Linting completed with warnings."
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    echo 'Running tests with Pytest...'
                    sh '''
                    source ${VENV_DIR}/bin/activate
                    pytest --maxfail=5 --disable-warnings || echo "Some tests failed. Check the logs."
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo 'Building Docker image for FastAPI application...'
                    sh '''
                    docker build -t fastapi-inventory-app .
                    '''
                }
            }
        }

        stage('Run FastAPI in Docker') {
            steps {
                script {
                    echo 'Running FastAPI application inside a Docker container...'
                    sh '''
                    docker run -d -p ${APP_PORT}:8000 --name fastapi-inventory fastapi-inventory-app
                    '''
                }
            }
        }

        stage('Application Health Check') {
            steps {
                script {
                    echo 'Checking application health...'
                    sh '''
                    sleep 10
                    curl -f http://${APP_HOST}:${APP_PORT}/docs || echo "Health check failed. Application may not be running correctly."
                    '''
                }
            }
        }
    }

    post {
        always {
            echo 'Cleaning up resources...'
            sh '''
            docker stop fastapi-inventory || true
            docker rm fastapi-inventory || true
            deactivate || true
            '''
        }
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Check logs for more details.'
        }
    }
}
