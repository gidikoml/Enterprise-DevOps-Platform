# Enterprise DevOps Platform

## Overview

Enterprise DevOps Platform is an end-to-end DevOps project demonstrating the design, development, containerization, automated testing, security scanning, infrastructure provisioning, CI/CD automation, Kubernetes orchestration, monitoring, alerting, and operational management of a Python Flask application.

The platform demonstrates a production-style deployment workflow running on AWS EKS with three isolated environments:

**DEV → STAGING → Manual Approval → PRODUCTION**

The project integrates application development, Infrastructure as Code, DevSecOps, CI/CD, cloud infrastructure, observability, and Git-based configuration management.

---

## Project Objectives

The main objectives of this project are to:

* Build and containerize a Python Flask application.
* Integrate PostgreSQL for persistent application data.
* Deploy containerized workloads to Kubernetes.
* Provision AWS infrastructure using Terraform.
* Run Kubernetes workloads on Amazon EKS.
* Store container images in Amazon ECR.
* Build an automated Jenkins CI/CD pipeline.
* Implement automated testing with Pytest.
* Perform code-quality analysis with SonarQube.
* Scan container images for vulnerabilities with Trivy.
* Separate DEV, STAGING, and PRODUCTION environments.
* Validate applications before promoting them between environments.
* Require manual approval before production deployment.
* Monitor Kubernetes workloads using Prometheus and Grafana.
* Configure alerts and email notifications.
* Manage sensitive credentials outside Git.
* Document troubleshooting and operational procedures.
* Clean up AWS resources when testing is complete to control cloud costs.

---

## Architecture

```text
Developer
    |
    v
GitHub Repository
    |
    v
Jenkins CI/CD
    |
    +-------------------------+
    |                         |
    v                         v
Pytest                    SonarQube
    |                         |
    +------------+------------+
                 |
                 v
           Quality Gate
                 |
                 v
          Docker Build
                 |
                 v
          Trivy Security Scan
                 |
                 v
            Amazon ECR
                 |
                 v
              AWS EKS
                 |
                 v
                DEV
                 |
                 v
             DEV Test
                 |
                 v
             STAGING
                 |
                 v
           STAGING Test
                 |
                 v
          Manual Approval
                 |
                 v
            PRODUCTION
                 |
                 v
        AWS Load Balancer
                 |
                 v
        Flask Application
                 |
                 v
            PostgreSQL
```

Monitoring architecture:

```text
AWS EKS
   |
   v
Prometheus
   |
   v
Grafana
   |
   +----------------+
   |                |
   v                v
Dashboard         Alerts
                    |
                    v
             Email Notification
```

---

## Technology Stack

### Application

* Python
* Flask
* PostgreSQL
* HTML
* Bootstrap

### Cloud

* Amazon Web Services
* Amazon EKS
* Amazon ECR
* Amazon EC2
* Amazon VPC
* AWS IAM
* Elastic Load Balancing
* Amazon EBS

### Containerization

* Docker
* Docker Desktop

### Container Orchestration

* Kubernetes
* Amazon EKS
* Deployments
* Services
* Namespaces
* Persistent Volumes
* Persistent Volume Claims
* StorageClass
* LoadBalancer Services

### CI/CD

* Jenkins
* Harness CI/CD
* GitHub
* Pytest
* SonarQube
* Trivy

### Infrastructure as Code

* Terraform
* Helm
* Kubernetes YAML

### Monitoring and Observability

* Prometheus
* Grafana
* kube-state-metrics
* Kubernetes metrics
* Grafana Alerting

### Scripting and Configuration

* Bash
* YAML
* Groovy
* Terraform HCL
* Git

---

## Project Structure

