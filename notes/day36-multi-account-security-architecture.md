# Day 36 — Multi-Account Security Architecture

## Topic

AWS Multi-Account Security Architecture, Dedicated Security Accounts, Cross-Account Roles, Delegated Administration, and Centralized Governance

---

## Objectives

- Understand why AWS uses a multi-account security architecture
- Understand the role of the management account
- Understand the purpose of Security Tooling and Log Archive accounts
- Understand Network and Shared Services accounts
- Understand Production and NonProduction workload accounts
- Learn how cross-account IAM roles work
- Understand trust policies and permission policies
- Understand the role of AWS IAM Identity Center
- Learn delegated administration
- Understand centralized security service administration
- Understand centralized networking
- Understand separation of duties
- Understand blast radius reduction
- Learn how SCPs support multi-account architecture
- Design a complete multi-account AWS security architecture

---

# Multi-Account Architecture Fundamentals

## 1. Why Multi-Account Architecture?

AWS accounts provide strong security and resource boundaries.

A multi-account architecture separates workloads and responsibilities.

Poor design:

```text
Single AWS Account
│
├── Production
├── Development
├── Security Tools
├── Networking
├── Logging
└── Shared Services
```

Potential problems:

```text
Large Blast Radius

Privilege Overlap

Difficult IAM Management

Weak Separation of Duties

Logging Can Be Modified by Workload Admins
```

Better:

```text
Multiple AWS Accounts
      |
      +-- Security
      +-- Logging
      +-- Networking
      +-- Production
      +-- Development
```

---

## 2. Account as a Security Boundary

Each AWS account has separate:

```text
IAM

Resources

Service Quotas

Billing Context

Security Configuration
```

Conceptually:

```text
Account A
   |
   X
Account B
```

Access between accounts requires explicit configuration.

This makes accounts useful for security isolation.

---

## 3. Main Security Benefits

Multi-account architecture provides:

```text
Blast Radius Reduction

Separation of Duties

Central Governance

Resource Isolation

Billing Separation

Security Service Centralization

Environment Isolation
```

---

# Organization Structure

## 4. Reference Architecture

A common architecture:

```text
AWS Organization
      |
      v
     Root
      |
      +-------------------------+
      |                         |
      v                         v
 Security OU             Infrastructure OU
      |                         |
 +----+----+               +----+----+
 |         |               |         |
 v         v               v         v
Security  Log           Network    Shared
Tooling   Archive                  Services

      |
      v
 Workloads OU
      |
 +----+----+
 |         |
 v         v
Prod     NonProd
```

---

# Management Account

## 5. Management Account

The management account owns and administers the AWS Organization.

Typical responsibilities:

```text
AWS Organizations

OU Management

Account Creation

Organization Policies

Delegated Administration

Billing Governance
```

---

## 6. Management Account Should Remain Minimal

The management account should not normally host application workloads.

Avoid:

```text
Production EC2

RDS Databases

Development Workloads

Security Analysis Tools
```

Use it primarily for:

```text
Organization Governance
```

---

## 7. Why This Matters

The management account has special privileges.

Also:

```text
SCPs
→ Do Not Restrict Management Account
```

Therefore, placing normal workloads there increases risk.

Conceptually:

```text
Highly Privileged Account
+
Application Workload
=
Unnecessary Attack Surface
```

---

# Security OU

## 8. Security OU

The Security OU contains centralized security accounts.

Typical structure:

```text
Security OU
│
├── Security Tooling
└── Log Archive
```

These accounts serve different security responsibilities.

---

# Security Tooling Account

## 9. Purpose

The Security Tooling account centralizes security operations.

Possible services include:

```text
Amazon GuardDuty

Amazon Inspector

Amazon Macie

AWS Security Hub

Security Hub CSPM

Security Automation
```

Conceptually:

```text
Organization Accounts
       |
       v
Security Signals
       |
       v
Security Tooling Account
       |
       v
Security Team
```

---

## 10. Why Separate Security Tooling?

