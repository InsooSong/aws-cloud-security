# Day 44 — Terraform Security Configuration

## Topic

Secure AWS Infrastructure with Terraform — Least Privilege, S3 Security, KMS Encryption, IAM Controls, and Terraform Validation

---

## Objectives

- Understand secure-by-default Infrastructure as Code
- Apply least privilege to Security Groups
- Prevent unnecessary public network exposure
- Configure S3 Block Public Access
- Configure S3 encryption with AWS KMS
- Understand KMS key rotation and key policies
- Apply least privilege to IAM roles and policies
- Use Terraform variable validation
- Understand resource preconditions and postconditions
- Understand Terraform check blocks
- Distinguish syntax validation from security validation
- Understand secure state handling
- Build a small secure AWS Terraform configuration
- Connect Terraform preventive controls with boto3 detective controls

---

# Secure Infrastructure as Code

## 1. Security as Code

Infrastructure as Code allows security controls to be defined before infrastructure is deployed.

Traditional model:

```text
Deploy Infrastructure
       ↓
Security Review
       ↓
Fix Problems
```

Secure IaC model:

```text
Security Requirements
       ↓
Terraform Configuration
       ↓
Review
       ↓
Deploy Secure Infrastructure
```

---

## 2. Secure by Default

A strong Terraform configuration should make the secure option the easiest option.

Examples:

```text
S3 Public Access
→ Blocked by Default

S3 Encryption
→ Enabled by Default

Security Groups
→ Minimal Inbound Rules

IAM
→ Least Privilege

Logging
→ Enabled

Tags
→ Standardized
```

---

# Defense in Depth

## 3. Terraform Is One Layer

Terraform can define:

```text
Network Controls

Encryption

IAM

Logging

Resource Policies
```

But Terraform alone does not replace:

```text
GuardDuty

Inspector

CloudTrail

AWS Config

Security Hub

Runtime Monitoring
```

Conceptually:

```text
Terraform
→ Preventive Control

AWS Security Services
→ Detective Controls

Automation
→ Response
```

---

# Network Security

## 4. Least Privilege Security Groups

Security Groups should allow only required traffic.

Poor:

```hcl
cidr_blocks = ["0.0.0.0/0"]
```

for administrative ports.

Better:

```text
Specific Source CIDR

or

Security Group Reference
```

---

## 5. Sensitive Ports

Examples:

```text
22
→ SSH

3389
→ RDP

3306
→ MySQL

5432
→ PostgreSQL
```

These should generally not be exposed directly to:

```text
0.0.0.0/0

or

::/0
```

without a deliberate security requirement.

---

## 6. Security Group Reference

A safer application pattern:

```text
Internet
   |
   v
ALB Security Group
   |
   v
Application Security Group
   |
   v
Database Security Group
```

Instead of:

```text
Internet
   |
   v
Database
```

---

# Security Group Example

## 7. Application Security Group

Example:

```hcl
resource "aws_security_group" "app" {
  name        = "day44-app-sg"
  description = "Security group for application resources"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "Allow HTTPS from ALB"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [
      aws_security_group.alb.id
    ]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }

  tags = local.common_tags
}
```

This is better than allowing the application directly from every internet source.

---

# S3 Security

## 8. S3 Security Controls

Important S3 controls include:

```text
Block Public Access

Encryption

Bucket Policy

Versioning

Logging

Access Monitoring
```

Day 44 focuses on:

```text
Block Public Access

SSE-KMS
```

---

## 9. S3 Block Public Access

Terraform:

```hcl
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}
```

The four controls are:

```text
BlockPublicAcls

IgnorePublicAcls

BlockPublicPolicy

RestrictPublicBuckets
```

---

## 10. Why All Four?

They protect against public access being introduced through:

```text
ACLs

Bucket Policies

Future Configuration Changes
```

The goal is:

```text
Public Access
→ Explicit Exception

not

Default Behavior
```

---

# S3 Bucket

## 11. Create Secure Bucket

Example:

```hcl
resource "aws_s3_bucket" "secure" {
  bucket_prefix = "day44-secure-"

  tags = merge(
    local.common_tags,
    {
      Name = "day44-secure-bucket"
    }
  )
}
```

Using:

