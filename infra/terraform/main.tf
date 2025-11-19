###############################################################################
# InvoWise – Terraform Root Module
# Basic main.tf – safe, expandable, no-cost default configuration
###############################################################################

terraform {
  required_version = ">= 1.6.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Backend will be enabled later (Phase 5)
  # backend "s3" {}
}

provider "aws" {
  region = var.aws_region
}

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

###############################################################################
# Outputs (empty for now)
###############################################################################

output "invo_wise_environment" {
  value       = local.environment
  description = "Current selected environment for the infrastructure."
}