Application administrators should not automatically control security monitoring.

Example:

```text
Application Admin
     |
     X
Disable Organization Security Monitoring
```

Instead:

```text
Security Team
→ Security Tooling Account

Application Team
→ Workload Account
```

This supports separation of duties.

---

# Log Archive Account

## 11. Purpose

The Log Archive account stores centralized security and audit logs.

Examples:

```text
CloudTrail Logs

AWS Config Data

VPC Flow Logs

WAF Logs

Network Firewall Logs

Application Security Logs
```

Architecture:

```text
Prod ─────────┐
Dev ──────────┤
Network ──────┼──> Log Archive
Security ─────┘
```

---

## 12. Why Separate the Log Archive?

Suppose a production account is compromised.

Poor architecture:

```text
Attacker
   |
   v
Production Admin
   |
   v
Delete Production Logs
```

Better:

```text
Production
   |
   v
Cross-Account Log Delivery
   |
   v
Log Archive
```

The attacker may compromise the workload account without gaining permission to delete central evidence.

---

## 13. Log Archive Security

Important controls include:

```text
Restricted Write Access

Restricted Delete Access

S3 Block Public Access

Encryption

Versioning

Object Lock

Retention Policies

Monitoring
```

The goal is:

```text
Workload Administrator
→ Cannot Destroy Central Evidence
```

---

# Security Tooling vs Log Archive

## 14. Different Responsibilities

A useful distinction:

```text
Security Tooling
→ Analyze and respond

Log Archive
→ Preserve evidence
```

Example:

```text
Security Analyst
→ Read logs

Log Archive Administrator
→ Manage retention

Application Developer
→ No delete access
```

---

# Infrastructure OU

## 15. Infrastructure OU

The Infrastructure OU contains shared foundational services.

Typical accounts:

```text
Network

Shared Services
```

---

# Network Account

## 16. Network Account

The Network account centralizes important networking services.

Examples:

```text
Transit Gateway

AWS Network Firewall

VPN

Direct Connect Connectivity

Central DNS

Ingress / Egress Infrastructure
```

Conceptually:

```text
Workload VPCs
      |
      v
Transit Gateway
      |
      v
Network Account
      |
      v
Internet / On-Premises / Shared Networks
```

---

## 17. Why Centralize Networking?

Benefits:

```text
Consistent Routing

Central Inspection

Reduced Workload Permissions

Central Egress Control

Simpler Governance
```

Application teams do not necessarily need permission to change:

```text
Organization-Wide Routing

Central Firewalls

VPN Connections
```

---

# Shared Services Account

## 18. Shared Services

Shared Services hosts common services used by multiple workloads.

Examples:

```text
Directory Services

Shared DNS

CI/CD Services

Artifact Repositories

Internal Tools
```

Architecture:

```text
Production ───┐
Development ──┼──> Shared Services
Other Apps ───┘
```

---

## 19. Shared Services Security

Shared Services can become highly privileged because many accounts depend on it.

Controls should include:

```text
Least Privilege

Network Segmentation

Strong Authentication

Central Logging

Backup

Monitoring
```

---

# Workload Accounts

## 20. Workload Accounts

Workload accounts contain application resources.

Examples:

```text
EC2

ECS

EKS

Lambda

RDS

S3

Application Load Balancers
```

These accounts should focus on running applications.

---

## 21. Production Accounts

Production workload accounts typically have stricter controls.

Examples:

```text
Approved Regions Only

Central Logging Mandatory

Security Services Mandatory

Restricted Public Networking

Strong Change Management
```

---

## 22. NonProduction Accounts

Development and testing accounts may provide more flexibility.

Examples:

```text
More Service Experimentation

More Developer Permissions
```

but still need baseline controls:

```text
Central Logging

GuardDuty

Region Restrictions

Cost Controls

No Organization Escape
```

---

# Application-Based Account Separation

## 23. Separate by Workload

A useful pattern:

```text
Payment-Prod

Payment-Dev

CustomerPortal-Prod

CustomerPortal-Dev
```

