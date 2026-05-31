# 🧟 ZombieGuard — Zombie API Discovery & Defence System

**Union Bank of India | iDEA 2.0 Hackathon | Problem Statement: PS9 (API Inventory & Security)**
**Team Name:** Team Insiders

---

## 🎯 Project Overview & Problem Statement

In modern enterprise and open-banking environments, databases and gateways accumulate hundreds of **zombie APIs** — unused, outdated, or abandoned endpoints that remain active in production. These invisible entry points account for **over 78% of enterprise API security incidents** and map directly to **OWASP API9: Improper Inventory Management**, **API3: Excessive Data Exposure**, and **API7: Security Misconfiguration**.

**ZombieGuard** is an AI-powered, real-time platform designed to **discover, score, and neutralise** zombie and shadow APIs in production. It ingests transactional logs, pipelines them through a high-throughput stream, uses unsupervised machine learning and temporal sequence models to flag anomalies, scores threat profiles, and automatically deploys defenses (disabling routes and rotating keys) — **all in under 3 seconds!**

---

## 🛠️ Complete System Architecture

```
                                 [ ZOMBIEGUARD DATA FLOW ]
                                 
  5 INPUT SOURCES                STREAM BUS (KAFKA)              AI & SCORING PIPELINE
  ┌───────────────────────┐      ┌─────────────────────────┐     ┌────────────────────────┐
  │ 📡 API Gateway Logs   │ ───> │ 🟣 api-gateway-logs     │ ──> │ Unsupervised ML        │
  ├───────────────────────┤      ├─────────────────────────┤     │ IsolationForest(n=200) │
  │ 🌐 Network Traffic    │ ───> │ 🔵 network-traffic      │     ├────────────────────────┤
  ├───────────────────────┤      ├─────────────────────────┤     │ Temporal ML            │
  │ 📋 API Registries     │ ───> │ 🟢 cve-feed             │     │ LSTM (30-day window)   │
  ├───────────────────────┤      ├─────────────────────────┤     ├────────────────────────┤
  │ 🛡️ CVE Database       │ ───> │ 🟡 ml-output            │     │ Real-time Scoring      │
  ├───────────────────────┤      ├─────────────────────────┤     │ NumPy Vectorised CVSS  │
  │ 💾 API Metadata (SQL) │ ───> │ 🔴 defence-actions      │     └────────────────────────┘
  └───────────────────────┘      └─────────────────────────┘                 │
                                                                             ▼
  DECEPS DEFENCE WEBHOOKS        SECURE ORM DATABASE               MANUAL / AUTO DEFENCE
  ┌───────────────────────┐      ┌─────────────────────────┐     ┌────────────────────────┐
  │ 💬 Slack Webhook      │ <─── │ SQL Alchemy (SQLite)    │ <─── │ 🔴 Auto-Disable Route  │
  ├───────────────────────┤      │ 7 normalized tables     │     ├────────────────────────┤
  │ 📧 Email Alerts       │      │ PCI-DSS Audit Logging   │     │ 🔑 Pydantic Key Rotate │
  ├───────────────────────┤      └─────────────────────────┘     ├────────────────────────┤
  │ 📟 PagerDuty / SMS    │                                      │ ✅ Whitelist Bypass    │
  └───────────────────────┘                                      └────────────────────────┘
```

---

## ✨ Key Innovations & Features

### 1. Unified 5-Channel Log Ingestion & BeautifulSoup Parser
ZombieGuard aggregates and normalizes structural schema definitions, Swagger specifications, API logs, and CVE patterns from five distinct sources:
* **BeautifulSoup Parsing**: Scrapes live HTML/JS files to find hidden developer routes and parses OpenAPI/Swagger specifications.
* **Traffic Fingerprinting**: Passive mapping isolates undocumented **shadow APIs** (endpoints handling live requests but absent from official registers).

### 2. Multi-Tiered AI Anomaly Engine
* **Isolation Forest Anomaly Classifier (`scikit-learn`)**: Evaluates a 7-feature matrix (`calls_per_day`, `days_since_active`, `error_rate_pct`, `has_auth`, `is_documented`, `is_registered`, `response_ms`) to catch structural, transactional deviations without requiring pre-labeled training datasets.
* **LSTM Time-Series Predictor (`NumPy` vectorized)**: Models sliding 30-day velocity sequences to identify sudden drops or spikes in transaction call frequency.

### 3. Multi-Factor NumPy Vectorized CVSS Scorer
Computes a granular, real-time threat score (0-100) per endpoint in a single vectorized matrix calculation, aligning with CVE vulnerabilities across five weighted threat dimensions:
$$\text{Threat Score (0-100)} = \text{Staleness (35)} + \text{No-Auth (25)} + \text{Zero-Traffic (20)} + \text{CVE Match (15)} + \text{Undocumented (5)}$$

### 4. Under 3-Second Active Auto-Defence
* **Route Disablement**: High-risk critical endpoints (Score $\ge 80$) are automatically neutralized via middleware block triggers.
* **Pydantic Key Rotation**: Rotates gateway authentication keys instantly, validating schemas via Pydantic.
* **Audit Trail**: Writes a cryptographic PCI-DSS compliant audit log to SQLite database.

