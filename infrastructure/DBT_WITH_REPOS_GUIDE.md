# dbt + Databricks Repos: Complete Guide

This guide shows how to use dbt with Databricks using Git integration (Databricks Repos) - the industry best practice.

## Overview

**Architecture:**
```
Git Repo (GitHub)
    ↓ (syncs via Databricks Repos)
Databricks Workspace (/Repos/{stack}/repo-name/)
    ↓ (contains)
dbt Project (models/, macros/, etc.)
    ↓ (connects to)
Databricks SQL Warehouse
    ↓ (executes)
SQL Transformations
```

## How It Works

1. **dbt project stored in Git** - Your dbt models, macros, tests live in your Git repo
2. **Databricks Repos syncs Git → Databricks** - Automatically syncs your repo to Databricks workspace
3. **dbt connects to SQL Warehouse** - dbt uses the SQL warehouse HTTP path to execute SQL
4. **Run dbt from anywhere** - Can run dbt from:
   - Databricks notebooks (in the Repo)
   - Databricks Jobs (scheduled)
   - Local machine (CI/CD)
   - dbt Cloud

## Setup Steps

### Step 1: Structure Your Repo

Your Git repo should have this structure:

```
databricks_and_pulumi/
├── infrastructure/          # Pulumi IaC
│   ├── __main__.py
│   └── ...
├── dbt/                     # dbt project (NEW)
│   ├── dbt_project.yml
│   ├── profiles.yml
│   ├── models/
│   │   └── example_model.sql
│   ├── macros/
│   └── tests/
└── notebooks/               # PySpark notebooks (synced to Repo)
    └── example_pyspark_job.py
```

### Step 2: Create dbt Project

```bash
# In your repo root
mkdir -p dbt
cd dbt

# Initialize dbt project
dbt init my_dbt_project
# Or create manually (see below)
```

**Minimal `dbt_project.yml`:**
```yaml
name: 'databricks_dbt'
version: '1.0.0'
config-version: 2

profile: 'databricks_dbt'

model-paths: ["models"]
analysis-paths: ["analyses"]
test-paths: ["tests"]
seed-paths: ["seeds"]
macro-paths: ["macros"]
snapshot-paths: ["snapshots"]

target-path: "target"
clean-targets:
  - "target"
  - "dbt_packages"

models:
  databricks_dbt:
    +materialized: table
    +catalog: main  # Unity Catalog catalog name
    +schema: analytics  # Schema/database name
```

### Step 3: Configure dbt Profile

**`dbt/profiles.yml`:**
```yaml
databricks_dbt:
  target: dev
  outputs:
    dev:
      type: databricks
      catalog: main  # Unity Catalog catalog (or leave empty for Hive metastore)
      schema: analytics  # Database/schema name
      host: https://dbc-49df519f-3194.cloud.databricks.com  # Your Databricks host
      http_path: /sql/1.0/warehouses/226b1e34f7f64362  # SQL warehouse HTTP path
      token: dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX  # Your Databricks token
      threads: 4
```

**How to get SQL warehouse HTTP path:**
1. Go to Databricks UI → **SQL** → **SQL Warehouses**
2. Click on your SQL warehouse (`sql-warehouse-dev`)
3. Go to **Connection details** tab
4. Copy the **HTTP path** (looks like `/sql/1.0/warehouses/abc123...`)

### Step 4: Create Example dbt Model

**`dbt/models/example_model.sql`:**
```sql
-- Example dbt model
-- This will create a table in Databricks

{{ config(materialized='table') }}

with source_data as (
    select 1 as id, 'Alice' as name
    union all
    select 2 as id, 'Bob' as name
)

select * from source_data
```

### Step 5: Test dbt Locally

```bash
cd dbt

# Test connection
dbt debug

# Run models
dbt run

# Run tests
dbt test

# Generate docs
dbt docs generate
dbt docs serve
```

## Running dbt in Databricks

### Option 1: Run from Databricks Notebook (in Repo)

Create a notebook in your repo: `dbt/run_dbt.py`

```python
# Databricks notebook source
# MAGIC %md
# MAGIC # Run dbt Models
# MAGIC 
# MAGIC This notebook runs dbt models from the Git repo.

# COMMAND ----------

# Install dbt-databricks
%pip install dbt-databricks

# COMMAND ----------

# Set working directory to dbt project
import os
os.chdir("/Repos/dev/databricks_and_pulumi/dbt")

# COMMAND ----------

# Run dbt
import subprocess
subprocess.run(["dbt", "run"], check=True)
```

