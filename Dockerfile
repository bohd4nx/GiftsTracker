FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Persistent data: SQLite DB + Pyrogram session
VOLUME ["/app/data"]

CMD ["python", "main.py"]
