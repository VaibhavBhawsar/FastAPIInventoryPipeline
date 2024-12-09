pipeline {
    agent any
    stages {
        stage('Initialization') {
            steps {
                echo 'Initializing the pipeline for FastAPIInventoryPipeline...'
                echo "Selected branch: ${env.BRANCH_NAME}"
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
                    echo Setting up dependencies and environment variables...
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Linting') {
            steps {
                echo 'Running code linting...'
                sh '''
                    . venv/bin/activate
                    echo Running flake8 for Python linting...
                    flake8 --max-line-length=88 .
                '''
            }
        }
        stage('Unit Testing') {
            steps {
                echo 'Executing unit tests...'
                sh '''
                    . venv/bin/activate
                    echo Running pytest for unit tests...
                    pytest --junitxml=test_results/unit_tests.xml
                '''
            }
        }
        stage('Integration Testing') {
            steps {
                echo 'Executing integration tests...'
                sh '''
                    . venv/bin/activate
                    echo Running integration tests...
                    pytest tests/integration --junitxml=test_results/integration_tests.xml
                '''
            }
        }
        stage('Package Application') {
            steps {
                echo 'Packaging the application...'
                sh '''
                    . venv/bin/activate
                    echo Creating application package...
                    python setup.py sdist
                    mkdir -p artifacts
                    mv dist/*.tar.gz artifacts/
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh '''
                    echo Compiling the application code...
                    mkdir -p build
                    echo "Build logs" > build/build.log
                '''
            }
        }
        stage('Deployment') {
            steps {
                echo 'Deploying application to Development environment...'
                sh '''
                    echo Deploying FastAPI application...
                    . venv/bin/activate
                    uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload &
                '''
            }
        }
    }
    post {
        always {
            echo 'Cleaning up temporary files...'
            sh 'rm -rf build test_results deployment setup.log artifacts'
        }
        success {
            echo 'Pipeline completed successfully!'
            emailext (
                to: 'bhavsarvaibhav001@gmail.com',
                subject: "Jenkins Pipeline Successful: ${env.JOB_NAME}",
                body: """
                    The pipeline ${env.JOB_NAME} completed successfully at ${env.BUILD_URL}.
                    
                    Summary:
                    - Linting passed.
                    - Unit and Integration tests passed.
                    - Application packaged and deployed successfully.
                    
                    Great job!
                """
            )
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
            emailext (
                to: 'bhavsarvaibhav001@gmail.com',
                subject: "Jenkins Pipeline Failed: ${env.JOB_NAME}",
                body: """
                    The pipeline ${env.JOB_NAME} failed at ${env.BUILD_URL}.
                    
                    Please review the logs and test reports for details.
                """
            )
        }
    }
}