```text
bucket_prefix
```

avoids requiring a globally unique hard-coded bucket name.

---

# Versioning

## 12. Enable Versioning

```hcl
resource "aws_s3_bucket_versioning" "secure" {
  bucket = aws_s3_bucket.secure.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

Versioning can help protect against:

```text
Accidental Deletion

Overwrite

Recovery Requirements
```

---

# KMS

## 13. Why Use SSE-KMS?

Amazon S3 already provides encryption by default.

SSE-KMS can add:

```text
Customer-Controlled Key Policy

Detailed KMS Auditability

Key Lifecycle Management

Access Separation
```

Use it when those controls are required.

---

## 14. KMS Key

Example:

```hcl
resource "aws_kms_key" "s3" {
  description = "KMS key for Day 44 secure S3 bucket"

  enable_key_rotation = true

  tags = merge(
    local.common_tags,
    {
      Name = "day44-s3-key"
    }
  )
}
```

---

## 15. KMS Alias

```hcl
resource "aws_kms_alias" "s3" {
  name          = "alias/day44-s3"
  target_key_id = aws_kms_key.s3.key_id
}
```

Aliases make keys easier to identify.

---

# S3 SSE-KMS

## 16. Bucket Encryption

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm     = "aws:kms"
      kms_master_key_id = aws_kms_key.s3.arn
    }

    bucket_key_enabled = true
  }
}
```

This configures:

```text
S3
  ↓
SSE-KMS
  ↓
Customer-Managed KMS Key
```

---

## 17. S3 Bucket Keys

S3 Bucket Keys can reduce the number of requests from S3 to KMS.

Conceptually:

```text
Without Bucket Key
S3 Objects
→ Frequent KMS Requests

With Bucket Key
S3 Bucket Key
→ Reduced KMS Request Volume
```

They can reduce SSE-KMS cost for appropriate workloads.

---

# Encryption Reality

## 18. SSE-S3 Is Still Encryption

Important:

```text
SSE-S3
≠
Unencrypted
```

Amazon S3 already encrypts new objects with SSE-S3 by default.

SSE-KMS is used when more control over:

```text
Key Access

Key Lifecycle

Audit

Separation of Duties
```

is required.

---

# S3 SSE-C Update

## 19. Modern S3 Security

For modern S3 general-purpose buckets, SSE-C is disabled by default unless deliberately enabled.

For most workloads prefer:

```text
SSE-S3

or

SSE-KMS
```

rather than customer-provided encryption keys.

---

# KMS Permissions

## 20. KMS and S3 Permissions

SSE-KMS requires appropriate permissions.

For uploads:

```text
kms:GenerateDataKey
```

is commonly needed.

For reading encrypted objects:

```text
kms:Decrypt
```

is required.

Permissions should be limited to principals that actually need access.

---

# IAM Least Privilege

## 21. Avoid Wildcards

Poor:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

Better:

```text
Specific Actions

Specific Resources

Conditions
```

---

## 22. Terraform IAM Policy

Terraform can create policy documents with:

```text
aws_iam_policy_document
```

Example:

```hcl
data "aws_iam_policy_document" "s3_read" {
  statement {
    effect = "Allow"

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.secure.arn}/*"
    ]
  }
}
```

---

## 23. Why Policy Document Data Source?

Compared with a large raw JSON string:

```text
Terraform Policy Document
→ Easier References
→ Easier Review
→ Better Composition
```

It also allows direct references to Terraform-managed resources.

---

# IAM Role

## 24. Trust Policy

Example:

```hcl
data "aws_iam_policy_document" "example_assume_role" {
  statement {
    effect = "Allow"

    principals {
      type = "Service"

      identifiers = [
        "ec2.amazonaws.com"
      ]
    }

    actions = [
      "sts:AssumeRole"
    ]
  }
}
```

---

## 25. Role

```hcl
resource "aws_iam_role" "example" {
  name = "day44-example-role"

  assume_role_policy = data.aws_iam_policy_document.example_assume_role.json

  tags = local.common_tags
}
```

Remember:

```text
Trust Policy
→ Who can assume?

Permission Policy
→ What can it do?
```

---

# Variable Validation

## 26. Restrict Regions

Example:

