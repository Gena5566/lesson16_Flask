# Образ Ubuntu
FROM ubuntu:latest

# Устанавливаем необходимые пакеты
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Создаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip3 install --no-cache-dir -r requirements.txt

# Копируем все содержимое текущей директории внутрь контейнера
COPY . /app/

# Определяем переменные окружения
ENV PYTHONUNBUFFERED 1

# Открываем порт, на котором будет работать приложение
EXPOSE 5000

# Запускаем команду при запуске контейнера
CMD ["python3", "routes_with_orm.py"]
