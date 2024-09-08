# Usa una imagen base de Python
FROM python:3.11-slim

# Instala Envoy
RUN apt-get update && apt-get install -y curl && \
    curl -sL https://getenvoy.io/gpg | apt-key add - && \
    echo "deb [arch=amd64] https://storage.googleapis.com/getenvoy-deb stable main" | tee /etc/apt/sources.list.d/getenvoy.list && \
    apt-get update && apt-get install -y envoy

# Copia tu archivo de configuración de Envoy
COPY envoy.yaml /etc/envoy/envoy.yaml

# Copia el código de tu aplicación
COPY . /app
WORKDIR /app

# Instala las dependencias de Python
RUN pip install -r requirements.txt

# Expone el puerto en el que tu servidor escucha
EXPOSE 50051

# Comando para ejecutar Envoy y tu aplicación
CMD ["sh", "-c", "envoy -c /etc/envoy/envoy.yaml & python server.py"]
