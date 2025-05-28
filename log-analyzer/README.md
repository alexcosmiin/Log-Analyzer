# 🧾 Log Analyzer

Un instrument simplu pentru analiza și clasificarea fișierelor de log.

---

## 📁 Structură Proiect

```
log-analyzer/
├── app/                   # Logica principală a aplicației (parsare + clasificare)
│   ├── __init__.py
│   ├── log_classifier.py
│   └── log_parser.py
├── src/                   # Scripturi auxiliare
│   ├── main.py            # Punct alternativ de pornire
│   ├── classifier.py
│   └── parser.py
├── test_framework/        # Framework propriu de testare
│   ├── core/              # TestCase, TestStep, TestSuite
│   ├── reporting/         # HTML și consola
│   ├── runners/           # Executori de teste
│   └── utils/             # Assertions, logger, decorators
├── tests/                 # Suita de teste automatizate
│   ├── common_functions.py
│   ├── dummy/
│   ├── framework/
│   ├── integration/
│   ├── smoke/
│   └── software/
├── logs/                  # Fișiere brute de log (ex: log.txt)
├── output/                # Output JSON generat de aplicație
├── reports/               # Rapoarte HTML de testare
├── run_tests.py           # Script pentru rularea testelor
├── start_script.sh        # Script pentru rulare automată
├── requirements.txt       # Dependențe Python
├── Dockerfile             # Definirea imaginii Docker
├── docker-compose.yml     # Configurare multi-container (opțional)
├── pytest.ini             # Configurații Pytest
└── README.md              # Acest fișier
```

---

## ✅ Prerechizite

* Python 3.11+
* Docker
* Docker Compose

---

## ⚙️ Instalare și Configurare Rapidă

```bash
git clone https://github.com/alexcosmiin/Log-Analyzer.git
cd Log-Analyzer
```

### Pentru rulare locală:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Pentru rulare completă cu Docker:

```bash
chmod +x start_script.sh
./start_script.sh
```

Acest script:

* construiește imaginea Docker
* pornește containerul
* extrage fișierul `output.json`
* îl salvează în `output/`

---

## 🐳 Alternativ: Comenzi Docker Manuale

### Build manual imagine Docker:

```bash
docker build -t log-analyzer .
```

### Rulare aplicație:

```bash
docker-compose up app
```

### Rulare aplicație în background:

```bash
docker-compose up -d --build app
```

### Rulare teste:

```bash
docker-compose up test
```

> Rapoartele HTML se vor genera în `reports/`

---

## 🧪 Rulare Teste (local)

Activare mediu virtual și rulare teste:

```bash
source venv/bin/activate
python3 run_tests.py
```

### Opțiuni:

* Rulare categorie:

  ```bash
  python3 run_tests.py --category software
  ```
* Filtrare după nume:

  ```bash
  python3 run_tests.py --filter test_log_parser
  ```

---

## 📄 Structură Output JSON

Fișierul `output/output.json` are forma:

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

---

## 🧪 Categorii de Teste

Testele sunt împărțite în:

* **Smoke tests** – verificări de bază
* **Software tests** – validarea logicii `parser` și `classifier`
* **Integration tests** – testarea orchestrării în medii reale (ex: Docker)
* **Framework tests** – validarea propriului sistem de testare
* **Dummy** – cazuri simple pentru validare funcțională

Rapoartele de testare sunt salvate în `reports/` în format HTML.

---

## 💻 Platformă de Testare

🛑 **IMPORTANT:** Acest proiect a fost testat **exclusiv** pe **Ubuntu 24.04 LTS**.
Funcționarea pe alte sisteme de operare (Windows, MacOS) **nu este garantată** și nu a fost verificată.

---

## 🌐 Cod sursă

Codul complet este disponibil pe GitHub:

👉 [https://github.com/alexcosmiin/Log-Analyzer](https://github.com/alexcosmiin/Log-Analyzer)
