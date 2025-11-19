# Databricks + dbt: Git-Based Infrastructure

Infrastructure as Code for Databricks using **Databricks Asset Bundles** - everything version controlled in Git.

## Architecture

```
Git Repository
├── databricks.yml          # SQL Warehouses + Jobs (YAML, version controlled)
├── resources/              # Job definitions (YAML, version controlled)
├── notebooks/              # PySpark notebooks (version controlled)
└── dbt/                    # dbt project (version controlled)
     ↓ (synced via Databricks Repos)
Databricks Workspace
├── SQL Warehouse           # Managed by Asset Bundles
├── Repos                   # Git integration (set up manually in UI)
└── Jobs                    # Managed by Asset Bundles
```

## Quick Start

### 1. Install Databricks CLI

```bash
# macOS
brew install databricks/tap/databricks

# Or via pip
pip install databricks-cli
```

### 2. Configure Databricks CLI

```bash
databricks configure --token
```

Enter:
- Databricks Host: `https://dbc-49df519f-3194.cloud.databricks.com`
- Token: Your Databricks token

### 3. Set Up Repo (One-Time, in Databricks UI)

1. Go to Databricks Workspace → Repos
2. Click "Add Repo"
3. Connect your GitHub account (if not already connected)
4. Select this repository: `tnorlund/databricks_and_pulumi`
5. Choose branch: `main`
6. Path: `/Repos/dev/databricks_and_pulumi`

### 4. Deploy Resources (Asset Bundles)

```bash
# From repo root
databricks bundle validate
databricks bundle deploy
```

## What's Managed Where

### Databricks Asset Bundles (`databricks.yml`)
- ✅ SQL Warehouses
- ✅ Jobs
- ✅ All in Git (YAML files)

### Git (via Databricks Repos)
- ✅ Notebooks (`notebooks/`)
- ✅ dbt project (`dbt/`)
- ✅ All code version controlled in Git

## Workflow

1. **Edit resources**: Modify `databricks.yml` or `resources/*.yml` (jobs, SQL warehouses)
2. **Edit code**: Modify notebooks or dbt models
3. **Commit**: `git add . && git commit -m "Update job"`
4. **Push**: `git push` (Repos auto-syncs from Git)
5. **Deploy**: `databricks bundle deploy` (deploys jobs and SQL warehouses)

## File Structure

```
databricks_and_pulumi/
├── databricks.yml              # Asset Bundles config
├── resources/                  # Resource definitions
│   └── example_pyspark_job.job.yml
├── notebooks/                  # PySpark notebooks
│   └── example_pyspark_job.py
└── dbt/                        # dbt project (create this)
    ├── dbt_project.yml
    ├── profiles.yml
    └── models/
```

## Adding a New Job

Create a new file `resources/my_new_job.job.yml`:

```yaml
resources:
  jobs:
    my_new_job:
      name: my-new-job-dev
      tasks:
        - task_key: run_notebook
          notebook_task:
            notebook_path: ${var.repo_path}/notebooks/my_notebook.py
          # Serverless compute - no cluster config needed
      timeout_seconds: 1800
```

Then deploy:
```bash
databricks bundle deploy
```

## Resources

- [Databricks Asset Bundles Docs](https://docs.databricks.com/dev-tools/bundles/index.html)
- [dbt-databricks Adapter](https://docs.getdbt.com/reference/warehouse-profiles/databricks-profile)
