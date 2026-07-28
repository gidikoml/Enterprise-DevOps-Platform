pipeline {
    agent any

    environment {
        AWS_REGION   = "us-east-1"
        AWS_ACCOUNT  = "519747128244"
        EKS_CLUSTER  = "enterprise-devops-cluster"

        ECR_REGISTRY = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_NAME   = "enterprise-devops-platform"
        IMAGE_TAG    = "${BUILD_NUMBER}"

        ECR_IMAGE    = "${ECR_REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}"
        ECR_LATEST   = "${ECR_REGISTRY}/${IMAGE_NAME}:latest"
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Pytest') {
            steps {
                sh '''
                    rm -rf .jenkins-venv

                    python3 -m venv .jenkins-venv

                    .jenkins-venv/bin/python -m pip install --upgrade pip

                    .jenkins-venv/bin/python -m pip install \
                      -r app/requirements.txt

                    .jenkins-venv/bin/python -m pytest \
                      app/tests \
                      -v \
                      --cov=app \
                      --cov-report=xml:coverage.xml
                '''
            }
        }

        stage('SonarQube Analysis') {
            steps {
                script {
                    def scannerHome = tool 'SonarScanner'

                    withSonarQubeEnv('SonarQube') {
                        sh """
                            ${scannerHome}/bin/sonar-scanner \
                              -Dsonar.projectKey=enterprise-devops-platform \
                              -Dsonar.projectName=Enterprise-DevOps-Platform \
                              -Dsonar.sources=app \
                              -Dsonar.sourceEncoding=UTF-8 \
                              -Dsonar.python.version=3.11 \
                              -Dsonar.python.coverage.reportPaths=coverage.xml
                        """
                    }
                }
            }
        }

        stage('Quality Gate') {
            steps {
                timeout(time: 5, unit: 'MINUTES') {
                    waitForQualityGate abortPipeline: true
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('app') {
                    sh '''
                        docker build \
                          -t ${IMAGE_NAME}:${IMAGE_TAG} \
                          .
                    '''
                }
            }
        }

        stage('Trivy Security Scan') {
            steps {
                sh '''
                    trivy image \
                      --severity HIGH,CRITICAL \
                      --ignore-unfixed \
                      --scanners vuln \
                      --exit-code 1 \
                      ${IMAGE_NAME}:${IMAGE_TAG}
                '''
            }
        }

        stage('Configure AWS / EKS') {
            steps {
                sh '''
                    aws sts get-caller-identity

                    aws eks update-kubeconfig \
                      --region ${AWS_REGION} \
                      --name ${EKS_CLUSTER}

                    kubectl get nodes
                '''
            }
        }

        stage('ECR Login') {
            steps {
                sh '''
                    aws ecr get-login-password \
                      --region ${AWS_REGION} \
                      | docker login \
                          --username AWS \
                          --password-stdin ${ECR_REGISTRY}
                '''
            }
        }

        stage('Push Image to ECR') {
            steps {
                sh '''
                    docker tag \
                      ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${ECR_IMAGE}

                    docker tag \
                      ${IMAGE_NAME}:${IMAGE_TAG} \
                      ${ECR_LATEST}

                    docker push ${ECR_IMAGE}
                    docker push ${ECR_LATEST}
                '''
            }
        }

        stage('Deploy DEV') {
            steps {
                sh '''
                    kubectl set image \
                      deployment/enterprise-platform \
                      enterprise-platform=${ECR_IMAGE} \
                      -n enterprise-dev

                    kubectl rollout status \
                      deployment/enterprise-platform \
                      -n enterprise-dev \
                      --timeout=180s
                '''
            }
        }

        stage('Test DEV') {
            steps {
                sh '''
                    kubectl get pods -n enterprise-dev

                    kubectl port-forward \
                      service/enterprise-platform-service \
                      5051:80 \
                      -n enterprise-dev \
                      > /tmp/dev-port-forward.log 2>&1 &

                    PF_PID=$!

                    sleep 5

                    curl -f http://127.0.0.1:5051/login

                    kill $PF_PID || true
                '''
            }
        }

        stage('Deploy STAGING') {
            steps {
                sh '''
                    kubectl set image \
                      deployment/enterprise-platform \
                      enterprise-platform=${ECR_IMAGE} \
                      -n enterprise-staging

                    kubectl rollout status \
                      deployment/enterprise-platform \
                      -n enterprise-staging \
                      --timeout=180s
                '''
            }
        }

        stage('Test STAGING') {
            steps {
                sh '''
                    kubectl get pods -n enterprise-staging

                    kubectl port-forward \
                      service/enterprise-platform-service \
                      5052:80 \
                      -n enterprise-staging \
                      > /tmp/staging-port-forward.log 2>&1 &

                    PF_PID=$!

                    sleep 5

                    curl -f http://127.0.0.1:5052/login

                    kill $PF_PID || true
                '''
            }
        }

        stage('Approve PROD') {
            steps {
                timeout(time: 15, unit: 'MINUTES') {
                    input(
                        message: 'Deploy this build to PRODUCTION?',
                        ok: 'Deploy'
                    )
                }
            }
        }

        stage('Deploy PROD') {
            steps {
                sh '''
                    kubectl set image \
                      deployment/enterprise-platform \
                      enterprise-platform=${ECR_IMAGE} \
                      -n enterprise-prod

                    kubectl rollout status \
                      deployment/enterprise-platform \
                      -n enterprise-prod \
                      --timeout=180s
                '''
            }
        }

        stage('Verify PROD') {
            steps {
                sh '''
                    kubectl get pods -n enterprise-prod

                    kubectl get deployment \
                      enterprise-platform \
                      -n enterprise-prod

                    kubectl get service \
                      enterprise-platform-service \
                      -n enterprise-prod
                '''
            }
        }

        stage('Smoke Test PROD') {
            steps {
                sh '''
                    PROD_URL=$(kubectl get svc \
                      enterprise-platform-service \
                      -n enterprise-prod \
                      -o jsonpath='{.status.loadBalancer.ingress[0].hostname}')

                    echo "Production URL: http://${PROD_URL}"

                    curl \
                      --retry 12 \
                      --retry-delay 10 \
                      --retry-connrefused \
                      -f \
                      http://${PROD_URL}/login
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
            echo "Image deployed: ${ECR_IMAGE}"
            echo "DEV -> STAGING -> PROD promotion completed."
        }

        failure {
            echo "Pipeline failed."
        }

        always {
            sh '''
                docker logout ${ECR_REGISTRY} || true
            '''
        }
    }
}