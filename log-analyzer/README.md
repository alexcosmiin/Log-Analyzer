# 📎 Log Analyzer

Un instrument simplu pentru analiza și clasificarea fișierelor de log.

---

## 📁 Structură Proiect

```
log-analyzer/
├── logs/                 # Fișiere de log (ex: pentru rulare manuală)
├── output/               # Fișiere JSON generate (ex: rulare manuală)
├── reports/              # Rapoarte HTML ale testelor
├── tests/                # Suită de teste automate
│   ├── common_functions.py
│   ├── dummy_category/     
│   ├── framework_tests/    
│   ├── integration_tests/  
│   └── software_tests/     
├── src/                  # Codul sursă principal
│   ├── __init__.py
│   ├── parser.py           
│   ├── classifier.py       
│   └── main.py             
├── .dockerignore         
├── .gitignore            
├── Dockerfile            
├── docker-compose.yml    
├── requirements.txt      
├── run_tests.py          
└── README.md             
```

---

## ✅ Prerechizite

* [x] Docker
* [x] Docker Compose
* [x] Python 3.11+ (pentru rulare locală și dezvoltare)

---

## ⚙️ Configurare Inițială

```bash
git clone <URL_REPOSITORY>
cd log-analyzer
```

### Creare mediu virtual și instalare dependințe

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 🐳 Instrucțiuni Docker

### Construire imagine Docker

```bash
docker build -t log-analyzer .
```

---

### Rulare aplicație cu Docker Compose (metoda recomandată)

1. Asigură-te că ai un fișier `logs/log.txt` în rădăcina proiectului.
2. Rulează:

```bash
docker-compose up app
```

Pentru rulare în background și reconstruirea imaginii:

```bash
docker-compose up -d --build app
```

> 📄 Output-ul va apărea în `output/output.json`.

---

### Rulare teste cu Docker Compose

```bash
docker-compose up test
```

Pentru reconstruirea imaginii de test:

```bash
docker-compose up --build test
```

> 📄 Rapoartele HTML vor fi generate în `reports/`.

---

### Rulare manuală aplicație (cu `docker run`)

```bash
mkdir -p logs output  # dacă nu există deja

docker run --rm \
  -v "$(pwd)/logs:/app/logs_mounted" \
  -v "$(pwd)/output:/app/output_mounted" \
  log-analyzer \
  python3 -m src.main \
    --log-file /app/logs_mounted/log.txt \
    --output-file /app/output_mounted/output.json
```

> Înlocuiește `log.txt` cu numele dorit pentru fișierul de log.

---

## 🧪 Rulare Teste Local (fără Docker)

```bash
source venv/bin/activate  # dacă nu este deja activ
python3 run_tests.py
```

### Alte comenzi utile:

Rularea unei anumite categorii de teste:

```bash
python3 run_tests.py --category software
```

Filtrare teste după nume:

```bash
python3 run_tests.py --filter filter_by_name
```

---

## 📋 Structură Output JSON

Aplicația generează un fișier JSON (ex: `output/output.json`) cu structura:

```json
{
  "INFO": {
    "count": 1,
    "messages": ["Info update"]
  },
  "ERROR": {
    "count": 1,
    "messages": ["error occurred"]
  },
  "UNKNOWN": {
    "count": 1,
    "messages": ["O linie de log care nu s-a potrivit cu niciun tip cunoscut."]
  },
  "metadata": {
    "total_lines_processed": 3,
    "log_file_path": "/app/logs_mounted/log.txt",
    "analysis_timestamp": "YYYY-MM-DDTHH:MM:SS.ffffffZ"
  }
}
```

* Fiecare nivel de log (`INFO`, `ERROR`, `CRITICAL`, `WARNING`, `DEBUG`, `FAILED`, `UNKNOWN`) conține:

  * `count`: numărul de mesaje.
  * `messages`: lista completă a liniilor de log.
* `metadata` oferă detalii despre fișierul procesat și momentul analizei.

---

## 🧰 Mediu Testat

* ✅ **Ubuntu 24.04 LTS**
* ⚠️ Alte sisteme de operare nu au fost testate explicit.