```hcl
variable "aws_region" {
  description = "Approved AWS Region"
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

    error_message = "Only approved AWS Regions may be used."
  }
}
```

This provides an early guardrail.

---

## 27. Environment Validation

```hcl
variable "environment" {
  type = string

  validation {
    condition = contains(
      [
        "development",
        "production"
      ],
      var.environment
    )

    error_message = "Invalid environment."
  }
}
```

---

# Preconditions

## 28. What Is a Precondition?

A precondition verifies an assumption before Terraform completes the associated operation.

Conceptually:

```text
Configuration
      ↓
Precondition
      |
   Pass?
   /   \
 Yes    No
 |      |
Continue Stop
```

---

## 29. Example Precondition

Example concept:

```hcl
lifecycle {
  precondition {
    condition = (
      var.environment != "production"
      || var.aws_region == "ap-northeast-1"
    )

    error_message = "Production resources must be deployed in the approved production Region."
  }
}
```

This can block an invalid configuration before deployment.

---

# Postconditions

## 30. Postcondition

A postcondition validates a result after a resource or data source operation.

Conceptually:

```text
Create / Read Resource
        ↓
Postcondition
        ↓
Expected State?
```

This can validate assumptions about the resulting infrastructure.

---

# Check Blocks

## 31. Terraform Check

Terraform supports:

```hcl
check "name" {
  assert {
    condition     = ...
    error_message = "..."
  }
}
```

Checks can validate infrastructure assumptions.

---

## 32. Important Check Behavior

A failed `check` assertion:

```text
Produces Warning

Does Not Automatically Block
Plan / Apply
```

This is different from:

```text
Variable Validation

Preconditions
```

which can prevent an invalid operation.

---

## 33. Validation Types

Remember:

```text
Variable Validation
→ Validate input

Precondition
→ Block invalid resource assumptions

Postcondition
→ Validate resource outcome

Check Block
→ Ongoing infrastructure assertion
```

---

# Security Validation

## 34. terraform validate

`terraform validate` checks:

```text
Terraform Syntax

Internal Configuration Consistency
```

It does not determine:

```text
Is this Security Group safe?

Is this IAM policy least privilege?

Should this bucket be public?
```

---

## 35. Security Testing Layers

A stronger workflow:

```text
terraform fmt
      ↓
terraform validate
      ↓
terraform plan
      ↓
Security Review
      ↓
Static IaC Security Scanner
      ↓
terraform apply
      ↓
Runtime / AWS Security Verification
```

Possible external tools include:

```text
Checkov

Trivy

tfsec-compatible workflows

OPA / Policy as Code
```

Tool choice depends on environment and pipeline.

---

# Secure Terraform State

## 36. State Security

Terraform state can contain:

```text
Resource IDs

ARNs

Policies

Configuration

Sensitive Values
```

Protect:

```text
terraform.tfstate

terraform.tfstate.backup
```

---

## 37. Local Learning

For Day 44:

```text
Local State
+
.gitignore
```

is acceptable.

For shared production environments:

```text
Secure Remote Backend
+
Access Control
+
Encryption
+
Locking
+
Versioning
```

should be considered.

---

# Secure Terraform Project

## 38. Suggested Structure

```text
terraform/
└── day44/
    ├── versions.tf
    ├── provider.tf
    ├── variables.tf
    ├── locals.tf
    ├── network.tf
    ├── kms.tf
    ├── s3.tf
    ├── iam.tf
    ├── checks.tf
    └── outputs.tf
```

Separating by responsibility makes security review easier.

---

# versions.tf

## 39. Terraform and AWS Provider

```hcl
terraform {
  required_version = ">= 1.10.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 6.0"
    }
  }
}
```

---

# provider.tf

## 40. Provider

```hcl
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = local.common_tags
  }
}
```

Default tags can help standardize resource ownership and environment metadata.

---

# variables.tf

## 41. Variables

```hcl
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
```

---

# locals.tf

## 42. Common Tags

