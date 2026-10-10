# Day 38 — AWS Security Architecture Review

## Topic

AWS Security Architecture Review — Organizations, Multi-Account Design, SCPs, Cross-Account Access, Centralized Security, Networking, and Logging

---

## Objectives

- Review AWS Organizations
- Review Organizational Units and account boundaries
- Review Service Control Policies
- Review multi-account security architecture
- Review Security Tooling and Log Archive accounts
- Review cross-account IAM roles
- Review IAM Identity Center
- Review delegated administration
- Review centralized security services
- Review centralized logging
- Review centralized networking
- Understand security service placement
- Understand separation of duties
- Understand blast radius reduction
- Practice architecture-based security decisions
- Design an end-to-end AWS security architecture

---

# Phase 6 Overview

## 1. Topics Covered

During Phase 6:

```text
Day 34
→ AWS Organizations

Day 35
→ Service Control Policies

Day 36
→ Multi-Account Security Architecture

Day 37
→ Centralized Security & Logging

Day 38
→ Security Architecture Review
```

The goal of this phase is to understand:

```text
How security is applied
across an entire AWS organization
```

rather than only inside a single AWS account.

---

# AWS Security Architecture

## 2. High-Level Architecture

A common AWS multi-account architecture:

```text
                         Management Account
                                |
                                v
                         AWS Organizations
                                |
        +-----------------------+-----------------------+
        |                       |                       |
        v                       v                       v
   Security OU          Infrastructure OU        Workloads OU
        |                       |                       |
   +----+----+             +----+----+             +----+----+
   |         |             |         |             |         |
   v         v             v         v             v         v
Security    Log          Network    Shared        Prod      NonProd
Tooling    Archive                 Services
```

Each account has a specific security responsibility.

---

# Account Boundaries

## 3. AWS Account as a Security Boundary

An AWS account provides isolation for:

```text
IAM

Resources

Service Quotas

Billing

Security Configuration
```

Conceptually:

```text
Account A
    |
    X
Account B
```

unless access is explicitly granted.

---

## 4. Why Account Separation Matters

Poor design:

```text
One Account
│
├── Production
├── Development
├── Security
├── Logging
└── Networking
```

A compromise may have a large blast radius.

Better:

```text
Production Account

Development Account

Security Account

Log Archive Account

Network Account
```

This provides stronger isolation.

---

# Management Account

## 5. Management Account Purpose

The management account should primarily manage:

```text
AWS Organizations

Account Creation

OU Structure

Organization Policies

Delegated Administration

Billing
```

It should not normally host:

```text
Application EC2

Production RDS

Developer Workloads
```

---

## 6. Why Keep It Minimal?

The management account has special organization privileges.

Also:

```text
SCPs
→ Do Not Restrict the Management Account
```

Therefore:

```text
More Workloads
+
More Users
=
More Attack Surface
```

Keep management-account access minimal.

---

# Organizational Units

## 7. OU Design

OUs group accounts with common:

```text
Security Requirements

Compliance Requirements

Operational Requirements

Guardrails
```

Example:

```text
Security OU

Infrastructure OU

Workloads OU
```

Avoid designing OUs only around temporary organizational teams.

---

## 8. Why Functional OUs?

Example:

```text
Production OU
→ Strict Security Controls

Development OU
→ More Flexibility

Security OU
→ Security Administration

Infrastructure OU
→ Network and Shared Services
```

Policies can then be applied consistently.

---

# Service Control Policies

## 9. SCP Review

SCPs define:

```text
Maximum Permission Guardrails
```

Remember:

```text
SCP
≠
Permission Grant
```

---

## 10. Permission Model

Simplified:

```text
IAM Permission
       ∩
SCP Permission
       =
Effective Permission
```

Example:

```text
IAM:
AdministratorAccess

SCP:
Deny cloudtrail:StopLogging

Result:
StopLogging = Denied
```

---

## 11. Explicit Deny

Important rule:

```text
Explicit Deny
>
Allow
```

Therefore:

