# Lab 01 — Workspace, Capacity, OneLake and Lakehouse

## Learning objectives
Explain the difference between **workspace**, **capacity**, **OneLake**, **Lakehouse**, **Files**, and **Tables**. Then create your first Lakehouse yourself.

## Verified starting point (30 October 2026)
- Fabric trial active in BJIT Group tenant
- Workspace: `bjit-ecommerce-fabric-poc-dev`
- Capacity mode: **Fabric Trial**, region **Southeast Asia**
- Workspace already created (confirmed by screenshot)

## The mental model
- **Workspace** = logical container for project assets and access management.
- **Capacity** = shared Fabric compute resources that execute workloads.
- **OneLake** = Fabric's unified storage layer.
- **Lakehouse** = Fabric item providing Files (raw files) and Tables (Delta tables); it also creates a SQL analytics endpoint.
- **Notebook** = Spark-based code execution and exploration.

## Your hands-on — do this in Fabric
1. Open [app.fabric.microsoft.com](https://app.fabric.microsoft.com).
2. Open workspace `bjit-ecommerce-fabric-poc-dev`.
3. Select **+ New item** → search **Lakehouse**.
4. Name: `lh_ecom_bronze` → **Create**.
5. In Lakehouse Explorer, locate both **Files** and **Tables**.
6. Leave them empty for now. Do not select a predesigned task flow; we are constructing the data platform manually.
7. Verify that the workspace now lists the Lakehouse and its automatically provisioned SQL analytics endpoint.

**Schemas note:** Fabric may enable Lakehouse schemas by default. Either setting can be used in future labs, but the starter notebooks use simple unqualified table names and assume they resolve in the default schema. If the UI asks, leave the default selected and record its value; adjust table qualification when we reach notebooks.

## Evidence
- Screenshot of the Lakehouse Explorer showing Files and Tables
- Workspace item list showing Lakehouse and SQL analytics endpoint

## Active recall — answer in your own words
1. Can a Workspace exist without a Lakehouse?
2. Where does Fabric store Lakehouse files?
3. What is the difference between Files and Tables?
4. What does trial *capacity* provide that a free user license alone does not?

## Client discussion
Why would you use separate dev/test/prod workspaces even when a learning POC uses only one?

## Official references
- https://learn.microsoft.com/en-us/fabric/data-engineering/create-lakehouse
- https://learn.microsoft.com/en-us/fabric/onelake/create-lakehouse-onelake
