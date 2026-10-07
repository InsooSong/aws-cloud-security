# Day 34 — AWS Organizations

## Topic

AWS Organizations Fundamentals, Multi-Account Governance, Organizational Units, Management Accounts, and Delegated Administration

---

## Objectives

- Understand the purpose of AWS Organizations
- Understand why AWS recommends multi-account environments
- Learn the organization hierarchy
- Understand roots and organizational units
- Understand management accounts and member accounts
- Learn how accounts create security boundaries
- Understand delegated administration
- Understand trusted access
- Learn the purpose of AWS Organizations policies
- Understand the role of SCPs at a high level
- Learn about Resource Control Policies and declarative policies
- Understand common foundational OU designs
- Understand how Security, Infrastructure, and Workload accounts are separated
- Learn how AWS Control Tower relates to AWS Organizations
- Design a basic multi-account AWS security architecture

---

# AWS Organizations Fundamentals

## 1. What Is AWS Organizations?

AWS Organizations is a service for centrally managing multiple AWS accounts.

Conceptually:

```text
AWS Organization
      |
      +-- Account A
      |
      +-- Account B
      |
      +-- Account C
```

Instead of operating every AWS account independently, Organizations provides centralized:

```text
Account Management

Governance

Policy Management

Service Integration

Billing Management
```

---

## 2. Why Use Multiple AWS Accounts?

An AWS account is an important security and resource isolation boundary.

Conceptually:

```text
One Large Account
      |
      +-- Production
      +-- Development
      +-- Security
      +-- Networking
```

can create a large blast radius.

A multi-account model can separate these environments:

```text
Production Account

Development Account

Security Account

Network Account

Log Archive Account
```

This improves:

```text
Isolation

Least Privilege

Separation of Duties

Billing Visibility

Blast Radius Reduction

Governance
```

---

## 3. Account as a Security Boundary

AWS accounts provide boundaries for:

```text
IAM

Resources

Quotas

Billing

Logging

Security Administration
```

By default:

```text
Account A
    |
    X
Account B
```

Resources in one account are not automatically accessible from another account.

Cross-account access must be explicitly configured.

---

## 4. Why Account Separation Matters

Suppose:

```text
Development
+
Production
```

exist in the same account.

A highly privileged development administrator might potentially affect production resources.

Better:

```text
Development Account
        |
        X
Production Account
```

Then cross-account access can be explicitly controlled.

This reduces unintended privilege overlap.

---

# Organization Hierarchy

## 5. AWS Organization Structure

A basic AWS Organizations hierarchy looks like:

```text
Organization
    |
    v
Root
    |
    +-- Security OU
    |
    +-- Infrastructure OU
    |
    +-- Workloads OU
```

Each OU can contain:

```text
AWS Accounts

or

Nested OUs
```

---

## 6. Root

The root is the top-level container in an AWS Organization.

Conceptually:

```text
Organization
     |
     v
Root
```

All member accounts eventually belong beneath the root.

Policies attached at the root can affect accounts and OUs beneath it according to the policy type.

---

## 7. Organizational Unit

An Organizational Unit, or OU, is a logical group of AWS accounts.

Example:

```text
Security OU
│
├── Security Tooling Account
└── Log Archive Account
```

Another:

```text
Workloads OU
│
├── Production OU
└── Development OU
```

OUs make it possible to apply common governance controls to groups of accounts.

---

## 8. Nested OUs

OUs can contain other OUs.

Example:

```text
Root
 |
 +-- Workloads
       |
       +-- Production
       |     |
       |     +-- Application A
       |     +-- Application B
       |
       +-- NonProduction
             |
             +-- Development
             +-- Test
```

This allows policies to be applied at different levels.

---

## 9. OU Design Principle

A common mistake is designing OUs directly from the company organization chart.

Poor:

```text
CEO
├── Department A
├── Department B
└── Department C
```

Better:

```text
Security

Infrastructure

Production

NonProduction

Sandbox
```

OUs should generally reflect:

