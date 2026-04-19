FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml .
RUN pip install --no-cache-dir .

COPY . .

# /app/data — persistent volume for SQLite DB + Pyrogram session
# Mount with: -v /path/on/host/data:/app/data
VOLUME ["/app/data"]

CMD ["python", "main.py"]
