// Jenkinsfile - исправленная версия
pipeline {
    agent any
    
    stages {
        stage('Checkout from GitHub') {
            steps {
                checkout scm
                echo ' Код получен из GitHub репозитория'
                sh 'ls -la'
            }
        }
        
        stage('Build Stage (Demo)') {
            steps {
                echo ' ЭТАП СБОРКИ DOCKER ОБРАЗА'
                echo 'В production среде выполняется:'
                echo 'docker build -t vk-faq-bot .'
                echo ''
                echo 'Для демонстрации показываем структуру проекта:'
                sh '''
                    echo "=== Файлы проекта ==="
                    ls -la
                    echo ""
                    echo "=== Dockerfile ==="
                    cat Dockerfile
                    echo ""
                    echo "=== Команда для сборки ==="
                    echo "docker build -t vk-faq-bot ."
                '''
            }
        }
        
        stage('Test Stage (Demo)') {
            steps {
                echo ' ЭТАП ТЕСТИРОВАНИЯ'
                echo 'В production среде выполняется:'
                echo 'docker run --rm vk-faq-bot'
                echo ''
                sh '''
                    echo "=== requirements.txt ==="
                    cat requirements.txt
                '''
            }
        }
        
        stage('Deploy Stage (Demo)') {
            steps {
                echo ' ЭТАП ДЕПЛОЯ'
                echo 'В production среде контейнер развертывается на сервере'
                echo ''
                echo 'Архитектура CI/CD:'
                echo '1. GitHub → 2. Jenkins → 3. Docker → 4. Production'
            }
        }
    }
    
    post {
        success {
            echo ' CI/CD PIPELINE НАСТРОЕН УСПЕШНО!'
            echo 'GitHub: https://github.com/Khagich/vk-faq-bot'
            echo 'Jenkins: http://localhost:8080'
            echo ''
            echo 'Для локальной сборки выполните:'
            echo 'docker build -t vk-faq-bot .'
            echo 'docker run --rm vk-faq-bot'
        }
    }
}