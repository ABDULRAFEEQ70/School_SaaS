variable "project_name" {
  description = "Project name"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "vpc_id" {
  description = "VPC ID"
  type        = string
}

variable "subnet_ids" {
  description = "List of subnet IDs"
  type        = list(string)
}

variable "security_group_ids" {
  description = "List of security group IDs"
  type        = list(string)
}

variable "instance_ids" {
  description = "List of EC2 instance IDs"
  type        = list(string)
}

variable "target_group_port" {
  description = "Target group port"
  type        = number
  default     = 5000
}

variable "health_check_path" {
  description = "Health check path"
  type        = string
  default     = "/health"
}
