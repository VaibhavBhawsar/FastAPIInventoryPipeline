provider "docker" {}

# Pull the NGINX Docker image
resource "docker_image" "nginx" {
  name         = "nginx:latest"
  keep_locally = false
}

# Create a Docker container
resource "docker_container" "nginx_container" {
  name  = var.container_name
  image = docker_image.nginx.latest
  ports {
    internal = 80
    external = var.host_port
  }
}
