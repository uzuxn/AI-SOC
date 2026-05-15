# AI-SOC
AI-powered Security Operations Center using Machine Learning
>>>>>>> 14a40d6b88161654af53c38df42214126850c84c

Yes — definitely add a proper `README.md` before final upload and push.

A good README:

* makes the repository look professional,
* helps evaluators run the project,
* improves presentation quality,
* and supports your appendix/user guide.

Keep it concise and practical.

Here’s a strong structure for your AI-SOC project:

---

# AI-SOC — Artificial Intelligence–Driven Security Operations Center

## Overview

AI-SOC is a prototype cybersecurity monitoring platform that integrates machine learning–based threat detection, anomaly analysis, centralized dashboard visualization, persistent security log management, and blockchain-inspired integrity verification.

---

## Features

* Real-time security event monitoring
* AI-based threat detection
* Anomaly detection using Isolation Forest
* Risk severity classification
* Persistent SQLite log storage
* Blockchain-inspired tamper-evident logging
* Interactive React dashboard
* CSV export functionality
* Authentication interface

---

## Technologies Used

### Backend

* Python
* FastAPI
* Scikit-learn
* SQLite

### Frontend

* React
* Tailwind CSS
* JavaScript

### Machine Learning

* Random Forest
* Isolation Forest
* UNSW-NB15 Dataset

---

## System Architecture

Briefly explain:

* frontend,
* backend,
* ML engine,
* database,
* blockchain module.

---

## Installation

### Clone Repository

```bash
git clone <repository-link>
cd AI-SOC
```

### Backend Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend Setup

```bash
cd frontend
npm install
python -m http.server 3000
```

---

## Running the System

Backend:

```bash
uvicorn main:app --reload
```

Frontend:

```bash
python -m http.server 3000
```

Access dashboard:

```text
http://localhost:3000
```

---

## Dataset

* UNSW-NB15 Dataset

---

## Project Structure

```text
backend/
frontend/
models/
datasets/
docs/
```

---

## Author

Uzman Fairoos
BSc (Hons) Computer Security
University of Plymouth

---
