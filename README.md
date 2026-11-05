# inventory-api

Small Flask API that serves a product catalog and stock summaries.

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | `/health` | Liveness check |
| GET | `/products` | List products, optional `?category=` filter |
| GET | `/products/<sku>` | Get one product |
| GET | `/stock/summary` | Products and units per category |

## Local development

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
pytest -q
flask --app app.main run --port 8000
```

## Historical data

`scripts/generate_data.py` writes synthetic stock events to `data/events/` for offline analysis. The API does not read these files.

## Container

```bash
docker build -t inventory-api .
docker run --rm -p 8000:8000 inventory-api
```
