variable "aws_region" {
  description = "Approved AWS deployment Region"
  type        = string
  default     = "ap-northeast-1"

  validation {
    condition = contains(
      [
        "ap-northeast-1",
        "ap-northeast-3"
      ],
      var.aws_region
    )

    error_message = "AWS Region is not approved."
  }
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "development"

  validation {
    condition = contains(
      [
        "development",
        "production"
      ],
      var.environment
    )

    error_message = "Environment must be development or production."
  }
}

variable "vpc_cidr" {
  description = "CIDR block for the secure VPC"
  type        = string
  default     = "10.20.0.0/16"
}

variable "private_subnet_cidr" {
  description = "CIDR block for the private subnet"
  type        = string
  default     = "10.20.10.0/24"
}
