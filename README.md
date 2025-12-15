# VK WorkSpace FAQ Bot (Docker версия)

Чат-бот с улучшенным поиском ответов на часто задаваемые вопросы.

##  Быстрый старт

### 1. Клонирование и настройка
```bash
# Создайте папку проекта
mkdir vk-faq-bot
cd vk-faq-bot

# Поместите файлы проекта:
# - Dockerfile
# - docker-compose.yml
# - requirements.txt
# - .env.example
# - src/bot.py
### Установка Jenkins:
```powershell
# Запустите скрипт установки
.\scripts\setup-jenkins.ps1

# Или вручную
docker-compose -f docker-compose.jenkins.yml up -d"# vk-faq-bot" 
