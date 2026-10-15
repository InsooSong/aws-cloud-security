# Day 43 — Terraform Fundamentals for AWS

## Topic

Terraform Fundamentals for AWS — Providers, Resources, Variables, Outputs, State, Plans, and Infrastructure as Code

---

## Objectives

- Understand Infrastructure as Code
- Understand Terraform's declarative model
- Learn Terraform configuration structure
- Understand providers and resources
- Understand variables and outputs
- Learn Terraform references and dependencies
- Understand Terraform state
- Understand why state must be protected
- Learn the Terraform initialization workflow
- Learn terraform fmt and validate
- Learn terraform plan and apply
- Understand terraform destroy
- Learn AWS authentication for Terraform
- Understand provider version management
- Understand the Terraform dependency lock file
- Create a basic AWS VPC with Terraform
- Prepare for secure Terraform configuration on Day 44

---

# Infrastructure as Code

## 1. What Is Infrastructure as Code?

Infrastructure as Code, or IaC, manages infrastructure using configuration files.

Traditional:

```text
AWS Console
    ↓
Click
    ↓
Create Resource
```

IaC:

```text
Code
   ↓
Review
   ↓
Deploy
   ↓
AWS Infrastructure
```

Benefits include:

```text
Repeatability

Version Control

Peer Review

Automation

Consistency

Auditability
```

---

## 2. Why IaC Matters for Security

Manual configuration can lead to:

```text
Inconsistent Settings

Configuration Drift

Missing Security Controls

Poor Change Visibility
```

IaC enables:

```text
Security Controls
      ↓
Code
      ↓
Review
      ↓
Repeatable Deployment
```

Example:

```text
Every S3 Bucket
→ Public Access Block

Every Database
→ Encryption

Every Security Group
→ Approved Rules
```

These controls can be defined in code rather than relying entirely on manual configuration.

---

# Terraform

## 3. What Is Terraform?

Terraform is an Infrastructure as Code tool developed by HashiCorp.

Terraform uses:

```text
HCL
```

or:

```text
HashiCorp Configuration Language
```

to define infrastructure.

Example:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

---

## 4. Declarative Model

Terraform is declarative.

You describe:

```text
What infrastructure should exist
```

rather than:

```text
Every step required to create it
```

Example:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

Terraform determines the required AWS API operations.

---

# Terraform Architecture

## 5. High-Level Flow

```text
Terraform Configuration
        |
        v
Terraform CLI
        |
        v
AWS Provider
        |
        v
AWS APIs
        |
        v
AWS Resources
```

---

# Terraform Configuration Files

## 6. .tf Files

Terraform configuration files typically use:

```text
.tf
```

Examples:

```text
main.tf

variables.tf

outputs.tf

versions.tf
```

Terraform loads all `.tf` files in the current module directory.

The filenames are primarily for organization and readability.

---

## 7. Recommended Structure

For this study:

```text
terraform/
└── day43/
    ├── versions.tf
    ├── provider.tf
    ├── variables.tf
    ├── main.tf
    └── outputs.tf
```

This keeps the Terraform code separate from the Python scripts.

---

# Terraform Block

## 8. Required Terraform Version

Example:

```hcl
terraform {
  required_version = ">= 1.10.0"
}
```

This specifies which Terraform versions may run the configuration.

---

## 9. Required Providers

Example:

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

This tells Terraform:

```text
Provider:
AWS

Source:
HashiCorp

Version:
Compatible 6.x release
```

---

# AWS Provider

## 10. Provider

A provider connects Terraform to an external API.

Examples:

```text
AWS

Azure

Google Cloud

GitHub

Kubernetes
```

For AWS:

```hcl
provider "aws" {
  region = var.aws_region
}
```

---

## 11. Provider Role

Conceptually:

```text
Terraform
    |
    v
AWS Provider
    |
    v
AWS API
```

Terraform itself does not directly implement all AWS APIs.

The AWS provider translates Terraform resource operations into AWS API calls.

---

# Authentication

## 12. AWS Credentials

Terraform needs AWS credentials just like:

```text
AWS CLI

boto3
```

Do not hard-code:

