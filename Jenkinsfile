pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Verify Environment') {
            steps {
                sh '''
                    echo "Jenkins worker information"
                    whoami
                    pwd
                    java -version
                '''
            }
        }

        stage('Verify Project Files') {
            steps {
                sh '''
                    ls -la
                    ls -la app
                '''
            }
        }
    }

    post {
        success {
            echo 'Pipeline completed successfully!'
        }

        failure {
            echo 'Pipeline failed!'
        }
    }
}