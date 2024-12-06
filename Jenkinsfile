pipeline {
    agent any

    environment {
        APP_NAME = 'FastAPIInventoryPipeline'
        REPO_URL = 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
        BUILD_DIR = 'build'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo 'Cloning the GitHub repository...'
                git branch: 'main', url: "${REPO_URL}"
            }
        }
        stage('Setup') {
            steps {
                echo 'Setting up the pipeline environment...'
                echo "Application Name: ${APP_NAME}"
            }
        }
        stage('Development') {
            steps {
                echo 'I am in development'
                sh 'echo "Simulating code development..." > development.log'
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh '''
                    mkdir -p ${BUILD_DIR}
                    echo "Simulating application build..." > ${BUILD_DIR}/build.log
                '''
            }
        }
        stage('Testing') {
            steps {
                echo 'Running tests...'
                sh 'echo "Simulating test execution..." > test_results.log'
            }
        }
        stage('Approval') {
            steps {
                input message: 'Approve Deployment?', ok: 'Deploy Now'
            }
        }
        stage('Deployment') {
            steps {
                echo 'Deploying the application...'
                sh 'echo "Simulating deployment process..." > deployment.log'
            }
        }
    }

    post {
        always {
            echo 'Cleaning up temporary files...'
            sh 'rm -rf ${BUILD_DIR} development.log test_results.log deployment.log'
        }
        success {
            echo 'Pipeline executed successfully!'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
        }
    }
}
