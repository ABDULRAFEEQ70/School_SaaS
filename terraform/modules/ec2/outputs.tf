output "instance_ids" {
  description = "IDs of EC2 instances"
  value       = aws_instance.app_servers[*].id
}

output "public_ips" {
  description = "Public IPs of EC2 instances"
  value       = aws_instance.app_servers[*].public_ip
}

output "private_ips" {
  description = "Private IPs of EC2 instances"
  value       = aws_instance.app_servers[*].private_ip
}

output "availability_zones" {
  description = "Availability zones of EC2 instances"
  value       = aws_instance.app_servers[*].availability_zone
}
