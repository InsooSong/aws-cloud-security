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
- [ ] Day 10 — Security Groups
- [ ] Day 11 — Network ACLs
- [ ] Day 12 — VPC Security Review

## Phase 3 — Compute & Storage Security

- [ ] Day 13 — EC2 Fundamentals & Security
- [ ] Day 14 — EC2 Security Hardening
- [ ] Day 15 — S3 Fundamentals
- [ ] Day 16 — S3 Access Control & Security
- [ ] Day 17 — EBS Encryption
- [ ] Day 18 — RDS Security
- [ ] Day 19 — Compute & Storage Security Review

## Phase 4 — Logging & Monitoring

- [ ] Day 20 — AWS CloudTrail
- [ ] Day 21 — Amazon CloudWatch
- [ ] Day 22 — AWS Config
- [ ] Day 23 — Centralized Logging
- [ ] Day 24 — Logging & Monitoring Review

## Phase 5 — Data Protection & Threat Detection

- [ ] Day 25 — AWS KMS Fundamentals
- [ ] Day 26 — KMS Keys & Encryption
- [ ] Day 27 — AWS Secrets Manager
- [ ] Day 28 — Amazon GuardDuty
- [ ] Day 29 — AWS Security Hub
- [ ] Day 30 — Amazon Inspector
- [ ] Day 31 — Amazon Macie
- [ ] Day 32 — AWS WAF & Shield
- [ ] Day 33 — Security Services Review

## Phase 6 — AWS Security Architecture

- [ ] Day 34 — AWS Organizations
- [ ] Day 35 — Service Control Policies
- [ ] Day 36 — Multi-Account Security Architecture
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
    └── day09-nat-gateway.md
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
Phase 2 — AWS Networking
```

## Current Topic

```text
Day 9 — NAT Gateway
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
