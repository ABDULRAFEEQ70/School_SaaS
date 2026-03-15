output "ec2_sg_id" {
  description = "ID of EC2 security group"
  value       = aws_security_group.ec2_sg.id
}

output "lb_sg_id" {
  description = "ID of Load Balancer security group"
  value       = aws_security_group.lb_sg.id
}

output "database_sg_id" {
  description = "ID of Database security group"
  value       = aws_security_group.database_sg.id
}
