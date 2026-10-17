# AWS Cloud Security

> Hands-on learning and security engineering practice for AWS Cloud Security.

This repository documents my hands-on AWS Cloud Security study journey, covering identity and access management, networking, compute and storage security, data protection, logging, threat detection, multi-account governance, security automation, and Infrastructure as Code.

The repository combines structured study notes with practical AWS CLI exercises, Python and boto3 security automation, and secure Terraform configurations.

---

# What This Repository Demonstrates

- AWS core architecture and the Shared Responsibility Model
- Identity and access management with least privilege
- Secure VPC and network architecture
- EC2, S3, EBS, and RDS security
- Encryption and key management with AWS KMS
- Secrets management
- Logging, monitoring, and configuration tracking
- Threat detection and vulnerability management
- Multi-account security architecture and governance
- Centralized security operations and logging
- AWS CLI-based security investigation
- Python and boto3 security automation
- Infrastructure as Code with Terraform
- Secure-by-default Terraform configuration
- Preventive and detective cloud security controls

---

# Roadmap

## Phase 1 — AWS Fundamentals & IAM

- [x] [Day 1 — AWS Fundamentals & Shared Responsibility Model](notes/day01-aws-fundamentals.md)
- [x] [Day 2 — IAM Fundamentals](notes/day02-iam-fundamentals.md)
- [x] [Day 3 — IAM Users, Groups, Roles & Policies](notes/day03-iam-identities-policies.md)
- [x] [Day 4 — IAM Policy Evaluation](notes/day04-iam-policy-evaluation.md)
- [x] [Day 5 — IAM Security Best Practices](notes/day05-iam-security-best-practices.md)

## Phase 2 — AWS Networking

- [x] [Day 6 — VPC Fundamentals](notes/day06-vpc-fundamentals.md)
- [x] [Day 7 — Public & Private Subnets](notes/day07-public-private-subnets.md)
- [x] [Day 8 — Route Tables & Internet Gateway](notes/day08-route-tables-internet-gateway.md)
- [x] [Day 9 — NAT Gateway](notes/day09-nat-gateway.md)
- [x] [Day 10 — Security Groups](notes/day10-security-groups.md)
- [x] [Day 11 — Network ACLs](notes/day11-network-acls.md)
- [x] [Day 12 — VPC Security Review](notes/day12-vpc-security-review.md)

## Phase 3 — Compute & Storage Security

- [x] [Day 13 — EC2 Fundamentals & Security](notes/day13-ec2-fundamentals-security.md)
- [x] [Day 14 — EC2 Security Hardening](notes/day14-ec2-security-hardening.md)
- [x] [Day 15 — S3 Fundamentals](notes/day15-s3-fundamentals.md)
- [x] [Day 16 — S3 Access Control & Security](notes/day16-s3-access-control-security.md)
- [x] [Day 17 — EBS Encryption](notes/day17-ebs-encryption.md)
- [x] [Day 18 — RDS Security](notes/day18-rds-security.md)
- [x] [Day 19 — Compute & Storage Security Review](notes/day19-compute-storage-security-review.md)

## Phase 4 — Logging & Monitoring

- [x] [Day 20 — AWS CloudTrail](notes/day20-aws-cloudtrail.md)
- [x] [Day 21 — Amazon CloudWatch](notes/day21-amazon-cloudwatch.md)
- [x] [Day 22 — AWS Config](notes/day22-aws-config.md)
- [x] [Day 23 — Centralized Logging](notes/day23-centralized-logging.md)
- [x] [Day 24 — Logging & Monitoring Review](notes/day24-logging-monitoring-review.md)

## Phase 5 — Data Protection & Threat Detection

- [x] [Day 25 — AWS KMS Fundamentals](notes/day25-aws-kms-fundamentals.md)
- [x] [Day 26 — KMS Keys & Encryption](notes/day26-kms-keys-encryption.md)
- [x] [Day 27 — AWS Secrets Manager](notes/day27-aws-secrets-manager.md)
- [x] [Day 28 — Amazon GuardDuty](notes/day28-amazon-guardduty.md)
- [x] [Day 29 — AWS Security Hub](notes/day29-aws-security-hub.md)
- [x] [Day 30 — Amazon Inspector](notes/day30-amazon-inspector.md)
- [x] [Day 31 — Amazon Macie](notes/day31-amazon-macie.md)
- [x] [Day 32 — AWS WAF & Shield](notes/day32-aws-waf-shield.md)
- [x] [Day 33 — Security Services Review](notes/day33-security-services-review.md)

## Phase 6 — AWS Security Architecture

- [x] [Day 34 — AWS Organizations](notes/day34-aws-organizations.md)
- [x] [Day 35 — Service Control Policies](notes/day35-service-control-policies.md)
- [x] [Day 36 — Multi-Account Security Architecture](notes/day36-multi-account-security-architecture.md)
- [x] [Day 37 — Centralized Security & Logging](notes/day37-centralized-security-logging.md)
- [x] [Day 38 — AWS Security Architecture Review](notes/day38-aws-security-architecture-review.md)

## Phase 7 — Security Automation & Infrastructure as Code

