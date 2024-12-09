pipeline {
    agent any

    environment {
        APP_NAME = 'FastAPIInventoryPipeline'
        REPO_URL = 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
        BUILD_DIR = 'build'
        TEST_DIR = 'test_results'
        DEPLOY_DIR = 'deployment'
    }

    parameters {
        string(name: 'BRANCH', defaultValue: 'main', description: 'Branch to build')
        choice(name: 'ENVIRONMENT', choices: ['Development', 'Staging', 'Production'], description: 'Deployment Environment')
    }

    stages {
        stage('Initialization') {
            steps {
                echo "Initializing the pipeline for ${APP_NAME}..."
                echo "Selected branch: ${params.BRANCH}"
                echo "Target environment: ${params.ENVIRONMENT}"
            }
        }

        stage('Checkout Code') {
            steps {
                echo 'Cloning the GitHub repository...'
                git branch: "${params.BRANCH}", url: "${REPO_URL}"
            }
        }

        stage('Setup') {
            steps {
                echo 'Setting up the pipeline environment...'
                echo "Application Name: ${APP_NAME}"
                sh '''
                    echo "Setting up dependencies and environment variables..." > setup.log
                    python3 -m venv venv
                    source venv/bin/activate
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building the application...'
                sh '''
                    mkdir -p ${BUILD_DIR}
                    echo "Simulating application build..." > ${BUILD_DIR}/build.log
                '''
                archiveArtifacts artifacts: "${BUILD_DIR}/build.log", onlyIfSuccessful: true
            }
        }

        stage('Parallel Testing') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        echo 'Running Unit Tests...'
                        sh '''
                            mkdir -p ${TEST_DIR}
                            echo "Executing unit tests..." > ${TEST_DIR}/unit_test_results.log
                        '''
                        archiveArtifacts artifacts: "${TEST_DIR}/unit_test_results.log", onlyIfSuccessful: true
                    }
                }
                stage('Integration Tests') {
                    steps {
                        echo 'Running Integration Tests...'
                        sh '''
                            mkdir -p ${TEST_DIR}
                            echo "Executing integration tests..." > ${TEST_DIR}/integration_test_results.log
                        '''
                        archiveArtifacts artifacts: "${TEST_DIR}/integration_test_results.log", onlyIfSuccessful: true
                    }
                }
            }
        }

        stage('Approval') {
            steps {
                input message: 'Approve Deployment?', ok: 'Deploy Now'
            }
        }

        stage('Deployment') {
            steps {
                echo "Deploying to ${params.ENVIRONMENT} environment..."
                sh '''
                    mkdir -p ${DEPLOY_DIR}
                    echo "Simulating deployment to ${params.ENVIRONMENT}..." > ${DEPLOY_DIR}/deploy.log
                '''
                archiveArtifacts artifacts: "${DEPLOY_DIR}/deploy.log", onlyIfSuccessful: true
            }
        }
    }

    post {
        always {
            echo 'Cleaning up temporary files...'
            sh 'rm -rf ${BUILD_DIR} ${TEST_DIR} ${DEPLOY_DIR} setup.log'
        }
        success {
            echo 'Pipeline executed successfully!'
            emailext subject: "Pipeline Success: ${APP_NAME}", 
                     body: "The pipeline for ${APP_NAME} executed successfully. Check Jenkins for details.", 
                     to: 'team@example.com'
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
            emailext subject: "Pipeline Failure: ${APP_NAME}", 
                     body: "The pipeline for ${APP_NAME} failed. Please check the logs on Jenkins for details.", 
                     to: 'team@example.com'
        }
    }
}
