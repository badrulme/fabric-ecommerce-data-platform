# Lab 02 — Synthetic E-Commerce ingestion with Data Factory

**Do this only after Lab 01 is verified.**

## Goal
Generate fake but internally consistent source data, upload five CSV files, and build a Fabric Data Factory Copy activity from a source folder into a raw landing folder.

## Source entities
| File | Expected rows | Business key |
|---|---:|---|
| customers.csv | 120 | customer_id |
| products.csv | 50 | product_id |
| orders.csv | 300 | order_id |
| order_items.csv | 600 | order_item_id |
| payments.csv | 300 | payment_id |

The generator is reproducible for a fixed seed, so teammates get the same input.

## Exercise A — Generate and validate
In the repository root on your laptop:

~~~powershell
python scripts/generate_data.py --output data/generated --seed 42
python -m unittest discover -s tests -v
~~~

Inspect `orders.csv` and `order_items.csv`. Observe that one order has two lines, and each item references a product.

## Exercise B — Upload to OneLake
1. Workspace → `lh_ecom_bronze` → **Files**.
2. Create folder `source`.
3. Upload the five generated CSV files to `Files/source/`.
4. Check the files were uploaded under **Files**, not **Tables**.

## Exercise C — Fabric Data Factory
1. Workspace → **New item** → **Data pipeline**.
2. Name it `pl_ecom_ingestion_dev`.
3. Add a **Copy data** activity named `copy_source_to_raw`.
4. Source: Lakehouse `lh_ecom_bronze` → **Files/source**. Use CSV file format and ensure the first row is treated as the header if the UI requests schema options.
5. Destination: same Lakehouse → **Files/raw**. Configure a file-to-file copy, not a table sink; retain original filenames.
6. Prefer a folder/wildcard copy with **Preserve hierarchy** or **Flatten hierarchy**, as appropriate to achieve exactly `Files/raw/<filename>.csv`. If the UI does not support the folder configuration, create **five Copy activities**, one per CSV.
7. Save, **Run**, then inspect **Run history / Monitor**. Verify success, file count, destination paths and copied bytes.
8. Open Lakehouse Files → raw and confirm all five files.

## Exercise D — Explain
- Why not directly write source CSVs to Gold?
- What is the practical difference between Files and Tables?
- Why do we retain raw copies?
- What is different about a **Copy activity** versus a **Notebook**?

## Success criteria
- [ ] 5 source CSVs in Files/source
- [ ] Copy activity succeeded
- [ ] 5 same-named CSVs in Files/raw
- [ ] No secrets, customer PII, or other company data used

## Official documentation
https://learn.microsoft.com/en-us/fabric/data-factory/connector-lakehouse-copy-activity

https://learn.microsoft.com/en-us/fabric/data-factory/monitor-copy-activity
