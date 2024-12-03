output "container_id" {
  description = "The ID of the Docker container"
  value       = docker_container.fastapi_container
}

output "container_name" {
  description = "The name of the Docker container"
  value       = docker_container.fastapi_container
}

output "container_status" {
  description = "The current status of the Docker container"
  value       = docker_container.fastapi_container
}

output "mapped_port" {
  description = "The host port mapped to the container"
  value       = var.host_port
}