```hcl
locals {
  common_tags = {
    Project     = "aws-cloud-security"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

---

# network.tf

## 43. VPC

```hcl
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true
}
```

---

## 44. Private Subnet

```hcl
resource "aws_subnet" "private" {
  vpc_id = aws_vpc.main.id

  cidr_block = "10.20.10.0/24"

  map_public_ip_on_launch = false

  tags = {
    Name = "day44-private-subnet"
  }
}
```

Important:

```text
map_public_ip_on_launch = false
```

prevents automatic public IPv4 assignment to resources launched in the subnet.

---

## 45. Internal Security Group

```hcl
resource "aws_security_group" "internal" {
  name        = "day44-internal-sg"
  description = "Internal application traffic only"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from within the VPC"

    from_port = 443
    to_port   = 443
    protocol  = "tcp"

    cidr_blocks = [
      var.vpc_cidr
    ]
  }

  egress {
    from_port = 0
    to_port   = 0
    protocol  = "-1"

    cidr_blocks = [
      "0.0.0.0/0"
    ]
  }
}
```

No inbound:

```text
0.0.0.0/0
```

is configured.

---

# kms.tf

## 46. KMS Key

```hcl
resource "aws_kms_key" "s3" {
  description = "KMS key for secure S3 storage"

  enable_key_rotation = true
}
```

---

## 47. Alias

```hcl
resource "aws_kms_alias" "s3" {
  name = "alias/day44-secure-s3"

  target_key_id = aws_kms_key.s3.key_id
}
```

---

# s3.tf

## 48. S3 Bucket

```hcl
resource "aws_s3_bucket" "secure" {
  bucket_prefix = "day44-secure-"
}
```

---

## 49. Public Access Block

```hcl
resource "aws_s3_bucket_public_access_block" "secure" {
  bucket = aws_s3_bucket.secure.id

  block_public_acls       = true
  ignore_public_acls      = true
  block_public_policy     = true
  restrict_public_buckets = true
}
```

---

## 50. Versioning

```hcl
resource "aws_s3_bucket_versioning" "secure" {
  bucket = aws_s3_bucket.secure.id

  versioning_configuration {
    status = "Enabled"
  }
}
```

---

## 51. SSE-KMS

```hcl
resource "aws_s3_bucket_server_side_encryption_configuration" "secure" {
  bucket = aws_s3_bucket.secure.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "aws:kms"

      kms_master_key_id = aws_kms_key.s3.arn
    }

    bucket_key_enabled = true
  }
}
```

---

# IAM

## 52. Least Privilege Policy

Example:

```hcl
data "aws_iam_policy_document" "s3_read" {
  statement {
    sid    = "ReadSecureBucket"
    effect = "Allow"

    actions = [
      "s3:GetObject"
    ]

    resources = [
      "${aws_s3_bucket.secure.arn}/*"
    ]
  }

  statement {
    sid    = "DecryptSecureBucketObjects"
    effect = "Allow"

    actions = [
      "kms:Decrypt"
    ]

    resources = [
      aws_kms_key.s3.arn
    ]
  }
}
```

---

## 53. IAM Policy

```hcl
resource "aws_iam_policy" "s3_read" {
  name = "day44-secure-s3-read"

  policy = data.aws_iam_policy_document.s3_read.json
}
```

Notice:

```text
No s3:*

No kms:*

No Resource: *
```

---

# checks.tf

## 54. Region Check

Example:

```hcl
check "approved_region" {
  assert {
    condition = contains(
      [
        "ap-northeast-1",
        "ap-northeast-3"
      ],
      var.aws_region
    )

    error_message = "Deployment Region is outside the approved list."
  }
}
```

Variable validation already blocks the same condition, so this is mainly an example of check syntax.

---

## 55. Public Access Check

Conceptually:

```hcl
check "s3_public_access_block" {
  assert {
    condition = (
      aws_s3_bucket_public_access_block.secure.block_public_acls
      &&
      aws_s3_bucket_public_access_block.secure.ignore_public_acls
      &&
      aws_s3_bucket_public_access_block.secure.block_public_policy
      &&
      aws_s3_bucket_public_access_block.secure.restrict_public_buckets
    )

    error_message = "All S3 Block Public Access settings should be enabled."
  }
}
```

Remember:

```text
check failure
→ Warning

not
→ Apply automatically blocked
```

---

# outputs.tf

## 56. Outputs

```hcl
output "vpc_id" {
  description = "Secure VPC ID"
  value       = aws_vpc.main.id
}

