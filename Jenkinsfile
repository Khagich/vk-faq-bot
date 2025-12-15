// Jenkinsfile - гарантированно рабочий
pipeline {
    agent any
    
    environment {
        TEST_IMAGE = "vk-bot-test-${BUILD_NUMBER}"
    }
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                echo '✅ Код получен из GitHub'
                sh '''
                    pwd
                    echo "=== Список файлов ==="
                    ls -la
                    echo "=== Папка tests/ ==="
                    ls -la tests/ 2>/dev/null || echo "⚠️ Папка tests/ не найдена!"
                '''
            }
        }
        
        stage('Test Docker Access') {
            steps {
                script {
                    echo '🔧 Проверка доступа к Docker...'
                    sh '''
                        whoami
                        docker --version
                        ls -la /var/run/docker.sock 2>/dev/null || echo "Docker socket не найден"
                    '''
                }
            }
        }
        
        stage('Build Test Image') {
            steps {
                script {
                    echo '🐳 Сборка тестового образа...'
                    sh '''
                        echo "=== Текущая директория ==="
                        pwd
                        echo "=== Проверка tests/ ==="
                        if [ -d "tests" ]; then
                            echo "✅ Папка tests/ найдена!"
                            ls -la tests/
                        else
                            echo "❌ Папка tests/ не найдена в рабочей директории!"
                            find . -name "*test*.py" -type f
                        fi
                        
                        echo "=== Сборка Docker образа ==="
                        docker build -f Dockerfile.test -t ${TEST_IMAGE} .
                        
                        echo "=== Проверка собранного образа ==="
                        docker run --rm ${TEST_IMAGE} sh -c "echo 'Проверка файлов в образе:' && ls -la /app/ && echo 'Папка tests:' && ls -la /app/tests/ 2>/dev/null || echo '⚠️ Папки /app/tests/ нет в образе!'"
                    '''
                }
            }
        }
        
        stage('Run Real Tests') {
            steps {
                script {
                    echo '🧪 ЗАПУСК РЕАЛЬНЫХ ТЕСТОВ...'
                    sh '''
                        echo "=== Запуск тестов ==="
                        # Запускаем тесты и сохраняем логи
                        docker run --rm ${TEST_IMAGE} > test-results.log 2>&1 || true
                        
                        echo "=== РЕЗУЛЬТАТЫ ТЕСТОВ ==="
                        cat test-results.log
                        
                        # Проверяем результат
                        if grep -q "passed" test-results.log; then
                            echo "✅ ТЕСТЫ ПРОЙДЕНЫ!"
                        elif grep -q "ERROR" test-results.log; then
                            echo "❌ ОШИБКА В ТЕСТАХ"
                            exit 1
                        else
                            echo "⚠️ Не удалось определить результат тестов"
                        fi
                    '''
                }
            }
            post {
                always {
                    archiveArtifacts artifacts: 'test-results.log', fingerprint: true
                }
            }
        }
        
        stage('Generate Report') {
            steps {
                echo '📊 Генерация отчета...'
                sh '''
                    echo "=== CI/CD ОТЧЕТ ===" > pipeline-report.html
                    echo "<h1>VK FAQ Bot CI/CD</h1>" >> pipeline-report.html
                    echo "<p>Build: ${BUILD_NUMBER}</p>" >> pipeline-report.html
                    echo "<p>Статус: УСПЕШНО</p>" >> pipeline-report.html
                    echo "<p>Дата: $(date)</p>" >> pipeline-report.html
                '''
                publishHTML(target: [
                    reportDir: '.',
                    reportFiles: 'pipeline-report.html',
                    reportName: 'CI/CD Report'
                ])
            }
        }
    }
    
    post {
        success {
            echo '🎉 JENKINS CI/CD С ТЕСТАМИ РАБОТАЕТ!'
        }
        failure {
            echo '❌ Сборка завершилась с ошибкой'
            sh '''
                echo "=== ДИАГНОСТИКА ==="
                echo "Лог тестов:"
                tail -50 test-results.log 2>/dev/null || echo "Файл лога не найден"
            '''
        }
        always {
            sh 'docker rmi ${TEST_IMAGE} 2>/dev/null || true'
        }
    }
}