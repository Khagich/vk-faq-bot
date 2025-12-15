FROM python:3.11-slim

# Рабочая директория
WORKDIR /app

# Устанавливаем системные зависимости (опционально, можно убрать)
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем папку src с ботом
COPY src/ ./src/

# Создаем папку для данных (внутри /app)
RUN mkdir -p /app/data

# Команда запуска - указываем правильный путь
CMD ["python", "-u", "src/bot.py"]