```text
IAM Allow
+
SCP Deny
=
DENIED
```

---

## 12. SCP Hierarchy

Example:

```text
Root
 |
 v
Workloads OU
 |
 v
Production OU
 |
 v
Production Account
```

Effective permissions must survive the entire hierarchy.

Conceptually:

```text
Root SCP
∩
Workloads SCP
∩
Production SCP
∩
IAM
=
Effective Permission
```

---

## 13. Common SCP Guardrails

Examples:

```text
Prevent Leaving Organization

Protect CloudTrail

Protect AWS Config

Protect Security Services

Restrict AWS Regions

Restrict Dangerous Administrative Actions
```

---

# Security OU

## 14. Security Tooling Account

The Security Tooling account handles:

```text
Detection

Monitoring

Investigation

Security Administration

Response Automation
```

Typical services:

```text
GuardDuty

Inspector

Macie

Security Hub

Security Hub CSPM

AWS Config Aggregator

EventBridge
```

---

## 15. Log Archive Account

The Log Archive account handles:

```text
Log Collection

Evidence Preservation

Retention

Audit

Forensics
```

Typical logs:

```text
CloudTrail

AWS Config

VPC Flow Logs

WAF Logs

DNS Logs

Network Logs

Application Logs
```

---

## 16. Why Separate Security Tooling and Log Archive?

Remember:

```text
Security Tooling
→ Analyze

Log Archive
→ Preserve
```

Security analysts need:

```text
Read
Query
Investigate
```

but generally do not need:

```text
Delete Evidence
```

---

# Centralized Security Services

## 17. Delegated Administration

Instead of:

```text
Management Account
→ Daily Security Operations
```

use:

```text
Management Account
       |
       v
Delegation
       |
       v
Security Tooling
```

Supported services can then be centrally managed from the security account.

---

## 18. GuardDuty

Conceptually:

```text
Member Accounts
      |
      v
GuardDuty
      |
      v
Delegated Administrator
      |
      v
Security Tooling
```

Purpose:

```text
Threat Detection
```

---

## 19. Inspector

Conceptually:

```text
EC2 / ECR / Lambda
Across Accounts
       |
       v
Inspector
       |
       v
Security Tooling
```

Purpose:

```text
Vulnerability Management
```

---

## 20. Macie

Conceptually:

```text
S3
Across Accounts
      |
      v
Macie
      |
      v
Security Tooling
```

Purpose:

```text
Sensitive Data Discovery
```

---

## 21. Security Hub

Conceptually:

```text
GuardDuty ───┐
Inspector ───┤
Macie ───────┼──> Security Hub
CSPM ────────┘
```

Purpose:

```text
Centralized Security Visibility

Correlation

Prioritization

Workflow
```

---

# Centralized Logging

## 22. Organization-Wide Logging

A common design:

```text
Prod ──────────────┐
Dev ───────────────┤
Network ───────────┼──> Log Archive
Shared Services ───┘
```

The authoritative log repository should not be controlled by workload administrators.

---

## 23. CloudTrail Organization Trail

Conceptually:

```text
AWS Organization
       |
       v
Organization Trail
       |
       v
All Member Accounts
       |
       v
Central S3
       |
       v
Log Archive
```

This supports consistent audit coverage.

---

## 24. Multi-Region Logging

Security visibility must cover every active Region.

Conceptually:

```text
Tokyo ──────┐
Singapore ──┼──> Central Logging
Virginia ───┘
```

Remember:

```text
Central Administration
≠
Single-Region Coverage
```

---

## 25. AWS Config Aggregation

AWS Config answers:

```text
What changed?
```

A Config Aggregator centralizes:

```text
Resource Inventory

Configuration State

Compliance
```

across accounts and Regions.

---

## 26. CloudTrail and Config Together

Example:

```text
AWS Config
→ Security Group became public

CloudTrail
→ Who changed it?
```

Then:

```text
Flow Logs
→ Was the resource contacted?

OS Logs
→ Was login successful?

GuardDuty
→ Was suspicious activity detected?
```