This is often better than:

```text
Team-A Account

Team-B Account
```

because teams may change while workloads remain.

---

# Cross-Account Access

## 24. Why Cross-Account Access Is Needed

Users and services sometimes need to access resources in another AWS account.

Example:

```text
Security Analyst
      |
      v
Security Tooling
      |
      v
Production Read-Only Role
```

Cross-account access should be explicitly delegated.

---

## 25. Cross-Account IAM Role

A common model:

```text
Account A
Principal
   |
   v
AssumeRole
   |
   v
Account B
IAM Role
```

The role in Account B defines what the caller can do after assuming it.

---

## 26. Trust Policy

The destination role contains a trust policy.

Example concept:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111122223333:role/SecurityAnalyst"
  },
  "Action": "sts:AssumeRole"
}
```

This answers:

```text
Who may assume this role?
```

---

## 27. Permission Policy

The role also has permissions.

Example:

```json
{
  "Effect": "Allow",
  "Action": [
    "ec2:Describe*",
    "cloudtrail:LookupEvents"
  ],
  "Resource": "*"
}
```

This answers:

```text
What may the assumed role do?
```

---

## 28. Trust vs Permissions

Remember:

```text
Trust Policy
→ Who can assume the role?

Permission Policy
→ What can the role do?
```

Both are needed.

---

## 29. Cross-Account Access Flow

```text
Security Analyst
      |
      v
Authenticated Identity
      |
      v
sts:AssumeRole
      |
      v
Production SecurityReadOnlyRole
      |
      v
Temporary Credentials
      |
      v
Read Production Resources
```

---

## 30. Temporary Credentials

Cross-account roles use:

```text
AWS STS
```

to issue temporary security credentials.

This is preferable to:

```text
Creating Long-Term IAM Users
in Every Account
```

---

# IAM Identity Center

## 31. Human Access

For workforce access, a scalable multi-account architecture commonly uses:

```text
AWS IAM Identity Center
```

Conceptually:

```text
Corporate Identity Provider
       |
       v
IAM Identity Center
       |
       +-- Production
       |
       +-- Development
       |
       +-- Security
```

Users can receive different permission sets per account.

---

## 32. Example Permission Sets

```text
Developer
→ Development Administrator

Developer
→ Production ReadOnly

Security Analyst
→ Security Tooling Analyst

Network Engineer
→ Network Administrator
```

This avoids creating separate IAM users in every account.

---

## 33. Human vs Workload Identity

A useful distinction:

```text
Human Access
→ Federation / IAM Identity Center

AWS Workload Access
→ IAM Roles

Cross-Account Workload Access
→ AssumeRole / Resource Policy
```

Long-term IAM access keys should be avoided where possible.

---

# Delegated Administration

## 34. Security Service Delegation

Supported services can delegate organization administration to a member account.

Conceptually:

```text
Management Account
      |
      v
Delegate
      |
      v
Security Tooling
      |
      +-- GuardDuty
      +-- Inspector
      +-- Macie
      +-- Security Hub CSPM
```

---

## 35. Why Delegate?

Poor:

```text
Management Account
→ Daily Security Operations
```

Better:

```text
Management Account
→ Organization Governance

Security Tooling
→ Security Operations
```

This reduces exposure of the management account.

---

# GuardDuty Architecture

## 36. Central GuardDuty

Conceptually:

```text
Production ─────┐
Development ────┤
Other Accounts ─┼──> GuardDuty Administrator
Network ────────┘
                         |
                         v
                 Security Tooling
```

The security account can centrally review findings across member accounts.

---

## 37. GuardDuty Auto-Enable

Organization integration can help automatically enable GuardDuty capabilities for appropriate member accounts.

This helps reduce gaps when:

```text
New Account Created
       |
       v
Security Monitoring Forgotten
```

---

# Inspector Architecture

## 38. Central Inspector

Conceptually:

```text
EC2 / ECR / Lambda
Across Member Accounts
          |
          v
