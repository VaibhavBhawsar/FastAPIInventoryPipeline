output "container_id" {
  description = "The ID of the Docker container"
  value       = docker_container.nginx_container.id
}

output "container_name" {
  description = "The name of the Docker container"
  value       = docker_container.nginx_container.name
}

output "container_status" {
  description = "The current status of the Docker container"
  value       = docker_container.nginx_container.status
}

output "mapped_port" {
  description = "The host port mapped to the container"
  value       = var.host_port
}
