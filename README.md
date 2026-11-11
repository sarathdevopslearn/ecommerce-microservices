# E-Commerce Microservices – End-to-End DevOps Project

## 1. Project Overview

This project demonstrates an end-to-end DevOps implementation for a Python-based E-Commerce Microservices application.

The application consists of six independent microservices, containerized using Docker and deployed using Kubernetes (K3s).

The infrastructure is provisioned using Terraform on AWS EC2. Continuous Integration and Continuous Deployment are automated using GitHub Actions. Prometheus and Grafana are used for application monitoring.

**Project objective:** Implement a practical DevOps workflow covering infrastructure provisioning, containerization, orchestration, CI/CD automation, deployment, and monitoring.

## 2. Architecture

## 🏗️ Project Architecture

The following diagram illustrates the complete CI/CD,
containerization, Kubernetes deployment and monitoring architecture.

![E-Commerce Microservices Architecture](docs/architecture.png)

```text
                  Developer
                      |
                      v
               GitHub Repository
                      |
                      v
                GitHub Actions
                      |
              Automated Testing
                  (Pytest)
                      |
                      v
               Docker Build
                      |
                      v
                  Docker Hub
                      |
                      v
               AWS EC2 - Ubuntu
                      |
                      v
               K3s Kubernetes
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
       Product       User       Order
       Service      Service    Service
          |           |           |
          +-----------+-----------+
                      |
          +-----------+-----------+
          |           |           |
          v           v           v
      Inventory    Payment   Notification
       Service     Service     Service

          Monitoring Layer
             Prometheus
                  |
                  v
                Grafana

       Infrastructure Provisioning
                Terraform
```

## 3. Technology Stack

| Category | Technology |
|---|---|
| Cloud | AWS EC2 |

| Infrastructure as Code | Terraform |
| Operating System | Ubuntu Linux |
| Containerization | Docker |
| Orchestration | Kubernetes (K3s) |
| CI/CD | GitHub Actions |
| Image Registry | Docker Hub |
| Programming | Python |
| Frameworks | Flask, FastAPI |
| Testing | Pytest |
| Monitoring | Prometheus, Grafana |
| Version Control | Git, GitHub |

## 4. Application Microservices

| Service | Framework | Port |
|---|---|---|
| Product Service | Flask | 5001 |
| User Service | Flask | 5000 |
| Order Service | FastAPI | 8000 |
| Inventory Service | Flask | 5003 |
| Payment Service | Flask | 5006 |
| Notification Service | Flask | Verify configuration |

### Service Responsibilities

- **Product Service:** Manages product information and product APIs.
- **User Service:** Handles user-related operations.
- **Order Service:** Handles order processing and integrates with other services.
- **Inventory Service:** Manages inventory information.
- **Payment Service:** Handles payment-related operations.
- **Notification Service:** Handles application notifications.

## 5. Infrastructure Provisioning – Terraform

Terraform is used to provision AWS infrastructure.

Implemented configurations include:

- AWS provider configuration.
- Ubuntu AMI selection.
- EC2 instance provisioning.
- Security group configuration.
- Infrastructure management using Terraform.

## 6. Containerization – Docker

Each microservice is containerized independently.

Implemented activities:

- Created Dockerfiles for microservices.
- Built Docker images.
- Tagged and versioned images.
- Published images to Docker Hub.
- Used Docker Compose for local development and testing.

## 7. Kubernetes Deployment – K3s

The six microservices are deployed on a Kubernetes K3s cluster.

Kubernetes configurations include:

- Deployments and ReplicaSets.
- ClusterIP and NodePort Services where required.
- ConfigMaps and Secrets.
- Readiness and Liveness Probes.
- Resource Requests and Limits.
- Horizontal Pod Autoscaling.
- Ingress Controller.
- TLS configuration.
- Role-Based Access Control.
- Helm-based deployments.

## 8. CI/CD – GitHub Actions

Automated CI/CD workflows are implemented using GitHub Actions.

### Pipeline Workflow

1. Checkout source code.
2. Configure Python environment.
3. Install application dependencies.
4. Execute automated tests using Pytest.
5. Perform code formatting checks using Black.
6. Build Docker images.
7. Push Docker images to Docker Hub.
8. Deploy updated application images to the Kubernetes environment.

Additional pipeline features:

- Dependency caching.
- Matrix builds.
- Workflow artifacts.
- Environment-based deployment configuration.
- SSH-based deployment automation where configured.

## 9. Monitoring – Prometheus and Grafana

Prometheus and Grafana are used for application monitoring.

Implemented activities:

- Configured Prometheus metrics collection.
- Added Prometheus as a Grafana data source.
- Created a Product Service Availability dashboard.
- Visualized application availability and monitoring metrics.

## 10. Key DevOps Concepts

- Infrastructure as Code.
- Containerization.
- Kubernetes orchestration.
- CI/CD automation.
- Automated application testing.
- Container image versioning.
- Kubernetes health checks.
- Configuration and secrets management.
- Rolling updates.
- Application monitoring.
- Deployment troubleshooting.

## 11. Repository Structure

```text
ecommerce-microservices/
│
├── services/
│   ├── product-service/
│   ├── user-service/
│   ├── order-service/
│   ├── inventory-service/
│   ├── payment-service/
│   └── notification-service/
│
├── k8s/
│   ├── deployments/
│   ├── services/
│   ├── ingress/
│   └── configurations/
│
├── monitoring/
│   ├── prometheus/
│   └── grafana/
│
├── scripts/
│
├── README.md
└── .gitignore
```

*Update this example to match the actual repository folders and files.*

## 12. Project Screenshots

Add screenshots demonstrating:

- GitHub Actions successful CI/CD execution.
- Docker Hub repositories and images.
- Kubernetes pods and services.
- AWS EC2 infrastructure.
- Prometheus targets.
- Grafana monitoring dashboard.

## 13. Learning Outcomes

Through this project, I gained hands-on experience in:

- Provisioning cloud infrastructure using Terraform.
- Containerizing Python applications using Docker.
- Deploying microservices using Kubernetes.
- Building CI/CD pipelines using GitHub Actions.
- Managing container images using Docker Hub.
- Monitoring applications using Prometheus and Grafana.
- Troubleshooting infrastructure, containers, and application deployments.

## Author

**DevOps Project Portfolio**

Skills: AWS | Terraform | Linux | Docker | Kubernetes | GitHub Actions | CI/CD | Prometheus | Grafana

GitHub: Add your GitHub profile URL