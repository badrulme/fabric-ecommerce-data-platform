"""Validate deterministic synthetic source data without external dependencies."""
import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from generate_data import generate, make_dataset


class DatasetTests(unittest.TestCase):
    def setUp(self):
        self.data = make_dataset(seed=42)

    def test_counts(self):
        self.assertEqual({k: len(v) for k, v in self.data.items()}, {
            "customers": 120, "products": 50,
            "orders": 300, "order_items": 600, "payments": 300})

    def test_unique_business_keys(self):
        keys = {
            "customers": "customer_id", "products": "product_id",
            "orders": "order_id", "order_items": "order_item_id",
            "payments": "payment_id",
        }
        for table, key in keys.items():
            values = [row[key] for row in self.data[table]]
            self.assertEqual(len(values), len(set(values)), table)

    def test_references_and_values(self):
        customers = {r["customer_id"] for r in self.data["customers"]}
        products = {r["product_id"] for r in self.data["products"]}
        orders = {r["order_id"] for r in self.data["orders"]}
        self.assertTrue(all(r["customer_id"] in customers for r in self.data["orders"]))
        self.assertTrue(all(r["order_id"] in orders and r["product_id"] in products
                            for r in self.data["order_items"]))
        self.assertTrue(all(r["order_id"] in orders for r in self.data["payments"]))
        self.assertTrue(all(int(r["quantity"]) > 0 for r in self.data["order_items"]))

    def test_csv_generation_is_deterministic(self):
        with tempfile.TemporaryDirectory() as d1, tempfile.TemporaryDirectory() as d2:
            generate(Path(d1), seed=42)
            generate(Path(d2), seed=42)
            for name in self.data:
                self.assertEqual((Path(d1) / f"{name}.csv").read_bytes(),
                                 (Path(d2) / f"{name}.csv").read_bytes())


if __name__ == "__main__":
    unittest.main()
