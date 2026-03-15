# School SaaS - Infrastructure Automation

Production-grade infrastructure automation for scaling School SaaS application across multiple environments.

## 📋 Table of Contents

- [Infrastructure Components](#infrastructure-components)
- [Quick Start](#quick-start)
- [Terraform Setup](#terraform-setup)
- [Ansible Deployment](#ansible-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [CI/CD Pipeline](#cicd-pipeline)
- [Application Monitoring](#application-monitoring)
- [Configuration](#configuration)

## 🏗️ Infrastructure Components

### 1. Terraform - AWS EC2 Provisioning
Automated provisioning of EC2 instances with:
- VPC with public/private subnets across multiple AZs
- Security groups with network policies
- Load balancer (ALB) with SSL termination
- Auto Scaling support
- IAM roles for EC2 instances
- CloudWatch integration

### 2. Ansible - Docker Compose Deployment
Automated deployment using AWS dynamic inventory:
- Dynamic discovery of EC2 instances
- Docker and Docker Compose installation
- Application deployment with health checks
- Backup automation
- Monitoring setup (CloudWatch Agent)
- Nginx reverse proxy configuration

### 3. Kubernetes - EKS Deployment
Production-grade K8s manifests for:
- Deployments with rolling updates
- Horizontal Pod Autoscaling (HPA)
- Pod Disruption Budgets
- Network policies
- Ingress with ALB
- StatefulSets for PostgreSQL and Redis
- Service accounts and RBAC

### 4. CI/CD Pipeline - GitHub Actions
Automated pipeline with:
- Linting and formatting checks
- Unit testing with coverage
- Security scanning (Trivy, Bandit)
- Dynamic Docker image versioning
- EKS deployment using Kustomize
- Slack/email notifications
- Terraform infrastructure provisioning

### 5. Application Monitoring - Python Script
Automated monitoring and recovery:
- Health check monitoring
- Multi-channel notifications (Slack, Email, SNS)
- Automatic recovery actions
- CloudWatch metrics integration
- Docker and K8s support

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured
- Docker and Docker Compose
- Python 3.9+
- kubectl and helm
- Ansible 2.15+
- Terraform 1.6+

### Environment Variables
Create a `.env` file:
```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_REGION=us-east-1
SLACK_WEBHOOK_URL=your_webhook_url
```

## 🔧 Terraform Setup

### Initialize and Plan
```bash
cd terraform
terraform init
terraform plan -var-file=terraform.tfvars
```

### Apply Infrastructure
```bash
terraform apply -auto-approve -var-file=terraform.tfvars
```

### Destroy Infrastructure
```bash
terraform destroy -auto-approve -var-file=terraform.tfvars
```

## 📦 Ansible Deployment

### Configure AWS Dynamic Inventory
Edit `ansible/inventory/aws_ec2.yml`:
```yaml
plugin: aws_ec2
regions:
  - us-east-1
filters:
  instance-state-name: running
  tag:Environment: production
```

### Deploy Application
```bash
cd ansible
ansible-playbook -i inventory/aws_ec2.yml deploy.yml
```

### Run Specific Tasks
```bash
ansible-playbook -i inventory/aws_ec2.yml deploy.yml --tags docker
ansible-playbook -i inventory/aws_ec2.yml deploy.yml --tags application
```

## ☸️ Kubernetes Deployment

### Deploy to EKS
```bash
# Update kubeconfig
aws eks update-kubeconfig --name school-saas-cluster --region us-east-1

# Deploy using Kustomize
kubectl apply -k k8s/production

# Check deployment status
kubectl get pods -n school-saas
kubectl get services -n school-saas
kubectl get ingress -n school-saas
```

### Rollback Deployment
```bash
kubectl rollout undo deployment/school-saas-app -n school-saas
```

### Scale Pods
```bash
kubectl scale deployment/school-saas-app --replicas=5 -n school-saas
```

## 🔄 CI/CD Pipeline

### Workflow Triggers
- Push to main/develop branches
- Pull requests
- Git tags (v*)
- Manual workflow dispatch

### Pipeline Stages
1. **Lint**: Black, isort, Flake8, MyPy
2. **Test**: Pytest with coverage
3. **Security Scan**: Trivy, Bandit
4. **Build**: Docker image with dynamic versioning
5. **Deploy**: EKS deployment with Kustomize

### Dynamic Versioning
The CI/CD pipeline automatically generates version tags:
- Tagged releases: `v1.0.0`
- Main branch: `2024.01.28-a1b2c3d`
- Other branches: `a1b2c3d`

### Manual Deployment
Use GitHub Actions to manually trigger deployment:
1. Go to Actions tab
2. Select "Deploy to EC2 via Ansible" or "Infrastructure Provisioning"
3. Click "Run workflow"
4. Select environment and parameters

## 👁️ Application Monitoring

### Run Monitor Locally
```bash
pip install -r monitor_requirements.txt
python monitor_app.py --config monitor_config.json
```

### Run as Docker Container
```bash
docker-compose -f docker-compose.monitor.yml up -d
```

### Run as System Service
```bash
# Copy service file
sudo cp school-saas-monitor.service /etc/systemd/system/

# Create monitor directory
sudo mkdir -p /opt/school-saas/monitor
sudo cp monitor_app.py monitor_config.json /opt/school-saas/monitor/

# Enable and start service
sudo systemctl enable school-saas-monitor
sudo systemctl start school-saas-monitor

# Check status
sudo systemctl status school-saas-monitor
```

### Test Health Check
```bash
python monitor_app.py --test
```

## ⚙️ Configuration

### Monitor Configuration (monitor_config.json)
```json
{
  "app_url": "http://localhost:5000",
  "health_endpoint": "/health",
  "check_interval": 60,
  "max_failures": 3,
  "recovery_enabled": true,
  "slack_webhook_url": "https://hooks.slack.com/services/...",
  "aws": {
    "region": "us-east-1",
    "sns_topic_arn": "arn:aws:sns:..."
  }
}
```

### Terraform Variables (terraform.tfvars)
```hcl
project_name     = "school-saas"
environment      = "production"
aws_region       = "us-east-1"
instance_count   = 3
instance_type    = "t3.medium"
ssh_key_name     = "your-ssh-key-pair"
```

### Ansible Variables (group_vars/production.yml)
```yaml
environment: production
app_replicas: 3
app_memory_limit: 2g
docker_image_tag: "latest"
```

## 📊 Monitoring & Logging

### CloudWatch Metrics
- CPU and memory utilization
- Health check status
- Recovery success/failure
- Custom application metrics

### Logs Locations
- Application: `/var/log/docker/*.log`
- Nginx: `/var/log/nginx/*.log`
- System: `/var/log/syslog`
- Monitor: `app_monitor.log`

### Health Check Endpoints
- Application: `GET /health`
- Readiness: `GET /ready`
- Metrics: `GET /metrics`

## 🔒 Security Considerations

1. **IAM Roles**: Use least privilege for all IAM roles
2. **Secrets Management**: Use AWS Secrets Manager or Parameter Store
3. **Network Policies**: Enforce strict network policies in K8s
4. **Container Security**: Scan images with Trivy
5. **Encryption**: Enable encryption for all EBS volumes and RDS instances

## 📈 Scaling Strategy

### Horizontal Scaling
- K8s HPA for pod auto-scaling
- ASG for EC2 instances
- Load balancer for traffic distribution

### Vertical Scaling
- Adjust instance types based on metrics
- Configure resource limits and requests

### Performance Optimization
- Enable CloudWatch metrics
- Optimize database queries
- Implement caching with Redis
- Use CDN for static assets

## 🐛 Troubleshooting

### Monitor Not Starting
```bash
# Check logs
journalctl -u school-saas-monitor -f

# Check configuration
python monitor_app.py --test
```

### Deployment Failing
```bash
# Check pod logs
kubectl logs -f deployment/school-saas-app -n school-saas

# Describe pod
kubectl describe pod <pod-name> -n school-saas
```

### Terraform State Locked
```bash
# Force unlock
terraform force-unlock <LOCK_ID>
```

## 📝 License

Copyright © 2024 School SaaS. All rights reserved.
