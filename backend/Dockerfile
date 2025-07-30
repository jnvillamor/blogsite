# Base Image
FROM python:3.11-alpine

WORKDIR /app/backend

COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

EXPOSE 8000

CMD [ "uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0" ]