---

# Log Protection

## 27. Central Log Protection

Use defense in depth:

```text
Dedicated Account
      ↓
S3 Block Public Access
      ↓
Bucket Policy
      ↓
KMS
      ↓
Versioning
      ↓
Object Lock
      ↓
Lifecycle
      ↓
SCP
```

---

## 28. Immutability

A security log should be difficult to modify or destroy.

Conceptually:

```text
Log Written
    |
    v
Retention Period
    |
    X
Deletion
```

S3 Object Lock can provide WORM-style retention.

---

## 29. Why Immutability Matters

Scenario:

```text
Attacker
   |
   v
Compromises Production Admin
   |
   v
Attempts to Delete Evidence
```

With central immutable storage:

```text
Production Compromise
≠
Evidence Destruction
```

---

# Cross-Account IAM

## 30. Cross-Account Roles

Example:

```text
Security Analyst
       |
       v
Security Tooling
       |
       v
sts:AssumeRole
       |
       v
Production Account
       |
       v
SecurityInvestigationRole
```

---

## 31. Trust Policy vs Permission Policy

Remember:

```text
Trust Policy
→ WHO can assume the role?

Permission Policy
→ WHAT can the role do?
```

---

## 32. Temporary Credentials

`AssumeRole` returns temporary STS credentials.

Preferred:

```text
Temporary Role Credential
```

instead of:

```text
Long-Term IAM User
in Every Account
```

---

# IAM Identity Center

## 33. Human Access

A scalable model:

```text
Corporate IdP
      |
      v
IAM Identity Center
      |
      +-- Security Account
      +-- Prod
      +-- Dev
      +-- Network
```

Users receive account-specific permission sets.

---

## 34. Example Access Model

```text
Developer
→ Dev Administrator

Developer
→ Prod ReadOnly

Security Analyst
→ Security Analyst

Network Engineer
→ Network Administrator
```

This supports least privilege.

---

# Centralized Networking

## 35. Network Account

The Network account can manage:

```text
Transit Gateway

Network Firewall

VPN

Direct Connect

Central DNS

Ingress / Egress
```

---

## 36. Hub-and-Spoke Architecture

```text
               Network Account
                     |
              Transit Gateway
              /      |       \
             /       |        \
            v        v         v
         Prod VPC  Dev VPC   Shared VPC
```

This centralizes connectivity.

---

## 37. Central Inspection

Conceptually:

```text
Workload
   |
   v
Transit Gateway
   |
   v
Network Firewall
   |
   v
Internet
```

Possible benefits:

```text
Central Inspection

Consistent Egress Control

Central Routing

Network Separation
```

---

## 38. Network Segmentation

Account separation does not automatically mean network isolation.

You must also control:

```text
Routes

Transit Gateway Attachments

Security Groups

Network Firewall

NACLs
```

---

# Separation of Duties

## 39. Organization Team

Responsible for:

```text
Organizations

OUs

Account Provisioning

SCPs
```

---

## 40. Security Team

Responsible for:

```text
GuardDuty

Inspector

Macie

Security Hub

Investigations
```

---

## 41. Logging Team / Platform

Responsible for:

```text
Log Retention

Archive Configuration

Log Pipeline
```

---

## 42. Network Team

Responsible for:

```text
Routing

Firewall

VPN

Transit Gateway
```

---

## 43. Application Team

Responsible for:

```text
Application Infrastructure

Deployment

Application Configuration
```

---

## 44. Why Separate Duties?

Avoid:

```text
One Administrator
→ Applications
→ Security
→ Logs
→ Network
→ Organization Policies
```

A single compromised credential would have enormous impact.

---

# Blast Radius

## 45. Single-Account Compromise

Poor architecture:

```text
Compromised Administrator
         |
         v
Entire Environment
```

---

## 46. Multi-Account Isolation

Better:

```text
Compromised Dev
      |
      X
Prod
      |
      X
Security
      |
      X
Log Archive
```

assuming cross-account permissions are correctly designed.

