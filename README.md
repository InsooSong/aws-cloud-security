# AWS Cloud Security

> Hands-on learning notes for AWS and Cloud Security.

This repository documents my practical AWS learning journey with a focus on cloud security, identity and access management, networking, data protection, logging, monitoring, threat detection, and security automation.

The goal of this repository is to build practical cloud security knowledge through structured study, hands-on practice, security-focused analysis, and continuous documentation.

---

# Learning Objectives

- Understand AWS core architecture and services
- Build strong AWS networking fundamentals
- Understand identity and access management
- Apply the Principle of Least Privilege
- Design secure AWS network architectures
- Understand encryption and key management
- Implement logging and monitoring
- Learn AWS threat detection services
- Understand multi-account security architecture
- Practice cloud security automation
- Develop practical skills for cloud security engineering

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
- [ ] Day 37 — Centralized Security & Logging
- [ ] Day 38 — AWS Security Architecture Review

## Phase 7 — Security Automation

- [ ] Day 39 — AWS CLI Fundamentals
- [ ] Day 40 — AWS CLI for Security Operations
- [ ] Day 41 — Python & boto3 Fundamentals
- [ ] Day 42 — Security Automation with boto3
- [ ] Day 43 — Terraform Fundamentals for AWS
- [ ] Day 44 — Terraform Security Configuration
- [ ] Day 45 — AWS Cloud Security Final Review

---

# Repository Structure

```text
aws-cloud-security/
│
├── README.md
│
└── notes/
    ├── day01-aws-fundamentals.md
    ├── day02-iam-fundamentals.md
    ├── day03-iam-identities-policies.md
    ├── day04-iam-policy-evaluation.md
    ├── day05-iam-security-best-practices.md
    ├── day06-vpc-fundamentals.md
    ├── day07-public-private-subnets.md
    ├── day08-route-tables-internet-gateway.md
    ├── day09-nat-gateway.md
    ├── day10-security-groups.md
    ├── day11-network-acls.md
    ├── day12-vpc-security-review.md
    ├── day13-ec2-fundamentals-security.md
    ├── day14-ec2-security-hardening.md
    ├── day15-s3-fundamentals.md
    ├── day16-s3-access-control-security.md
    ├── day17-ebs-encryption.md
    ├── day18-rds-security.md
    ├── day19-compute-storage-security-review.md
    ├── day20-aws-cloudtrail.md
    ├── day21-amazon-cloudwatch.md
    ├── day22-aws-config.md
    ├── day23-centralized-logging.md
    ├── day24-logging-monitoring-review.md
    ├── day25-aws-kms-fundamentals.md
    ├── day26-kms-keys-encryption.md
    ├── day27-aws-secrets-manager.md
    ├── day28-amazon-guardduty.md
    ├── day29-aws-security-hub.md
    ├── day30-amazon-inspector.md
    ├── day31-amazon-macie.md
    ├── day32-aws-waf-shield.md
    ├── day33-security-services-review.md
    ├── day34-aws-organizations.md
    ├── day35-service-control-policies.md
    └── day36-multi-account-security-architecture.md
```

Each daily note contains detailed study material, examples, security considerations, hands-on practice, and reflections.

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
- Are activities logged?
- Can suspicious behavior be detected?
- Can permissions or network access be reduced?

---

# Security Focus Areas

This repository focuses on the following cloud security areas:

```text
Identity
Network
Data Protection
Logging
Monitoring
Threat Detection
Governance
Automation
```

These areas are used as a consistent framework when analyzing AWS services and architectures.

---

# Progress

## Current Phase

```text
Phase 6 — AWS Security Architecture
```

## Current Topic

```text
Day 36 — Multi-Account Security Architecture
```

## Completed Topics

- AWS Fundamentals
- Shared Responsibility Model
- IAM Fundamentals
- IAM Users, Groups, Roles & Policies
- IAM Policy Evaluation
- IAM Security Best Practices
- VPC Fundamentals
- Public & Private Subnets
- Route Tables & Internet Gateway
- NAT Gateway
- Security Groups
- Network ACLs
- VPC Security Review
- EC2 Fundamentals & Security
- EC2 Security Hardening
- S3 Fundamentals
- S3 Access Control & Security
- EBS Encryption
- RDS Security
- Compute & Storage Security Review
- AWS CloudTrail
- Amazon CloudWatch
- AWS Config
- Centralized Logging
- Logging & Monitoring Review
- AWS KMS Fundamentals
- KMS Keys & Encryption
- AWS Secrets Manager
- Amazon GuardDuty
- AWS Security Hub
- Amazon Inspector
- Amazon Macie
- AWS WAF & Shield
- Security Services Review
- AWS Organizations
- Service Control Policies
- Multi-Account Security Architecture

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
