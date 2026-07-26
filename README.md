# Enterprise DevOps Platform



## Overview



Enterprise DevOps Platform is a hands-on DevOps project demonstrating the design, deployment, CI/CD automation, monitoring, and operational management of a containerized application on Kubernetes.



The project combines application development, containerization, orchestration, CI/CD, Infrastructure as Code, security scanning, observability, alerting, and Git-based configuration management.



---



## Architecture



```text

Developer

    |

    v

GitHub Repository

    |

    +-------------------+

    |                   |

    v                   v

Jenkins CI/CD        Harness CI/CD

    |

    v

Build & Test

    |

    v

Security / Quality Checks

    |

    v

Docker Image

    |

    v

Kubernetes

    |

    +-------------------+

    |                   |

    v                   v

Flask Application   PostgreSQL

    |

    v

Prometheus

    |

    v

Grafana

    |

    v

Dashboard + Alerts

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



### Containerization



* Docker

* Docker Desktop



### Container Orchestration



* Kubernetes

* Deployments

* Services

* Namespaces

* Persistent Storage



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



### Monitoring and Observability



* Prometheus

* Grafana

* kube-state-metrics

* Kubernetes metrics



### Alerting



* Grafana Alerting

* Prometheus metrics

* SMTP email notifications



---



## Project Structure



```text

Enterprise-DevOps-Platform/

|

|-- app/

|   |-- app.py

|   |-- Dockerfile

|   |-- requirements.txt

|   `-- ...

|

|-- kubernetes/

|   `-- Kubernetes manifests

|

|-- helm/

|   `-- Helm configuration

|

|-- terraform/

|   `-- Terraform configuration

|

|-- .harness/

|   `-- Harness configuration

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



## Application Deployment



### Local Development



Create a Python virtual environment:



```bash

python -m venv venv

```



On Windows:



```cmd

venv\\Scripts\\activate

```



Install the application dependencies:



```cmd

pip install -r app\\requirements.txt

```



The Flask application can then be started according to the application configuration.



---



## Docker



The application is containerized using Docker.



Build the application image:



```cmd

docker build -t enterprise-devops-platform ./app

```



The project also includes a custom Jenkins image:



```text

Dockerfile.jenkins

```



The Jenkins image includes tools used by the CI/CD environment:



* Python

* Node.js and npm

* Docker CLI

* kubectl

* Trivy

* pytest



---



## Kubernetes



The application runs in the Kubernetes namespace:



```text

enterprise-devops

```



The environment includes the Flask application and PostgreSQL.



Check the workloads:



```cmd

kubectl get pods -n enterprise-devops

```



A healthy environment contains the application replicas and PostgreSQL pod in the `Running` state.



Kubernetes automatically restarts an application container when its main process terminates.



---



## CI/CD



### Jenkins



The repository contains a `Jenkinsfile` for CI/CD automation.



The pipeline supports application testing, code-quality analysis, security scanning, container workflows, and Kubernetes deployment.



The custom Jenkins environment is defined in:



```text

Dockerfile.jenkins

```



### Harness CI/CD



Harness CI/CD is integrated with the project for pipeline automation and GitHub-based workflows.



Harness configuration is stored under:



```text

.harness/

```



---



## Testing and Code Quality



Pytest is used for Python testing and test coverage.



SonarQube is used for code-quality analysis.



Trivy is included in the Jenkins environment for security scanning.



---



## Prometheus Monitoring



Prometheus collects Kubernetes metrics used to monitor the application workloads.



### Memory Usage



```promql

container_memory_working_set_bytes{namespace="enterprise-devops"}

```



### CPU Usage



```promql

rate(container_cpu_usage_seconds_total{namespace="enterprise-devops"}[5m])

```



### Pod Restarts



```promql

kube_pod_container_status_restarts_total{namespace="enterprise-devops"}

```



### Pod Status



```promql

kube_pod_status_phase{namespace="enterprise-devops", phase="Running"}

```



---



## Grafana Dashboard



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



This allows the dashboard configuration to be restored after a new Grafana installation.



---



## Grafana Persistence



Grafana persistent storage is enabled so its data survives pod restarts.



The configuration is stored in:



```text

grafana-smtp-values.yaml

```



The persistence configuration includes:



```yaml

persistence:

  enabled: true

  type: sts

  accessModes:

    - ReadWriteOnce

  size: 5Gi

```



---



## Grafana Alerting



The project includes the alert rule:



```text

Pod Restart Detected

```



The rule monitors:



```promql

kube_pod_container_status_restarts_total{namespace="enterprise-devops"}

```



The alert condition is triggered when a container restart count is greater than zero.



The exported alert configuration is stored in:



```text

grafana-alert-rules.yaml

```



---



## Email Notifications



Grafana SMTP is configured using Gmail SMTP:



```text

smtp.gmail.com:587

```



The SMTP password is not stored directly in the Git repository.



Grafana references the password using:



```text

$__env{GF_SMTP_PASSWORD}

```



The actual value is supplied through a Kubernetes Secret.



This separates sensitive credentials from version-controlled configuration.



---



## Alert Validation



The Grafana alerting workflow was tested by intentionally terminating the main process inside one application container:



```cmd

kubectl exec -n enterprise-devops <pod-name> -c enterprise-platform -- sh -c "kill 1"

```



Kubernetes restarted the container.



Prometheus detected the restart count.



Grafana detected the condition and triggered the configured alert.



The email notification was successfully delivered.



The validated workflow is:



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



## Configuration Recovery



Important monitoring configuration is stored in Git:



```text

enterprise-devops-monitoring-dashboard.json

grafana-alert-rules.yaml

grafana-smtp-values.yaml

```



A recovery test was performed by cloning the GitHub repository into a separate directory and verifying that the version-controlled files and Git history were successfully restored.



Sensitive Kubernetes Secret values are intentionally not stored in Git and must be recreated separately.



---



## Git Workflow



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

```



Application code, infrastructure configuration, CI/CD configuration, dashboards, and alert rules are version controlled.



---



## DevOps Practices Demonstrated



* Git-based source control

* Containerized application delivery

* Kubernetes orchestration

* PostgreSQL integration

* Jenkins CI/CD

* Harness CI/CD

* Automated testing

* SonarQube code-quality analysis

* Trivy security scanning

* Infrastructure as Code

* Prometheus monitoring

* Grafana dashboards

* Kubernetes workload monitoring

* Grafana alerting

* SMTP email notifications

* Persistent Grafana storage

* Secret separation from Git

* Configuration backup

* GitHub recovery testing



---



## Future Enhancements



* AWS EKS deployment

* AWS infrastructure provisioning with Terraform

* Kubernetes Ingress

* TLS/HTTPS

* CPU threshold alerts

* Memory threshold alerts

* Application-level metrics

* Centralized logging

* GitOps deployment

* Automated disaster recovery validation



---



## Author



Komlavi Gidi



DevOps Engineer | Cloud Engineer




