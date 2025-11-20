###############################################################################
# Root module outputs
###############################################################################

output "invo_wise_environment" {
  value       = local.environment
  description = "Current selected environment for the InvoWise infrastructure."
}

# Future examples:
#
# output "state_bucket_name" {
#   value       = aws_s3_bucket.tf_state[0].bucket
#   description = "Name of the S3 bucket used for Terraform state."
#   sensitive   = false
# }
#
# output "analytics_backups_bucket" {
#   value       = aws_s3_bucket.analytics_backups[0].bucket
#   description = "Bucket for storing exported analytics snapshots."
#   sensitive   = false
# }