```text
Common Security Controls

Common Compliance Requirements

Common Operational Requirements
```

rather than temporary reporting structures.

---

# Management Account

## 10. Management Account

The AWS account used to create the organization becomes the:

```text
Management Account
```

Conceptually:

```text
Management Account
        |
        v
AWS Organization
```

The management account has special administrative capabilities.

---

## 11. Management Account Responsibilities

The management account can perform organization-level actions such as:

```text
Create Accounts

Invite Accounts

Create OUs

Move Accounts

Manage Organization Policies

Configure Organization Integrations
```

Because of its high privilege, it should be tightly protected.

---

## 12. Avoid Running Workloads in the Management Account

A strong design principle is:

```text
Management Account
→ Organization Management

NOT

Application Workloads
```

Avoid putting:

```text
Production EC2

Databases

Application Servers

Developer Workloads
```

inside the management account.

This reduces exposure of the most privileged account.

---

## 13. Management Account Security

Recommended controls include:

```text
Strong Root Protection

MFA

Minimal Human Access

No Daily Administration

Centralized Logging

Strict Monitoring

Emergency Access Procedures
```

The management account should be treated as a highly sensitive administrative environment.

---

# Member Accounts

## 14. Member Account

Any account that belongs to the organization but is not the management account is a:

```text
Member Account
```

Examples:

```text
Production

Development

Security Tooling

Log Archive

Network

Shared Services
```

---

## 15. Member Account Independence

Each member account still has its own:

```text
IAM

Resources

Service Quotas

CloudTrail Events

Security Configuration
```

But AWS Organizations can apply centralized governance controls to it.

---

# Foundational OU Structure

## 16. Recommended Conceptual Structure

A common foundational structure is:

```text
Root
│
├── Security OU
│   ├── Security Tooling
│   └── Log Archive
│
├── Infrastructure OU
│   ├── Network
│   └── Shared Services
│
└── Workloads OU
    ├── Production
    └── NonProduction
```

This separates foundational security and infrastructure services from application workloads.

---

# Security OU

## 17. Security OU

The Security OU contains accounts used for centralized security functions.

Example:

```text
Security OU
│
├── Security Tooling
└── Log Archive
```

Possible centralized services include:

```text
GuardDuty

Security Hub

Inspector

Macie

CloudTrail

AWS Config

Central Security Monitoring
```

---

## 18. Security Tooling Account

The Security Tooling account can centrally manage security services.

Conceptually:

```text
Security Tooling Account
        |
        +-- GuardDuty
        |
        +-- Inspector
        |
        +-- Macie
        |
        +-- Security Hub
```

This helps separate:

```text
Security Administration

from

Application Administration
```

---

## 19. Log Archive Account

The Log Archive account is dedicated to protected centralized log storage.

Conceptually:

```text
Production ─────┐
Development ────┤
Security ───────┼──> Log Archive
Network ────────┘
```

Typical logs include:

```text
CloudTrail

VPC Flow Logs

WAF Logs

DNS Logs

Application Logs

Security Logs
```

The account should be strongly restricted.

---

## 20. Why Separate Security Tooling and Log Archive?

A security administrator might need:

```text
Analyze Findings

Manage GuardDuty

Manage Security Hub
```

but should not automatically have permission to:

```text
Delete Historical Logs
```

Therefore:

```text
Security Tooling
→ Analyze / Operate

Log Archive
→ Preserve Evidence
```

This supports separation of duties.

---

# Infrastructure OU

## 21. Infrastructure OU

The Infrastructure OU contains centralized infrastructure accounts.

Example:

```text
Infrastructure OU
│
├── Network
└── Shared Services
```

---

## 22. Network Account

The Network account can host centralized networking components.

Examples:

```text
Transit Gateway

Network Firewall

VPN

Direct Connect Connectivity

DNS Infrastructure

Shared VPC Connectivity
```

Conceptually:

```text
Workload Accounts
      |
      v
Network Account
      |
      v
External / Shared Connectivity
```

---

## 23. Why Separate Networking?

