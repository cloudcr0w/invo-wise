# Terraform Infrastructure (InvoWise)

This folder contains the initial Terraform setup for InvoWise.  
It is not fully implemented yet — the goal is to prepare a clean structure for
future AWS-based infrastructure (state backend, S3 backups, DynamoDB locks, etc.).

---

## 📁 File Overview

### `providers.tf`
Defines Terraform providers (currently AWS) and the required versions.  
This is the place where additional providers (e.g. archive, http) will be added.

### `variables.tf`
Input variables for the infrastructure such as AWS region or project name.  
More variables will be added once resources are introduced.

### `outputs.tf`
Contains Terraform outputs.  
Currently a placeholder, waiting for real AWS resources.

### `s3-dynamodb-stubs.tf`
This file is a **placeholder** created for the future Terraform backend setup.

It will hold:

- S3 bucket for Terraform remote state  
- DynamoDB table for state locking  
- (Optional) S3 buckets for analytics backups  
- (Optional) mock/stub resources for local runs

The file is intentionally empty — it documents the plan and avoids confusion
when more infrastructure is added in the next phases.

---

## 🚀 Future Plans (Phase 5 – Integrations)

This Terraform module will eventually manage:

### 1. **Terraform backend**  
```hcl
terraform {
  backend "s3" {
    bucket         = "invo-wise-tf-state"
    key            = "terraform.tfstate"
    region         = "eu-central-1"
    dynamodb_table = "invo-wise-tf-locks"
  }
}
```

### 2. S3 backup bucket

For exported CSV/JSON monthly analytics reports.

### 3. DynamoDB table

For locking + (optional) storing invoice metadata in the future.

### 4. IAM roles

To allow API or scheduled tasks to upload analytics reports to S3.

### 5. Terraform Modules

This folder contains all reusable Terraform modules used by InvoWise.

Currently includes:

- `state-backend/` – future S3 + DynamoDB backend for Terraform state

New modules will be added as infrastructure grows in Phase 5.


### 📝 Notes

This module is intentionally minimal — the application is still in local/dev mode.

Infrastructure work will begin in Phase 5 of the roadmap.

All files are placeholders to keep the repository ready for incremental IaC expansion.