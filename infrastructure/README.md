# Databricks Infrastructure with Pulumi

Infrastructure as Code for managing Databricks resources using Pulumi.

## Overview

This Pulumi project manages:
- **SQL Warehouse** - For SQL queries, dbt, and Spark SQL
- **Databricks Repos** - Git integration for notebooks and dbt projects
- **PySpark Jobs** - Using serverless compute

## Architecture

```
GitHub Repo
    ↓ (synced via Databricks Repos)
Databricks Workspace (/Repos/dev/databricks_and_pulumi/)
    ├── infrastructure/     # This Pulumi code
    ├── notebooks/          # PySpark notebooks
    └── dbt/                # dbt project (when created)
         ↓ (connects to)
Databricks SQL Warehouse
    ↓ (executes)
SQL Transformations
```

## Prerequisites

- Python 3.8+
- Pulumi CLI installed ([install guide](https://www.pulumi.com/docs/get-started/install/))
- Databricks account with API token
- Pulumi account ([sign up](https://app.pulumi.com/signup))

## Setup

### 1. Install Dependencies

```bash
cd infrastructure
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Login to Pulumi

```bash
pulumi login
```

### 3. Configure Databricks Credentials

```bash
# Select dev stack
pulumi stack select dev

# Set Databricks workspace URL
pulumi config set databricks:host "https://your-workspace.cloud.databricks.com"

# Set Databricks token (stored securely)
pulumi config set --secret databricks:token "your-databricks-token"
```

**Getting your Databricks token:**
1. Log in to your Databricks workspace
2. Click your user icon → **User Settings**
3. Go to **Access Tokens** tab
4. Click **Generate New Token**
5. Copy the token (you won't see it again!)

### 4. Deploy Infrastructure

```bash
# Preview changes
pulumi preview

# Deploy
pulumi up
```

## Project Structure

```
infrastructure/
├── __main__.py              # Main Pulumi program
├── Pulumi.yaml              # Pulumi project configuration
├── requirements.txt         # Python dependencies
├── notebooks/               # Example notebooks (synced to Databricks)
│   └── example_pyspark_job.py
└── README.md                # This file
```

## Resources Created

- **SQL Warehouse** (`sql-warehouse-dev`) - For dbt and SQL queries
- **Databricks Repo** (`/Repos/dev/databricks_and_pulumi`) - Git integration
- **PySpark Job** (`example-pyspark-job-dev`) - Example serverless job

## Stack Management

### View Current Stack

```bash
pulumi stack
```

### View Stack Outputs

```bash
pulumi stack output
```

### Switch Stacks

```bash
pulumi stack select dev   # Switch to dev
pulumi stack select prod  # Switch to prod (if exists)
```

### View Configuration

```bash
pulumi config
```

## Using with dbt

See `DBT_WITH_REPOS_GUIDE.md` for complete dbt integration guide.

Quick start:
1. Create `dbt/` directory in repo root
2. Initialize dbt project
3. Configure `dbt/profiles.yml` with SQL warehouse HTTP path
4. Run `dbt run` from Databricks notebook or locally

## Common Commands

```bash
# Preview changes
pulumi preview

# Deploy changes
pulumi up

# Destroy resources (careful!)
pulumi destroy

# View logs
pulumi logs

# View stack history
pulumi stack history
```

## Troubleshooting

### Error: "no current project found"
Make sure you're in the `infrastructure/` directory.

### Error: "databricks:host is required"
Configure the Databricks host:
```bash
pulumi config set databricks:host "https://your-workspace.cloud.databricks.com"
```

### Error: "databricks:token is required"
Set the Databricks token:
```bash
pulumi config set --secret databricks:token "your-token"
```

### Repo not syncing in Databricks
1. Check Git credentials in Databricks Settings → Git Integration
2. Manually sync repo in Databricks UI (Workspace → Repos → Sync)

## Documentation

- `GETTING_STARTED.md` - Detailed setup guide
- `SUMMARY.md` - Overview of what's been set up
- `DBT_WITH_REPOS_GUIDE.md` - Complete dbt integration guide

## Next Steps

1. Add your dbt project to the repo
2. Create notebooks in `notebooks/` directory
3. Add more Databricks resources as needed
4. Set up CI/CD for automated deployments

## Resources

- [Pulumi Documentation](https://www.pulumi.com/docs/)
- [Databricks Provider Docs](https://www.pulumi.com/registry/packages/databricks/)
- [dbt-databricks Adapter](https://docs.getdbt.com/reference/warehouse-profiles/databricks-profile)