```text
Enterprise-DevOps-Platform/
|
|-- app/
|   |-- app.py
|   |-- database.py
|   |-- models.py
|   |-- requirements.txt
|   |-- Dockerfile
|   |-- tests/
|   |-- templates/
|   |-- static/
|   `-- k8s/
|
|-- kubernetes/
|   `-- environments/
|       |-- dev/
|       |   |-- namespace.yaml
|       |   `-- deployment.yaml
|       |
|       |-- staging/
|       |   |-- namespace.yaml
|       |   `-- deployment.yaml
|       |
|       |-- prod/
|       |   |-- namespace.yaml
|       |   `-- deployment.yaml
|       |
|       `-- services.yaml
|
|-- terraform/
|   |-- main.tf
|   |-- variables.tf
|   |-- outputs.tf
|   `-- .terraform.lock.hcl
|
|-- helm/
|
|-- .harness/
|
|-- docs/
|
|-- Jenkinsfile
|-- Dockerfile.jenkins
|-- enterprise-devops-monitoring-dashboard.json
|-- grafana-alert-rules.yaml
|-- grafana-smtp-values.yaml
|-- .gitignore
`-- README.md
```

---

# Application

The application is a Python Flask web application backed by PostgreSQL.

It includes a web interface for user registration and supports application data and uploaded media.

## Local Development

Create a Python virtual environment:

```cmd
python -m venv venv
```

Activate the environment on Windows:

```cmd
venv\Scripts\activate
```

Install application dependencies:

```cmd
pip install -r app\requirements.txt
```

The Flask application can then be started according to the application configuration.

---

# Docker

The Flask application is containerized using Docker.

Build the application image:

```cmd
docker build -t enterprise-devops-platform ./app
```

Check the image:

```cmd
docker images
```

The project also contains:

```text
Dockerfile.jenkins
```

The custom Jenkins environment provides tools required by the CI/CD pipeline, including:

* Python
* Docker CLI
* kubectl
* AWS CLI
* Trivy
* Pytest
* SonarScanner integration

---

# Infrastructure as Code with Terraform

Terraform is used to manage AWS infrastructure required by the platform.

Terraform configuration is stored under:

```text
terraform/
```

## Initialize Terraform

```cmd
cd terraform
terraform init
```

## Validate Configuration

```cmd
terraform validate
```

## Review Infrastructure Changes

```cmd
terraform plan
```

## Provision Infrastructure

```cmd
terraform apply
```

Always review the Terraform plan before approving infrastructure creation.

## Terraform Outputs

Infrastructure information can be displayed with:

```cmd
terraform output
```

---

# AWS EKS

The Kubernetes platform runs on Amazon Elastic Kubernetes Service.

AWS CLI and kubectl are used to interact with the cluster.

Verify AWS authentication:

```cmd
aws sts get-caller-identity
```

Configure kubeconfig:

```cmd
aws eks update-kubeconfig --region us-east-1 --name enterprise-devops-cluster
```

Verify cluster connectivity:

```cmd
kubectl get nodes
```

A healthy cluster should show the EKS worker nodes in the `Ready` state.

---

# Kubernetes Multi-Environment Architecture

The project uses three Kubernetes environments:

```text
enterprise-dev
enterprise-staging
enterprise-prod
```

These namespaces isolate workloads while allowing the same application artifact to move through the release lifecycle.

Verify namespaces:

```cmd
kubectl get namespaces
```

---

## DEV Environment

DEV is the first deployment target for a new application image.

Check DEV pods:

```cmd
kubectl get pods -n enterprise-dev
```

The pipeline deploys the image and performs an application smoke test before promotion.

---

## STAGING Environment

After DEV validation succeeds, the same image is promoted to STAGING.

Check STAGING:

```cmd
kubectl get pods -n enterprise-staging
```

STAGING must pass validation before production approval becomes available.

---

## PRODUCTION Environment

Production uses:

```text
enterprise-prod
```

Check production workloads:

```cmd
kubectl get pods -n enterprise-prod
```

Production deployment occurs only after:

```text
DEV Deployment
      |
      v
DEV Validation
      |
      v
STAGING Deployment
      |
      v
STAGING Validation
      |
      v
Manual Approval
      |
      v
PRODUCTION
```

---

# Kubernetes Services

DEV and STAGING use internal Kubernetes services.

PRODUCTION uses a LoadBalancer service to expose the application through AWS.

Check services:

```cmd
kubectl get svc -n enterprise-dev
kubectl get svc -n enterprise-staging
kubectl get svc -n enterprise-prod
```

The production LoadBalancer provides an external AWS endpoint for the application.

---

# Amazon ECR

