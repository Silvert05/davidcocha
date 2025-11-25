# Imagen base oficial de Python
FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Copiar dependencias y código
COPY . /app

# Instalar Flask
RUN pip install -r requirements.txt

# Comando por defecto
CMD ["python", "app.py"]