```hcl
provider "aws" {
  access_key = "REAL_ACCESS_KEY"
  secret_key = "REAL_SECRET"
}
```

Never commit credentials into Terraform configuration.

---

## 13. Use Existing AWS Authentication

A better model:

```text
AWS CLI Profile
       ↓
Terraform AWS Provider
       ↓
AWS APIs
```

Example shell:

```bash
export AWS_PROFILE=development
```

Then:

```bash
terraform plan
```

Terraform's AWS provider can use AWS shared configuration and credential sources.

---

## 14. Verify AWS Identity First

Before running Terraform:

```bash
aws sts get-caller-identity
```

Also verify:

```bash
aws configure get region
```

Then run Terraform.

Security workflow:

```text
Verify Identity
      ↓
Verify Account
      ↓
Verify Region
      ↓
terraform plan
```

---

# Resources

## 15. Resource Block

Terraform resources represent infrastructure objects.

Syntax:

```hcl
resource "<TYPE>" "<NAME>" {
  ...
}
```

Example:

```hcl
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}
```

---

## 16. Resource Address

The Terraform address is:

```text
aws_vpc.main
```

Breakdown:

```text
aws_vpc
→ Resource Type

main
→ Terraform Local Name
```

---

## 17. Local Name vs AWS Name

The Terraform name:

```text
main
```

is internal to Terraform.

The AWS Name tag can be:

```hcl
tags = {
  Name = "day43-vpc"
}
```

These are different concepts.

---

# Variables

## 18. Input Variables

Variables make configurations reusable.

Example:

```hcl
variable "aws_region" {
  description = "AWS Region used for the Terraform lab"
  type        = string
  default     = "ap-northeast-1"
}
```

Use:

```hcl
provider "aws" {
  region = var.aws_region
}
```

---

## 19. VPC CIDR Variable

Example:

```hcl
variable "vpc_cidr" {
  description = "CIDR block for the study VPC"
  type        = string
  default     = "10.0.0.0/16"
}
```

Then:

```hcl
resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr
}
```

---

## 20. Variable Types

Common Terraform variable types include:

```text
string

number

bool

list

set

map

object
```

Example:

```hcl
variable "enable_dns" {
  type    = bool
  default = true
}
```

---

# Variable Validation

## 21. Validation

Terraform can validate input variables.

Example:

```hcl
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
```

This helps prevent invalid infrastructure input.

---

# Local Values

## 22. Locals

Local values allow reusable expressions.

Example:

```hcl
locals {
  common_tags = {
    Project     = "aws-cloud-security"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}
```

Use:

```hcl
tags = local.common_tags
```

---

## 23. Why Locals?

Without locals:

```text
Repeat Tags
Repeat Naming
Repeat Expressions
```

With locals:

```text
Define Once
Reuse
```

This reduces configuration inconsistency.

---

# Outputs

## 24. Output Values

Outputs expose useful Terraform values.

Example:

```hcl
output "vpc_id" {
  description = "ID of the Terraform-managed VPC"
  value       = aws_vpc.main.id
}
```

After apply:

```bash
terraform output
```

can display the value.

---

## 25. Resource References

This:

```hcl
aws_vpc.main.id
```

references:

```text
Resource:
aws_vpc.main

Attribute:
id
```

Terraform uses references to understand dependencies between resources.

---

# Dependencies

## 26. Implicit Dependency

Example:

```hcl
resource "aws_subnet" "example" {
  vpc_id = aws_vpc.main.id
}
```

Terraform sees:

```text
Subnet
depends on
VPC
```

because one resource references another.

Conceptually:

```text
VPC
 ↓
Subnet
```

Terraform automatically determines the correct creation order.

---

## 27. depends_on

Terraform also supports explicit dependencies:

```hcl
depends_on = [
  aws_vpc.main
]
```

However:

```text
Prefer Natural Resource References
```

where possible.

Use explicit `depends_on` only when Terraform cannot infer the dependency from data references.

---

# Terraform State

## 28. What Is State?

Terraform tracks managed infrastructure using:

```text
Terraform State
```

By default:

```text
terraform.tfstate
```