Amazon Elastic Container Registry stores application container images.

The CI/CD workflow is:

```text
Docker Build
     |
     v
Trivy Scan
     |
     v
Amazon ECR
```

Jenkins creates a versioned image using the Jenkins build number.

Example:

```text
enterprise-devops-platform:27
```

The same versioned image is promoted through all environments.

```text
Build Once
    |
    v
DEV
    |
    v
STAGING
    |
    v
PRODUCTION
```

This ensures that the artifact validated in DEV and STAGING is the same artifact deployed to production.

---

# Jenkins CI/CD Pipeline

The pipeline is defined in:

```text
Jenkinsfile
```

The complete CI/CD workflow is:

```text
Checkout
   |
   v
Pytest
   |
   v
SonarQube Analysis
   |
   v
Quality Gate
   |
   v
Build Docker Image
   |
   v
Trivy Security Scan
   |
   v
Configure AWS / EKS
   |
   v
ECR Login
   |
   v
Push Image to ECR
   |
   v
Deploy DEV
   |
   v
Test DEV
   |
   v
Deploy STAGING
   |
   v
Test STAGING
   |
   v
Approve PROD
   |
   v
Deploy PROD
   |
   v
Verify PROD
   |
   v
Smoke Test PROD
```

---

# Automated Testing with Pytest

Pytest validates the Python application before container deployment.

Tests run early in the pipeline.

If application tests fail:

```text
Pytest Failure
      |
      v
Pipeline Stops
```

This prevents broken application code from reaching the container deployment process.

---

# SonarQube Code Quality

SonarQube performs static code-quality analysis.

Pipeline workflow:

```text
SonarQube Analysis
        |
        v
Quality Gate
```

The Quality Gate determines whether the application can continue through the pipeline.

A failed Quality Gate stops the release.

---

# Trivy Security Scanning

Trivy scans the Docker image before it is pushed to Amazon ECR.

The pipeline checks for:

```text
HIGH
CRITICAL
```

vulnerabilities.

A failed security scan prevents the image from being promoted.

This introduces security validation directly into the CI/CD lifecycle.

---

# DEV Deployment

After the Docker image passes testing, quality checks, and vulnerability scanning, Jenkins pushes it to Amazon ECR.

The image is deployed to DEV.

```text
Amazon ECR
     |
     v
DEV Deployment
     |
     v
Rollout Status
     |
     v
Smoke Test
```

A failed DEV deployment or smoke test stops the pipeline.

---

# STAGING Deployment

After DEV succeeds, Jenkins promotes the same image to STAGING.

```text
DEV Passed
    |
    v
STAGING
    |
    v
Rollout Validation
    |
    v
Smoke Test
```

Production cannot be reached if STAGING fails.

---

# Manual Production Approval

A manual approval gate protects production.

Jenkins pauses at:

```text
Approve PROD
```

The pipeline asks whether the validated application should be promoted to production.

Only after approval does the production deployment begin.

This provides a controlled release gate between automated validation and production.

---

# Production Deployment

After approval, Jenkins deploys the same tested image to:

```text
enterprise-prod
```

Jenkins validates:

* Production pods
* Deployment status
* Replica availability
* Kubernetes Service
* AWS LoadBalancer
* Application endpoint

The final smoke test sends an HTTP request to the production endpoint.

A successful response confirms that the deployment is operational.

---

# Successful End-to-End Pipeline Validation

The complete CI/CD workflow has been successfully validated.

```text
GitHub
   |
   v
Jenkins
   |
   v
Pytest
   |
   v
SonarQube
   |
   v
Quality Gate
   |
   v
Docker Build
   |
   v
Trivy
   |
   v
Amazon ECR
   |
   v
DEV
   |
   v
DEV Test
   |
   v
STAGING
   |
   v
STAGING Test
   |
   v
Manual Approval
   |
   v
PRODUCTION
   |
   v
Production Verification
   |
   v
Smoke Test
   |
   v
SUCCESS
```

The pipeline successfully promoted a versioned application image through DEV, STAGING, and PRODUCTION.

---

# Harness CI/CD

Harness CI/CD is also integrated into the project for CI/CD experimentation and GitHub-based automation.

