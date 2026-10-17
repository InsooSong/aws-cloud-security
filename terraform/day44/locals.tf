locals {
  common_tags = {
    Project     = "aws-cloud-security"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