- [x] [Day 39 — AWS CLI Fundamentals](notes/day39-aws-cli-fundamentals.md)
- [x] [Day 40 — AWS CLI for Security Operations](notes/day40-aws-cli-security-operations.md)
- [x] [Day 41 — Python & boto3 Fundamentals](notes/day41-python-boto3-fundamentals.md)
- [x] [Day 42 — Security Automation with boto3](notes/day42-security-automation-boto3.md)
- [x] [Day 43 — Terraform Fundamentals for AWS](notes/day43-terraform-fundamentals-aws.md)
- [x] [Day 44 — Terraform Security Configuration](notes/day44-terraform-security-configuration.md)
- [x] [Day 45 — AWS Cloud Security Final Review](notes/day45-aws-cloud-security-final-review.md)

---

# Repository Structure

```text
aws-cloud-security/
├── README.md
├── .gitignore
│
├── notes/
│   └── dayXX-*.md
│
├── scripts/
│   ├── check_identity.py
│   ├── list_ec2.py
│   ├── list_roles.py
│   ├── list_s3.py
│   └── security_scan.py
│
├── reports/
│   └── .gitkeep
│
└── terraform/
    ├── day43/
    │   ├── main.tf
    │   ├── outputs.tf
    │   ├── provider.tf
    │   ├── variables.tf
    │   └── versions.tf
    │
    └── day44/
        ├── checks.tf
        ├── iam.tf
        ├── kms.tf
        ├── locals.tf
        ├── network.tf
        ├── outputs.tf
        ├── provider.tf
        ├── s3.tf
        ├── variables.tf
        └── versions.tf
```

The `notes/` directory contains the complete Day 1–45 study roadmap.

The `scripts/` directory contains read-only AWS inventory and security automation examples built with Python and boto3.

The `terraform/` directory contains Infrastructure as Code exercises, including secure AWS configuration examples.

Generated security reports and Terraform state files are intentionally excluded from version control.

---

# Study Approach

Each topic is studied from both a technical and security perspective.

The general approach is:

```text
Understand the Service
        ↓
Understand the Architecture
        ↓
Identify Security Controls
        ↓
Analyze Misconfiguration Risks
        ↓
Perform Hands-on Practice
        ↓
Document Key Findings
```

For security-related topics, I focus on questions such as:

- Who can access the resource?
- From where can the resource be accessed?
- What permissions are required?
- Is the resource exposed to the Internet?
- Is sensitive data encrypted?
- Who can access the encryption keys?
- Are activities logged?
- Can configuration changes be tracked?
- Can suspicious behavior be detected?
- Can permissions or network access be reduced?
- Can the security requirement be enforced through automation or Infrastructure as Code?

---

# Security Focus Areas

```text
Identity
Network
Compute & Storage
Data Protection
Logging
Monitoring
Threat Detection
Governance
Security Automation
Infrastructure as Code
```

These areas provide a consistent framework for analyzing AWS services and cloud security architectures.

---

# Hands-on Security Automation

The repository includes several Python and boto3 exercises for interacting with AWS APIs.

Examples include:

- Verifying the current AWS identity with STS
- Enumerating EC2 instances
- Enumerating IAM roles
- Enumerating S3 buckets
- Reviewing public EC2 exposure
- Reviewing Security Group rules
- Reviewing S3 security configuration
- Retrieving GuardDuty and Inspector findings
- Generating normalized security findings

The automation examples are intentionally designed around **read-only operations first** to reduce the risk of unintended changes.

---

# Infrastructure as Code

Terraform exercises demonstrate how cloud security controls can be implemented as preventive controls.

Examples include:

- VPC and private subnet configuration
- Prevention of automatic public IP assignment
- Least-privilege Security Groups
- S3 Block Public Access
- S3 SSE-KMS encryption
- AWS KMS key management
- IAM least-privilege policies
- Terraform variable validation
- Terraform security checks

Terraform state and generated plan files are treated as sensitive and are excluded from version control.

---

# Security Model

The repository approaches cloud security using three control categories:

```text
Prevent
   ↓
Detect
   ↓
Respond
```

Examples:

```text
Prevent
├── IAM
├── SCP
├── Security Groups
├── S3 Block Public Access
├── KMS
└── Terraform

Detect
├── CloudTrail
├── AWS Config
├── CloudWatch
├── GuardDuty
├── Inspector
├── Macie
└── Security Hub

Respond
├── AWS CLI Investigation
├── boto3 Automation
├── EventBridge
├── Systems Manager
└── Incident Response Processes
```

---

# Progress

**Status:** Completed

**Final Topic:** Day 45 — AWS Cloud Security Final Review

The 45-day AWS Cloud Security study roadmap has been completed.

The repository now combines:

```text
AWS Fundamentals
        +
Cloud Security Architecture
        +
Security Operations
        +
Python / boto3 Automation
        +
Secure Infrastructure as Code
```

---

# Notes

Detailed learning content is stored in the [`notes/`](notes/) directory.

Each daily note may include:

- Learning objectives
- Core concepts
- Architecture examples
- Security considerations
- Hands-on practice
- Security checklist
- Key takeaways
- Reflection
- Vocabulary
