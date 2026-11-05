"""Inventory API: exposes a small product catalog and stock summaries."""

import json
from pathlib import Path

from flask import Flask, abort, jsonify, request

CATALOG_PATH = Path(__file__).with_name("catalog.json")


def load_catalog():
    with CATALOG_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


def create_app(catalog=None):
    app = Flask(__name__)
    products = catalog if catalog is not None else load_catalog()

    @app.get("/health")
    def health():
        return jsonify(status="ok")

    @app.get("/products")
    def list_products():
        category = request.args.get("category")
        items = [p for p in products if category is None or p["category"] == category]
        return jsonify(items)

    @app.get("/products/<sku>")
    def get_product(sku):
        for product in products:
            if product["sku"] == sku:
                return jsonify(product)
        abort(404)

    @app.get("/stock/summary")
    def stock_summary():
        summary = {}
        for product in products:
            entry = summary.setdefault(product["category"], {"products": 0, "units": 0})
            entry["products"] += 1
            entry["units"] += product["stock"]
        return jsonify(summary)

    return app


app = create_app()