---

## 47. Account Boundary Can Be Weakened

Example:

```text
DevAdmin
   |
   v
ProdAdminRole
   |
   v
AdministratorAccess
```

This can turn:

```text
Dev Compromise
```

into:

```text
Prod Compromise
```

Therefore account boundaries must be reinforced with:

```text
Least Privilege

SCPs

Cross-Account IAM

Network Segmentation
```

---

# Break-Glass Access

## 48. Emergency Roles

Production environments may require emergency access.

Conceptually:

```text
Normal Access
→ Restricted

Emergency
→ BreakGlassRole
```

Controls should include:

```text
Strong MFA

Short Session

Limited Trust

CloudTrail Monitoring

Alerting

Post-Use Review
```

---

# Security Service Coverage

## 49. Coverage Is a Security Control

Always ask:

```text
Which Accounts?

Which Regions?

Which Resources?

Which Services?
```

Example:

```text
GuardDuty enabled in Tokyo only

Workload deployed in Singapore
```

means:

```text
Security Coverage Gap
```

---

## 50. No Finding vs No Coverage

Important distinction:

```text
No Finding
→ No issue detected

No Coverage
→ We do not know
```

The second can be more dangerous.

---

# Account Provisioning

## 51. Secure New Account Workflow

```text
Create Account
      ↓
Assign OU
      ↓
Apply SCP
      ↓
Configure Identity
      ↓
Enable Logging
      ↓
Enable Security Services
      ↓
Configure Network
      ↓
Validate Coverage
      ↓
Deploy Workload
```

Security should precede workload deployment.

---

## 52. Security Baseline

A baseline may include:

```text
CloudTrail

AWS Config

GuardDuty

Inspector

Security Hub / CSPM

Central Logging

IAM Identity Center

Region Guardrails

Required Tags
```

---

# Incident Scenario 1

## 53. Compromised Production EC2

Signals:

```text
GuardDuty
→ Suspicious EC2 Activity

Inspector
→ Critical CVE
```

Investigation:

```text
Security Tooling
      |
      v
Security Hub
      |
      v
Cross-Account Investigation Role
      |
      v
Production Account
```

Evidence:

```text
CloudTrail

VPC Flow Logs

OS Logs

AWS Config

GuardDuty
```

---

## 54. Response

Potential flow:

```text
Detect
   ↓
Preserve Evidence
   ↓
Isolate EC2
   ↓
Review IAM Role
   ↓
Analyze Logs
   ↓
Patch / Rebuild
   ↓
Verify
```

Log Archive remains independent throughout.

---

# Incident Scenario 2

## 55. Public S3 with PII

Signals:

```text
Macie
→ PII Detected

AWS Config
→ Public Bucket

GuardDuty
→ Suspicious S3 Access
```

Investigation:

```text
CloudTrail Data Events
→ Who accessed objects?

CloudTrail Management Events
→ Who changed policy?

Config
→ When did bucket become public?
```

---

## 56. Response

```text
Restrict Public Access

Preserve Access Evidence

Determine Exposure Window

Rotate Exposed Credentials

Remove Unnecessary Sensitive Data

Review Security Controls
```

---

# Incident Scenario 3

## 57. Credential Compromise

GuardDuty:

```text
Suspicious IAM Credential
```

CloudTrail shows:

```text
GetSecretValue

Decrypt

GetObject
```

Investigation:

```text
Which Principal?

Which Access Key?

Which Secret?

Which KMS Key?

Which Data?

Which Accounts?
```

---

## 58. Response

Potential actions:

```text
Disable Credential

Revoke Sessions

Rotate Secrets

Review KMS Usage

Review Data Access

Review Cross-Account Roles
```

---

# Incident Scenario 4

## 59. Logging Disabled Attempt

Scenario:

```text
Workload Administrator
      |
      v
cloudtrail:StopLogging
```

Expected protection:

```text
IAM Allow
+
SCP Deny
=
Access Denied
```

Then:

```text
CloudTrail
→ Record Attempt

Security Monitoring
→ Generate Alert
```