Harness configuration is stored under:

```text
.harness/
```

---

# Prometheus Monitoring

Prometheus collects Kubernetes metrics used to monitor application workloads.

## Memory Usage

```promql
container_memory_working_set_bytes{namespace="enterprise-devops"}
```

## CPU Usage

```promql
rate(container_cpu_usage_seconds_total{namespace="enterprise-devops"}[5m])
```

## Pod Restarts

```promql
kube_pod_container_status_restarts_total{namespace="enterprise-devops"}
```

## Pod Status

```promql
kube_pod_status_phase{namespace="enterprise-devops", phase="Running"}
```

---

# Grafana Dashboard

The project includes a Grafana dashboard named:

```text
Enterprise DevOps Monitoring
```

The dashboard monitors:

* Memory Usage by Pod
* CPU Usage by Pod
* Pod Restarts
* Pod Status

The exported dashboard is stored in:

```text
enterprise-devops-monitoring-dashboard.json
```

---

# Grafana Persistence

Grafana persistent storage is enabled so configuration can survive pod restarts.

The configuration is stored in:

```text
grafana-smtp-values.yaml
```

---

# Grafana Alerting

The project includes the alert rule:

```text
Pod Restart Detected
```

The alert monitors Kubernetes container restart metrics.

The exported configuration is stored in:

```text
grafana-alert-rules.yaml
```

---

# Email Notifications

Grafana SMTP is configured for email notifications.

Sensitive SMTP credentials are not stored directly in the Git repository.

The SMTP password is supplied through a Kubernetes Secret and referenced by the application environment.

This separates sensitive credentials from version-controlled configuration.

---

# Alert Validation

The monitoring workflow was validated by intentionally terminating the main process inside an application container.

Kubernetes restarted the container.

Prometheus detected the restart count.

Grafana detected the alert condition.

The configured email notification was successfully delivered.

```text
Container Restart
       |
       v
Kubernetes
       |
       v
Prometheus
       |
       v
Grafana Alert
       |
       v
Email Notification
```

---

# Security Practices

The project demonstrates several DevSecOps practices:

* Automated application testing
* SonarQube static analysis
* Quality Gates
* Trivy container vulnerability scanning
* Jenkins Credentials
* AWS IAM authentication
* Kubernetes Secrets
* Secret separation from Git
* Versioned Docker images
* Environment isolation
* Manual production approval
* Infrastructure as Code
* Controlled artifact promotion

Sensitive values such as AWS Secret Access Keys, passwords, API tokens, SMTP passwords, and application secrets must never be committed to Git.

---

# Challenges Encountered and Solutions

Building the platform required troubleshooting several real-world DevOps problems across Docker, Kubernetes, AWS, Terraform, Jenkins, security, and CI/CD.

---

## Challenge 1: Docker Engine Connectivity

### Problem

During the initial containerization phase, Docker commands could not communicate with the Docker Desktop Linux engine.

### Solution

Docker Desktop was started and the Docker daemon was verified.

```cmd
docker version
docker ps
```

The Flask application was then successfully built and executed inside a Docker container.

---

## Challenge 2: Kubernetes Deployment YAML Error

### Problem

The initial Kubernetes Deployment contained an incorrect `containerPort` configuration.

This prevented Kubernetes from accepting the deployment correctly.

### Solution

The Deployment manifest was corrected:

```yaml
ports:
  - containerPort: 5000
```

The manifest was reapplied and the application pods reached the `Running` state.

---

## Challenge 3: Kubernetes Service Configuration

### Problem

An incorrect Kubernetes Service type initially prevented the application from being exposed correctly.

### Solution

The Service manifest was corrected and reapplied.

The architecture was later improved to use:

```text
DEV      -> ClusterIP
STAGING  -> ClusterIP
PROD     -> LoadBalancer
```

This keeps non-production environments internal while exposing production through AWS.

---

## Challenge 4: AWS CLI Missing During EKS Authentication

### Problem

`kubectl` could not authenticate with Amazon EKS.

The error included:

```text
getting credentials: exec: executable aws not found
```

The EKS kubeconfig depends on AWS CLI to obtain Kubernetes authentication tokens.

