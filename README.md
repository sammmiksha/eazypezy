# EasyPezy: Multilingual Saree & Ethnic Wear Search Engine

AI-powered vertical search engine for Indian ethnic wear that parses natural language and voice queries, extracts fine-grained fashion and logistical attributes, applies hard filters (budget, stock, delivery SLA), and ranks cross-platform results with transparent match explanations.

---

## Architecture Overview

```
                      +-----------------------------+
                      |   React PWA (Voice / Text)  |
                      +--------------+--------------+
                                     |
                                     v
                       +---------------------------+
                       |    FastAPI Gateway        |
                       +-------------+-------------+
                                     |
               +---------------------+---------------------+
               |                     |                     |
               v                     v                     v
     +-------------------+  +------------------+  +------------------+
     | LLM / Rule Parser |  | Connectors &     |  | Delivery Checker |
     | (Attributes & SLA)|  | Catalogs         |  | & SLA Evaluator  |
     +-------------------+  +------------------+  +------------------+
               |                     |                     |
               +---------------------+---------------------+
                                     |
                                     v
                       +---------------------------+
                       |    Multi-Factor Ranker    |
                       |    & Reason Generator     |
                       +---------------------------+
                                     |
                                     v
                       +---------------------------+
                       | Top Ranked Results Cards  |
                       +---------------------------+
```

---

## Project Structure

```
easypezy/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── v1/
│   │   │       ├── endpoints/
│   │   │       │   └── search.py           # Search & parse endpoints
│   │   │       └── router.py
│   │   ├── core/
│   │   │   ├── config.py                   # Pydantic environment configuration
│   │   │   └── database.py                 # SQLAlchemy engine and session provider
│   │   ├── models/
│   │   │   └── product.py                  # Product and DeliveryCache models
│   │   ├── schemas/
│   │   │   └── search.py                   # Pydantic validation schemas
│   │   ├── services/
│   │   │   ├── parser/
│   │   │   │   └── extractor.py            # LLM / Rule-based attribute extraction
│   │   │   ├── connectors/
│   │   │   │   ├── base.py                 # Platform connector interface
│   │   │   │   └── mock_catalog.py         # Multi-platform simulated feeds
│   │   │   ├── delivery/
│   │   │   │   └── checker.py              # Pincode serviceability & SLA deadline checks
│   │   │   └── ranker/
│   │   │       └── scorer.py               # Multi-factor ranker & explanation generator
│   │   └── main.py                         # FastAPI application entrypoint
│   ├── requirements.txt
│   ├── Dockerfile
│   └── test_pipeline.py                    # End-to-end verification test
├── frontend/                               # React + Vite + TypeScript PWA
│   ├── src/
│   │   ├── App.tsx                         # Voice/text search UI & results grid
│   │   ├── types.ts                        # TypeScript interfaces
│   │   └── main.tsx
│   ├── index.html
│   └── package.json
└── docker-compose.yml                      # PostgreSQL (pgvector) + Redis + Backend
```

---

## Key Modules

### 1. Attribute Extraction (`services/parser/extractor.py`)
Extracts structured saree attributes:
- `primary_color` (e.g. purple, magenta, red, yellow)
- `border_type` (zari, temple, contrast, embroidered)
- `zari_type` (golden, silver, copper, antique)
- `finish` (matte, glossy, sheer)
- `fabric` (silk, kanjivaram, banarasi, georgette, chiffon)
- `budget_max` / `budget_min` (INR)
- `deadline_days` (e.g. within 2 days)
- `pincode` (6-digit Indian PIN)
- `clarifications_needed` (triggered when budget or terms are ambiguous)

### 2. Platform Connectors (`services/connectors/base.py`)
`BasePlatformConnector` interface requires:
- `search(query, attributes, max_budget)`
- `check_serviceability(pincode, product_id)`
Implemented by `MockCatalogConnector` simulating Myntra, Ajio, Amazon, and Meesho catalog feeds.

### 3. Delivery SLA & Serviceability (`services/delivery/checker.py`)
- Evaluates estimated delivery days against user deadline constraints.
- Filters out items that cannot arrive before the specified deadline.
- Marks fulfillment confidence (`confirmed`, `estimated`, or `unverified`).

### 4. Multi-Factor Ranker (`services/ranker/scorer.py`)
- Weighted attribute matching: color match (+35%), border/zari match (+25%), fabric match (+20%).
- Budget fit and savings calculation.
- Rating and delivery speed bonuses.
- Generates transparent `why_matched` explanations (e.g., *"Matches requested Purple color • Features Golden zari border • Rs. 1,299 is Rs. 201 below your Rs. 1,500 budget • Highly rated (4.3) • Express 2-day delivery"*).

---

## Running the Application

### 1. Run Backend Locally

```powershell
cd backend
.\venv\Scripts\Activate.ps1
$env:PYTHONPATH="."
python -m uvicorn app.main:app --reload --port 8000
```

Verify backend health at: `http://localhost:8000/health`
Interactive Swagger Docs at: `http://localhost:8000/docs`

### 2. Run Verification Pipeline Test

```powershell
cd backend
$env:PYTHONIOENCODING="utf-8"
$env:PYTHONPATH="."
.\venv\Scripts\python.exe test_pipeline.py
```

### 3. Run Frontend Locally

```powershell
cd frontend
npm run dev
```

Visit `http://localhost:5173` in your browser.

### 4. Running with Docker Compose (Postgres + pgvector + Redis)

When Docker Desktop daemon is started:

```bash
docker compose up -d
```
"# eazypezy" 
