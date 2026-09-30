
terraform {
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

# Find the default VPC
data "aws_vpc" "default" {
  default = true
}

# Find Ubuntu 22.04 LTS
data "aws_ami" "ubuntu" {
  most_recent = true
  owners      = ["099720109477"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }

  filter {
    name   = "architecture"
    values = ["x86_64"]
  }
}

# Security group for the application server
resource "aws_security_group" "ecommerce_sg" {
  name        = "ecommerce-terraform-sg"
  description = "Access for ecommerce application"
  vpc_id      = data.aws_vpc.default.id

  # SSH from your current public IP only
  ingress {
    description = "SSH from my IP"
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["103.98.63.154/32"]
  }

  # HTTP access
  ingress {
    description = "HTTP"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # Flask application testing from your IP only
  ingress {
    description = "Flask app testing"
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["103.98.63.154/32"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "ecommerce-terraform-sg"
  }
}

# E-commerce deployment server
resource "aws_instance" "ecommerce_server" {
  ami                    = data.aws_ami.ubuntu.id
  instance_type          = "t3.micro"
  key_name               = "ecommerce-terraform-key"
  vpc_security_group_ids = [aws_security_group.ecommerce_sg.id]

  user_data = <<-EOF
    #!/bin/bash
    apt-get update -y
    apt-get install -y docker.io
    systemctl enable --now docker
    usermod -aG docker ubuntu
  EOF

  root_block_device {
    volume_size = 8
    volume_type = "gp3"
  }

  tags = {
    Name        = "ecommerce-microservices-server"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }
}

output "instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.ecommerce_server.id
}

output "public_ip" {
  description = "Public IP of the application server"
  value       = aws_instance.ecommerce_server.public_ip
}

output "ssh_command" {
  description = "SSH command to connect to EC2"
  value       = "ssh -i ~/.ssh/ecommerce-terraform-key.pem ubuntu@${aws_instance.ecommerce_server.public_ip}"
}