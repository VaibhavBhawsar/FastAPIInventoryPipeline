pipeline {
    agent any

    environment {
        VENV_DIR = 'venv'
        TERRAFORM_DIR = 'terraform'
    }

    stages {
        stage('Checkout') {
            steps {
                git 'https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git'
            }
        }

        stage('Set Up Python Environment') {
            steps {
                sh '''
                python3 -m venv ${VENV_DIR}
                source ${VENV_DIR}/bin/activate
                '''
            }
        }

        stage('Terraform Init') {
            steps {
                dir("${TERRAFORM_DIR}") {
                    sh 'terraform init'
                }
            }
        }

        stage('Terraform Plan') {
            steps {
                dir("${TERRAFORM_DIR}") {
                    sh 'terraform plan -out=tfplan'
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                dir("${TERRAFORM_DIR}") {
                    sh 'terraform apply -auto-approve tfplan'
                }
            }
        }

        stage('Run FastAPI Application') {
            steps {
                sh '''
                source ${VENV_DIR}/bin/activate
                nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
                '''
            }
        }
    }

    post {
        always {
            echo 'Cleaning up...'
            sh 'deactivate || true'
        }
    }
}