### Solution

AWS CLI was installed in the environment running Jenkins and Kubernetes operations.

Validation:

```bash
aws --version
kubectl version --client
```

---

## Challenge 5: AWS Credentials Missing in Jenkins

### Problem

After AWS CLI was installed, AWS commands returned:

```text
Unable to locate credentials
```

Jenkins had the AWS tooling but did not yet have credentials.

### Solution

AWS credentials were configured in Jenkins Credentials.

The credential ID used by the pipeline is:

```text
aws-credentials
```

Credentials are injected into the pipeline instead of being stored directly in the repository.

---

## Challenge 6: Incorrect AWS Credential Mapping

### Problem

During AWS integration, the Access Key ID and Secret Access Key were initially mapped incorrectly.

AWS authentication returned errors such as:

```text
IncompleteSignature
```

and:

```text
SignatureDoesNotMatch
```

### Solution

A Jenkins credential of type `Username with password` was configured as:

```text
Username = AWS Access Key ID
Password = AWS Secret Access Key
ID       = aws-credentials
```

Both values must belong to the same AWS access key pair.

Authentication was verified using:

```bash
aws sts get-caller-identity
```

---

## Challenge 7: Jenkins Kubeconfig Read-Only Filesystem

### Problem

AWS authentication started working, but Jenkins failed while generating the EKS kubeconfig.

The error was:

```text
Can't open kubeconfig for writing:
Read-only file system: '/root/.kube/config'
```

### Solution

Instead of writing the kubeconfig to `/root/.kube/config`, Jenkins was configured to use its writable workspace:

```groovy
KUBECONFIG = "${WORKSPACE}/.kube/config"
```

The pipeline creates the directory:

```bash
mkdir -p "$(dirname "$KUBECONFIG")"
```

Then generates the EKS configuration:

```bash
aws eks update-kubeconfig \
  --region "$AWS_REGION" \
  --name "$EKS_CLUSTER" \
  --kubeconfig "$KUBECONFIG"
```

Jenkins could then successfully communicate with EKS.

---

## Challenge 8: AWS Credentials Missing During Kubernetes Tests

### Problem

Jenkins successfully authenticated with AWS, connected to EKS, pushed the Docker image, and deployed DEV.

However, `Test DEV` failed with:

```text
Unable to locate credentials
```

The EKS kubeconfig existed, but `kubectl` still needed AWS credentials to generate an EKS authentication token.

### Solution

AWS credentials were made available to every pipeline stage that communicates with EKS.

```bash
export AWS_ACCESS_KEY_ID="$AWS_CREDS_USR"
export AWS_SECRET_ACCESS_KEY="$AWS_CREDS_PSW"
export AWS_DEFAULT_REGION="$AWS_REGION"
```

The correction was applied across DEV, STAGING, and PRODUCTION Kubernetes operations.

---

## Challenge 9: Moving from One Environment to Three Environments

### Problem

The original Kubernetes deployment used a single environment.

This did not represent a production-style application release lifecycle.

### Solution

Three Kubernetes namespaces were created:

```text
enterprise-dev
enterprise-staging
enterprise-prod
```

Environment configuration was organized under:

```text
kubernetes/environments/dev/
kubernetes/environments/staging/
kubernetes/environments/prod/
```

Jenkins was updated to automate promotion between the environments.

---

## Challenge 10: Safe Production Deployment

### Problem

Automatically deploying every successful build directly to production creates additional deployment risk.

### Solution

A manual production approval stage was introduced.

```groovy
stage('Approve PROD') {
    steps {
        timeout(time: 15, unit: 'MINUTES') {
            input(
                message: 'DEV and STAGING passed. Deploy this build to PRODUCTION?',
                ok: 'Deploy to PROD'
            )
        }
    }
}
```

Production deployment occurs only after DEV and STAGING pass validation and production deployment is explicitly approved.

---

## Challenge 11: Artifact Consistency Across Environments

### Problem

Building separate Docker images for DEV, STAGING, and PRODUCTION could result in production receiving an artifact different from the one previously tested.

### Solution

The Docker image is built once.

Jenkins assigns the image a version using the build number.

Example:

