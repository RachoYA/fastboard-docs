FROM python:3.12-slim

WORKDIR /app

# Системные зависимости для сборки колёс некоторых пакетов
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# По умолчанию запускаем бота; индексатор переопределяет command в compose
CMD ["python", "scripts/telegram_bot.py"]