---

# Incident Scenario 5

## 60. Unapproved Region Usage

Scenario:

```text
Developer
→ Launches EC2
→ Unapproved Region
```

Preventive control:

```text
SCP
+
aws:RequestedRegion
```

Operational control:

```text
Approved Region List
```

Security benefit:

```text
Reduced Attack Surface

Reduced Monitoring Complexity

Compliance
```

---

# Incident Scenario 6

## 61. Security Analyst Needs Production Access

Requirement:

```text
Investigate Incident

No Daily Admin Access
```

Solution:

```text
Security Tooling
       |
       v
AssumeRole
       |
       v
Production
SecurityInvestigationRole
```

Permissions:

```text
Read EC2

Read IAM Metadata

Read CloudTrail

Read Config

Read Logs
```

Avoid unnecessary:

```text
TerminateInstance

DeleteTrail

CreateAdminUser
```

---

# Architecture Decision Questions

## 62. Where Should This Live?

### GuardDuty Administration

```text
Security Tooling
```

### CloudTrail Archive

```text
Log Archive
```

### Transit Gateway

```text
Network
```

### Production RDS

```text
Production Workload
```

### Shared Directory

```text
Shared Services
```

### Organization SCPs

```text
Management / Organizations Governance
```

---

# Prevent / Detect / Respond

## 63. Prevent

Examples:

```text
SCP

IAM

Network Segmentation

WAF

KMS Policies

Account Isolation
```

---

## 64. Detect

Examples:

```text
GuardDuty

Inspector

Macie

Security Hub CSPM

CloudTrail

AWS Config
```

---

## 65. Respond

Examples:

```text
Security Hub

EventBridge

Lambda

Systems Manager

Incident Response Roles
```

---

# Complete Security Architecture

## 66. End-to-End Model

```text
                           Internet
                              |
                              v
                      Shield / AWS WAF
                              |
                              v
                        Network Account
                              |
                     Transit Gateway
                              |
           +------------------+------------------+
           |                                     |
           v                                     v
       Prod Account                          Dev Account
           |                                     |
           +---------------+---------------------+
                           |
                           v
                    Security Telemetry
                           |
           +---------------+---------------+
           |                               |
           v                               v
   Security Tooling                   Log Archive
           |                               |
     +-----+-----+                   +-----+-----+
     |     |     |                   |           |
     v     v     v                   v           v
 GuardDuty Inspector Macie       CloudTrail      Config
     |     |     |                   |
     +-----+-----+                   +-- Flow Logs
           |                         +-- WAF Logs
           v                         +-- App Logs
     Security Hub
           |
           v
      EventBridge
           |
           v
 Security Operations
```

---

# Architecture Review Questions

## 67. Organization

Ask:

```text
Are accounts separated appropriately?

Are OUs based on common controls?

Is the management account protected?
```

---

## 68. Identity

Ask:

```text
Are users federated?

Are long-term IAM users minimized?

Are cross-account roles least privileged?

Are trust policies restricted?
```

---

## 69. Guardrails

Ask:

```text
Can workloads disable CloudTrail?

Can workloads leave the organization?

Are unapproved Regions blocked?

Can security services be disabled?
```

---

## 70. Logging

Ask:

```text
Are logs centralized?

Can workload admins delete them?

Are logs encrypted?

Is retention defined?

Is immutability required?
```

---

## 71. Security Monitoring

Ask:

```text
Does GuardDuty cover every account?

Does Inspector cover all required resources?

Does Macie cover sensitive S3 data?

Are findings centralized?
```

---

## 72. Networking

Ask:

```text
Are Prod and Dev segmented?

Is egress controlled?

Is inspection centralized?

Who can change routes and firewalls?
```

---

## 73. Incident Response

Ask:

```text
Can security analysts investigate other accounts?

Is break-glass access available?

Are response actions logged?

Is evidence preserved?
```

---

# Common Architecture Mistakes

## 74. Everything in One Account

Risk:

```text
Large Blast Radius
```

