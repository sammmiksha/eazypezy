# EasyPezy: Requirement-Aware Product Search

EasyPezy is a product-agnostic shopping search engine. A customer can describe any item in natural language — for example, “5G phone under ₹40,000 with the best screen”, “ergonomic office chair below ₹15,000”, or “quiet 8 kg washing machine” — and receive a ranked cross-store shortlist with an explanation of why each offer fits.

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

### 1. Requirement extraction (`services/parser/requirements_parser.py`)
Separates the request into:

- hard requirements, such as 5G, storage, RAM, display technology, refresh rate, price ceiling, and delivery deadline;
- ranking preferences, such as the best display, camera, battery, performance, or rating;
- a category-agnostic source query, so a live shopping provider receives the customer’s complete request even for a category not represented in the demo data.

### 2. Platform Connectors (`services/connectors/base.py`)
`BasePlatformConnector` interface requires:
- `search(query, attributes, max_budget)`
- `check_serviceability(pincode, product_id)`
Implemented by `MockCatalogConnector` simulating Myntra, Ajio, Amazon, and Meesho catalog feeds.

### 3. Delivery SLA & Serviceability (`services/delivery/checker.py`)
- Evaluates estimated delivery days against user deadline constraints.
- Filters out items that cannot arrive before the specified deadline.
- Marks fulfillment confidence (`confirmed`, `estimated`, or `unverified`).

### 4. Requirement-aware ranker (`services/ranker/requirement_ranker.py`)
- filters every hard requirement before ranking;
- weights the customer’s explicit preferences, then value, seller rating, and delivery;
- produces a fit score and plain-language explanation for every recommendation.

## Live product data

The repository ships with a clearly labelled demo catalog for predictable local development. It does **not** scrape retailer pages or pretend demo prices are live.

For product-agnostic production search, configure an approved shopping-search or affiliate-feed provider. A SerpApi-compatible Google Shopping connector is included and can search across categories from the full natural-language request:

```dotenv
# backend/.env
SERPAPI_API_KEY=your-provider-key
# optional: defaults to https://serpapi.com/search.json
SERPAPI_ENDPOINT=https://serpapi.com/search.json
```

With the key set, API responses return `data_source: "live_shopping_api"`. Without it, results return `data_source: "demo_catalog"`, which the UI displays prominently.

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
