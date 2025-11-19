# Getting Started with Databricks and Pulumi

This guide will walk you through setting up your first Databricks resources with Pulumi.

## Step 1: Get Your Databricks Workspace Information

### What is a Databricks Workspace?

A Databricks workspace is your cloud-based environment where you run data analytics and machine learning workloads. Think of it as your "Databricks account" - it's where all your clusters, notebooks, and jobs live.

### Finding Your Workspace URL

1. **Log in to Databricks**: Go to https://databricks.com and sign in
2. **Find your workspace URL**: It looks like one of these:
   - `https://your-workspace.cloud.databricks.com` (AWS)
   - `https://adb-1234567890123456.7.azuredatabricks.net` (Azure)
   - `https://your-workspace.gcp.databricks.com` (GCP)

   The URL is usually shown in your browser's address bar when you're logged in.

### Creating a Databricks Access Token

You need a token to authenticate Pulumi with Databricks:

1. **In Databricks**, click your **user icon** (top right corner)
2. Click **User Settings**
3. Go to the **Access Tokens** tab
4. Click **Generate New Token**
5. Give it a description (e.g., "Pulumi Infrastructure")
6. Set an expiration (or leave blank for no expiration)
7. Click **Generate**
8. **Copy the token immediately** - you won't be able to see it again!

   The token looks like: `dapiXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX`

## Step 2: Configure Pulumi with Your Databricks Credentials

Now let's configure your Pulumi stack with your Databricks information:

```bash
cd infrastructure
source venv/bin/activate  # Activate virtual environment if not already active

# Make sure you're on the dev stack
pulumi stack select dev

# Set your Databricks workspace URL
pulumi config set databricks:host "https://your-workspace.cloud.databricks.com"
# Replace with your actual workspace URL!

# Set your Databricks token (this is stored securely, encrypted)
pulumi config set --secret databricks:token "dapi1234567890abcdef..."
# Replace with your actual token!
```

### Verify Your Configuration

```bash
# View your configuration (token will be hidden)
pulumi config

# You should see:
# databricks:host: https://your-workspace.cloud.databricks.com
# databricks:token: [secret]
```

## Step 3: Understand What Resources You Can Create

The current `__main__.py` creates two basic resources:

### 1. Databricks Cluster
A **cluster** is a group of computers (nodes) that run your Spark jobs. Think of it as your "compute engine."

- **What it does**: Runs notebooks, jobs, and Spark workloads
- **When to use**: For running Python/Scala notebooks, Spark jobs, or interactive analysis
- **Cost**: You pay for compute time while it's running

### 2. SQL Warehouse
A **SQL warehouse** is a compute resource optimized for running SQL queries. It's what dbt uses.

- **What it does**: Runs SQL queries (like what dbt sends)
- **When to use**: For SQL-based transformations, BI tools, or dbt
- **Cost**: You pay for compute time while queries are running

## Step 4: Preview What Will Be Created

Before deploying, see what Pulumi will create:

```bash
pulumi preview
```

This shows you:
- What resources will be created
- Their configuration
- Any potential issues

**Don't worry if you see errors about missing configuration** - that's normal if you haven't set your credentials yet!

## Step 5: Deploy Your First Resources

Once your configuration is set, deploy:

```bash
pulumi up
```

Pulumi will:
1. Show you a preview of what will be created
2. Ask for confirmation (type `yes`)
3. Create the resources in Databricks
4. Show you the outputs (like cluster IDs)

### Example Output

```
Updating (dev)

     Type                          Name                      Status
 +   pulumi:pulumi:Stack          databricks-infrastructure-dev  created
 +   ├─ databricks:index:Provider databricks-provider-dev    created
 +   ├─ databricks:core:Cluster   databricks-cluster-dev     created
 +   └─ databricks:sql:SqlEndpoint sql-warehouse-dev         created

Outputs:
    cluster_id        : "1234-567890-abc123"
    cluster_name      : "databricks-cluster-dev"
    sql_warehouse_id  : "abc123def456"
    stack             : "dev"
    databricks_host   : "https://your-workspace.cloud.databricks.com"

Resources:
    + 4 created

Duration: 2m30s
```

## Step 6: Verify in Databricks UI

After deployment, check your Databricks workspace:

1. **For the Cluster**:
   - Go to **Compute** → **Clusters** in the Databricks UI
   - You should see `databricks-cluster-dev`

2. **For the SQL Warehouse**:
   - Go to **SQL** → **SQL Warehouses** in the Databricks UI
   - You should see `sql-warehouse-dev`

## Common Databricks Concepts

### Clusters vs SQL Warehouses

| Feature | Cluster | SQL Warehouse |
|---------|---------|---------------|
| **Use Case** | Python/Scala notebooks, Spark jobs | SQL queries, dbt, BI tools |
| **Language** | Python, Scala, R, SQL | SQL only |
| **Best For** | Data engineering, ML, complex processing | Analytics, reporting, dbt |
| **Cost** | Pay while running | Pay per query (can auto-stop) |

### Node Types

Node types determine the size of your compute:

- **Small**: `i3.xlarge` - Good for development, testing
- **Medium**: `i3.2xlarge` - Good for production workloads
- **Large**: `i3.4xlarge` - For heavy workloads

The current setup uses:
- **Dev**: `i3.xlarge` with 1 worker (cheaper, good for testing)
- **Prod**: `i3.2xlarge` with 4 workers (more powerful, for production)

## Next Steps: Adding More Resources

Once you have clusters and SQL warehouses working, you can add:

### 1. Databricks Jobs
Jobs run notebooks or scripts on a schedule or on-demand.

```python
# Example: Add to __main__.py
job = databricks.Job(
    f"my-job-{stack}",
    name=f"my-job-{stack}",
    existing_cluster_id=cluster.cluster_id,
    notebook_task=databricks.JobNotebookTaskArgs(
        notebook_path="/Shared/my-notebook",
    ),
    schedule=databricks.JobScheduleArgs(
        quartz_cron_expression="0 0 * * * ?",  # Daily at midnight
        timezone_id="America/New_York",
    ),
    opts=pulumi.ResourceOptions(provider=databricks_provider),
)
```

### 2. Notebooks
Store and version control your Python/Scala code.

### 3. Secrets
Store sensitive information (API keys, passwords).

### 4. Libraries
Install Python packages on your clusters.

### 5. Permissions
Control who can access what.

## Troubleshooting

### Error: "Invalid host"
- Make sure your workspace URL is correct
- It should start with `https://` and end with `.databricks.com` or `.azuredatabricks.net`

### Error: "Invalid token"
- Your token might have expired
- Generate a new token in Databricks
- Make sure you copied the entire token (they're long!)

### Error: "Permission denied"
- Your token might not have the right permissions
- Make sure you're using a token from an account with admin/workspace permissions

### Resources not showing in Databricks UI
- Wait a minute or two - resources take time to appear
- Refresh your browser
- Check that you're looking at the correct workspace

## Getting Help

- **Pulumi Docs**: https://www.pulumi.com/docs/
- **Databricks Docs**: https://docs.databricks.com/
- **Pulumi Databricks Provider**: https://www.pulumi.com/registry/packages/databricks/

## Quick Reference Commands

```bash
# View current stack
pulumi stack

# Switch stacks
pulumi stack select dev
pulumi stack select prod

# View configuration
pulumi config

# View outputs (after deployment)
pulumi stack output

# Preview changes
pulumi preview

# Deploy changes
pulumi up

# Destroy resources (be careful!)
pulumi destroy
```

