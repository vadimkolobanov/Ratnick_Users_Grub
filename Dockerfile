FROM python:3.12-alpine

COPY requirements.txt /app/
WORKDIR /app
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

WORKDIR /app
CMD ["python", "main.py"]
LABEL authors="Marlen"

