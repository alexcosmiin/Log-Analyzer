FROM python:3.9-slim

WORKDIR /app

# Copiem requirements.txt pentru a instala dependențele
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiem restul codului sursa
COPY . .

# Adaugă în Dockerfile
COPY logs/log.txt /app/logs/log.txt

# Cream directorul pentru output
RUN mkdir -p /app/output

# Comanda implicită - ruleaza aplicația
CMD ["python", "src/main.py"]