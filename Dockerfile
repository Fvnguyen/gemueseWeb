# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.8-slim

EXPOSE 8080
EXPOSE 80

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# API Keys
ENV EDAMAM_api="48df8510bddb6aeeb43853f947ec1f02"
ENV EDAMAM_app="6e9fd246"

ENV REDIS_TLS_URL="rediss://:p0b9c0fe31971bc1c4b62fd7296dae8f619fcb454ffdb06a2f1c1617045ea1656@ec2-52-51-25-108.eu-west-1.compute.amazonaws.com:10430"
ENV REDIS_URL="redis://:p0b9c0fe31971bc1c4b62fd7296dae8f619fcb454ffdb06a2f1c1617045ea1656@ec2-52-51-25-108.eu-west-1.compute.amazonaws.com:10429"

ENV SPOONACULAR_API="c4580f32420d491aa7cc0da3e49c5019"

# Install pip requirements
COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:80", "main:app"]