Amazon Inspector
          |
          v
Delegated Administrator
          |
          v
Security Tooling
```

This enables centralized vulnerability visibility.

---

# Macie Architecture

## 39. Central Macie

Conceptually:

```text
S3 Buckets
Across Member Accounts
       |
       v
Amazon Macie
       |
       v
Macie Administrator
       |
       v
Security Tooling
```

This provides organization-wide sensitive data visibility.

---

# Security Hub Architecture

## 40. Central Security Hub

Conceptually:

```text
GuardDuty ──┐
Inspector ──┤
Macie ──────┼──> Security Hub
CSPM ───────┘
                 |
                 v
        Security Tooling Account
```

This provides centralized security finding management.

---

## 41. Security Hub CSPM Central Configuration

A delegated administrator can centrally define:

```text
Security Hub CSPM Enabled?

Which Standards?

Which Controls?
```

for:

```text
Accounts

OUs

Regions
```

This improves configuration consistency.

---

# Cross-Account Logging

## 42. Central Logging Flow

Example:

```text
Production Account
     |
     +-- CloudTrail
     +-- VPC Flow Logs
     +-- WAF Logs
     |
     v
Log Archive Account
```

Logs should be delivered using tightly controlled cross-account permissions.

---

## 43. Log Writer vs Log Reader

A useful permission model:

```text
Workload Account
→ Write Logs

Security Analyst
→ Read Logs

Workload Admin
→ Cannot Delete Logs

Security Analyst
→ Cannot Modify Application
```

This creates strong separation of duties.

---

# SCP Integration

## 44. Multi-Account Architecture + SCP

SCPs strengthen account separation.

Example:

```text
Workload Administrator
       |
       X
Stop Organization Logging
```

Possible guardrails:

```text
Prevent CloudTrail Disable

Prevent Config Disable

Prevent GuardDuty Disable

Restrict Regions

Prevent Leaving Organization
```

---

## 45. Security OU SCPs

Be careful not to over-restrict the Security OU.

Security administrators may require actions not available to ordinary workload accounts.

Example:

```text
Workloads OU
→ Strict Denies

Security OU
→ Security Administration Exceptions
```

Exceptions should be narrowly scoped.

---

# Centralized Networking

## 46. Hub-and-Spoke Model

A common multi-account network architecture:

```text
              Network Account
                    |
              Transit Gateway
               /     |      \
              /      |       \
             v       v        v
          Prod VPC  Dev VPC  Shared VPC
```

This provides centralized connectivity.

---

## 47. Central Inspection

Traffic can be routed through centralized inspection infrastructure.

Example:

```text
Workload VPC
     |
     v
Transit Gateway
     |
     v
AWS Network Firewall
     |
     v
Internet
```

Benefits:

```text
Consistent Inspection

Centralized Egress Control

Security Policy Enforcement
```

---

## 48. Network Separation

Production and development networks can remain separate even when sharing central infrastructure.

Conceptually:

```text
Production
     |
     X
Development
```

unless explicitly routed and permitted.

---

# Separation of Duties

## 49. Organization Administrator

Responsibilities:

```text
Organizations

OU Structure

SCPs

Account Provisioning
```

Should not necessarily perform:

```text
Daily Application Administration
```

---

## 50. Security Team

Responsibilities:

```text
GuardDuty

Inspector

Macie

Security Hub

Investigation
```

Should not automatically control:

```text
Application Deployment

Production Database Administration
```

---

## 51. Network Team

Responsibilities:

```text
Transit Gateway

Network Firewall

VPN

Central Routing
```

Should not automatically access:

```text
Secrets

Customer Database Records
```

---

## 52. Application Team

Responsibilities:

```text
Application Deployment

Application Infrastructure

Application Monitoring
```

Should not automatically modify:

```text
Organization SCPs

Central Security Monitoring

Central Logs

Organization Networking
```

---

# Blast Radius

## 53. Security Incident Example

Suppose a development administrator is compromised.

Single-account architecture:

```text
Compromised Dev Admin
      |
      v
