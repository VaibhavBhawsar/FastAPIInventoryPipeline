pipeline {
    agent any
    stages {
        stage('Checkout') {
            steps {
                // Checkout the code from Git
                git 'https://github.com/yourusername/fastapi_inventory.git' // Update with your repo URL
            }
        }
        stage('Install Dependencies') {
            steps {
                // Install dependencies
                sh 'pip install -r requirements.txt'
            }
        }
        stage('Test') {
            steps {
                // Run tests (add your test commands here)
                echo 'No tests defined yet.' // Update with your test command if you add tests
            }
        }
        stage('Build') {
            steps {
                // Build the application (if applicable, e.g., Docker image)
                echo 'Building the application...'
            }
        }
        stage('Deploy') {
            steps {
                // Deploy the application
                echo 'Deploying the application...'
            }
        }
    }
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}