Centralizing important network infrastructure can provide:

```text
Consistent Network Controls

Reduced Workload Privileges

Central Inspection

Separation of Duties
```

Application teams do not necessarily need permissions to modify organization-wide network infrastructure.

---

## 24. Shared Services Account

The Shared Services account hosts services consumed by multiple workloads.

Examples:

```text
Directory Services

Central CI/CD

Shared DNS

Internal Package Repositories

Common Automation Services
```

This prevents every application account from duplicating shared infrastructure.

---

# Workloads OU

## 25. Workloads OU

The Workloads OU contains application accounts.

Example:

```text
Workloads
│
├── Production
│   ├── App-A-Prod
│   └── App-B-Prod
│
└── NonProduction
    ├── App-A-Dev
    └── App-B-Dev
```

---

## 26. Production vs NonProduction

Production commonly requires stricter controls.

Example:

```text
Production
→ Strong Guardrails
→ Restricted Regions
→ Limited Administrator Access
→ Mandatory Logging
```

while:

```text
Development
→ More Flexibility
→ Still Governed
```

This is one reason separate OUs are useful.

---

## 27. Workload-Based Accounts

A good account strategy often organizes workloads by application or security boundary.

Example:

```text
Payment-App-Prod

Customer-Portal-Prod

Analytics-Dev
```

instead of:

```text
Developer-Team-A

Developer-Team-B
```

Teams change over time.

Application and security boundaries are usually more stable.

---

# Sandbox OU

## 28. Sandbox Accounts

Organizations may provide isolated sandbox accounts.

Example:

```text
Sandbox OU
│
├── Developer-A
├── Developer-B
└── Lab
```

These accounts can allow experimentation without giving access to production.

However, sandbox does not mean:

```text
No Security Controls
```

Important guardrails can still restrict:

```text
Expensive Resources

Unapproved Regions

External Sharing

Security Service Disabling
```

---

# Delegated Administration

## 29. What Is a Delegated Administrator?

Some AWS services support a:

```text
Delegated Administrator
```

This allows a member account to manage an AWS service for the organization.

Conceptually:

```text
Management Account
      |
      v
Delegates Service Administration
      |
      v
Security Tooling Account
```

---

## 30. Why Delegated Administration Matters

Without delegated administration:

```text
Management Account
→ Security Operations
```

This creates unnecessary operational use of the most privileged account.

Better:

```text
Management Account
→ Organization Governance

Security Account
→ Security Service Administration
```

---

## 31. Security Service Example

Conceptually:

```text
AWS Organizations
       |
       v
Security Tooling Account
       |
       +-- GuardDuty Administrator
       +-- Inspector Administrator
       +-- Macie Administrator
       +-- Security Hub Administration
```

The exact supported delegation mechanism depends on the AWS service.

---

# Trusted Access

## 32. What Is Trusted Access?

Trusted access allows supported AWS services to interact with AWS Organizations.

Conceptually:

```text
AWS Service
     |
     v
Trusted Access
     |
     v
AWS Organizations
```

This can allow the service to perform organization-aware operations.

---

## 33. Why Trusted Access Exists

A service may need to:

```text
Discover Organization Accounts

Configure Member Accounts

Create Service-Linked Roles

Apply Organization-Wide Features
```

Trusted access provides the integration required for those operations.

---

## 34. Trusted Access Is Service-Specific

Enabling trusted access for one AWS service does not automatically grant organization access to every service.

Conceptually:

```text
Organizations
│
├── GuardDuty Trusted Access
├── Config Trusted Access
└── Other Service Trusted Access
```

Each integration should be deliberately enabled and reviewed.

---

# Organizations Policies

## 35. Organizations Policy Types

AWS Organizations supports several policy mechanisms.

Important examples include:

```text
Service Control Policies

Resource Control Policies

Declarative Policies

Tag Policies

Backup Policies
```

Different policies solve different governance problems.

---

# Service Control Policies

## 36. SCP Overview

