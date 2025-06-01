# 🧾 Log Analyzer

Un instrument simplu pentru analiza și clasificarea fișierelor de log, cu rulare automată în Docker și un framework propriu de testare.

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

* Docker
* Docker Compose
* Python 3.11+ (pentru rularea testelor, nu pentru aplicația în sine)

---

## ⚙️ Instalare și Configurare Rapidă

### 1. Clonare proiect

```bash
git clone https://github.com/alexcosmiin/Log-Analyzer.git
cd log-analyzer
```

### 2. Acordare drepturi pe director (dacă este necesar)

```bash
sudo chown -R $USER:$USER .
```

### 3. Acordare drepturi de execuție pentru scriptul de start

```bash
chmod +x start_script.sh
```

### 4. Rulare aplicație prin scriptul automat

```bash
./start_script.sh
```

Acest script:

* Creează directorul `output/` dacă nu există.
* Construiește imaginea Docker `log-analyzer`.
* Rulează containerul și montează `output/` în container.
* Verifică și afișează conținutul fișierului `output/output.json`.

---

## 🐳 Comenzi Docker (alternative manuale)

### Construire imagine:

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

## 🧪 Rulare Teste

### Rulare completă (local, cu Python):

```bash
python3 run_tests.py
```

### Rulare pe categorii:

```bash
python3 run_tests.py --category software
```

### Filtrare după nume:

```bash
python3 run_tests.py --filter test_log_parser
```

> Nu este necesară activarea unui mediu virtual (`venv`).

---

## 📄 Structură Output JSON

Fișierul `output/output.json` va arăta astfel:

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

* **Smoke tests** – verificări de bază
* **Software tests** – validarea logicii `parser` și `classifier`
* **Integration tests** – testarea orchestrării în Docker
* **Framework tests** – validarea frameworkului de testare
* **Dummy** – cazuri minimale de test

> Rapoartele de testare se salvează în `reports/` în format HTML.

---

## 💻 Platformă de Testare

🛑 **IMPORTANT:** Aplicația a fost testată **exclusiv pe Ubuntu 24.04 LTS**.
Funcționarea pe alte sisteme (Windows, macOS) **nu a fost verificată** și **nu este garantată**.

---

## 🌐 Cod sursă

👉 [https://github.com/alexcosmiin/Log-Analyzer](https://github.com/alexcosmiin/Log-Analyzer)