Production
Security
Logging
Network
```

Potentially large impact.

Multi-account architecture:

```text
Compromised Dev Account
      |
      X
Production
      |
      X
Security Tooling
      |
      X
Log Archive
```

assuming permissions are correctly designed.

---

## 54. Cross-Account Role Risk

Account separation can be weakened by broad cross-account roles.

Risky:

```text
Dev Admin
   |
   v
AssumeRole
   |
   v
Prod AdministratorAccess
```

Better:

```text
Dev User
   |
   v
Prod ReadOnlyRole
```

or no production access at all unless required.

---

# Break-Glass Access

## 55. Emergency Administrative Access

Organizations may need emergency access for incidents.

Conceptually:

```text
Normal Access
→ Restricted

Emergency
→ Break-Glass Role
```

A break-glass role should have:

```text
Strong Authentication

Limited Trusted Principals

Monitoring

Alerting

Short Sessions

Post-Incident Review
```

---

## 56. Break-Glass Is Not Daily Admin

Avoid:

```text
Use Emergency Role Every Day
```

The role should be reserved for exceptional events.

Every use should trigger review.

---

# Resource Sharing

## 57. Cross-Account Resource Sharing

Some AWS resources can be shared using:

```text
Resource-Based Policies

AWS RAM

Cross-Account Roles
```

Examples:

```text
S3 Bucket

KMS Key

Transit Gateway

Route 53 Resolver Rules
```

Sharing should be intentional and documented.

---

## 58. AWS Resource Access Manager

AWS RAM can share supported resources across accounts.

Conceptually:

```text
Network Account
      |
      v
Transit Gateway
      |
      v
AWS RAM
      |
      +-- Production
      +-- Development
```

This allows centralized ownership without duplicating the resource.

---

# Account Provisioning

## 59. New Account Workflow

A secure account lifecycle might look like:

```text
Request New Account
       |
       v
Create Account
       |
       v
Assign OU
       |
       v
Apply SCPs
       |
       v
Enable Central Logging
       |
       v
Enable Security Services
       |
       v
Configure IAM Identity Center
       |
       v
Deploy Workload
```

Security should be applied before production workloads start.

---

## 60. Account Baseline

Every account should have a baseline.

Possible controls:

```text
CloudTrail

AWS Config

GuardDuty

Security Hub / CSPM

Required Tags

Approved Regions

IAM Access

Central Logging
```

---

# Common Misconfigurations

## 61. Security Team Has Production AdministratorAccess Everywhere

Risk:

```text
Security Analyst
      |
      v
AdministratorAccess
      |
      v
Every Account
```

This creates excessive privilege.

Better:

```text
SecurityReadOnly

Investigation Role

Separate Remediation Role
```

---

## 62. Workload Admin Can Delete Central Logs

Poor:

```text
Production Admin
      |
      v
Delete Log Archive Data
```

This defeats centralized logging.

Cross-account permissions should prevent it.

---

## 63. Management Account Used for Daily Work

Risk:

```text
More Human Access
+
More Credentials
+
More Workloads
=
Greater Attack Surface
```

Keep management account usage minimal.

---

## 64. Security Service Enabled Manually Per Account

Poor:

```text
Account A → GuardDuty Enabled

Account B → Enabled

Account C → Forgotten
```

Better:

```text
Organization Integration
+
Delegated Administration
+
Automatic Enrollment
```

where supported.

---

## 65. Broad Cross-Account Trust

Risky trust:

```text
Principal:
Entire External Account
```

without additional controls.

Better:

```text
Specific Role

Specific Organization

Conditions

Least Privilege
```

---

## 66. No Network Separation

Poor:

```text
Prod
↔
Dev
↔
Shared
```

with unrestricted routing.

Better:

```text
Explicit Network Paths

Firewall Inspection

Security Groups

Route Controls
```

---

# Investigation Scenario

## 67. Compromised Production Account

Scenario:

```text
GuardDuty
→ Potential Compromise