### 5. Premium UI URL / API Link Scanner (Advanced Page)
* **Visual Port Telemetry & Service Auditing**: Integrates passive service/port telemetry directly, rendering open port mappings (e.g. `22` SSH, `80/443` Web Services, `8080` Spring Boot Gateway) along with service banners and risk scores.
* **Spring Boot & Framework Prober**: Detects backend Spring Boot / Springdoc routes (`/v2/api-docs`, `/v3/api-docs`) to identify microservice endpoints automatically.
* **Instant Terminal Emulator Logs**: Displays simulated terminal audits (like Nmap/Masscan output) in real-time.

---

## 💻 Tech Stack

| Technology | Role | Version |
| :--- | :--- | :--- |
| **FastAPI** | Core Backend REST API Engine | `0.115.0` |
| **Uvicorn** | High-performance ASGI Web Server | `0.30.6` |
| **scikit-learn** | Unsupervised Isolation Forest Model | `1.5.1` |
| **NumPy** | Vectorized Math & Matrix Scorer | `1.26.4` |
| **SQLAlchemy** | Relational Database SQLite ORM | `2.0.32` |
| **BeautifulSoup4**| HTML/JS Parsing & Spec Scraping | `4.12.3` |
| **Pydantic v2** | Request/Response Schema Validation | `2.8.2` |
| **Chart.js** | Interactive Frontend Visual Analytics | `4.4.1` |
| **Apache Kafka** | Real-time Stream Broker (simulated) | `2.0.2` |

---

## 📂 Project Directory Structure

```
ZombieGuard-By-Team-Insiders/
├── ZombieGuard_Backend_v2/
│   └── zombieguard_backend/
│       ├── app/
│       │   ├── api/routes/api.py       # FastAPI Route Handlers
│       │   ├── core/kafka_bus.py       # Kafka Broker & Event Bus Simulators
│       │   ├── db/                     # DB Models, Session & DB Schemas
│       │   │   ├── models.py           # SQLAlchemy normalized DB Models
│       │   │   └── session.py          # SQLite engine & session generators
│       │   ├── ml/detector.py          # IsolationForest, LSTM & NumPy scorer
│       │   ├── parsers/bs4_parser.py   # BeautifulSoup HTML, XML, & CVE scrapers
│       │   ├── schemas/schemas.py      # Pydantic v2 Request & Response schemas
│       │   └── services/               # URL Scanner & File Upload business logic
│       ├── templates/index.html        # Premium Dark-Themed UI Dashboard
│       ├── tests/test_all.py           # Comprehensive Test Suite (60 tests)
│       ├── mock_vulnerable_bank.py     # Local Mock Target Server (Port 8001)
│       ├── requirements.txt            # Python Backend dependencies
│       └── run.py                      # Server bootstrap launch script
├── ZombieGuard_Frontend_v2/            # Advanced React UI Workspace
├── ZombieGuard_ScanPages.jsx           # Advanced React Custom scanner forms
└── README.md                           # Master Project README Documentation
```

---

## 🚀 Execution & Setup Guide

### 1. Prerequisites
Ensure you have **Python 3.10+** and `pip` installed.

### 2. Setup Dependencies
Clone the repository:
```bash
git clone https://github.com/Asterioxer/ZombieGuard_Insiders.git
```
Navigate into the backend project directory and install the required modules:
```bash
cd ZombieGuard_Backend_v2/zombieguard_backend
pip install -r requirements.txt
```

### 3. Launch the Core Platform
Start the core ZombieGuard platform:
```bash
python run.py
```
This boots the FastAPI ASGI server on [http://localhost:8000](http://localhost:8000), initializing the local relational SQLite database (`zombieguard.db`) and generating the mock Apache Kafka partitions.

### 4. Launch the Mock Vulnerable Banking API (Demo Target)
In a new terminal window, boot the local target server containing exposed legacy endpoints:
```bash
python mock_vulnerable_bank.py
```
This runs the legacy server on [http://localhost:8001](http://localhost:8001), serving as a safe target for sandbox tests.

### 5. Access the Platform
* **SecOps Dashboard UI**: [http://localhost:8000](http://localhost:8000)
* **Swagger Interactive Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
* **ReDoc Specifications**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Comprehensive Automated Testing

ZombieGuard has a robust test suite covering all core engines: BeautifulSoup scrapers, ML classifiers, Pydantic schemas, SQLAlchemy database layers, and FastAPI route handlers.

### How to Run Tests
From the backend directory, execute `pytest`:
```bash
pytest tests/ -v
```

### Passing Test Summary
```bash
============================= test session starts =============================
platform win32 -- Python 3.12.1, pytest-8.3.2, pluggy-1.6.0
collected 60 items

tests\test_all.py ...................................................... [ 90%]
......                                                                   [100%]
================ 60 passed, 708 warnings in 154.16s (0:02:34) =================
```
*Note: Includes defensive cleanup logic preventing file connection locks on Windows platforms.*

---

## 👥 Team Insiders (Union Bank of India iDEA 2.0 PS9)

* **Pramit Sasmal**: Security Researcher + ML Engineer
* **Soham Mukherjee**: Backend Developer (FastAPI + SQLAlchemy)
* **Ashutosh Kumar**: ML Pipeline (Isolation Forest + NumPy)
* **Pratyush Sharma**: Frontend + BeautifulSoup Parser
