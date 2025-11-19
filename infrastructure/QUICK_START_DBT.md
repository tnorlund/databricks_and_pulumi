# Quick Start: dbt + Databricks Repos

## What We Just Set Up

✅ **Databricks Repos** - Your Git repo is synced to Databricks  
✅ **SQL Warehouse** - Ready for dbt connections  
✅ **Jobs** - Can run notebooks from Repo  

## Next Steps to Use dbt

### 1. Get SQL Warehouse HTTP Path

```bash
# Go to Databricks UI
# SQL → SQL Warehouses → sql-warehouse-dev → Connection details
# Copy the HTTP path (looks like: /sql/1.0/warehouses/226b1e34f7f64362)
```

### 2. Create dbt Project Structure

```bash
# In your repo root
mkdir -p dbt/models
cd dbt
```

Create `dbt/dbt_project.yml`:
```yaml
name: 'databricks_dbt'
version: '1.0.0'
config-version: 2
profile: 'databricks_dbt'

model-paths: ["models"]
```

Create `dbt/profiles.yml`:
```yaml
databricks_dbt:
  target: dev
  outputs:
    dev:
      type: databricks
      catalog: main
      schema: analytics
      host: https://dbc-49df519f-3194.cloud.databricks.com
      http_path: /sql/1.0/warehouses/YOUR_WAREHOUSE_HTTP_PATH  # Get from UI
      token: YOUR_DATABRICKS_TOKEN
      threads: 4
```

### 3. Create First Model

Create `dbt/models/example.sql`:
```sql
{{ config(materialized='table') }}

select 1 as id, 'Hello dbt!' as message
```

### 4. Test Locally

```bash
cd dbt
pip install dbt-databricks
dbt debug  # Test connection
dbt run    # Run models
```

### 5. Commit and Push

```bash
git add dbt/
git commit -m "Add dbt project"
git push
```

### 6. Use in Databricks

After pushing, your dbt project will be available at:
```
/Repos/dev/databricks_and_pulumi/dbt/
```

You can:
- Run dbt from a Databricks notebook in the Repo
- Create a Databricks Job to run dbt on a schedule
- Use dbt Cloud connected to your Databricks SQL warehouse

## Full Guide

See `DBT_WITH_REPOS_GUIDE.md` for complete documentation.

