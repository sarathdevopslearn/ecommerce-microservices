
terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "ap-south-1"
}

# Ubuntu 24.04 LTS AMI in Mumbai
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd-gp3/ubuntu-noble-24.04-amd64-server-*"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "root-device-type"
    values = ["ebs"]
  }
}

# Use the existing default VPC
data "aws_vpc" "default" {
  default = true
}

# Restrict SSH to your public IP.
# UPDATE this CIDR if your public IP has changed.
resource "aws_security_group" "k3s_lab_sg" {
  name        = "k3s-lab-terraform-sg"
  description = "Restricted SSH access for temporary K3s lab"
  vpc_id      = data.aws_vpc.default.id

  ingress {
    description = "SSH from authorized IP only"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["103.98.209.95/32"]
  }

  # Allow outbound access for package installation,
  # image pulls and K3s installation.
  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name        = "k3s-lab-terraform-sg"
    Environment = "temporary-lab"
    ManagedBy   = "Terraform"
  }
}

# Dedicated temporary Kubernetes lab server
resource "aws_instance" "k3s_lab" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.large"
  key_name               = "ecommerce-terraform-key"
  vpc_security_group_ids = [aws_security_group.k3s_lab_sg.id]

  # Require IMDSv2 for instance metadata access
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  # Install K3s automatically at first boot.
  # K3s includes its own container runtime.
  user_data = <<-EOF
    #!/bin/bash
    set -euxo pipefail

    exec > >(tee -a /var/log/k3s-lab-bootstrap.log) 2>&1

    apt-get update -y
    apt-get install -y curl ca-certificates

    # Install lightweight Kubernetes
    curl -sfL https://get.k3s.io | \
      INSTALL_K3S_EXEC="server --write-kubeconfig-mode 644" sh -

    # Wait for Kubernetes API and node readiness
    for i in $(seq 1 60); do
      if /usr/local/bin/k3s kubectl get nodes >/dev/null 2>&1; then
        break
      fi
      sleep 10
    done

    /usr/local/bin/k3s kubectl wait \
      --for=condition=Ready node \
      --all \
      --timeout=300s

    # Permit the Ubuntu user to run kubectl
    mkdir -p /home/ubuntu/.kube
    cp /etc/rancher/k3s/k3s.yaml /home/ubuntu/.kube/config
    chown -R ubuntu:ubuntu /home/ubuntu/.kube
    chmod 600 /home/ubuntu/.kube/config

    echo "K3s bootstrap finished" > /var/log/k3s-lab-ready
  EOF

  # Encrypted root volume
  root_block_device {
    volume_size           = 30
    volume_type           = "gp3"
    encrypted             = true
    delete_on_termination = true
  }

  # Allow Terraform to replace the instance if this configuration
  # requires replacement, without a name conflict on the security group.
  tags = {
    Name        = "k3s-kubernetes-lab"
    Environment = "temporary-lab"
    ManagedBy   = "Terraform"
    Purpose     = "DevOps-CICD-Monitoring"
    AutoCleanup = "REQUIRED"
  }

  depends_on = [aws_security_group.k3s_lab_sg]
}

output "instance_id" {
  description = "Temporary K3s lab EC2 instance ID"
  value       = aws_instance.k3s_lab.id
}

output "public_ip" {
  description = "Public IP for SSH access"
  value       = aws_instance.k3s_lab.public_ip
}

output "ssh_command" {
  description = "SSH command to access the lab"
  value       = "ssh -i ~/.ssh/ecommerce-terraform-key.pem ubuntu@${aws_instance.k3s_lab.public_ip}"
}
