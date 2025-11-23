###############################################################################
# InvoWise – Terraform Root Module
# Basic main.tf – safe, expandable, no-cost default configuration
###############################################################################



  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend will be enabled later (Phase 5)
  # backend "s3" {}




###############################################################################
# Locals
###############################################################################

locals {
  project     = var.project_name
  environment = var.environment

  tags = merge(
    var.common_tags,
    {
      Project     = local.project
      Environment = local.environment
    }
  )
}

###############################################################################
# Modules / Resources (future)
###############################################################################

# Placeholder for future modules:
# - Backend (S3 + DynamoDB)
# - Analytics backup bucket
# - Scheduled tasks / Lambdas
# - IAM roles

# Example structure:
#
# module "state_backend" {
#   source = "./modules/state-backend"
#   enabled = var.enable_backend
# }


# TODO: wire up state-backend module once backend resources are enabled
#
# module "state_backend" {
#   source       = "./modules/state-backend"
#   project_name = local.project
#   environment  = local.environment
#   tags         = local.tags
#   # enabled only when backend is planned for deployment
# }
