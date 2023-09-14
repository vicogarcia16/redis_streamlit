# Usa una imagen oficial de Python
FROM python:3.11

# Establece el directorio de trabajo en /app
WORKDIR /app

# Copia tus archivos app.py, Pipfile, Pipfile.lock y redis_db.py al contenedor
COPY app.py Pipfile Pipfile.lock redis_db.py ./

# Instala pipenv y luego las dependencias del proyecto
RUN pip install pipenv && pipenv install --deploy --ignore-pipfile

# Ejecuta la aplicación con pipenv
CMD ["pipenv", "run", "streamlit", "run", "app.py"]
