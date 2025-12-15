// Jenkinsfile
pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo " Репозиторий загружен"
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    docker.build("vk-faq-bot:${env.BUILD_NUMBER}")
                }
            }
        }
        
        stage('Test Run') {
            steps {
                script {
                    docker.image("vk-faq-bot:${env.BUILD_NUMBER}").run(
                        '-d --name test-bot --rm -v /tmp/data:/app/data'
                    )
                    sleep 5
                    sh 'docker logs test-bot'
                    sh 'docker stop test-bot'
                }
            }
        }
        
        stage('Deploy') {
            steps {
                sh '''
                    docker stop vk-faq-bot-prod || true
                    docker rm vk-faq-bot-prod || true
                    docker run -d \
                        --name vk-faq-bot-prod \
                        -v ${PWD}/data:/app/data \
                        --restart unless-stopped \
                        vk-faq-bot:${BUILD_NUMBER}
                '''
            }
        }
    }
    
    post {
        success {
            echo " Pipeline успешно завершен!"
        }
    }
}