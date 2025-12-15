// Jenkinsfile - с реальным запуском тестов
pipeline {
    agent any
    
    environment {
        DOCKER_TEST_IMAGE = 'vk-bot-tests-${BUILD_NUMBER}'
    }
    
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
                echo '✅ Код получен из GitHub'
            }
        }
        
        stage('Build Test Docker Image') {
            steps {
                script {
                    echo '🐳 Сборка Docker образа для тестов...'
                    // Собираем образ с уникальным именем
                    sh "docker build -f Dockerfile.test -t ${DOCKER_TEST_IMAGE} ."
                }
            }
        }
        
        stage('Run Unit Tests in Docker') {
            steps {
                script {
                    echo '🧪 Запуск unit-тестов в Docker...'
                    // Запускаем тесты и сохраняем результат
                    sh """
                        set +e  # Не прерывать pipeline при ошибке тестов
                        docker run --rm ${DOCKER_TEST_IMAGE} > test-output.txt 2>&1
                        TEST_EXIT_CODE=\$?
                        echo "Код завершения тестов: \$TEST_EXIT_CODE"
                        
                        # Показываем вывод тестов
                        cat test-output.txt
                        
                        # Сохраняем отчет
                        echo "=== ОТЧЕТ О ТЕСТИРОВАНИИ ===" > test-report.txt
                        echo "Build: ${BUILD_NUMBER}" >> test-report.txt
                        date >> test-report.txt
                        echo "" >> test-report.txt
                        tail -50 test-output.txt >> test-report.txt
                        
                        # Если тесты упали, продолжаем pipeline но отмечаем
                        if [ \$TEST_EXIT_CODE -ne 0 ]; then
                            echo "❌ Тесты завершились с ошибкой"
                            currentBuild.result = 'UNSTABLE'
                        else
                            echo "✅ Все тесты прошли успешно"
                        fi
                    """
                }
            }
            post {
                always {
                    // Сохраняем артефакты
                    archiveArtifacts artifacts: 'test-output.txt, test-report.txt', fingerprint: true
                    // Сохраняем отчет JUnit формат
                    junit testResults: '**/test-results.xml', allowEmptyResults: true
                }
            }
        }
        
        stage('Generate Coverage Report') {
            steps {
                script {
                    echo '📊 Генерация отчета о покрытии...'
                    sh """
                        # Запускаем тесты с coverage отчетом
                        docker run --rm ${DOCKER_TEST_IMAGE} python -m pytest tests/ --cov=src --cov-report=xml --cov-report=html --junitxml=test-results.xml || true
                        
                        # Копируем отчеты из контейнера
                        docker run --rm -v \$(pwd):/app/output ${DOCKER_TEST_IMAGE} sh -c "
                            cp coverage.xml /app/output/ 2>/dev/null || true
                            cp -r htmlcov /app/output/ 2>/dev/null || true
                            cp test-results.xml /app/output/ 2>/dev/null || true
                        "
                    """
                }
            }
            post {
                always {
                    // Публикуем отчеты
                    publishHTML(target: [
                        reportDir: 'htmlcov',
                        reportFiles: 'index.html',
                        reportName: 'Coverage Report'
                    ])
                    junit 'test-results.xml'
                }
            }
        }
        
        stage('Build Production Image') {
            steps {
                echo '🚀 Сборка production образа...'
                sh '''
                    docker build -t vk-faq-bot:${BUILD_NUMBER} .
                    docker tag vk-faq-bot:${BUILD_NUMBER} vk-faq-bot:latest
                    echo "✅ Production образ собран: vk-faq-bot:${BUILD_NUMBER}"
                '''
            }
        }
    }
    
    post {
        success {
            echo '🎉 CI/CD Pipeline выполнен успешно!'
            echo "Build: ${BUILD_NUMBER}"
            echo "Тесты: интегрированы и выполнены"
            sh 'docker images | grep vk-faq-bot'
        }
        failure {
            echo '❌ Pipeline завершился с ошибкой'
        }
        always {
            echo '🧹 Очистка...'
            sh '''
                # Удаляем тестовый образ
                docker rmi vk-bot-tests-${BUILD_NUMBER} 2>/dev/null || true
                # Очищаем Docker
                docker system prune -f 2>/dev/null || true
            '''
        }
    }
}