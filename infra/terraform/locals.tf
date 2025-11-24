###############################################################################
# Root locals
# Additional computed values for infra-wide usage (naming, tagging, env logic)
###############################################################################

locals {
  infra_name = "${var.project_name}-${var.environment}"
}
