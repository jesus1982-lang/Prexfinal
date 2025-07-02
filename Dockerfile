# Dockerfile
FROM python:3.12-slim

# Crear directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

# Comando por defecto (redundante si se usa en docker-compose)
CMD ["uvicorn", "analizador_prex_api:app", "--host", "0.0.0.0", "--port", "8000"]

