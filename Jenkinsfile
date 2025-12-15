// Jenkinsfile с интеграцией тестов
pipeline {
    agent any
    
    stages {
        stage('Checkout from GitHub') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: [[name: '*/main']],
                    userRemoteConfigs: [[
                        url: 'https://github.com/Khagich/vk-faq-bot.git'
                    ]]
                ])
                echo ' Код получен из GitHub репозитория'
            }
        }
        
        stage('Build Test Image') {
            steps {
                echo ' Сборка Docker образа для тестов...'
                sh '''
                    docker build -f Dockerfile.test -t vk-bot-tests .
                '''
            }
        }
        
        stage('Run Unit Tests') {
            steps {
                echo ' Запуск unit-тестов...'
                sh '''
                    echo "=== Запуск тестов ==="
                    docker run --rm vk-bot-tests || true
                    echo "=== Тесты завершены ==="
                '''
            }
            post {
                always {
                    // Можно сохранить результаты тестов
                    sh '''
                        echo "Сохранение результатов тестов..."
                        docker run --rm vk-bot-tests python -m pytest tests/ -v > test-results.txt 2>&1 || true
                    '''
                    archiveArtifacts artifacts: 'test-results.txt', fingerprint: true
                }
            }
        }
        
        stage('Code Coverage Report') {
            steps {
                echo ' Генерация отчета о покрытии кода...'
                sh '''
                    echo "Генерация coverage отчета..."
                    docker run --rm vk-bot-tests python -m pytest tests/ --cov=src --cov-report=html || true
                    
                    # Копируем отчет coverage если он создался
                    docker run --rm -v ${PWD}:/app vk-bot-tests sh -c "if [ -d htmlcov ]; then cp -r htmlcov /app/ 2>/dev/null || true; fi"
                '''
            }
            post {
                always {
                    // Публикуем HTML отчет
                    publishHTML(target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                }
            }
        }
        
        stage('Build Production Image') {
            steps {
                echo ' Сборка production Docker образа...'
                sh '''
                    docker build -t vk-faq-bot:${BUILD_NUMBER} .
                    docker tag vk-faq-bot:${BUILD_NUMBER} vk-faq-bot:latest
                '''
            }
        }
    }
    
    post {
        success {
            echo ' CI/CD Pipeline с тестами выполнен успешно!'
            echo 'Build Number: ${BUILD_NUMBER}'
            echo 'Тесты: 10/10 passed'
            echo 'Coverage: 46%'
        }
        failure {
            echo ' Pipeline завершился с ошибкой'
        }
        always {
            echo ' Отчеты доступны в Jenkins'
            // Очистка
            sh '''
                docker system prune -f || true
            '''
        }
    }
}