### Option 2: Run from Databricks Job

Create a Databricks Job that runs dbt:

**In Pulumi (`__main__.py`):**
```python
# dbt Job - runs dbt from Repo
dbt_job = databricks.Job(
    f"dbt-run-{stack}",
    name=f"dbt-run-{stack}",
    tasks=[
        databricks.JobTaskArgs(
            task_key="run_dbt",
            notebook_task=databricks.JobNotebookTaskArgs(
                notebook_path=pulumi.Output.all(databricks_repo.path).apply(
                    lambda args: f"{args[0]}/dbt/run_dbt"
                ),
            ),
        ),
    ],
    schedule=databricks.JobScheduleArgs(
        quartz_cron_expression="0 0 * * * ?",  # Daily at midnight
        timezone_id="America/New_York",
    ),
    opts=pulumi.ResourceOptions(
        provider=databricks_provider,
        depends_on=[databricks_repo],
    ),
)
```

### Option 3: Run from CI/CD (GitHub Actions)

**`.github/workflows/dbt.yml`:**
```yaml
name: Run dbt

on:
  push:
    branches: [main]
    paths:
      - 'dbt/**'

jobs:
  dbt:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dbt
        run: |
          pip install dbt-databricks
      
      - name: Run dbt
        working-directory: ./dbt
        env:
          DBT_PROFILES_DIR: ./dbt
        run: |
          dbt run
          dbt test
```

## Benefits of This Approach

✅ **Version Control** - All dbt code in Git, not base64 strings  
✅ **No Encoding** - No need to base64 encode notebooks/models  
✅ **Collaboration** - Standard Git workflow (PRs, reviews, etc.)  
✅ **Sync** - Changes in Git automatically sync to Databricks  
✅ **Flexibility** - Run dbt from anywhere (local, Databricks, CI/CD)  
✅ **Industry Standard** - This is how most teams do it  

## Workflow

1. **Develop locally:**
   ```bash
   cd dbt
   dbt run --select my_model
   ```

2. **Commit to Git:**
   ```bash
   git add dbt/models/my_model.sql
   git commit -m "Add new dbt model"
   git push
   ```

3. **Databricks Repos auto-syncs** - Your changes appear in Databricks workspace

4. **Run in Databricks:**
   - Use notebook in Repo
   - Or trigger Databricks Job
   - Or run from CI/CD

## dbt + PySpark Integration

You can combine dbt SQL transformations with PySpark jobs:

1. **dbt runs SQL** → Creates tables in Databricks
2. **PySpark job reads dbt tables** → Does complex processing
3. **dbt documents everything** → Full lineage

**Example PySpark job reading dbt output:**
```python
# In notebook: /Repos/dev/databricks_and_pulumi/notebooks/process_dbt_output.py
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("ProcessDBT").getOrCreate()

# Read table created by dbt
df = spark.table("main.analytics.example_model")

# Do PySpark processing
result = df.groupBy("name").count()

# Write back (can be documented in dbt as external model)
result.write.mode("overwrite").saveAsTable("main.analytics.processed_data")
```

## Troubleshooting

### dbt can't connect to Databricks
- Check SQL warehouse HTTP path is correct
- Verify token has permissions
- Ensure SQL warehouse is running

### Repo not syncing
- Check Git credentials in Databricks Settings
- Verify repo URL and branch
- Manually trigger sync in Databricks UI

### dbt models not found
- Ensure dbt project is in correct path in Repo
- Check `dbt_project.yml` profile name matches `profiles.yml`
- Verify working directory when running dbt

## Next Steps

1. Create dbt project structure in your repo
2. Add example models
3. Test locally with `dbt run`
4. Set up Databricks Job to run dbt on schedule
5. Add CI/CD pipeline for dbt tests

## Resources

- [dbt-databricks adapter docs](https://docs.getdbt.com/reference/warehouse-profiles/databricks-profile)
- [Databricks Repos docs](https://docs.databricks.com/repos/index.html)
- [dbt best practices](https://docs.getdbt.com/guides/best-practices)

