/*
  This file contains stubs/placeholders for future AWS resources
  required by the InvoWise infrastructure.

  Planned resources (Phase 5 – Integrations):
  - S3 bucket for Terraform remote state
  - DynamoDB table for state locking
  - S3 bucket for monthly analytics backups
  - IAM roles/policies for analytics export automation

  All resources below have "count = 0" so that the module can be
  safely applied in dev/local environments without provisioning
  anything on AWS yet.
*/

locals {
  project = var.project_name != "" ? var.project_name : "invo-wise"
}

# ------------------------------
# S3 bucket for Terraform state
# ------------------------------
resource "aws_s3_bucket" "tf_state" {
  count = 0

  bucket = "${local.project}-tf-state"
  acl    = "private"

  versioning {
    enabled = true
  }

  tags = {
    Name        = "${local.project}-tf-state"
    Environment = var.environment
  }
}

# -----------------------------------
# DynamoDB table for state locking
# -----------------------------------
resource "aws_dynamodb_table" "tf_locks" {
  count = 0

  name         = "${local.project}-tf-locks"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "LockID"

  attribute {
    name = "LockID"
    type = "S"
  }

  tags = {
    Name        = "${local.project}-tf-locks"
    Environment = var.environment
  }
}

# ------------------------------------------------------
# S3 bucket for storing exported analytics (future use)
# ------------------------------------------------------
resource "aws_s3_bucket" "analytics_backups" {
  count = 0

  bucket = "${local.project}-analytics-backups"
  acl    = "private"

  versioning {
    enabled = true
  }

  lifecycle_rule {
    enabled = true

    expiration {
      days = 365
    }
  }

  tags = {
    Name        = "${local.project}-analytics-backups"
    Environment = var.environment
  }
}