Conceptually:

```text
Terraform Configuration
       |
       v
Terraform State
       |
       v
Real AWS Resources
```

---

## 29. Why State Exists

Terraform needs to know:

```text
Which AWS Resource
corresponds to
which Terraform Resource
```

Example:

```text
aws_vpc.main
      ↕
vpc-xxxxxxxx
```

This mapping is stored in state.

---

## 30. State Is Security-Sensitive

Terraform state can contain:

```text
Resource IDs

ARNs

IP Addresses

Infrastructure Metadata

Passwords

Secrets

Sensitive Attributes
```

Therefore:

```text
terraform.tfstate
```

must be treated as sensitive information.

---

## 31. Never Commit State

Do not commit:

```text
terraform.tfstate

terraform.tfstate.backup
```

to public Git repositories.

For local learning:

```text
State
→ Local

Git
→ Ignore
```

For team environments:

```text
Remote State
```

is generally preferred.

---

# Sensitive Values

## 32. sensitive

Terraform supports:

```hcl
variable "example_secret" {
  type      = string
  sensitive = true
}
```

This hides the value from ordinary CLI output.

However:

```text
sensitive = true
```

does NOT necessarily mean:

```text
Value Is Not Stored in State
```

Sensitive values can still exist in state.

---

## 33. Modern Ephemeral Values

Modern Terraform also supports ephemeral values for certain use cases.

Conceptually:

```text
Sensitive
→ Hide from normal output

Ephemeral
→ Avoid persistence in state/plan
```

This is useful for temporary credentials or values that should not persist.

Day 43 only requires awareness of this feature.

---

# Initialization

## 34. terraform init

The first command for a Terraform working directory is:

```bash
terraform init
```

It prepares the working directory.

It can:

```text
Download Providers

Initialize Backend

Download Modules

Create Dependency Lock Information
```

---

## 35. .terraform Directory

After initialization:

```text
.terraform/
```

is created.

Do not commit it.

Add to:

```text
.gitignore
```

---

# Dependency Lock File

## 36. .terraform.lock.hcl

Terraform creates:

```text
.terraform.lock.hcl
```

This records selected provider versions and checksums.

Unlike:

```text
.terraform/
```

the lock file should normally be:

```text
Committed to Git
```

This makes provider selection more reproducible.

---

# Formatting

## 37. terraform fmt

Run:

```bash
terraform fmt
```

This formats Terraform files according to Terraform's standard style.

For recursive formatting:

```bash
terraform fmt -recursive
```

---

## 38. Why Formatting Matters

Consistent formatting improves:

```text
Readability

Code Review

Git Diffs

Maintenance
```

---

# Validation

## 39. terraform validate

Run:

```bash
terraform validate
```

This checks whether the Terraform configuration is syntactically and internally valid.

Typical workflow:

```text
terraform init
      ↓
terraform fmt
      ↓
terraform validate
```

---

## 40. validate Is Not a Security Scanner

Important:

```text
terraform validate
```

checks configuration validity.

It does not mean:

```text
Infrastructure Is Secure
```

For example:

```hcl
cidr_blocks = ["0.0.0.0/0"]
```

may be syntactically valid while being insecure for SSH.

Security validation will be covered more deeply on Day 44.

---

# Planning

## 41. terraform plan

Run:

```bash
terraform plan
```

Terraform compares:

```text
Configuration

State

Real Infrastructure
```

and shows proposed changes.

---

## 42. Plan Symbols

Common symbols include:

```text
+
Create

~
Update

-
Destroy

-/+
Replace
```

Always review the plan before applying.

---

## 43. Why Plan Is Important for Security

A Terraform plan may reveal:

```text
Security Group Opening

Encryption Removal

Resource Replacement

Public Exposure

IAM Policy Change
```

Therefore:

```text
terraform plan
```

is not just deployment preparation.

It is also an important:

```text
Change Review Step
```

---

# Apply

## 44. terraform apply

Run:

```bash
terraform apply
```

Terraform creates a plan and asks for confirmation before making changes.

Conceptually:

```text
Configuration
     ↓
Plan
     ↓
Approval
     ↓
AWS API
     ↓
Infrastructure
```