---

## 75. Security Tooling and Workloads Together

Risk:

```text
Workload Admin
→ Security Monitoring Control
```

---

## 76. Logs Stored Only in Workload Accounts

Risk:

```text
Attacker
→ Deletes Evidence
```

---

## 77. Broad Cross-Account Administrator Roles

Risk:

```text
One Account Compromise
→ Organization-Wide Compromise
```

---

## 78. No Region Strategy

Risk:

```text
Workload Exists
in Unmonitored Region
```

---

## 79. Security Services Enabled Manually

Risk:

```text
New Account
→ GuardDuty Forgotten
```

Prefer organization-based deployment and delegated administration.

---

## 80. SCP Attached Directly to Root Without Testing

Risk:

```text
Organization-Wide Outage
```

Better:

```text
Test OU
→ Validate
→ Gradual Deployment
```

---

## 81. Security Analysts Have Delete Access to Logs

Risk:

```text
Compromised Security Credential
→ Evidence Destruction
```

Separate:

```text
Read

from

Delete / Retention Administration
```

---

# Hands-on Practice

## 82. Draw the Entire Architecture

Draw:

```text
Management
   |
Organizations
   |
   +-- Security
   |     +-- Security Tooling
   |     +-- Log Archive
   |
   +-- Infrastructure
   |     +-- Network
   |     +-- Shared Services
   |
   +-- Workloads
         +-- Prod
         +-- NonProd
```

For each account, write:

```text
Purpose

Owner

Services

Permissions

SCPs

Logging

Cross-Account Access
```

---

## 83. Architecture Scenario

Requirements:

```text
Public Customer Website

Sensitive Customer Data

Production and Development

Central Security Team

Central Network Team

Compliance Logging

Incident Response
```

Design the accounts:

```text
Management

Security Tooling

Log Archive

Network

Shared Services

CustomerApp-Prod

CustomerApp-Dev
```

---

## 84. Security Service Placement

Add:

```text
Security Tooling
→ GuardDuty
→ Inspector
→ Macie
→ Security Hub

Log Archive
→ CloudTrail
→ Config History
→ Flow Logs

Network
→ Transit Gateway
→ Network Firewall

Prod
→ EC2 / ECS
→ RDS
→ S3
→ KMS
→ Secrets Manager
```

---

## 85. Guardrail Exercise

Design guardrails:

```text
All Accounts
→ Cannot Leave Organization

Workloads
→ Cannot Disable Logging

Production
→ Approved Regions Only

Security Accounts
→ Security Administration Allowed

Log Archive
→ Delete Restricted
```

---

## 86. Investigation Exercise

Scenario:

```text
GuardDuty
→ Compromised IAM Credential
```

Write investigation path:

```text
1. Review GuardDuty finding

2. Identify principal

3. Review CloudTrail

4. Review cross-account AssumeRole activity

5. Review Secrets Manager access

6. Review KMS activity

7. Review S3 access

8. Determine scope

9. Disable credentials

10. Preserve evidence

11. Remediate

12. Verify
```

---

## 87. Optional CLI Review

Organization:

```bash
aws organizations describe-organization
```

Accounts:

```bash
aws organizations list-accounts
```

SCPs:

```bash
aws organizations list-policies \
  --filter SERVICE_CONTROL_POLICY
```

Delegated administrators:

```bash
aws organizations list-delegated-administrators
```

CloudTrail:

```bash
aws cloudtrail describe-trails
```

Config aggregators:

```bash
aws configservice describe-configuration-aggregators
```

Do not expose real internal AWS architecture information in a public repository.

---

# Security Architecture Checklist

