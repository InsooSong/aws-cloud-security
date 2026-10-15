variable "aws_region" {
  description = "AWS Region used for the Terraform lab"
  type        = string
  default     = "ap-northeast-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the study VPC"
  type        = string
  default     = "10.10.0.0/16"
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"

  validation {
    condition = contains(
      ["development", "production"],
      var.environment
    )

    error_message = "Environment must be development or production."
  }
}