---

## 45. Apply Carefully

Before:

```bash
terraform apply
```

verify:

```text
AWS Account

AWS Profile

AWS Region

Terraform Plan

Expected Cost

Expected Resources
```

---

# Destroy

## 46. terraform destroy

Terraform can remove resources it manages:

```bash
terraform destroy
```

This is useful for disposable labs.

But:

```text
terraform destroy
```

is a destructive operation.

Always review the plan.

---

## 47. Lab Cleanup

For Day 43:

```text
Create Test VPC
      ↓
Review
      ↓
Destroy Test VPC
```

This avoids leaving unnecessary lab infrastructure.

---

# Basic Terraform Lab

## 48. versions.tf

Create:

```text
terraform/day43/versions.tf
```

Content:

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

## 49. provider.tf

Create:

```text
terraform/day43/provider.tf
```

Content:

```hcl
provider "aws" {
  region = var.aws_region
}
```

Credentials are intentionally not defined in this file.

---

## 50. variables.tf

Create:

```hcl
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
```

---

## 51. main.tf

Create:

```hcl
locals {
  common_tags = {
    Project     = "aws-cloud-security"
    Environment = var.environment
    ManagedBy   = "Terraform"
  }
}

resource "aws_vpc" "main" {
  cidr_block = var.vpc_cidr

  enable_dns_support   = true
  enable_dns_hostnames = true

  tags = merge(
    local.common_tags,
    {
      Name = "day43-terraform-vpc"
    }
  )
}
```

---

## 52. outputs.tf

Create:

```hcl
output "vpc_id" {
  description = "ID of the Terraform-managed VPC"
  value       = aws_vpc.main.id
}

output "vpc_cidr" {
  description = "CIDR block of the Terraform-managed VPC"
  value       = aws_vpc.main.cidr_block
}
```

---

# Lab Workflow

## 53. Enter Directory

```bash
cd terraform/day43
```

---

## 54. Verify Terraform

```bash
terraform version
```

---

## 55. Verify AWS Identity

```bash
aws sts get-caller-identity
```

If using a profile:

```bash
export AWS_PROFILE=development
```

Then verify again:

```bash
aws sts get-caller-identity
```

---

## 56. Initialize

```bash
terraform init
```

Expected:

```text
Provider downloaded

Working directory initialized

.terraform.lock.hcl created
```

---

## 57. Format

```bash
terraform fmt
```

---

## 58. Validate

```bash
terraform validate
```

Expected:

```text
Success!
The configuration is valid.
```

---

## 59. Plan

```bash
terraform plan
```

Review:

```text
Plan: 1 to add, 0 to change, 0 to destroy
```

before continuing.

---

## 60. Apply

If the plan is correct:

```bash
terraform apply
```

Review again.

Then approve:

```text
yes
```

---

## 61. Check Output

```bash
terraform output
```

Example:

```text
vpc_id
vpc_cidr
```

---

## 62. Verify With AWS CLI

Use the AWS CLI:

```bash
aws ec2 describe-vpcs \
  --filters \
  Name=tag:Name,Values=day43-terraform-vpc
```

This confirms:

```text
Terraform State

and

Actual AWS Resource
```

match.

---

## 63. Run Plan Again

After successful apply:

```bash
terraform plan
```

Expected:

```text
No changes.
```

This demonstrates Terraform's idempotent desired-state model.

---

## 64. Destroy Lab

When finished:

```bash
terraform destroy
```

Review:

```text
Plan: 0 to add, 0 to change, 1 to destroy
```

Then confirm.

---

# Terraform State Inspection

## 65. State List

Before destroying:

```bash
terraform state list
```

Example:

```text
aws_vpc.main
```

---

## 66. State Show

Inspect:

```bash
terraform state show aws_vpc.main
```

This shows Terraform's stored view of the VPC.

Do not manually edit:

```text
terraform.tfstate
```

---

# Drift

## 67. What Is Configuration Drift?

Drift occurs when:

```text
Terraform Code
       ≠
Real Infrastructure
```

Example:

