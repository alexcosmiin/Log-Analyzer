# Log Analyzer

Acest proiect oferă un sistem complet pentru analiza automată a fișierelor de log, folosind Python și Docker. Include parsare, clasificare, generare de rezultate și un framework personalizat de testare.

## 📁 Structura Proiectului

.
├── app/                     # Logica principală a aplicației pentru analiză
│   ├── log_classifier.py   # Clasificarea logurilor
│   └── log_parser.py       # Parsarea fișierelor de log
│
├── src/                    # Scripturi auxiliare sau versiuni experimentale
│   ├── main.py             # Punct alternativ de pornire
│   ├── classifier.py
│   └── parser.py
│
├── tests/                  # Teste unitare și de integrare
│   ├── smoke/              # Teste de tip smoke
│   ├── software/           # Teste pentru componente software
│   ├── integration/        # Teste de integrare
│   ├── framework/          # Exemple sau teste de structură
│   ├── common_functions.py # Funcții comune de testare (loguri, helperi)
│   └── __init__.py
│
├── test_framework/         # Framework propriu de testare
│   ├── core/               # Clase de bază: TestCase, TestStep, TestSuite
│   ├── reporting/          # Generatoare de rapoarte (HTML și consolă)
│   ├── runners/            # Executori de teste
│   └── utils/              # Utilitare: assertions, logger, decorators
│
├── logs/                   # Fișierele brute de intrare (ex: log.txt)
├── output/                 # Fișierele de ieșire generate de aplicație
├── reports/                # Rapoarte HTML ale testelor
├── start_script.sh         # Script pentru rularea containerului și extragerea rezultatelor
├── run_tests.py            # Script de rulare a testelor cu filtrare și categorii
├── Dockerfile              # Definirea imaginii Docker
├── docker-compose.yml      # (opțional) configurare multi-container
├── requirements.txt        # Lista de dependințe Python
├── README.md               # Documentație generală
├── pytest.ini              # Configurații pentru pytest (dacă e folosit)


## ⚙️ Cerințe

- Python 3.8+
- Docker
- Sistem de operare: Linux (testat pe Ubuntu)

## 🚀 Instalare și Rulare

1. Asigură-te că Docker este instalat și activ.
2. Clonează acest repository:
   git clone https://github.com/numele-tau/log-analyzer.git
   cd log-analyzer

Rularea completă a aplicației:
chmod +x start_script.sh
./start_script.sh
Scriptul va: construi imaginea Docker, porni containerul, extrage output.json din container în directorul output/.


## Testare
Framework-ul de testare permite rularea testelor filtrat pe categorii sau nume:
# Toate testele smoke
python3 run_tests.py --category smoke

# Teste software (unitare)
python3 run_tests.py --category software

# Teste de integrare
python3 run_tests.py --category integration

# Rulare după numele unui test
python3 run_tests.py --filter test_log_parser
Rezultatele sunt afișate în consolă și salvate într-un raport HTML interactiv.

## 🧪 Categorii de Teste
smoke/ – Teste simple de validare a intrărilor

software/ – Teste unitare pentru parser și classifier

integration/ – Teste end-to-end pe întreg sistemul

## 🧰 Tehnologii utilizate
# Python 3.x
# Docker
# Bash
# HTML (raport testare)
# Framework personalizat pentru testare bazat pe unittest