A Service Control Policy, or SCP, defines permission guardrails for accounts in an organization.

Conceptually:

```text
IAM Permission
      |
      v
SCP Guardrail
      |
      v
Effective Permission
```

Important:

```text
SCP
≠
Permission Grant
```

An SCP defines what permissions may be available.

IAM policies still grant the actual permissions.

---

## 37. Example SCP Concept

Suppose an IAM administrator grants:

```text
ec2:RunInstances
```

but an SCP denies EC2 usage in that account.

Result:

```text
Access Denied
```

Conceptually:

```text
IAM Allow
+
SCP Deny
=
Denied
```

SCPs will be studied in detail on Day 35.

---

# Resource Control Policies

## 38. Resource Control Policies

Resource Control Policies, or RCPs, provide centralized access guardrails for resources.

Conceptually:

```text
Resource
    |
    v
RCP
    |
    v
Maximum Allowed Resource Access
```

They complement SCPs.

A simplified distinction:

```text
SCP
→ Guardrail for principals in member accounts

RCP
→ Guardrail for organization resources
```

---

## 39. Why RCPs Matter

Suppose an S3 bucket resource policy accidentally allows overly broad external access.

An organization-level resource control policy can provide an additional guardrail.

Conceptually:

```text
Bucket Policy
     |
     v
RCP Boundary
     |
     v
Effective Resource Access
```

This adds another layer of organization-wide protection.

---

# Declarative Policies

## 40. Declarative Policies

Declarative policies allow an organization to centrally declare desired service configuration for supported AWS services.

Conceptually:

```text
Organization Policy
      |
      v
Desired Service Configuration
      |
      v
Member Accounts
```

Unlike IAM-style permissions policies, they are intended to enforce specific service configuration centrally.

---

## 41. Governance Layers

A modern Organizations governance model can include:

```text
SCP
→ What actions principals may perform

RCP
→ What access resources may allow

Declarative Policy
→ How supported services must be configured
```

These mechanisms complement each other.

---

# Tag Policies

## 42. Tag Policies

Tag policies help standardize tagging across AWS resources.

Example standard:

```text
Environment

Owner

CostCenter

Application
```

Possible expected values:

```text
Environment:
Production
Development
Test
```

Consistent tagging improves:

```text
Cost Management

Automation

Security

Inventory

Governance
```

---

# Backup Policies

## 43. Backup Policies

AWS Organizations can centrally define AWS Backup policies.

Conceptually:

```text
Organization
    |
    v
Backup Policy
    |
    +-- Production OU
    +-- Database Accounts
```

This helps establish consistent backup requirements across accounts.

---

# Consolidated Billing

## 44. Consolidated Billing

AWS Organizations can combine billing across member accounts.

Conceptually:

```text
Account A ──┐
Account B ──┼──> Organization Billing
Account C ──┘
```

Each account still maintains resource isolation.

Billing centralization does not mean:

```text
Resources Automatically Shared
```

---

# Account Creation

## 45. Account Provisioning

Organizations can create new AWS accounts centrally.

Conceptually:

```text
Organization
     |
     v
Create Account
     |
     v
New Member Account
```

The account can then be moved to the correct OU.

Example:

```text
New Payment Application
        |
        v
Payment-Prod Account
        |
        v
Production OU
```

---

# Policy Inheritance

## 46. Policy Hierarchy

Organization policies can apply through the hierarchy.

Conceptually:

```text
Root Policy
     |
     v
OU Policy
     |
     v
Nested OU Policy
     |
     v
Account
```

The effective result depends on all relevant policies of that policy type.

---

## 47. Why Hierarchy Matters

Example:

```text
Root
→ Deny Unapproved Regions

Production OU
→ Additional Production Restrictions

Account
→ Workload-Specific Guardrail
```

The production account is governed by multiple layers.

---

# Multi-Account Security Architecture

## 48. Basic Architecture

