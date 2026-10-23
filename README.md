# hkhr_store
# 🛒 Serverless Event-Driven Cloud E-Commerce Store

A complete, production-ready, event-driven online storefront built using a **100% free open-source cloud tech stack**. This project replaces traditional heavy infrastructure (like local Apache Kafka and Docker containers) with a modern, zero-cost serverless architecture.

## 🚀 Live Demo
* **Storefront URL:** [Paste your Render URL here, e.g., https://onrender.com]
* **Message Broker:** Hosted Serverless on Upstash Redis

---

## 🏗️ Architecture & Tech Stack

This project demonstrates a decoupling of frontend/backend requests from intensive processing pipelines using an asynchronous message stream:

```text
[ Browser Frontend ] 
         │  (POST /api/order)
         ▼
[ Flask REST API (Render) ] ──(XADD Stream)──> [ Upstash Redis Cloud Queue ]
         │                                              │
         └───(Async Background Consumer Thread) <───────┘
```

### 🛠️ Core Components (All 100% Free)
* **Frontend & Backend API:** Built with **Flask (Python)** and served via **Gunicorn** for production stability.
* **Message Queue / Event Broker:** **Upstash Redis Streams**, mimicking Apache Kafka’s append-only log paradigm over a secure TLS connection (`rediss://`).
* **Cloud Hosting Container:** **Render (Free Web Service Tier)** with automated environment variable injection.
* **Cloud Development IDE:** **GitHub Codespaces** providing a sandboxed, browser-based runtime terminal.
* **CI/CD Pipeline:** **GitHub Actions** executing syntax verification and code architecture standards automatically on every code push.

---

## 🛠️ Local Development & Testing

You can spin up and test this project directly in the cloud using **GitHub Codespaces**:

1. Open the repository in a **Codespace**.
2. Install the production dependencies:
   ```bash
   pip install -r backend/requirements.txt
   ```
3. Inject your secure Upstash credentials into your environment:
   ```bash
   export REDIS_URL="rediss://default:YOUR_PASSWORD@your-endpoint.upstash.io:6379"
   ```
4. Run the application:
   ```bash
   python backend/app.py
   ```
5. Navigate to the **Ports** tab in Codespaces and open Port `5000` to interact with the UI.

---

## 🔄 CI/CD Pipeline Configuration

The automated pipeline is defined in `.github/workflows/cicd.yml` and triggers on every `push` or `pull_request` to the `main` branch. It handles:
* Python runtime environment provisioning.
* Dependency installation verification.
* Code style auditing and error scanning using `flake8`.

