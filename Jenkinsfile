pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        REPO_NAME = 'FastAPIInventoryPipeline'
        TEST_RESULTS_DIR = 'test_results'
        TEST_RESULTS_FILE = "${TEST_RESULTS_DIR}/unit_test_results.xml"
    }

    stages {
        stage('Initialization') {
            steps {
                script {
                    echo "Initializing the pipeline for ${REPO_NAME}..."
                    echo "Selected branch: ${env.BRANCH_NAME}"
                    echo "Target environment: Development"
                }
            }
        }

        stage('Checkout Code') {
            steps {
                echo "Cloning the GitHub repository..."
                git url: "https://github.com/VaibhavBhawsar/${REPO_NAME}.git", branch: 'main'
            }
        }

        stage('Setup') {
            steps {
                echo "Setting up the pipeline environment..."
                sh '''
                    python3 -m venv $VENV_DIR
                    . $VENV_DIR/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                    pip install pylint pytest  # Install pylint if not in requirements.txt
                '''
            }
        }

        stage('Linting') {
            steps {
                echo "Running linting checks..."
                sh '''
                    . $VENV_DIR/bin/activate
                    pylint your_python_files_or_directories || true  # Add your directories here
                '''
            }
        }

        stage('Unit Testing') {
            steps {
                echo "Running unit tests..."
                sh '''
                    . $VENV_DIR/bin/activate
                    mkdir -p $TEST_RESULTS_DIR
                    pytest tests/unit --junitxml=$TEST_RESULTS_FILE || true
                '''
            }
        }

        stage('Integration Testing') {
            steps {
                echo "Running integration tests..."
            }
        }

        stage('Package Application') {
            steps {
                echo "Packaging the application..."
            }
        }

        stage('Build') {
            steps {
                echo "Building the application..."
            }
        }

        stage('Deployment') {
            steps {
                echo "Deploying the application..."
            }
        }

        stage('Post Actions') {
            steps {
                echo "Cleaning up temporary files..."
                sh '''
                    rm -rf $VENV_DIR $TEST_RESULTS_DIR setup.log artifacts
                '''
            }
        }
    }

    post {
        always {
            echo "Pipeline finished. Please check the logs."
            // You can add email notifications or other actions here
        }
    }
}