output "private_subnet_id" {
  description = "Private subnet ID"
  value       = aws_subnet.private.id
}

output "s3_bucket_name" {
  description = "Secure S3 bucket name"
  value       = aws_s3_bucket.secure.id
}

output "kms_key_arn" {
  description = "KMS key ARN used by the secure bucket"
  value       = aws_kms_key.s3.arn
}
```

Be careful with outputs because they are also represented in Terraform state.

---

# Terraform Workflow

## 57. Verify Identity

Before running Terraform:

```bash
aws sts get-caller-identity
```

---

## 58. Initialize

```bash
terraform init
```

---

## 59. Format

```bash
terraform fmt -recursive
```

---

## 60. Validate

```bash
terraform validate
```

---

## 61. Plan

```bash
terraform plan
```

Review:

```text
Public Access?

Security Group Rules?

KMS?

IAM Wildcards?

Unexpected Resources?

Destroy / Replace?
```

---

## 62. Apply

Only if expected:

```bash
terraform apply
```

---

## 63. Verify

Use AWS CLI or boto3.

Examples:

```bash
aws s3api get-public-access-block \
  --bucket <bucket-name>
```

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name>
```

```bash
aws ec2 describe-security-groups \
  --group-ids <group-id>
```

---

# Terraform + boto3

## 64. Preventive + Detective Controls

Day 44 Terraform:

```text
Prevent insecure configuration
```

Day 42 boto3 scanner:

```text
Detect insecure configuration
```

Together:

```text
Terraform
→ Secure Default

boto3
→ Verify Runtime State
```

---

## 65. Why Both?

Terraform may say:

```text
Secure Configuration
```

but real AWS can experience:

```text
Manual Change

Configuration Drift

External Automation

Incorrect Permissions
```

Therefore:

```text
IaC
+
Runtime Verification
```

is stronger than either alone.

---

# Common Security Mistakes

## 66. Public SSH

Avoid:

```hcl
from_port = 22
to_port   = 22

cidr_blocks = [
  "0.0.0.0/0"
]
```

unless there is a deliberate, reviewed requirement.

---

## 67. Public Databases

Avoid public access for:

```text
3306

5432

1433

1521
```

in normal application architectures.

---

## 68. IAM Wildcards

Avoid unnecessary:

```text
Action = "*"

Resource = "*"
```

Use least privilege.

---

## 69. S3 Without Public Access Guardrails

Do not depend only on:

```text
"We will not create a public bucket policy."
```

Add explicit preventive controls.

---

## 70. KMS Permissions Too Broad

Poor:

```text
kms:*
Resource: *
```

Better:

```text
Specific KMS Actions

Specific Key ARN
```

---

## 71. Security by Naming

Do not assume:

```text
private-subnet
```

means:

```text
Actually Private
```

Verify:

```text
Route Tables

Public IP Settings

Internet Gateway Paths
```

Security comes from configuration, not resource names.

---

## 72. Checks Without Enforcement

Remember:

```text
Terraform check
→ Warning
```

A critical invariant that must prevent deployment may be better implemented using:

```text
Variable Validation

Precondition

Policy-as-Code

CI Gate
```

depending on the requirement.

---

# Hands-on Practice

## 73. Create Day 44 Directory

```bash
mkdir -p terraform/day44
```

Create:

```text
versions.tf

provider.tf

variables.tf

locals.tf

network.tf

kms.tf

s3.tf

iam.tf

checks.tf

outputs.tf
```

---

## 74. Initialize

```bash
cd terraform/day44

terraform init
```

---

## 75. Validate

```bash
terraform fmt -recursive

terraform validate
```

---

## 76. Review Security Plan

```bash
terraform plan
```

Review:

```text
No Public Administrative Ports

S3 BPA Enabled

SSE-KMS Enabled

KMS Rotation Enabled

No Broad IAM Wildcards
```

---

## 77. Deploy Lab

If authorized:

```bash
terraform apply
```

---

## 78. Verify S3 Security

```bash
aws s3api get-public-access-block \
  --bucket <bucket-name>
```

Expected:

```text
All Four Settings
→ true
```

---

