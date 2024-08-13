# Usar una imagen base de Python
FROM python:3.11.8-slim

# Establecer el directorio de trabajo en el contenedor
WORKDIR /app

# Copiar el archivo de requerimientos
COPY requirements.txt .

# Actualizar pip y instalar las dependencias
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar el resto de la aplicación al contenedor
COPY . .

# Exponer el puerto en el que la aplicación Flask correrá
EXPOSE 5000

# Configurar la variable de entorno para indicar el archivo principal de Flask
ENV FLASK_APP=app.py

# Comando para ejecutar la aplicación Flask
CMD ["flask", "run", "--host=0.0.0.0"]
