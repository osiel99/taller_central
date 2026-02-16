# Imagen base oficial de Python
FROM python:3.11-slim

# Evitar que Python genere .pyc y que haga buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Crear directorio de trabajo dentro del contenedor
WORKDIR /app

# Instalar dependencias del sistema (si luego necesitas más, se agregan aquí)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements y luego instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el resto del código
COPY . /app

# Exponer el puerto donde corre FastAPI (por defecto 8000)
EXPOSE 8000

# Comando por defecto: levantar la app con uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
