FROM debian:11-slim

ENV DEBIAN_FRONTEND=noninteractive
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV DJANGO_SETTINGS_MODULE=bakery_pos_project.settings

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-dev \
    python3-venv \
    nginx \
    supervisor \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Actualizar pip e instalar herramientas
RUN pip3 install --upgrade pip setuptools wheel

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copiar el proyecto
COPY . .

# Recopilar archivos estáticos
RUN python3 manage.py collectstatic --noinput

# Exponer puerto
EXPOSE 8000

# Comando para iniciar la aplicación
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "bakery_pos_project.wsgi"]