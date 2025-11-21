###############################################################################
# Module: state-backend
#
# Purpose:
#   Future home for:
#   - S3 bucket for Terraform remote state
#   - DynamoDB table for state locking
#   - Optional analytics backup bucket
#
# Currently this module is just a skeleton and does not create any resources.
###############################################################################

terraform {
  required_version = ">= 1.6.0"
}

# Example (to be implemented later):
#
# resource "aws_s3_bucket" "tf_state" {
#   bucket = "${var.project_name}-tf-state"
#   acl    = "private"
#
#   versioning {
#     enabled = true
#   }
#
#   tags = var.tags
# }
#
# resource "aws_dynamodb_table" "tf_locks" {
#   name         = "${var.project_name}-tf-locks"
#   billing_mode = "PAY_PER_REQUEST"
#   hash_key     = "LockID"
#
#   attribute {
#     name = "LockID"
#     type = "S"
#   }
#
#   tags = var.tags
# }
