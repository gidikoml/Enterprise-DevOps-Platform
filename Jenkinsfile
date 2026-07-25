pipeline {
    agent any

    environment {
        IMAGE_NAME = "amenvi/enterprise-devops-platform"
        IMAGE_TAG = "${BUILD_NUMBER}"
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
                    python3 -m pip install --no-cache-dir -r app/requirements.txt
                    python3 -m pytest app/tests -v
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
                              -Dsonar.python.version=3.11
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
                          -t ${IMAGE_NAME}:latest \
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

        stage('Docker Hub Login') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'dockerhub-credentials',
                        usernameVariable: 'DOCKERHUB_USER',
                        passwordVariable: 'DOCKERHUB_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$DOCKERHUB_TOKEN" | \
                        docker login \
                          -u "$DOCKERHUB_USER" \
                          --password-stdin
                    '''
                }
            }
        }

        stage('Push Docker Image') {
            steps {
                sh '''
                    docker push ${IMAGE_NAME}:${IMAGE_TAG}
                    docker push ${IMAGE_NAME}:latest
                '''
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                sh '''
                    kubectl set image \
                      deployment/enterprise-platform \
                      enterprise-platform=${IMAGE_NAME}:${IMAGE_TAG} \
                      -n enterprise-devops

                    kubectl rollout status \
                      deployment/enterprise-platform \
                      -n enterprise-devops \
                      --timeout=120s
                '''
            }
        }

        stage('Verify Deployment') {
            steps {
                sh '''
                    kubectl get pods -n enterprise-devops

                    kubectl get deployment \
                      enterprise-platform \
                      -n enterprise-devops
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    kubectl port-forward \
                      service/enterprise-platform-service \
                      5050:5000 \
                      -n enterprise-devops \
                      > /tmp/port-forward.log 2>&1 &

                    PF_PID=$!

                    sleep 5

                    curl -f http://127.0.0.1:5050/login

                    kill $PF_PID || true
                '''
            }
        }
    }

    post {

        success {
            echo "Pipeline completed successfully!"
            echo "Image deployed: ${IMAGE_NAME}:${IMAGE_TAG}"
        }

        failure {
            echo "Pipeline failed."
        }

        always {
            sh '''
                docker logout || true
            '''
        }
    }
}