output "vpc_id" {
  description = "ID of the VPC"
  value       = module.vpc.vpc_id
}

output "public_subnet_ids" {
  description = "IDs of public subnets"
  value       = module.vpc.public_subnet_ids
}

output "private_subnet_ids" {
  description = "IDs of private subnets"
  value       = module.vpc.private_subnet_ids
}

output "ec2_instance_ids" {
  description = "IDs of EC2 instances"
  value       = module.ec2.instance_ids
}

output "ec2_instance_public_ips" {
  description = "Public IPs of EC2 instances"
  value       = module.ec2.public_ips
}

output "load_balancer_dns" {
  description = "DNS name of the load balancer"
  value       = module.load_balancer.lb_dns_name
}

output "load_balancer_zone_id" {
  description = "Zone ID of the load balancer"
  value       = module.load_balancer.lb_zone_id
}