Production Account
```

Security architecture should allow:

```text
Security Tooling
→ Review Finding

Log Archive
→ Preserve Evidence

Security Analyst Role
→ Read Production Data

Network Account
→ Isolate Network

Production Account
→ Remediation
```

No single compromised workload account should control the entire response infrastructure.

---

## 68. Incident Response Flow

```text
GuardDuty Finding
       |
       v
Security Tooling
       |
       v
Security Analyst
       |
       v
Cross-Account Investigation Role
       |
       v
Affected Production Account
       |
       +-- CloudTrail
       +-- EC2
       +-- IAM
       +-- Config
       |
       v
Containment
```

Meanwhile:

```text
Log Archive
→ Evidence Remains Protected
```

---

# Hands-on Practice

## 69. Draw the Architecture

Create this diagram:

```text
Management
   |
Organizations
   |
   +-- Security
   |    +-- Security Tooling
   |    +-- Log Archive
   |
   +-- Infrastructure
   |    +-- Network
   |    +-- Shared Services
   |
   +-- Workloads
        +-- Production
        +-- NonProduction
```

For each account, write:

```text
Purpose

Owner

Major Services

Who Can Access?

Which SCPs Apply?
```

---

## 70. Cross-Account Role Exercise

Scenario:

```text
Security Analyst
in Security Tooling
```

needs read-only investigation access to:

```text
Production Account
```

Design:

```text
Production:
SecurityInvestigationRole

Trust:
Security Analyst Principal

Permissions:
Read-Only Security APIs
```

Ask:

```text
Does the analyst need write access?

Can the role modify IAM?

Can it delete logs?

Can it terminate EC2?
```

Apply least privilege.

---

## 71. Delegated Administration Exercise

Choose the account that should manage:

```text
GuardDuty
→ Security Tooling

Inspector
→ Security Tooling

Macie
→ Security Tooling

Security Hub
→ Security Tooling
```

Avoid daily management from:

```text
Management Account
```

where delegation is supported.

---

## 72. Logging Exercise

Design:

```text
Production CloudTrail
      |
      v
Log Archive S3
```

Permissions:

```text
Production
→ Write

Security Analyst
→ Read

Production Admin
→ No Delete

Developer
→ No Access
```

---

## 73. Network Exercise

Design:

```text
Prod VPC
    \
     \
 Transit Gateway
     /
    /
Dev VPC
```

Then add:

```text
Network Firewall
```

and determine:

```text
Which traffic requires inspection?

Should Dev reach Prod?

Where should Internet egress occur?
```

---

## 74. Optional CLI Practice

Assume a cross-account role:

```bash
aws sts assume-role \
  --role-arn arn:aws:iam::<account-id>:role/SecurityInvestigationRole \
  --role-session-name security-investigation
```

List organization accounts:

```bash
aws organizations list-accounts
```

List delegated administrators:

```bash
aws organizations list-delegated-administrators
```

List delegated services for an account:

```bash
aws organizations list-delegated-services-for-account \
  --account-id <account-id>
```

Do not publish real:

```text
Account IDs

Role ARNs

Organization IDs

Network Architecture Details

Internal Security Account Names
```

to a public repository.

---

# Architecture Exercise

## 75. Complete Production Architecture

```text
                           Management Account
                                  |
                                  v
                           AWS Organizations
                                  |
             +--------------------+---------------------+
             |                    |                     |
             v                    v                     v
        Security OU        Infrastructure OU       Workloads OU
             |                    |                     |
        +----+----+          +----+----+           +----+----+
        |         |          |         |           |         |
        v         v          v         v           v         v
    Security    Log       Network   Shared       Prod      NonProd
    Tooling     Archive              Services
        |         |          |
        |         |          +-- Transit Gateway
        |         |          +-- Network Firewall
        |         |
        |         +-- CloudTrail
        |         +-- Config
        |         +-- WAF Logs
        |
        +-- GuardDuty
        +-- Inspector
        +-- Macie
        +-- Security Hub
