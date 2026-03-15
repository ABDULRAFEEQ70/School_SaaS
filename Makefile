.PHONY: help terraform-init terraform-plan terraform-apply terraform-destroy \
        ansible-deploy ansible-check ansible-install \
        k8s-deploy k8s-undeploy k8s-status \
        monitor-start monitor-stop monitor-status monitor-test \
        docker-build docker-push \
        clean

help:
	@echo "School SaaS Infrastructure Automation"
	@echo ""
	@echo "Terraform:"
	@echo "  make terraform-init   Initialize Terraform"
	@echo "  make terraform-plan   Create Terraform plan"
	@echo "  make terraform-apply  Apply Terraform changes"
	@echo "  make terraform-destroy Destroy Terraform infrastructure"
	@echo ""
	@echo "Ansible:"
	@echo "  make ansible-deploy   Deploy application via Ansible"
	@echo "  make ansible-check    Verify Ansible configuration"
	@echo "  make ansible-install  Install Ansible dependencies"
	@echo ""
	@echo "Kubernetes:"
	@echo "  make k8s-deploy       Deploy to Kubernetes"
	@echo "  make k8s-undeploy     Remove Kubernetes resources"
	@echo "  make k8s-status       Check Kubernetes status"
	@echo ""
	@echo "Monitoring:"
	@echo "  make monitor-start    Start application monitor"
	@echo "  make monitor-stop     Stop application monitor"
	@echo "  make monitor-status   Check monitor status"
	@echo "  make monitor-test     Run monitor test"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build     Build Docker image"
	@echo "  make docker-push      Push Docker image to registry"
	@echo ""
	@echo "Other:"
	@echo "  make clean            Clean temporary files"

# Terraform commands
terraform-init:
	cd terraform && terraform init

terraform-plan:
	cd terraform && terraform plan -var-file=terraform.tfvars

terraform-apply:
	cd terraform && terraform apply -auto-approve -var-file=terraform.tfvars

terraform-destroy:
	cd terraform && terraform destroy -auto-approve -var-file=terraform.tfvars

# Ansible commands
ansible-install:
	pip install ansible boto3 botocore

ansible-check:
	cd ansible && ansible-inventory --list -i inventory/aws_ec2.yml

ansible-deploy:
	cd ansible && ansible-playbook -i inventory/aws_ec2.yml deploy.yml

# Kubernetes commands
k8s-deploy:
	kubectl apply -k k8s/production

k8s-undeploy:
	kubectl delete -k k8s/production

k8s-status:
	kubectl get pods -n school-saas
	kubectl get services -n school-saas
	kubectl get ingress -n school-saas

# Monitoring commands
monitor-start:
	docker-compose -f docker-compose.monitor.yml up -d

monitor-stop:
	docker-compose -f docker-compose.monitor.yml down

monitor-status:
	docker-compose -f docker-compose.monitor.yml ps

monitor-test:
	python monitor_app.py --test

# Docker commands
docker-build:
	docker build -t school-saas:latest .

docker-push:
	docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/school-saas:latest

# Clean up
clean:
	rm -rf .terraform *.tfstate *.tfstate.backup
	rm -rf k8s/production/kustomization.yaml.bak
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
