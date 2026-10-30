# Microsoft Fabric — Enterprise E-Commerce Analytics POC

Hands-on, client-readiness data engineering training from scratch. All data is **synthetic**; this repository contains no client credentials or real customer records.

## Current setup
- Tenant: BJIT Group
- Workspace: `bjit-ecommerce-fabric-poc-dev` (Fabric Trial, Southeast Asia)
- First Lakehouse to create: `lh_ecom_bronze`
- GitHub default branch: `main`

## What we will build

```text
Synthetic E-Commerce CSVs (five source entities)
    -> Fabric Lakehouse Files/source
    -> Fabric Data Factory Copy activity -> Files/raw
    -> Fabric Spark Notebook 01 -> bronze_* Delta tables
    -> Fabric Spark Notebook 02 -> silver_* Delta tables
    -> Fabric Spark Notebook 03 -> dim_* / fact_sales Delta tables
    -> SQL analytics endpoint -> semantic model -> Power BI
```

## Practical lab order
1. **Foundation** — Workspace, trial capacity, OneLake, create Lakehouse. See [Lab 01](docs/lab-01-workspace.md).
2. **Ingestion** — Generate five source CSV files, upload into Lakehouse Files and build Copy activity. See [Lab 02](docs/lab-02-ingestion.md).
3. **Bronze** — Read raw CSVs with Spark and write Delta tables.
4. **Silver** — Clean, type, validate and check relationships.
5. **Gold** — Create customer/product/date dimensions and sales fact.
6. **Reporting** — SQL analytics endpoint, semantic model, Power BI.
7. **Production patterns** — Orchestration, incremental loading, monitoring, governance and CI/CD.

## Local setup
Python 3.10+; no additional packages for the synthetic data generator.

```bash
python scripts/generate_data.py --output data/generated --seed 42
python -m unittest discover -s tests -v
```

Expected row counts: **120 customers, 50 products, 300 orders, 600 order items, 300 payments**. Generated CSV files are deliberately gitignored; reproduce them from the deterministic generator or use the shared starter ZIP.

Fabric notebooks in `notebooks/` are **Spark code**, not ordinary local Python scripts. Create Fabric notebooks, attach `lh_ecom_bronze` as **default Lakehouse**, then paste the code in sequence.

## Learning method
For every lab: **Concept → Do it yourself → Validate output → Troubleshoot → Explain to a client**. Capture screenshots of non-sensitive output, and answer the review questions without reading the guide.

## Security / ownership
This is a public training repository, **not an approved client data repository**. Never commit work email tokens, tenant IDs, API keys, credentials, confidential BJIT/client material, or real customer data. Use synthetic data only. Review official corporate policy before sharing client-specific work.

## Useful official documentation
- [Create a Fabric Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse)
- [Fabric Notebook and default Lakehouse](https://learn.microsoft.com/en-us/fabric/data-engineering/how-to-use-notebook)
- [Data Factory Lakehouse Copy activity](https://learn.microsoft.com/en-us/fabric/data-factory/connector-lakehouse-copy-activity)
- [Copy activity monitoring](https://learn.microsoft.com/en-us/fabric/data-factory/monitor-copy-activity)