```text
Terraform:
DNS Hostnames = true

Console:
Changed manually
```

The next:

```bash
terraform plan
```

can detect a difference.

---

## 68. Why Drift Matters for Security

Manual changes can bypass:

```text
Code Review

Security Review

CI/CD

IaC Standards
```

Example:

```text
Terraform:
SSH restricted

Manual Change:
SSH → 0.0.0.0/0
```

IaC-based review helps detect or correct such drift.

---

# State Security

## 69. Local State

By default:

```text
terraform.tfstate
```

is stored locally.

This is acceptable for a simple learning lab.

It is not ideal for:

```text
Teams

Production

Sensitive Infrastructure
```

---

## 70. Remote State

For team environments, use a secure remote backend.

Benefits include:

```text
Central State

Access Control

Shared State

Locking

Backup
```

Backend design will not be deeply implemented on Day 43.

---

## 71. State Locking

State locking prevents:

```text
User A
and
User B
```

from modifying the same state concurrently where the backend supports locking.

Conceptually:

```text
Terraform A
     |
    LOCK
     |
Terraform B
→ Wait / Fail
```

This helps prevent state corruption.

---

# Terraform Security

## 72. State Must Be Protected

Remember:

```text
Terraform Code
→ Usually Safe to Share after review

Terraform State
→ Potentially Sensitive
```

Even if a Terraform variable is:

```hcl
sensitive = true
```

its value may still exist in state.

---

## 73. Plan Files Can Also Be Sensitive

A saved plan:

```bash
terraform plan \
  -out=tfplan
```

can contain sensitive infrastructure information.

Do not publish:

```text
*.tfplan
```

files.

---

# .gitignore

## 74. Terraform Entries

Add:

```gitignore
# Terraform
.terraform/
*.tfstate
*.tfstate.*
*.tfplan
crash.log
crash.*.log

# Terraform variable files that may contain secrets
*.tfvars
*.tfvars.json
```

---

## 75. Do Not Ignore the Lock File

Do NOT add:

```gitignore
.terraform.lock.hcl
```

The lock file should generally be committed.

It helps ensure consistent provider selections.

---

# Common Mistakes

## 76. Hard-Coding AWS Credentials

Never:

```hcl
access_key = "..."
secret_key = "..."
```

Use the AWS provider credential chain.

---

## 77. Running Apply Without Reviewing Plan

Poor:

```text
terraform apply
→ Blind Approval
```

Better:

```text
Plan
→ Review
→ Apply
```

---

## 78. Committing State

Never intentionally publish:

```text
terraform.tfstate
```

State can expose sensitive infrastructure information.

---

## 79. Ignoring Provider Versions

Poor:

```hcl
required_providers {
  aws = {
    source = "hashicorp/aws"
  }
}
```

Better:

```text
Version Constraint

+

Dependency Lock File
```

This provides more predictable builds.

---

## 80. Manually Editing State

Avoid:

```text
Open terraform.tfstate
→ Modify JSON
```

Use supported Terraform state commands instead.

---

## 81. Treating validate as Security Validation

```text
terraform validate
```

means:

```text
Configuration Is Structurally Valid
```

not:

```text
Configuration Is Secure
```

---

## 82. Treating Plan as Harmless Output

Plans can contain:

```text
Resource Information

Sensitive Values

Infrastructure Design
```

Treat saved plan artifacts as sensitive.

---

# Terraform vs boto3

## 83. Different Purposes

boto3 security scanner:

```text
Observe Existing AWS

Evaluate Security

Generate Findings
```

Terraform:

```text
Define Desired AWS Infrastructure

Create / Modify Infrastructure

Maintain Desired State
```

---

## 84. Together

A mature workflow could be:

```text
Terraform
→ Deploy Secure Infrastructure
       ↓
AWS
       ↓
boto3 Scanner
→ Verify Security Configuration
```

This combines:

```text
Preventive Security

+

Detective Security
```

---

# Day 44 Preview

## 85. Secure Terraform

Day 44 can extend this lab with:

```text
Private / Public Subnets

Security Groups

S3 Block Public Access

S3 Encryption

KMS

IAM

Secure Defaults

Terraform Security Validation
```