```text
[ ] AWS Organizations is used for multi-account governance

[ ] Management account is tightly protected

[ ] Application workloads are outside the management account

[ ] Security Tooling has a dedicated account

[ ] Log Archive has a dedicated account

[ ] Network infrastructure is separated where appropriate

[ ] Shared Services are isolated where appropriate

[ ] Production and non-production are separated

[ ] OUs reflect common security controls

[ ] SCPs provide organization-wide guardrails

[ ] SCPs are tested before broad deployment

[ ] Human access uses federation / IAM Identity Center

[ ] Cross-account access uses IAM roles

[ ] Trust policies are narrowly scoped

[ ] Cross-account permissions follow least privilege

[ ] Delegated administration is used where supported

[ ] GuardDuty is centrally administered

[ ] Inspector coverage is centrally reviewed

[ ] Macie covers required sensitive-data environments

[ ] Security findings are centralized

[ ] Organization-wide CloudTrail is configured

[ ] AWS Config provides centralized configuration visibility

[ ] Logs are stored outside workload accounts

[ ] Log storage uses strong access controls

[ ] Encryption protects centralized logs

[ ] Versioning and Object Lock are considered for evidence protection

[ ] Workload administrators cannot delete authoritative logs

[ ] Logging failures are monitored

[ ] Security services cover every approved Region

[ ] Centralized networking is protected

[ ] Prod and Dev network access is explicitly controlled

[ ] Break-glass access is monitored

[ ] Incident responders can obtain required cross-account visibility

[ ] Security architecture is reviewed periodically
```

---

## Key Takeaways

- AWS Organizations provides the foundation for scalable multi-account governance.
- AWS accounts provide strong security and resource boundaries.
- OUs group accounts that require common controls.
- SCPs define organization-level permission guardrails but do not grant permissions.
- The management account should remain minimal and strongly protected.
- Security Tooling centralizes security administration, detection, and response.
- Log Archive preserves authoritative audit and forensic evidence.
- Security Tooling and Log Archive should have different responsibilities.
- Cross-account IAM roles provide temporary access between AWS accounts.
- Trust policies determine who can assume a role.
- Permission policies determine what an assumed role can do.
- IAM Identity Center provides scalable workforce access across accounts.
- Delegated administration reduces operational dependency on the management account.
- Centralized networking provides consistent routing and inspection.
- Organization-wide logging improves traceability and forensic readiness.
- Log immutability protects evidence from compromised workload administrators.
- Multi-Region coverage must be explicitly designed.
- Security-service coverage is as important as security findings.
- Multi-account architecture reduces blast radius only when cross-account permissions remain least privileged.
- A secure AWS architecture combines preventive, detective, and responsive controls.

---

## Reflection

During this phase, I learned how AWS security services can be organized into a scalable multi-account security architecture.

AWS Organizations provides centralized governance, while Organizational Units and dedicated accounts create isolation boundaries for security, logging, networking, shared services, and application workloads.

Service Control Policies provide preventive guardrails that restrict dangerous operations even when administrators have broad IAM permissions.

I also learned that Security Tooling and Log Archive accounts serve fundamentally different purposes. Security Tooling focuses on detection, investigation, and response, while Log Archive protects the evidence required for auditing and incident investigation.

Cross-account IAM roles, delegated administration, centralized logging, centralized networking, and organization-wide security services allow security teams to manage large AWS environments without giving every administrator unrestricted access.

The most important lesson is that cloud security architecture is not based on one security product. It depends on carefully designed account boundaries, identity, governance, logging, monitoring, networking, data protection, and incident response working together.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Blast Radius | Scope of impact caused by a security compromise or failure |
| Cross-Account Access | Access from a principal in one AWS account to resources or roles in another account |
| Delegated Administration | Allowing a member account to centrally administer a supported AWS service |
| Forensic Readiness | Ability to preserve and analyze reliable evidence during a security incident |
| Guardrail | Preventive boundary controlling what actions are permitted |
| Log Immutability | Protection that prevents security evidence from being modified or deleted |
| Multi-Account Architecture | AWS architecture that separates functions and workloads across multiple AWS accounts |
| Organizational Unit | Logical AWS Organizations container for accounts requiring common governance |
| Security Architecture | Overall design of security controls, boundaries, identities, monitoring, and response systems |
| Separation of Duties | Dividing responsibilities to prevent one identity from controlling an entire security process |