```text
                         AWS Organization
                                |
                                v
                               Root
                                |
          +---------------------+----------------------+
          |                     |                      |
          v                     v                      v
     Security OU        Infrastructure OU        Workloads OU
          |                     |                      |
     +----+----+           +----+----+           +----+----+
     |         |           |         |           |         |
     v         v           v         v           v         v
 Security   Log Archive  Network   Shared     Prod       Dev
 Tooling                          Services
```

---

## 49. Security Service Placement

Example:

```text
Security Tooling
│
├── GuardDuty Administration
├── Inspector Administration
├── Macie Administration
└── Security Hub

Log Archive
│
├── CloudTrail
├── VPC Flow Logs
├── WAF Logs
└── Other Security Logs

Network
│
├── Transit Gateway
├── Network Firewall
└── Central Connectivity

Workload Accounts
│
├── Applications
├── Databases
└── Application Data
```

---

# Separation of Duties

## 50. Security Team

Security team permissions might include:

```text
Review GuardDuty

Review Inspector

Review Security Hub

Investigate Logs
```

but not:

```text
Modify Production Application Code
```

---

## 51. Application Team

Application teams might manage:

```text
EC2

Lambda

ECS

Application Databases
```

within their account.

They should not automatically have permission to:

```text
Disable Organization Logging

Modify Organization Policies

Delete Central Logs
```

---

## 52. Network Team

Network administrators may manage:

```text
Transit Gateway

Firewall

Routing

Connectivity
```

without receiving:

```text
Application Database Credentials
```

This is separation of duties implemented through account architecture.

---

# Blast Radius

## 53. What Is Blast Radius?

Blast radius describes how much of an environment can be affected when something goes wrong.

Example:

```text
Compromised Administrator
        |
        v
Single Huge AWS Account
        |
        v
Many Resources Exposed
```

Multi-account separation can reduce this.

```text
Compromised Dev Account
        |
        X
Production Account
```

assuming cross-account permissions and organization controls are properly designed.

---

## 54. Account Isolation Is Not Automatic Security

Multiple accounts alone are not enough.

Poor configuration:

```text
Development Admin
      |
      v
Production AssumeRole
      |
      v
AdministratorAccess
```

can remove much of the isolation benefit.

Multi-account architecture still requires:

```text
Least Privilege

SCPs

Strong IAM

Logging

Monitoring

Controlled Cross-Account Roles
```

---

# AWS Control Tower

## 55. What Is AWS Control Tower?

AWS Control Tower helps create and govern a multi-account AWS environment using AWS Organizations and other AWS services.

Conceptually:

```text
AWS Control Tower
       |
       +-- AWS Organizations
       |
       +-- AWS Config
       |
       +-- CloudTrail
       |
       +-- Governance Controls
```

It provides a managed landing zone experience.

---

## 56. Landing Zone

A landing zone is a preconfigured multi-account environment.

Conceptually:

```text
AWS Organization
      |
      +-- Security Accounts
      |
      +-- Logging
      |
      +-- Governance
      |
      +-- Account Provisioning
```

This gives organizations a standardized starting point.

---

## 57. Control Tower Accounts

A typical Control Tower landing zone includes accounts for:

```text
Log Archive

Audit / Security
```

inside a Security OU.

Additional workload and infrastructure OUs can then be created.

---

## 58. Organizations vs Control Tower

A useful distinction:

```text
AWS Organizations
→ Core multi-account governance service

AWS Control Tower
→ Managed landing-zone and governance experience
   built using Organizations and other AWS services
```

Organizations can be used without Control Tower.

Control Tower uses Organizations as part of its foundation.

---

# Common Misconfigurations

## 59. Everything in One Account

Poor:

```text
Production
Development
Security
Networking
Logging
```

all in one account.

Risks:

```text
Large Blast Radius

Privilege Overlap

Weak Separation of Duties

Complex IAM
```

---

## 60. Workloads in Management Account

Poor:

```text
Management Account
      |
      +-- Production Database
      +-- Developers
      +-- Application EC2
```

This unnecessarily exposes a highly privileged account.

---

## 61. OU Based Only on Teams

Poor:

