variable "container_name" {
  description = "Name of the Docker container"
  type        = string
  default     = "my-nginx-container"
}

variable "host_port" {
  description = "The port on the host to map to the container"
  type        = number
  default     = 8080
}
