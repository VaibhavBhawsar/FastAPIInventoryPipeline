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
                    pip install -r requirements.txt
                '''
            }
        }
        stage('Build') {
            steps {
                echo 'Building the application...'
                sh 'mkdir -p build && echo "Build logs" > build/build.log'
            }
        }
        // Remaining pipeline stages...
    }
    post {
        always {
            echo 'Cleaning up temporary files...'
            sh 'rm -rf build test_results deployment setup.log'
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
