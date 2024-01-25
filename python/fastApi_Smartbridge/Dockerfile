# Используйте базовый образ Python
FROM python:3.11

# Установите рабочую директорию в /app
WORKDIR /app

# Скопируйте файлы requirements.txt в текущую директорию образа
COPY requirements.txt .

# Установите зависимости
RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org --upgrade pip && \
    pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt

# Скопируйте остальные файлы в текущую директорию образа
COPY . .

# Команда для запуска приложения с использованием Gunicorn
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:14931", "main:app"]

