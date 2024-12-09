pipeline {
    agent any
    environment {
        VENV_DIR = "${env.WORKSPACE}/venv"  // Define a virtual environment directory within the workspace
        BUILD_DIR = "${env.WORKSPACE}/build"  // Directory for build artifacts
        TEST_RESULTS_DIR = "${env.WORKSPACE}/test_results"  // Directory for test results
    }
    stages {
        stage('Initialization') {
            steps {
                echo 'Initializing the pipeline for FastAPIInventoryPipeline...'
                echo "Selected branch: ${env.BRANCH_NAME ?: 'main'}"  // Default to 'main' if BRANCH_NAME is null
                echo "Target environment: Development"
            }
        }
        stage('Checkout Code') {
            steps {
                echo 'Cloning the GitHub repository...'
                git url: 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git', branch: 'main'
            }
        }
        stage('Setup') {
            steps {
                echo 'Setting up the pipeline environment...'
                sh '''
                    echo Setting up Python virtual environment...
                    python3 -m venv ${VENV_DIR}  # Create virtual environment
                    . ${VENV_DIR}/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt  # Install dependencies
                '''
            }
        }
        stage('Linting') {
            steps {
                echo 'Running linting checks...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pylint your_python_files_or_directories || true  # Replace with actual paths
                '''
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p ${TEST_RESULTS_DIR}
                    pytest tests/unit --junitxml=${TEST_RESULTS_DIR}/unit_test_results.xml  # Path to unit tests
                '''
            }
        }
        stage('Integration Testing') {
            steps {
                echo 'Running integration tests...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    pytest tests/integration --junitxml=${TEST_RESULTS_DIR}/integration_test_results.xml  # Path to integration tests
                '''
            }
        }
        stage('Package Application') {
            steps {
                echo 'Packaging the application...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p ${BUILD_DIR}
                    echo "Packaging logs" > ${BUILD_DIR}/package.log
                    # Add your packaging commands here (e.g., Docker, zip, etc.)
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    mkdir -p ${BUILD_DIR} && echo "Build logs" > ${BUILD_DIR}/build.log
                '''
            }
        }
        stage('Deployment') {
            steps {
                echo 'Deploying the application...'
                sh '''
                    . ${VENV_DIR}/bin/activate
                    # Add your deployment commands here (e.g., upload to server, deploy with Docker)
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up temporary files...'
            sh "rm -rf ${VENV_DIR} ${BUILD_DIR} ${TEST_RESULTS_DIR} setup.log artifacts"
        }
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                to: 'bhavsarvaibhav001@gmail.com',
                subject: "Jenkins Pipeline Successful: ${env.JOB_NAME}",
                body: "The pipeline ${env.JOB_NAME} completed successfully at ${env.BUILD_URL}. Great job!"
            )
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
            emailext (
                to: 'bhavsarvaibhav001@gmail.com',
                subject: "Jenkins Pipeline Failed: ${env.JOB_NAME}",
                body: "The pipeline ${env.JOB_NAME} failed at ${env.BUILD_URL}. Please review the logs for details."
            )
        }
    }
}
