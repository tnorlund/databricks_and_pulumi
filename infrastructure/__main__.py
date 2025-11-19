"""
Main Pulumi program for Databricks infrastructure.

This program manages:
1. SQL Warehouse - for SQL queries, dbt, and Spark SQL
2. Databricks Repos - Git integration for notebooks and dbt projects
3. PySpark Jobs - using serverless compute with notebooks from Repos

Best Practice: Using Databricks Repos (Git integration) instead of managing notebooks directly.
This allows notebooks and dbt projects to be version controlled in Git and synced to Databricks.
"""
import pulumi
import pulumi_databricks as databricks


def main():
    """Main entry point for Pulumi program."""
    stack = pulumi.get_stack()
    databricks_config = pulumi.Config("databricks")
    
    # Configure Databricks provider
    databricks_provider = databricks.Provider(
        f"databricks-provider-{stack}",
        host=databricks_config.require("host"),
        token=databricks_config.get_secret("token"),
    )
    
    # SQL Warehouse - for dbt, SQL queries, and Spark SQL
    # This is used by:
    # - dbt (via dbt-databricks adapter)
    # - SQL queries
    # - BI tools
    sql_warehouse = databricks.SqlEndpoint(
        f"sql-warehouse-{stack}",
        name=f"sql-warehouse-{stack}",
        cluster_size="2X-Small",
        min_num_clusters=1,
        max_num_clusters=1,
        auto_stop_mins=10,
        enable_serverless_compute=True,
        warehouse_type="PRO",
        opts=pulumi.ResourceOptions(provider=databricks_provider),
    )
    
    # Databricks Repo - Git integration (BEST PRACTICE)
    # This syncs your Git repo to Databricks workspace
    # Notebooks and dbt projects stored in Git are automatically synced
    git_repo_url = databricks_config.get("git_repo_url") or "https://github.com/tnorlund/databricks_and_pulumi.git"
    git_branch = databricks_config.get("git_branch") or "main"
    
    databricks_repo = databricks.Repo(
        f"databricks-repo-{stack}",
        url=git_repo_url,
        path=f"/Repos/{stack}/databricks_and_pulumi",
        branch=git_branch,
        opts=pulumi.ResourceOptions(provider=databricks_provider),
    )
    
    # Create PySpark Job using serverless compute
    # Job references notebook from Repo (not /Shared)
    # Notebooks in Git are synced to /Repos/{stack}/repo-name/notebooks/
    example_job = databricks.Job(
        f"example-pyspark-job-{stack}",
        name=f"example-pyspark-job-{stack}",
        tasks=[
            databricks.JobTaskArgs(
                task_key="pyspark_example",
                notebook_task=databricks.JobNotebookTaskArgs(
                    # Reference notebook from Repo (Git-synced)
                    # Path: /Repos/{stack}/databricks_and_pulumi/infrastructure/notebooks/example_pyspark_job
                    notebook_path=pulumi.Output.all(databricks_repo.path).apply(
                        lambda args: f"{args[0]}/infrastructure/notebooks/example_pyspark_job"
                    ),
                ),
                # No existing_cluster_id = uses serverless compute automatically
            ),
        ],
        max_retries=1,
        timeout_seconds=1800,  # 30 minutes
        opts=pulumi.ResourceOptions(
            provider=databricks_provider,
            depends_on=[databricks_repo],  # Job depends on Repo being synced
        ),
    )
    
    # Export outputs
    pulumi.export("sql_warehouse_id", sql_warehouse.id)
    pulumi.export("sql_warehouse_name", sql_warehouse.name)
    pulumi.export("databricks_repo_path", databricks_repo.path)
    pulumi.export("databricks_repo_url", databricks_repo.url)
    pulumi.export("example_job_id", example_job.id)
    pulumi.export("example_job_name", example_job.name)
    pulumi.export("databricks_host", databricks_config.require("host"))
    pulumi.export("stack", stack)
    
    # dbt connection info (SQL warehouse HTTP path needed for dbt)
    # Note: HTTP path is available after warehouse is created
    # Get it from: Databricks UI → SQL Warehouses → Connection details
    pulumi.export("dbt_connection_note", "Get SQL warehouse HTTP path from Databricks UI for dbt profiles.yml")


if __name__ == "__main__":
    main()