```text
Team A OU

Team B OU

Team C OU
```

When the organization changes:

```text
OU Structure
→ Constantly Changes
```

Better:

```text
Security Requirements

Environment

Workload Function
```

as stable design criteria.

---

## 62. Too Many OUs

Overengineering:

```text
Root
 ↓
OU
 ↓
OU
 ↓
OU
 ↓
OU
 ↓
Account
```

can make governance difficult.

Create OUs only when they represent meaningful:

```text
Policy

Security

Compliance

Operational
```

boundaries.

---

## 63. No Central Security Account

Poor:

```text
Each Workload Account
→ Own Security Tools
```

with no central view.

This can cause:

```text
Inconsistent Configuration

Visibility Gaps

Slow Investigation
```

Central security administration improves consistency.

---

## 64. Logs Stored in Workload Account Only

Scenario:

```text
Compromised Production Account
      |
      v
Attacker Has Admin Access
      |
      v
Deletes Local Logs
```

Better:

```text
Production
      |
      v
Central Log Archive
```

This makes evidence harder for a workload administrator or attacker to destroy.

---

## 65. Delegation Not Used

Poor:

```text
Management Account
→ Used Daily by Security Team
```

Better:

```text
Management Account
→ Organization Governance

Security Account
→ Delegated Administration
```

where supported.

---

# Hands-on Practice

## 66. Practice — Review Organizations

If you have access to an AWS Organization:

```text
AWS Console
   |
   v
AWS Organizations
```

Review:

```text
Management Account

Member Accounts

Root

Organizational Units
```

Do not modify an organization solely for practice.

---

## 67. Practice — Draw an OU Tree

Create a conceptual design:

```text
Root
│
├── Security
│   ├── Security Tooling
│   └── Log Archive
│
├── Infrastructure
│   ├── Network
│   └── Shared Services
│
└── Workloads
    ├── Production
    └── NonProduction
```

Then answer:

```text
Why does each OU exist?

What common policies should apply?

Who administers each account?
```

---

## 68. Practice — Account Classification

Classify these accounts:

```text
Central GuardDuty Administration
→ Security Tooling

Organization CloudTrail Storage
→ Log Archive

Transit Gateway
→ Network

Production Web Application
→ Workloads / Production

Developer Test Environment
→ Workloads / NonProduction
```

---

## 69. Practice — Separation of Duties

For each role, determine which account it should primarily access.

### Security Analyst

```text
Security Tooling
Log Archive Read Access
```

### Application Developer

```text
Development Workload
```

### Network Engineer

```text
Network Account
```

### Organization Administrator

```text
Management Account
```

Apply least privilege.

---

## 70. Practice — Governance Design

Scenario:

```text
Company has:

10 Production Accounts

8 Development Accounts

1 Security Team

1 Network Team
```

Create an OU design.

Possible structure:

```text
Root
│
├── Security
│   ├── Security Tooling
│   └── Log Archive
│
├── Infrastructure
│   └── Network
│
└── Workloads
    ├── Production
    │   ├── Prod-01
    │   ├── Prod-02
    │   └── ...
    │
    └── Development
        ├── Dev-01
        ├── Dev-02
        └── ...
```

---

## 71. Optional CLI Practice

Describe the organization:

```bash
aws organizations describe-organization
```

List roots:

```bash
aws organizations list-roots
```

List OUs under a parent:

```bash
aws organizations list-organizational-units-for-parent \
  --parent-id <root-or-ou-id>
```

List accounts:

```bash
aws organizations list-accounts
```

List accounts in an OU:

```bash
aws organizations list-accounts-for-parent \
  --parent-id <ou-id>
```

Do not publish:

```text
Real AWS Account IDs

Organization IDs

OU IDs

Email Addresses

Production Account Names
```

to a public GitHub repository.

---

# Architecture Exercise

## 72. Design a Secure AWS Organization

Requirements:

```text
Production Workloads

Development Workloads

Central Security Monitoring

Immutable Log Archive

Central Networking

Shared Services

Strong Production Controls
```

