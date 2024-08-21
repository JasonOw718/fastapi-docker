FROM python:3.11-slim

WORKDIR /app

# Copy and install dependencies first
COPY requirements.txt .

RUN apt-get update
RUN apt install -y libgl1-mesa-glx

RUN pip install --upgrade pip && \
    pip install --no-cache-dir --default-timeout=10000 -r requirements.txt

# Then copy the rest of the application code
COPY . .

EXPOSE 80
ENV PYTHONUNBUFFERED=1

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