```

---

## 76. Security Layers

### Organization Layer

```text
Organizations

OUs

SCPs
```

### Identity Layer

```text
IAM Identity Center

IAM Roles

Cross-Account AssumeRole
```

### Security Layer

```text
GuardDuty

Inspector

Macie

Security Hub
```

### Logging Layer

```text
CloudTrail

AWS Config

Flow Logs

Central S3 Archive
```

### Network Layer

```text
Transit Gateway

Network Firewall

Security Groups

Route Tables
```

### Workload Layer

```text
EC2

ECS

Lambda

RDS

S3
```

Defense in depth exists across every layer.

---

# Security Checklist

```text
[ ] Management account contains no unnecessary workloads

[ ] Security Tooling account is separated from workloads

[ ] Log Archive account is separately protected

[ ] Network account centralizes required networking functions

[ ] Shared Services are separated where appropriate

[ ] Production and non-production workloads are separated

[ ] Account boundaries match security requirements

[ ] Human access uses federation / IAM Identity Center where appropriate

[ ] Cross-account access uses temporary IAM role credentials

[ ] Trust policies are narrowly scoped

[ ] Cross-account role permissions follow least privilege

[ ] Security services use delegated administration where supported

[ ] New accounts receive required security services automatically where possible

[ ] SCPs protect organization security controls

[ ] Central logs cannot be deleted by workload administrators

[ ] Network paths between accounts are explicitly controlled

[ ] Break-glass roles are monitored and rarely used

[ ] Security findings are centralized

[ ] Account provisioning applies security baselines before workload deployment

[ ] Cross-account permissions are periodically reviewed
```

---

## Key Takeaways

- AWS accounts provide strong security and resource isolation boundaries.
- Multi-account architecture reduces blast radius and improves separation of duties.
- The management account should focus on organization governance.
- Security Tooling centralizes security operations.
- Log Archive preserves security evidence independently from workload accounts.
- Network accounts can centralize routing, inspection, and external connectivity.
- Shared Services provide common organization-wide capabilities.
- Production and non-production workloads should be isolated.
- Cross-account IAM roles provide temporary delegated access between accounts.
- Trust policies determine who can assume a role.
- Permission policies determine what an assumed role can do.
- Human multi-account access should use federation or IAM Identity Center where appropriate.
- Delegated administration reduces daily operational use of the management account.
- Organization integrations help reduce security coverage gaps.
- SCPs reinforce account boundaries with organization-wide guardrails.
- Centralized networking can provide consistent inspection and egress control.
- Multi-account architecture is effective only when cross-account permissions remain least-privileged.

---

## Reflection

Today I learned how multiple AWS security concepts fit together into a complete multi-account architecture.

The most important lesson is that account separation provides both organizational structure and security isolation.

The management account should be used primarily for organization governance, while dedicated Security Tooling, Log Archive, Network, Shared Services, and workload accounts handle operational responsibilities.

I also learned that cross-account IAM roles allow security teams and other administrators to access accounts without creating permanent IAM users everywhere.

From a cloud security perspective, multi-account architecture combines account isolation, delegated administration, centralized logging, centralized security services, network segmentation, SCP guardrails, and least-privilege cross-account access to reduce organizational risk.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Blast Radius | Scope of resources or systems potentially affected by a compromise or failure |
| Cross-Account Role | IAM role that can be assumed by an authorized principal from another AWS account |
| IAM Identity Center | AWS service for centralized workforce access to multiple AWS accounts |
| Log Archive Account | Dedicated account for protected centralized log storage |
| Multi-Account Architecture | AWS design that separates workloads and functions across multiple AWS accounts |
| Network Account | Account hosting centralized network infrastructure |
| Security Tooling Account | Dedicated account for centralized security services and security operations |
| Shared Services Account | Account hosting common services used by multiple workloads |
| STS | AWS service that issues temporary security credentials |
| Trust Policy | IAM role policy that defines who can assume the role |
