# ServiceFlow

> **Portfolio edition:** a generic, privacy-aware front-office and service-request management platform inspired by a real administrative workflow, with all institutional data removed.

ServiceFlow turns scattered service records into structured, searchable and reusable operational data.

## Portfolio snapshot

This project demonstrates **workflow digitization, Django domain modeling, authentication, filters, dashboards, idempotent historical import and exportable management data**.

**Stack:** Django · PostgreSQL/SQLite · OpenPyXL · Bootstrap-free responsive UI · Tests · CI

## Core workflow

Each service record can include:

- request date;
- requester type and reference/protocol;
- requester name;
- category and subcategory;
- subject;
- response/resolution;
- channel;
- status;
- notes;
- responsible staff member;
- authenticated creator.

Categories and subcategories are administrable without code changes.

## Management features

- authenticated access;
- structured registration form;
- search across requester, reference, subject and resolution;
- filters by period, category, status, channel and staff member;
- dashboard with total/open requests and operational breakdowns;
- CSV and Excel export;
- historical XLSX import with **dry-run** and **idempotency key**;
- synthetic demo dataset;
- server-side validation and security settings.

## Run locally

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

Demo credentials:

- `admin` / `Demo-Admin-12345`
- `agent.demo` / `Demo-Agent-12345`

Demo credentials are for local portfolio use only.

## Origin and privacy

The operational system that inspired this case remains separate. This repository contains no institutional logo, production spreadsheet, real requester data, database backup or inherited Git history.
