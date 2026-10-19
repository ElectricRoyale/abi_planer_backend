# Abi Planer – Backend

REST- und WebSocket-API zur Verwaltung von Abiball-Gästen. Das Backend speichert Gäste samt Ticketanzahl, Essenswahl, Sitzplatz und Zahlungsstatus in einer MySQL-Datenbank und überträgt jede Änderung per WebSocket in Echtzeit an alle verbundenen Clients.

## Datenfluss

```
Google Form → Google Apps Script → Datenbank (MySQL)
                                        ↑
Flutter-App ⇄ WebSocket / REST ⇄ dieses Backend
```

Gäste tragen sich per Google Form ein, ein Google-Apps-Script schreibt die Antworten in die Datenbank. Dieses Backend stellt die Daten für die [Flutter-App](https://github.com/ElectricRoyale/abiball_planer) bereit.

## Features

- CRUD für Gäste (`students`-Tabelle): Name, E-Mail, Tickets, Hardcards, Sitzplatzwunsch, Essenswahl (Fleisch / vegetarisch / vegan), Allergene, Platznummer, Betrag, Zahlungsstatus
- Duplikatsprüfung beim Anlegen (Vor- und Nachname)
- Echtzeit-Synchronisation: Änderungen werden per WebSocket an alle Clients gebroadcastet
- Zwei Zugriffswege: klassische REST-Endpunkte und eine WebSocket-Methodenschnittstelle
- Docker-Support (Gunicorn + Uvicorn Worker)

## Tech Stack

| Bereich    | Technologie                      |
|------------|----------------------------------|
| Sprache    | Python 3.12                      |
| Framework  | FastAPI, Uvicorn, Gunicorn       |
| Datenbank  | MySQL (PyMySQL)                  |
| Echtzeit   | WebSockets                       |
| Deployment | Docker / Docker Compose          |

## Setup

```bash
git clone https://github.com/ElectricRoyale/abi_planer_backend.git
cd abi_planer_backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

`.env` im Projektroot anlegen:

```env
MySQL_server=<host>
MySQL_user=<user>
MySQL_password=<password>
MySQL_table_visitors=<datenbankname>
```

Starten:

```bash
uvicorn main:app --reload --port 8000
```

## Docker

```bash
docker compose up --build
```

Die API ist anschließend unter `http://localhost:8000` erreichbar. Die DB-Zugangsdaten werden per Umgebungsvariablen übergeben (z. B. `--env-file .env`).

## API

Interaktive Doku: `http://localhost:8000/docs`

### REST

| Methode | Endpoint        | Parameter (Query)                                              | Beschreibung              |
|---------|-----------------|----------------------------------------------------------------|---------------------------|
| GET     | `/getstudents`  | –                                                              | Alle Gäste                |
| POST    | `/insert/`      | `firstname`, `lastname`, `email`, `number_of_tickets`, optional weitere Felder | Gast anlegen |
| POST    | `/update/`      | `update_data` (JSON), `condition` (JSON)                       | Gast aktualisieren        |
| POST    | `/delete/`      | `condition` (JSON)                                             | Gast löschen              |

### WebSocket

Endpoint: `ws://localhost:8000/ws`

Nachrichtenformat:

```json
{ "method": "addStudent", "args": { "firstname": "Max", "lastname": "Muster", "email": "max@example.com", "number_of_tickets": 2 } }
```

Verfügbare Methoden: `getStudents`, `getSingleStudent`, `addStudent`, `updateStudent`, `deleteStudent`.
Erfolgreiche Antworten gehen an alle Clients, Fehler nur an den Absender.

## Projektstruktur

```
.
├── main.py              # FastAPI-App, REST-Endpunkte, WebSocket-Handling
├── database_helper.py   # MySQL-Zugriff und Gäste-Operationen
├── Dockerfile
├── docker-compose.yml
└── requirements.txt
```

## Lizenz

[MIT / nicht angegeben]
