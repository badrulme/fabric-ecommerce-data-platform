"""Generate reproducible, entirely synthetic E-Commerce CSV source files.

Run: python scripts/generate_data.py --output data/generated --seed 42
No packages required outside the Python standard library.
"""
import argparse
import csv
import random
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

CUSTOMER_COUNT = 120
PRODUCT_COUNT = 50
ORDER_COUNT = 300
ITEM_COUNT = 600


def money(value):
    return str(Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))


def make_dataset(seed=42):
    r = random.Random(seed)
    cities = ["Dhaka", "Chattogram", "Khulna", "Rajshahi", "Sylhet"]
    categories = ["Fashion", "Electronics", "Home", "Personal Care", "Accessories"]
    methods = ["Card", "Bank Transfer", "Cash on Delivery", "Mobile Wallet"]
    customers = [
        dict(customer_id=f"C{i:04}", customer_name=f"Demo Customer {i:04}",
             email=f"customer{i:04}@example.invalid", city=r.choice(cities),
             country="Bangladesh",
             signup_date=(datetime(2025, 1, 1) + timedelta(days=r.randint(0, 360))).date().isoformat())
        for i in range(1, CUSTOMER_COUNT + 1)
    ]
    products = [
        dict(product_id=f"P{i:04}", product_name=f"Demo Product {i:04}",
             category=categories[(i - 1) % len(categories)],
             unit_price=money(Decimal(r.randint(1000, 20000)) / 100),
             is_active="true" if i % 10 else "false")
        for i in range(1, PRODUCT_COUNT + 1)
    ]
    price_lookup = {p["product_id"]: p["unit_price"] for p in products}
    orders, items, payments = [], [], []
    for i in range(1, ORDER_COUNT + 1):
        order_id = f"O{i:05}"
        when = (datetime(2026, 1, 1, 8)
                + timedelta(days=r.randint(0, 220),
                            hours=r.randint(0, 12), minutes=r.randint(0, 59)))
        status = r.choices(["Completed", "Shipped", "Pending", "Cancelled"],
                           weights=[60, 20, 12, 8], k=1)[0]
        orders.append(dict(
            order_id=order_id, customer_id=r.choice(customers)["customer_id"],
            order_date=when.strftime("%Y-%m-%d %H:%M:%S"),
            order_status=status, currency="BDT"))
        for line in (1, 2):
            product_id = r.choice(products)["product_id"]
            items.append(dict(
                order_item_id=f"OI{i:05}{line}", order_id=order_id,
                product_id=product_id, quantity=r.randint(1, 4),
                unit_price=price_lookup[product_id],
                discount_pct=r.choice([0, 0, 0, 5, 10, 15])))
        payments.append(dict(
            payment_id=f"PAY{i:05}", order_id=order_id,
            payment_method=r.choice(methods),
            payment_status={"Completed": "Paid", "Shipped": "Paid",
                            "Pending": "Unpaid", "Cancelled": "Refunded"}[status],
            payment_date=(when + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S")))
    return dict(customers=customers, products=products, orders=orders,
                order_items=items, payments=payments)


def generate(output: Path, seed=42):
    output.mkdir(parents=True, exist_ok=True)
    dataset = make_dataset(seed)
    for name, rows in dataset.items():
        target = output / f"{name}.csv"
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)
        print(f"{target}: {len(rows)} rows")
    return dataset


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("data/generated"))
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    generate(args.output, args.seed)