The goal becomes:

```text
Security Requirements
       ↓
Terraform Code
       ↓
Secure AWS Infrastructure
```

---

# Hands-on Practice

## 86. Check Version

```bash
terraform version
```

---

## 87. Initialize

```bash
terraform init
```

---

## 88. Format

```bash
terraform fmt
```

---

## 89. Validate

```bash
terraform validate
```

---

## 90. Plan

```bash
terraform plan
```

Review every proposed change.

---

## 91. Apply

If authorized:

```bash
terraform apply
```

Do not create resources in a production account for practice.

---

## 92. Verify

```bash
terraform state list
```

and:

```bash
terraform output
```

---

## 93. Re-Plan

```bash
terraform plan
```

Expected:

```text
No changes.
```

---

## 94. Cleanup

```bash
terraform destroy
```

Review before confirming.

---

# Security Checklist

```text
[ ] AWS identity is verified before Terraform operations

[ ] AWS credentials are not hard-coded

[ ] AWS Provider version is constrained

[ ] .terraform.lock.hcl is committed

[ ] .terraform/ is not committed

[ ] Terraform state is excluded from Git

[ ] Terraform plan files are excluded from Git

[ ] Sensitive tfvars files are excluded from Git

[ ] terraform fmt is run before committing

[ ] terraform validate succeeds

[ ] terraform plan is reviewed before apply

[ ] Account and Region are verified before apply

[ ] Resource changes are understood before approval

[ ] State is treated as sensitive

[ ] Local state is used only for learning or appropriate local workflows

[ ] Remote state is considered for shared environments

[ ] State locking is used where supported in collaborative environments

[ ] terraform destroy is reviewed before confirmation

[ ] Lab resources are cleaned up when no longer needed
```

---

## Key Takeaways

- Terraform enables declarative Infrastructure as Code.
- AWS resources are defined using Terraform resource blocks.
- Providers connect Terraform with external APIs such as AWS.
- Input variables make configurations reusable.
- Local values reduce duplicated configuration.
- Outputs expose useful infrastructure values.
- Terraform automatically builds dependencies from resource references.
- Terraform state maps Terraform resources to real infrastructure.
- Terraform state can contain sensitive information and must not be committed publicly.
- `terraform init` initializes providers, modules, and backend configuration.
- `terraform fmt` standardizes configuration formatting.
- `terraform validate` validates configuration structure but does not guarantee security.
- `terraform plan` previews proposed infrastructure changes.
- `terraform apply` performs the approved changes.
- `.terraform.lock.hcl` should normally be committed for reproducible provider selection.
- AWS credentials should be supplied through supported credential mechanisms rather than hard-coded.
- Infrastructure as Code provides an important foundation for preventive cloud security.

---

## Reflection

Today I learned how Terraform can define and manage AWS infrastructure using Infrastructure as Code.

The most important concept is that Terraform uses declarative configuration to describe the desired infrastructure state. Terraform then compares the configuration, state, and actual AWS environment to determine the changes required.

I also learned that Terraform state is security-sensitive because it can contain detailed infrastructure information and sensitive values. State and saved plan files must therefore be protected and excluded from public version control.

The Terraform workflow of `init`, `fmt`, `validate`, `plan`, and `apply` provides a structured way to create infrastructure while reviewing changes before deployment.

From a cloud security perspective, Terraform creates an opportunity to move security controls earlier in the deployment process by defining secure defaults, reviewing infrastructure changes as code, and reducing manual configuration drift.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Backend | Mechanism used to store Terraform state |
| Drift | Difference between desired Terraform configuration and real infrastructure |
| HCL | HashiCorp Configuration Language used by Terraform |
| Infrastructure as Code | Managing infrastructure through version-controlled configuration |
| Output | Value exposed from Terraform configuration |
| Provider | Plugin that allows Terraform to interact with an external API |
| Resource | Infrastructure object managed by Terraform |
| State | Terraform data that maps configuration resources to real infrastructure |
| Terraform | HashiCorp Infrastructure as Code tool |
| Variable | Input value used to make Terraform configuration reusable |