```text
enterprise-devops-platform:27
```

The same artifact is promoted:

```text
Build Once
    |
    v
DEV
    |
    v
STAGING
    |
    v
PRODUCTION
```

This ensures artifact consistency throughout the deployment lifecycle.

---

## Challenge 12: Terraform and AWS Cost Management

### Problem

Cloud resources such as EKS worker nodes, load balancers, EBS storage, and other AWS infrastructure may continue generating charges after testing.

### Solution

Terraform-managed resources are reviewed before cleanup:

```cmd
terraform plan -destroy
```

When the infrastructure is no longer required:

```cmd
terraform destroy
```

Resources created outside Terraform must also be reviewed separately.

Cloud resource cleanup is treated as part of the infrastructure lifecycle.

---

# Troubleshooting Methodology

A systematic troubleshooting approach was used throughout the project.

```text
Identify Failure
      |
      v
Review Logs
      |
      v
Identify Failed Component
      |
      v
Correct Configuration
      |
      v
Validate
      |
      v
Commit Changes
      |
      v
Push to GitHub
      |
      v
Run Jenkins
      |
      v
Validate DEV
      |
      v
Validate STAGING
      |
      v
Approve PROD
      |
      v
Validate PRODUCTION
```

The project therefore demonstrates not only successful deployment, but also hands-on troubleshooting across the complete DevOps lifecycle.

---

# Git Workflow

The project follows a Git-based workflow:

```text
Development
    |
    v
git add
    |
    v
git commit
    |
    v
git push
    |
    v
GitHub
    |
    v
Jenkins CI/CD
```

Application code, infrastructure configuration, Kubernetes manifests, CI/CD configuration, monitoring dashboards, and alert rules are version controlled.

---

# Configuration Recovery

Important monitoring and platform configuration is stored in Git.

Examples include:

```text
enterprise-devops-monitoring-dashboard.json
grafana-alert-rules.yaml
grafana-smtp-values.yaml
```

Sensitive Kubernetes Secret values are intentionally excluded and must be recreated securely when required.

---

# AWS Resource Cleanup

AWS resources should be removed when the lab environment is no longer required to avoid unnecessary charges.

Before destroying Terraform-managed resources:

```cmd
cd terraform
terraform plan -destroy
```

Review the plan carefully.

Then:

```cmd
terraform destroy
```

Confirm only after verifying that the listed resources can safely be removed.

After Terraform cleanup, AWS resources created by Kubernetes or manually should also be checked.

Examples include:

* Load Balancers
* EBS volumes
* ECR images
* EKS resources
* EC2 resources

---

# DevOps Practices Demonstrated

This project demonstrates hands-on experience with:

* Git-based source control
* Python application development
* Flask
* PostgreSQL
* Docker containerization
* Kubernetes orchestration
* Amazon EKS
* Amazon ECR
* AWS IAM
* AWS Load Balancing
* Terraform Infrastructure as Code
* Multi-environment deployments
* DEV / STAGING / PROD isolation
* Jenkins CI/CD
* Harness CI/CD
* Automated testing with Pytest
* SonarQube code analysis
* Quality Gates
* Trivy security scanning
* DevSecOps
* Versioned container artifacts
* Automated Kubernetes rollouts
* Smoke testing
* Manual production approval
* Prometheus monitoring
* Grafana dashboards
* Grafana alerting
* Email notifications
* Kubernetes persistent storage
* Secrets management
* Configuration recovery
* Cloud troubleshooting
* AWS cost management

---

# Future Enhancements

The core AWS EKS multi-environment CI/CD workflow is operational.

Future improvements include:

* Kubernetes Ingress
* TLS/HTTPS
* Custom domain
* AWS Load Balancer Controller
* Horizontal Pod Autoscaling
* CPU threshold alerts
* Memory threshold alerts
* Application-level metrics
* Centralized logging
* GitOps with Argo CD
* Automated rollback
* Terraform remote state
* Improved secrets management
* Backup and disaster recovery validation

---

# Author

**Komlavi Gidi**

DevOps Engineer | Cloud Engineer

AWS | Kubernetes | Terraform | Jenkins | Docker | CI/CD | DevSecOps
