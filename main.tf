terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.25.0"
    }
  }
}

provider "docker" {}

# Build Docker Image
resource "docker_image" "fastapi_image" {
  name = "fastapi_app:latest"

  build {
    context    = "$${home/vaibhav/Downloads/Practice/FastAPIInventoryPipeline}/.."  # Adjust based on Dockerfile location
    dockerfile = "dockerfile"
  }
}

# Create Docker Container
resource "docker_container" "fastapi_container" {
  name  = "fastapi_container"
  image = docker_image.fastapi_image.name
  ports {
    internal = 8000
    external = 8080
  }
}
