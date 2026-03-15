output "lb_arn" {
  description = "ARN of the load balancer"
  value       = aws_lb.application_lb.arn
}

output "lb_dns_name" {
  description = "DNS name of the load balancer"
  value       = aws_lb.application_lb.dns_name
}

output "lb_zone_id" {
  description = "Zone ID of the load balancer"
  value       = aws_lb.application_lb.zone_id
}

output "lb_listener_arns" {
  description = "ARNs of the load balancer listeners"
  value       = [aws_lb_listener.http_listener.arn, aws_lb_listener.https_listener.arn]
}

output "target_group_arn" {
  description = "ARN of the target group"
  value       = aws_lb_target_group.app_target_group.arn
}
