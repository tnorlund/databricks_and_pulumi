# Setting Up Databricks Asset Bundles

## Step 1: Install Databricks CLI

```bash
# macOS
brew install databricks/tap/databricks

# Verify installation
databricks --version
```

## Step 2: Configure Authentication

```bash
databricks configure --token
```

Enter:
- **Databricks Host**: `https://dbc-49df519f-3194.cloud.databricks.com`
- **Token**: Your Databricks API token

## Step 3: Validate Configuration

```bash
# From repo root
databricks bundle validate
```

This checks your `databricks.yml` for errors.

## Step 4: Deploy Resources

```bash
# Deploy to default (dev) target
databricks bundle deploy

# Or specify target
databricks bundle deploy -t default
```

## Step 5: Verify Deployment

Check in Databricks UI:
- **SQL Warehouses**: SQL → SQL Warehouses → `sql-warehouse-dev`
- **Jobs**: Workflows → Jobs → `example-pyspark-job-dev`

## Common Commands

```bash
# Validate configuration
databricks bundle validate

# Preview changes (dry-run)
databricks bundle deploy --dry-run

# Deploy
databricks bundle deploy

# View bundle info
databricks bundle info

# Run a job
databricks bundle run example_pyspark_job
```

## Troubleshooting

### Error: "bundle not found"
Make sure you're in the repo root where `databricks.yml` exists.

### Error: "authentication failed"
Run `databricks configure --token` again.

### Error: "workspace not found"
Check the `databricks_host` variable in `databricks.yml`.

## Next Steps

1. Add more jobs to `databricks.yml`
2. Set up dbt project in `dbt/` directory
3. Create notebooks in `notebooks/` directory
4. Everything syncs via Repos automatically!