Architecture:

```text
AWS Organization
       |
       v
      Root
       |
       +-------------------+
       |                   |
       v                   v
 Security OU        Infrastructure OU
       |                   |
   +---+---+           +---+---+
   |       |           |       |
   v       v           v       v
Security  Log       Network   Shared
Tooling   Archive             Services

       |
       v
 Workloads OU
       |
   +---+---+
   |       |
   v       v
 Prod     NonProd
```

---

## 73. Security Questions

For every OU or account, ask:

```text
What is its purpose?

What resources belong here?

Who administers it?

What must users be prevented from doing?

What logs must be centralized?

Which security services should be delegated?

Which policies apply?
```

---

# Security Checklist

```text
[ ] AWS Organizations is used for multi-account governance where appropriate

[ ] Organization uses all required features

[ ] Management account is tightly protected

[ ] Application workloads are not placed in the management account

[ ] Root user access is strongly protected

[ ] Accounts are separated by meaningful security or operational boundaries

[ ] OUs are based on common controls rather than organizational reporting structure

[ ] Security OU exists where appropriate

[ ] Security Tooling account exists where appropriate

[ ] Log Archive account is separated from workloads

[ ] Infrastructure services are separated where appropriate

[ ] Production and non-production workloads are separated

[ ] Cross-account access follows least privilege

[ ] Delegated administration is used where appropriate

[ ] Trusted access integrations are reviewed

[ ] Organization policies are documented

[ ] SCP strategy is defined

[ ] RCPs are considered where appropriate

[ ] Declarative policies are considered for supported services

[ ] Central security service coverage is reviewed

[ ] Centralized logs are protected from workload administrators
```

---

## Key Takeaways

- AWS Organizations provides centralized governance for multiple AWS accounts.
- AWS accounts are important security, resource, and billing boundaries.
- Multi-account architectures reduce blast radius and improve separation of duties.
- The management account should primarily be used for organization administration.
- Member accounts host security, infrastructure, and workload functions.
- Organizational Units group accounts that require common controls.
- OUs should be designed around functions and security requirements rather than temporary reporting structures.
- Security Tooling and Log Archive should typically be separated.
- Infrastructure services such as networking can be separated from application workloads.
- Delegated administration reduces operational dependency on the management account.
- Trusted access allows supported AWS services to integrate with AWS Organizations.
- SCPs define organization-level permission guardrails but do not directly grant permissions.
- RCPs provide centralized resource access guardrails.
- Declarative policies can enforce supported AWS service configurations centrally.
- AWS Control Tower provides a managed landing-zone experience built on AWS Organizations and other AWS services.
- Multi-account design is a fundamental part of AWS security architecture.

---

## Reflection

Today I learned that AWS Organizations is the foundation for managing security at scale across multiple AWS accounts.

The most important lesson is that an AWS account itself is a strong security boundary. Instead of placing production, development, security tooling, networking, and logging in one large account, these responsibilities can be separated into dedicated accounts and organizational units.

I also learned that the management account should be protected and used primarily for organization governance, while operational responsibilities such as security service administration should be delegated to dedicated accounts where possible.

From a cloud security perspective, a good AWS Organization structure reduces blast radius, improves separation of duties, simplifies centralized governance, and provides the foundation for applying security guardrails consistently across all workloads.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AWS Organizations | AWS service for centrally governing multiple AWS accounts |
| Delegated Administrator | Member account authorized to administer a supported AWS service for the organization |
| Landing Zone | Standardized multi-account AWS environment with centralized governance |
| Management Account | Account with primary administrative authority over an AWS Organization |
| Member Account | AWS account belonging to an organization other than the management account |
| Organizational Unit | Logical container used to group AWS accounts with common controls |
| RCP | Organization-level policy that defines resource access guardrails |
| Root | Top-level container of an AWS Organization |
| SCP | Organization-level policy that defines permission guardrails |
| Trusted Access | Integration that allows supported AWS services to work with AWS Organizations |
