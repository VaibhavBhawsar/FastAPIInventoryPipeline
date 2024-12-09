pipeline {
    agent any

    environment {
        APP_NAME = 'FastAPIInventoryPipeline'
        REPO_URL = 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
        BUILD_DIR = 'build'
        TEST_DIR = 'test_results'
        DEPLOY_DIR = 'deployment'
        RECIPIENTS = 'bhavsarvaibhav001@gmail.com' // Email address for notifications
    }

    stages {
        stage('Initialization') {
            steps {
                echo "Initializing the pipeline for ${APP_NAME}..."
                echo "Selected branch: main"
                echo "Target environment: Development"
            }
        }
        stage('Checkout Code') {
            steps {
                echo 'Cloning the GitHub repository...'
                git branch: 'main', url: "${REPO_URL}"
            }
        }
        stage('Setup') {
            steps {
                echo 'Setting up the pipeline environment...'
                sh '''
                    #!/bin/bash
                    echo "Setting up dependencies and environment variables..."
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
                    echo "Build logs" > ${BUILD_DIR}/build.log
                '''
                archiveArtifacts artifacts: "${BUILD_DIR}/build.log"
            }
        }
        stage('Parallel Testing') {
            parallel {
                stage('Unit Tests') {
                    steps {
                        echo 'Running Unit Tests...'
                        sh '''
                            mkdir -p ${TEST_DIR}
                            echo "Unit test logs" > ${TEST_DIR}/unit_tests.log
                        '''
                        archiveArtifacts artifacts: "${TEST_DIR}/unit_tests.log"
                    }
                }
                stage('Integration Tests') {
                    steps {
                        echo 'Running Integration Tests...'
                        sh '''
                            mkdir -p ${TEST_DIR}
                            echo "Integration test logs" > ${TEST_DIR}/integration_tests.log
                        '''
                        archiveArtifacts artifacts: "${TEST_DIR}/integration_tests.log"
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
                echo 'Deploying the application...'
                sh '''
                    mkdir -p ${DEPLOY_DIR}
                    echo "Deployment logs" > ${DEPLOY_DIR}/deploy.log
                '''
                archiveArtifacts artifacts: "${DEPLOY_DIR}/deploy.log"
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
            emailext(
                subject: "SUCCESS: Pipeline ${APP_NAME}",
                body: """
                <h2>Pipeline Executed Successfully</h2>
                <p>The pipeline for <b>${APP_NAME}</b> completed successfully.</p>
                <p><b>Summary:</b></p>
                <ul>
                    <li>Branch: main</li>
                    <li>Environment: Development</li>
                    <li>Build Logs: See Jenkins</li>
                </ul>
                """,
                to: "${RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
        failure {
            echo 'Pipeline failed. Please check the logs.'
            emailext(
                subject: "FAILURE: Pipeline ${APP_NAME}",
                body: """
                <h2>Pipeline Execution Failed</h2>
                <p>The pipeline for <b>${APP_NAME}</b> encountered a failure.</p>
                <p><b>Details:</b></p>
                <ul>
                    <li>Branch: main</li>
                    <li>Environment: Development</li>
                    <li>Logs: See Jenkins</li>
                </ul>
                <p>Please review the logs and fix the issue.</p>
                """,
                to: "${RECIPIENTS}",
                mimeType: 'text/html'
            )
        }
    }
}
