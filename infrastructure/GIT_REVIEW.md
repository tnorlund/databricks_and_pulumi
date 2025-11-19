# Git Commit Review: What Should Be Committed?

## Summary

This document reviews all files created and categorizes them for git commits.

## ✅ SHOULD COMMIT (Core Infrastructure)

### Essential Files
- **`__main__.py`** - Main Pulumi infrastructure code (manages SQL warehouse, Repos, Jobs)
- **`Pulumi.yaml`** - Pulumi project configuration
- **`requirements.txt`** - Python dependencies
- **`notebooks/example_pyspark_job.py`** - Example notebook (referenced by jobs)

### Useful Documentation
- **`GETTING_STARTED.md`** - Setup guide for new users
- **`SUMMARY.md`** - Overview of what's been set up
- **`DBT_WITH_REPOS_GUIDE.md`** - Complete guide for dbt + Repos integration
- **`QUICK_START_DBT.md`** - Quick start for dbt

## ❌ DO NOT COMMIT (Secrets & Sensitive)

- **`Pulumi.dev.yaml`** - Contains encrypted Databricks token (even if encrypted, best practice is to not commit)
  - **Action**: Add to `.gitignore`
  - **Note**: Each developer should create their own with `pulumi config set`

## ❌ DO NOT COMMIT (Temporary/Debug Scripts)

These were created for troubleshooting and aren't needed long-term:

- **`check_repo_status.py`** - Temporary script to check repo status
- **`check_and_sync_repo.py`** - Temporary script to sync repo
- **`sync_repo.py`** - Another temporary sync script
- **`create_notebook.py`** - Script to create notebook via API (not needed with Repos)
- **`get_cluster_id.py`** - Helper script (not needed)
- **`get_warehouse_id.py`** - Helper script (not needed)

**Action**: Delete these or add to `.gitignore`

## ❌ DO NOT COMMIT (Duplicate/Experimental Files)

- **`example_pyspark_job.py`** - Duplicate of `notebooks/example_pyspark_job.py`
- **`pyspark_job_example.py`** - Another duplicate/experimental file
- **`repos_example.py`** - Example code that's now integrated into `__main__.py`

**Action**: Delete these

## ⚠️ MAYBE COMMIT (Review First)

### Documentation (Some May Be Redundant)
- **`BEST_PRACTICES.md`** - Good reference, but overlaps with other docs
- **`NOTEBOOK_MANAGEMENT_GUIDE.md`** - Useful, but info is in other guides
- **`REPO_SETUP.md`** - Useful setup guide
- **`TROUBLESHOOT_REPO.md`** - Useful troubleshooting
- **`QUICK_FIX_REPO.md`** - Quick reference (may be redundant)

### Code Examples
- **`examples.py`** - Code snippets/examples (could be useful reference, but not essential)

### Historical/Context Docs (Probably Don't Need)
- **`CHECK_WORKSPACE_TYPE.md`** - Historical troubleshooting
- **`CREATE_CLUSTER_MANUALLY.md`** - Historical instructions
- **`IMPORT_SQL_WAREHOUSE.md`** - Historical instructions
- **`MANUAL_SETUP.md`** - Historical instructions
- **`PYSPARK_SERVERLESS_GUIDE.md`** - Info is in other guides
- **`SERVERLESS_WORKSPACE_GUIDE.md`** - Info is in other guides
- **`SPARK_JOBS_SETUP.md`** - Info is in other guides
- **`UPGRADE_INSTRUCTIONS.md`** - Historical context
- **`QUICK_START.md`** - May be redundant with GETTING_STARTED.md
- **`README.md`** - Check if it's useful or just placeholder

## Recommended Actions

### 1. Update `.gitignore`

Add these to `.gitignore`:
```
# Pulumi secrets (even if encrypted)
Pulumi.*.yaml

# Temporary scripts
check_*.py
sync_*.py
create_notebook.py
get_*_id.py
```

### 2. Delete Temporary Files

```bash
cd infrastructure
rm check_repo_status.py check_and_sync_repo.py sync_repo.py
rm create_notebook.py get_cluster_id.py get_warehouse_id.py
rm example_pyspark_job.py pyspark_job_example.py repos_example.py
```

### 3. Keep Essential Docs

Keep these documentation files:
- `GETTING_STARTED.md`
- `SUMMARY.md`
- `DBT_WITH_REPOS_GUIDE.md`
- `QUICK_START_DBT.md`
- `REPO_SETUP.md` (useful for team)

### 4. Consider Consolidating Docs

Many docs overlap. Consider:
- Merging `QUICK_START_DBT.md` into `DBT_WITH_REPOS_GUIDE.md`
- Keeping `SUMMARY.md` as the main overview
- Deleting historical troubleshooting docs

## Minimal Commit Set

If you want to keep it minimal, commit only:

```
infrastructure/
├── __main__.py              # Core infrastructure
├── Pulumi.yaml              # Project config
├── requirements.txt        # Dependencies
├── notebooks/
│   └── example_pyspark_job.py
├── GETTING_STARTED.md       # Setup guide
└── SUMMARY.md               # Overview
```

Everything else can be added later as needed.

## Questions to Consider

1. **Do you want all the documentation?** - Some is redundant, some is historical
2. **Do you want example code?** - `examples.py` has snippets that might be useful
3. **Do you want troubleshooting guides?** - Useful for future issues, but adds clutter
4. **Do you want a README?** - Should create a proper README.md for the repo

## Next Steps

1. Review this document
2. Decide which docs to keep
3. Delete temporary files
4. Update `.gitignore`
5. Commit the essential files
6. Add other files incrementally as needed

