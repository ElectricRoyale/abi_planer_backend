# Abi Planer – Backend

REST-API für den Abi-Planer: [Kernfunktionen, z. B. Aufgaben, Events, Finanzen, Nutzerverwaltung] für Abiturjahrgänge.

## Features

- [Authentifizierung & Rollen, z. B. JWT]
- [Verwaltung von Events / Aufgaben / Budget]
- [Weitere Kernfunktion]
- REST-API mit [OpenAPI/Swagger-Doku]

## Tech Stack

| Bereich       | Technologie         |
|---------------|---------------------|
| Sprache       | [Java / Node.js / …] |
| Framework     | [Spring Boot / Express / …] |
| Datenbank     | [PostgreSQL / MySQL / …] |
| Build-Tool    | [Maven / Gradle / npm] |
| Deployment    | [Docker] |

## Voraussetzungen

- [JDK 21 / Node 20]
- [Datenbank]
- [Docker (optional)]

## Setup

```bash
git clone https://github.com/ElectricRoyale/abi_planer_backend.git
cd abi_planer_backend
cp .env.example .env   # Variablen anpassen
[./mvnw spring-boot:run | npm install && npm run dev]
```

## Konfiguration

| Variable       | Beschreibung              | Beispiel |
|----------------|---------------------------|----------|
| `DB_URL`       | Datenbank-Verbindung      | `[…]`    |
| `JWT_SECRET`   | Secret für Token-Signatur | `[…]`    |

## Docker

```bash
docker build -t abi-planer-backend .
docker run -p 8080:8080 --env-file .env abi-planer-backend
```

## Projektstruktur

```
src/
├── [controller/]   # HTTP-Schicht
├── [service/]      # Geschäftslogik
├── [repository/]   # Datenzugriff
└── [config/]       # Konfiguration
```

## API-Dokumentation

Nach dem Start unter `[http://localhost:8080/swagger-ui.html]`.

## Tests

```bash
[./mvnw test | npm test]
```

## Frontend

Zugehöriges Frontend: [Link zum Frontend-Repo]

## Lizenz

[MIT / Proprietär]
