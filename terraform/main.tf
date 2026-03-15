terraform {
  required_version = ">= 1.0"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  backend "s3" {
    bucket         = "school-saas-terraform-state"
    key            = "terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "school-saas-terraform-locks"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project     = "School-SaaS"
      Environment = var.environment
      ManagedBy   = "Terraform"
    }
  }
}

data "aws_ami" "amazon_linux_2" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["amzn2-ami-hvm-*-x86_64-gp2"]
  }
}

module "vpc" {
  source = "./modules/vpc"

  project_name     = var.project_name
  environment      = var.environment
  vpc_cidr         = var.vpc_cidr
  availability_zones = var.availability_zones
}

module "security_groups" {
  source = "./modules/security_groups"

  project_name = var.project_name
  environment  = var.environment
  vpc_id       = module.vpc.vpc_id
  vpc_cidr     = module.vpc.vpc_cidr
}

module "iam" {
  source = "./modules/iam"

  project_name = var.project_name
  environment  = var.environment
}

module "ec2" {
  source = "./modules/ec2"

  project_name          = var.project_name
  environment           = var.environment
  instance_count        = var.instance_count
  instance_type         = var.instance_type
  ami_id                = data.aws_ami.amazon_linux_2.id
  subnet_ids            = module.vpc.private_subnet_ids
  security_group_ids    = [module.security_groups.ec2_sg_id]
  iam_instance_profile  = module.iam.ec2_instance_profile_name
  key_name              = var.ssh_key_name
  enable_monitoring     = true

  user_data = <<-EOF
              #!/bin/bash
              yum update -y
              yum install -y docker
              systemctl start docker
              systemctl enable docker
              usermod -aG docker ec2-user
              EOF
}

module "load_balancer" {
  source = "./modules/load_balancer"

  project_name       = var.project_name
  environment        = var.environment
  vpc_id             = module.vpc.vpc_id
  subnet_ids         = module.vpc.public_subnet_ids
  security_group_ids = [module.security_groups.lb_sg_id]
  instance_ids       = module.ec2.instance_ids
  target_group_port  = var.app_port
}

output "vpc_id" {
  description = "VPC ID"
  value       = module.vpc.vpc_id
}

output "ec2_instance_public_ips" {
  description = "Public IPs of EC2 instances"
  value       = module.ec2.public_ips
}

output "load_balancer_dns" {
  description = "Load balancer DNS name"
  value       = module.load_balancer.lb_dns_name
}

output "instance_ids" {
  description = "EC2 instance IDs"
  value       = module.ec2.instance_ids
}
