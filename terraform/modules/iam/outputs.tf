output "ec2_role_name" {
  description = "Name of EC2 IAM role"
  value       = aws_iam_role.ec2_role.name
}

output "ec2_role_arn" {
  description = "ARN of EC2 IAM role"
  value       = aws_iam_role.ec2_role.arn
}

output "ec2_instance_profile_name" {
  description = "Name of EC2 instance profile"
  value       = aws_iam_instance_profile.ec2_instance_profile.name
}

output "ec2_policy_arn" {
  description = "ARN of EC2 policy"
  value       = aws_iam_policy.ec2_policy.arn
}
