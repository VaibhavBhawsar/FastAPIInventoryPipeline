# FastAPI Inventory Pipeline

# Project Description

This project utilizes Terraform to manage the infrastructure as code for deploying a FastAPI application in a Docker container. The deployment process involves building a Docker image from the FastAPI application and running it in a Docker container. Additionally, a Jenkins pipeline is set up to automate the CI/CD process, ensuring the application is tested and deployed smoothly.
ory contains a Jenkins pipeline for building, testing, and deploying a FastAPI application. The pipeline automates the process of setting up the environment, running tests, and deploying the application.

# FastAPI Application Deployment

This repository contains a comprehensive configuration for deploying a FastAPI application using Docker, managed by Terraform and orchestrated through a Jenkins pipeline. The goal is to automate the processes of building, testing, and deploying the FastAPI application in a Docker container, adhering to infrastructure as code (IaC) principles.

## Table of Contents
- [Project Description](#project-description)
- [Requirements](#requirements)
- [Setup Instructions](#setup-instructions)
- [Jenkins Pipeline](#jenkins-pipeline)
- [Terraform Configuration](#terraform-configuration)
- [Execution Plan](#execution-plan)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Prerequisites

Before using this pipeline, ensure you have the following:

- [Jenkins](https://www.jenkins.io/doc/book/installing/) installed and running.
- Git installed on the Jenkins server.
- [Terraform](https://www.terraform.io/downloads.html) (version 1.x or later)
- [Docker](https://docs.docker.com/get-docker/) (version 20.x or later)
- A compatible Docker environment (e.g., Docker Desktop, Docker on Linux)
- Python 3.x installed on the Jenkins server.
- Required Python packages defined in `requirements.txt`.
- A FastAPI application repository available on GitHub.

## Setup

1. Clone this repository to your local machine or Jenkins server.
2. Update the Jenkins pipeline configuration to point to your FastAPI application repository.
3. Ensure the `requirements.txt` file is present in the root of your FastAPI application directory.

## Pipeline Stages

The Jenkins pipeline consists of the following stages:

1. **Initialization**: Initializes the pipeline and sets up the environment.
2. **Checkout Code**: Clones the GitHub repository containing the FastAPI application.
3. **Setup**: Creates a Python virtual environment and installs the necessary packages.
4. **Linting**: Runs linting checks using `pylint`.
5. **Unit Testing**: Executes unit tests using `pytest` and generates a JUnit XML report.
6. **Integration Testing**: (Skipped if unit tests fail).
7. **Package Application**: (Skipped if previous stages fail).
8. **Build**: (Skipped if previous stages fail).
9. **Deployment**: (Skipped if previous stages fail).
10. **Post Actions**: Cleans up temporary files and sends notifications.

## Usage

1. Create a new Jenkins pipeline job.
2. Set the repository URL to this project and configure it to use the Jenkinsfile included in this repository.
3. Trigger the pipeline manually or set it to run automatically on code changes.

## Troubleshooting

- **Failed to clone the repository**: Ensure that the Git URL is correct and accessible by the Jenkins server.
- **Pylint not found**: Make sure `pylint` is included in your `requirements.txt`.
- **Junitxml must be a filename error**: Check the `pytest` command in the pipeline to ensure the output path is correct.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.


## Setup Instructions

1. **Clone the Repository:**
```bash 
git clone https://github.com/VaibhavBhawsar/FastAPIInventoryPipeline.git
