Desigur, iată conținutul actualizat al fișierului README.md, formatat ca un bloc de cod:

Markdown

# Log Analyzer

Un instrument simplu pentru analiza și clasificarea fișierelor de log.

## Structură Proiect

log-analyzer/
├── logs/                 # Director pentru fișierele de log (ex: pentru rulare manuală)
├── output/               # Director pentru fișierele JSON de output (ex: pentru rulare manuală)
├── reports/              # Director pentru rapoartele HTML generate de teste
├── tests/                # Suita de teste automate
│   ├── common_functions.py # Funcții ajutătoare pentru teste
│   ├── dummy_category/     # Categorie de teste "dummy" pentru testarea framework-ului
│   ├── framework_tests/    # Teste pentru framework-ul de testare custom
│   ├── integration_tests/  # Teste de integrare (ex: rulare în Docker)
│   └── software_tests/     # Teste unitare pentru componentele software
├── src/                  # Codul sursă principal al aplicației
│   ├── init.py
│   ├── parser.py           # Modul pentru citirea și parsarea fișierelor de log
│   ├── classifier.py       # Modul pentru clasificarea liniilor de log
│   └── main.py             # Scriptul principal care orchestrează analiza
├── .dockerignore         # Specifică ce fișiere să fie ignorate la build-ul Docker
├── Dockerfile            # Instrucțiuni pentru construirea imaginii Docker a aplicației
├── docker-compose.yml    # Configurare pentru rularea serviciilor cu Docker Compose
├── requirements.txt      # Dependințele Python ale proiectului
├── run_tests.py          # Script pentru rularea suitei de teste și generarea rapoartelor
└── README.md             # Acest fișier (descrierea proiectului)


## Prerechizite

* Docker
* Docker Compose (pentru comenzile `docker-compose`)
* Python 3.11+ (pentru rulare locală și dezvoltare)

## Configurare Inițială

1.  **Clonare Repository (dacă este cazul):**
    ```bash
    git clone <URL_REPOSITORY>
    cd log-analyzer
    ```

2.  **Creare Mediu Virtual și Instalare Dependințe (pentru dezvoltare locală):**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```

## Instrucțiuni Docker

### Construire Imagine Docker

Pentru a construi imaginea Docker pentru aplicație (se construiește automat și la `docker-compose up --build`):
```bash
docker build -t log-analyzer .
Rulare Aplicație cu Docker Compose
Aceasta este metoda recomandată pentru a rula aplicația. Va folosi src/main.py cu căile default pentru log (/app/logs/log.txt) și output (/app/output/output.json) din container.
Fișierele locale logs/log.txt și output/output.json vor fi mapate în container.

Asigură-te că ai un fișier logs/log.txt în rădăcina proiectului. Poți folosi cel existent sau crea unul nou.
Rulează:
Bash

docker-compose up app
Sau pentru a rula în background și a reconstrui imaginea dacă s-au făcut modificări:
Bash

docker-compose up -d --build app
Output-ul va apărea în output/output.json în rădăcina proiectului.
Rulare Teste cu Docker Compose
Aceasta va rula scriptul run_tests.py într-un container dedicat.

Bash

docker-compose up test
Sau pentru a reconstrui imaginea de test dacă s-au făcut modificări (ex: la requirements.txt sau Dockerfile):

Bash

docker-compose up --build test
Rapoartele HTML ale testelor vor fi salvate în directorul reports/ din rădăcina proiectului.

Rulare Manuală Aplicație (direct cu docker run)
Pentru a rula aplicația direct, specificând volume pentru loguri și output:

Bash

# Asigură-te că directoarele ./logs și ./output există în rădăcina proiectului pe mașina gazdă
mkdir -p logs output

# Rulează containerul, mapând directoarele locale la cele din container
# și specificând opțional alte argumente pentru main.py
docker run --rm \
  -v "<span class="math-inline">\(pwd\)/logs\:/app/logs\_mounted" \\
\-v "</span>(pwd)/output:/app/output_mounted" \
  log-analyzer \
  python3 -m src.main --log-file /app/logs_mounted/log.txt --output-file /app/output_mounted/output.json
Poți schimba log.txt cu numele fișierului tău de log.

Rularea Testelor Local (fără Docker)
Activează mediul virtual (dacă nu este deja activ):
Bash

source venv/bin/activate
Rulează scriptul de teste:
Bash

python3 run_tests.py
Pentru a rula teste dintr-o anumită categorie (ex: software, integration, framework, dummy):
Bash

python3 run_tests.py --category software
Pentru a filtra testele după nume (ex: cele care conțin filter_by_name):
Bash

python3 run_tests.py --filter filter_by_name
Structură Output JSON
Aplicația generează un fișier JSON (default: output/output.json) care conține liniile de log clasificate și metadate. Structura este următoarea:

JSON

{
    "INFO": {
        "count": 1,
        "messages": [
            "Info update"
        ]
    },
    "ERROR": {
        "count": 1,
        "messages": [
            "error occurred"
        ]
    },
    "UNKNOWN": {
        "count": 1,
        "messages": [
            "O linie de log care nu s-a potrivit cu niciun tip cunoscut."
        ]
    },
    "metadata": {
        "total_lines_processed": 3,
        "log_file_path": "/app/logs_mounted/log.txt",
        "analysis_timestamp": "YYYY-MM-DDTHH:MM:SS.ffffffZ"
    }
}
Fiecare cheie de nivel de log (ex: INFO, ERROR, CRITICAL, WARNING, DEBUG, FAILED, UNKNOWN) va conține un obiect cu:
count: Numărul de mesaje de acel tip.
messages: O listă cu mesajele respective (liniile complete din log).
Cheia metadata conține informații despre procesul de analiză. Timestamp-ul este generat dinamic la fiecare rulare.
Mediu Testat
Acest proiect a fost dezvoltat și testat pe Ubuntu 24.04 LTS. Funcționalitatea pe alte sisteme de operare nu a fost verificată explicit.
