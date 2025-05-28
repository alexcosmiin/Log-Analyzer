# Log Analyzer

Un instrument simplu pentru analiza și clasificarea fișierelor de log.

## Structură

```
log-analyzer/
├── logs/                   # loguri de test
├── tests/                  # testele automate
├── src/                    # codul sursă principal
│   ├── parser.py           # extragere informații din loguri
│   ├── classifier.py       # clasificare erori/mesaje
│   └── main.py             # rulează totul cap-coadă
├── Dockerfile              # containerizarea aplicației
├── docker-compose.yml      # pentru orchestrare
├── requirements.txt        # dependințele Python
└── README.md               # descrierea proiectului
```

## Instrucțiuni Docker

### Rulare aplicație

Pentru a rula aplicația într-un container Docker:

```bash
docker-compose up app
```

### Rulare teste

Pentru a rula testele automate într-un container Docker:

```bash
docker-compose up test
```

### Construire imagine Docker

Pentru a construi imaginea Docker:

```bash
docker build -t log-analyzer .
```

### Rulare manual

Pentru a rula aplicația manual în container:

```bash
docker run -v $(pwd)/logs:/app/logs -v $(pwd)/output:/app/output log-analyzer
```

## Structură Output

Output-ul va fi scris în fișierul `/app/output/output.json` în formatul:

```json
[
  {
    "type": "ERROR|WARNING|INFO|UNKNOWN",
    "message": "Mesajul de log"
  },
  ...
]
```