## 79. Verify Encryption

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name>
```

Expected:

```text
aws:kms
```

and the intended KMS key.

---

## 80. Verify Network

```bash
aws ec2 describe-security-groups \
  --group-ids <group-id>
```

Confirm:

```text
No Unintended
0.0.0.0/0
or
::/0
Inbound Rule
```

---

## 81. Run Day 42 Scanner

After deployment:

```bash
python scripts/security_scan.py
```

Compare scanner findings with the intended Terraform configuration.

This creates a useful:

```text
Prevent
+
Verify
```

exercise.

---

## 82. Cleanup

When complete:

```bash
terraform destroy
```

Review the destroy plan before confirming.

---

# Security Checklist

```text
[ ] AWS identity is verified before Terraform operations

[ ] Terraform configuration uses secure defaults

[ ] Public administrative ports are not exposed unnecessarily

[ ] Private workloads do not receive public IP addresses by default

[ ] S3 Block Public Access enables all required settings

[ ] S3 encryption requirements are explicit

[ ] SSE-S3 is understood as valid encryption

[ ] SSE-KMS is used when additional key control is required

[ ] KMS key rotation is enabled where appropriate

[ ] KMS access follows least privilege

[ ] IAM policies avoid unnecessary wildcards

[ ] IAM trust and permission policies are reviewed separately

[ ] Region values are validated

[ ] Environment values are validated

[ ] Preconditions are used for critical configuration assumptions where appropriate

[ ] Check blocks are understood as non-blocking warnings

[ ] terraform validate is not treated as a security scanner

[ ] terraform plan is reviewed for security-impacting changes

[ ] Terraform state is protected

[ ] Generated plan files are protected

[ ] Runtime configuration is verified after deployment

[ ] boto3 or AWS security services are used for detective validation

[ ] Lab resources are destroyed when no longer required
```

---

## Key Takeaways

- Terraform can implement preventive security controls before AWS resources are deployed.
- Secure-by-default configuration reduces the chance of manual misconfiguration.
- Security Groups should follow least privilege and avoid unnecessary internet exposure.
- S3 Block Public Access provides an explicit public-access guardrail.
- Amazon S3 already encrypts objects by default with SSE-S3.
- SSE-KMS provides additional control over encryption keys and permissions.
- KMS permissions should be narrowly scoped.
- IAM policies should avoid unnecessary wildcards.
- Terraform variable validation can prevent invalid input.
- Preconditions can block invalid infrastructure assumptions.
- Terraform check blocks provide non-blocking assertions and ongoing validation.
- `terraform validate` validates Terraform configuration, not security posture.
- Terraform state remains security-sensitive even when values are marked sensitive.
- Secure IaC should be combined with runtime verification and detective security controls.
- Terraform and boto3 complement each other as preventive and detective security mechanisms.

---

## Reflection

Today I learned how Terraform can be used not only to create AWS infrastructure but also to encode security requirements directly into infrastructure configuration.

The most important lesson is that security should be defined as part of the desired infrastructure state. Controls such as private networking, S3 Block Public Access, KMS encryption, and least-privilege IAM can be applied before resources are deployed.

I also learned that Terraform validation has multiple levels. Variable validation and preconditions can prevent invalid configurations, while check blocks provide additional assertions without necessarily blocking deployment.

From a cloud security perspective, the strongest approach combines preventive controls in Terraform with detective controls such as boto3 security scanning, AWS Config, GuardDuty, Inspector, and Security Hub.

This creates a continuous security model where infrastructure is deployed securely and then continuously verified after deployment.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Block Public Access | Amazon S3 controls that prevent public access through ACLs and policies |
| Check Block | Terraform non-blocking infrastructure assertion |
| Detective Control | Security control designed to discover unsafe activity or configuration |
| Least Privilege | Granting only the minimum permissions or network access required |
| Policy as Code | Defining governance and security policies in machine-readable code |
| Postcondition | Terraform condition used to validate a resulting resource state |
| Precondition | Terraform condition evaluated before completing a resource operation |
| Preventive Control | Security control designed to stop an unsafe action before it occurs |
| Secure by Default | Design approach where the default configuration is the safer configuration |
| SSE-KMS | Server-side S3 encryption using AWS KMS keys |
