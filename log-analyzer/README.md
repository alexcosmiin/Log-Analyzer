# Log Analyzer

Acest proiect oferă un sistem complet pentru analiza automată a fișierelor de log, folosind Python și Docker. Include parsare, clasificare, generare de rezultate și un framework personalizat de testare.

## ⚙️ Cerințe

- Python 3.8+
- Docker
- Sistem de operare: Linux (testat pe Ubuntu)

## 🚀 Instalare și Rulare

Asigură-te că Docker este instalat și activ.
Clonează acest repository:
   git clone https://github.com/numele-tau/log-analyzer.git
   cd log-analyzer

Rularea completă a aplicației:
   chmod +x start_script.sh
   ./start_script.sh
Scriptul va: construi imaginea Docker, porni containerul, extrage output.json din container în directorul output/.


## Testare
Framework-ul de testare permite rularea testelor filtrat pe categorii sau nume:
### Toate testele smoke
python3 run_tests.py --category smoke

### Teste software (unitare)
python3 run_tests.py --category software

### Teste de integrare
python3 run_tests.py --category integration

### Rulare după numele unui test
python3 run_tests.py --filter test_log_parser

Rezultatele sunt afișate în consolă și salvate într-un raport HTML interactiv.

## 🧰 Tehnologii utilizate
### Python 3.x
### Docker
### Bash
### HTML (raport testare)
### Framework personalizat pentru testare bazat pe unittest
