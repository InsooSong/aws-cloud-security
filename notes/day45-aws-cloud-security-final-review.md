# Day 45 — AWS Cloud Security Final Review

## Topic

AWS Cloud Security Final Review — Identity, Network, Data Protection, Detection, Governance, Automation, and Infrastructure as Code

---

## Objectives

- Review the complete AWS cloud security learning path
- Connect individual AWS security services into one architecture
- Understand preventive, detective, and responsive controls
- Review identity and access management
- Review network and infrastructure protection
- Review data protection and encryption
- Review logging, monitoring, and threat detection
- Review multi-account security architecture
- Review centralized security operations
- Review AWS CLI and boto3 security automation
- Review Terraform-based preventive controls
- Practice security investigation scenarios
- Practice cloud security architecture interview questions
- Identify areas for future study

---

# AWS Cloud Security Mental Model

## 1. Security Is a System

Cloud security is not:

```text
IAM
+
Security Groups
+
Encryption
```

as independent features.

A secure architecture connects:

```text
Identity
     ↓
Permissions
     ↓
Network
     ↓
Resources
     ↓
Data
     ↓
Logging
     ↓
Detection
     ↓
Investigation
     ↓
Response
```

A failure in one layer should not automatically compromise the entire environment.

This is:

```text
Defense in Depth
```

---

# Shared Responsibility

## 2. AWS Shared Responsibility Model

Remember:

```text
Security OF the Cloud
→ AWS

Security IN the Cloud
→ Customer
```

AWS protects the underlying cloud infrastructure.

Customers remain responsible for security controls such as:

```text
IAM

Data

Operating Systems

Applications

Network Configuration

Encryption Configuration

Logging Configuration
```

depending on the AWS service being used.

---

# Identity Security

## 3. Identity Is the First Security Boundary

Strong cloud security starts with identity.

Important controls:

```text
IAM Identity Center

IAM Roles

Temporary Credentials

MFA

Least Privilege

Separation of Duties

Access Analyzer
```

Prefer:

```text
Temporary Credentials
```

over:

```text
Long-Term Access Keys
```

whenever possible.

---

## 4. IAM Mental Model

```text
Principal
    ↓
Authentication
    ↓
Policies
    ↓
Authorization
    ↓
AWS Resource
```

---

## 5. IAM Permission Evaluation

Simplified model:

```text
Implicit Deny
      ↓
Explicit Allow
      ↓
Explicit Deny
      ↓
DENY
```

Important rule:

```text
Explicit Deny
>
Allow
```

---

## 6. Effective Permissions

Permissions may be influenced by:

```text
Identity Policy

Resource Policy

Permissions Boundary

SCP

RCP

Session Policy

KMS Key Policy
```

Therefore:

```text
IAM Policy Allows
```

does not always mean:

```text
Request Is Allowed
```

---

# Temporary Credentials

## 7. STS and IAM Roles

Preferred model:

```text
Identity
   ↓
AssumeRole
   ↓
STS
   ↓
Temporary Credentials
   ↓
AWS Resource
```

Benefits include:

```text
Short Lifetime

No Permanent Secret

Better Cross-Account Access

Reduced Credential Exposure
```

---

# Network Security

## 8. VPC Security Layers

```text
VPC
 |
 +-- Subnet
 |
 +-- Route Table
 |
 +-- Internet Gateway
 |
 +-- NAT Gateway
 |
 +-- Security Group
 |
 +-- Network ACL
```

Security requires understanding how these controls interact.

---

## 9. Public vs Private

Public subnet:

```text
Route
→ Internet Gateway
```

Private subnet:

```text
No direct route
→ Internet Gateway
```

A public IP alone does not fully determine reachability.

Actual exposure depends on:

```text
Public IP

Route Table

Internet Gateway

Security Group

NACL

Host Firewall

Application
```

---

# Security Groups

## 10. Security Group

Security Groups are:

```text
Stateful

Allow Only

Resource / ENI Level
```

Security Group design should follow:

```text
Least Privilege
```

Example:

```text
ALB-SG
   ↓
APP-SG
   ↓
DB-SG
```

is generally better than:

```text
Internet
   ↓
Database
```

---

# Network ACLs

## 11. Network ACL

NACLs are:

```text
Subnet Level

Stateless

Allow + Deny

Numbered Rule Evaluation
```

Remember:

```text
Security Group
→ Primary workload access control

NACL
→ Additional subnet-level guardrail
```

---

# Compute Security

## 12. EC2 Security

Important controls:

```text
IAM Role

Security Group

EBS Encryption

IMDSv2

Patch Management

Amazon Inspector

Systems Manager

CloudWatch

Host Firewall
```

Avoid long-lived AWS credentials stored on EC2.

Use:

```text
IAM Role
```

instead.

---

# Metadata Security

## 13. IMDSv2

Instance Metadata Service can provide:

```text
Temporary Role Credentials
```

to EC2 workloads.

IMDSv2 provides protections against certain metadata access and SSRF-related attack scenarios.

Security pattern:

```text
Application
    ↓
IMDSv2
    ↓
Temporary Role Credentials
```

---

# S3 Security

## 14. S3 Security Model

Important controls:

```text
IAM

Bucket Policy

Block Public Access

Encryption

Versioning

Logging

Access Analyzer
```

---

## 15. S3 Public Access

Use:

```text
Block Public Access
```

as an explicit guardrail.

Review:

```text
BlockPublicAcls

IgnorePublicAcls

BlockPublicPolicy

RestrictPublicBuckets
```

A missing bucket-level setting alone does not necessarily prove that a bucket is public.

Effective access can also depend on:

```text
Account Controls

Organization Controls

Bucket Policy

ACL

Access Point
```

---

# Encryption

## 16. Encryption at Rest

Common AWS encryption controls:

```text
S3
→ SSE-S3 / SSE-KMS

EBS
→ KMS

RDS
→ KMS

Secrets Manager
→ KMS
```

Encryption should be combined with:

```text
Access Control

Key Management

Logging

Rotation
```

---

# AWS KMS

## 17. KMS Mental Model

```text
Application
    ↓
KMS Data Key
    ↓
Encrypt Data
    ↓
Encrypted Data Key
+
Encrypted Data
```

This is:

```text
Envelope Encryption
```

---

## 18. KMS Permission Model

KMS access may require:

```text
IAM Permission
+
KMS Key Policy
```

depending on the architecture.

Cross-account access requires careful configuration of both sides.

---

# Secrets

## 19. Secrets Manager

Use Secrets Manager for values such as:

```text
Database Passwords

API Credentials

Application Secrets
```

instead of:

```text
Source Code

GitHub

Container Images

Plaintext Configuration
```

Security model:

```text
Application Role
      ↓
Secrets Manager
      ↓
KMS
```

---

# Logging

## 20. CloudTrail

CloudTrail answers:

```text
Who did what?
```

Useful information:

```text
Principal

API

Resource

Time

Region

Source IP
```

CloudTrail is fundamental for:

```text
Audit

Investigation

Incident Response
```

---

# CloudWatch

## 21. CloudWatch

CloudWatch provides:

```text
Metrics

Logs

Alarms

Logs Insights
```

Think:

```text
CloudTrail
→ API activity

CloudWatch
→ Operational telemetry
```

---

# AWS Config

## 22. AWS Config

AWS Config answers:

```text
What changed?
```

It provides:

```text
Configuration History

Compliance Evaluation

Managed Rules

Custom Rules

Remediation Integration
```

---

## 23. CloudTrail + Config

Useful investigation combination:

```text
AWS Config
→ What changed?

CloudTrail
→ Who changed it?
```

---

# Centralized Logging

## 24. Log Architecture

Recommended multi-account model:

```text
Workload Accounts
      |
      v
Central Logging
      |
      v
Log Archive Account
```

Security logs should be protected from workload compromise.

---

## 25. Important Log Sources

Examples:

```text
CloudTrail

AWS Config

VPC Flow Logs

WAF

Route 53

CloudFront

ALB

Network Firewall

Application Logs

Operating System Logs
```

---

# Threat Detection

## 26. GuardDuty

GuardDuty focuses on:

```text
Threat Detection
```

It analyzes AWS telemetry to identify suspicious activity.

Think:

```text
Activity
→ GuardDuty
→ Threat Finding
```

---

# Vulnerability Management

## 27. Amazon Inspector

Inspector focuses on:

```text
Vulnerability Management
```

Examples:

```text
EC2 Vulnerabilities

ECR Container Vulnerabilities

Lambda Vulnerabilities
```

Think:

```text
Resource
→ Vulnerability
→ Inspector Finding
```

---

# Sensitive Data

## 28. Amazon Macie

Macie focuses primarily on:

```text
Sensitive Data Discovery
```

for Amazon S3.

Think:

```text
S3 Data
→ Sensitive Information
→ Macie
```

---

# Security Hub

## 29. Security Hub

Security Hub provides centralized security findings and security posture capabilities.

Think:

```text
GuardDuty
Inspector
Macie
Other Security Signals
        ↓
Security Hub
        ↓
Central Security View
```

Security Hub should be understood as part of a broader centralized security operations architecture rather than as a replacement for the individual security services.

---

# WAF and DDoS Protection

## 30. AWS WAF

AWS WAF operates primarily at:

```text
Layer 7
```

Use cases include:

```text
SQL Injection

XSS

IP Rules

Geo Rules

Rate-Based Rules

Bot Management
```

---

## 31. AWS Shield

Shield focuses on:

```text
DDoS Protection
```

Conceptually:

```text
Shield
→ DDoS

WAF
→ HTTP Request Filtering
```

---

# Multi-Account Security

## 32. Why Multiple Accounts?

AWS accounts provide strong boundaries for:

```text
Resources

Permissions

Billing

Blast Radius
```

Separate accounts can reduce the impact of a compromise.

---

# AWS Organizations

## 33. Recommended Concept

```text
Organization
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

---

## 34. Management Account

The management account should be:

```text
Highly Protected

Minimally Used

Free of Normal Workloads
```

Remember:

```text
SCPs do not restrict
the management account.
```

---

# Service Control Policies

## 35. SCP

SCPs define:

```text
Maximum Available Permissions
```

They do NOT grant permissions.

Simplified:

```text
IAM Permission
∩
SCP Permission
=
Effective Permission
```

---

## 36. Typical Guardrails

Examples:

```text
Protect CloudTrail

Prevent Leaving Organization

Restrict Regions

Protect Security Services

Prevent Dangerous Operations
```

---

# Security Tooling Account

## 37. Centralized Security Operations

Security Tooling account can centralize services such as:

```text
GuardDuty

Inspector

Macie

Security Hub
```

using delegated administration.

AWS Security Reference Architecture recommends a multi-account model with dedicated Security Tooling and Log Archive accounts within a Security OU.

---

# Log Archive Account

## 38. Purpose

Log Archive should prioritize:

```text
Integrity

Retention

Limited Write Access

Limited Delete Access

Controlled Read Access
```

Possible controls:

```text
S3 Block Public Access

KMS

Versioning

Object Lock

Lifecycle

SCP
```

---

# Cross-Account Access

## 39. AssumeRole

Typical security operations:

```text
Security Tooling Account
        ↓
STS AssumeRole
        ↓
Production Account
        ↓
Read-Only Security Role
```

Use temporary credentials and least privilege.

---

# AWS CLI Security Operations

## 40. CLI Investigation

Useful investigation flow:

```text
STS
 ↓
IAM
 ↓
CloudTrail
 ↓
EC2 / Security Groups
 ↓
S3
 ↓
KMS
 ↓
GuardDuty
 ↓
Inspector
 ↓
Security Hub
```

Always start with:

```bash
aws sts get-caller-identity
```

Verify:

```text
Account

Principal

Region
```

before investigation or changes.

---

# boto3 Security Automation

## 41. Security Automation Flow

```text
boto3 Session
      ↓
AWS Client
      ↓
Enumerate Resources
      ↓
Evaluate Security Rule
      ↓
Finding
```

Example:

```text
Security Group
      ↓
0.0.0.0/0?
      ↓
Sensitive Port?
      ↓
Finding
```

---

## 42. Pagination

Always consider:

```text
Pagination
```

during security enumeration.

Otherwise:

```text
Script Completed
≠
All Resources Checked
```

---

# Security Scanner

## 43. Day 42 Scanner

Security checks included:

```text
EC2 Public IP

Security Group Exposure

S3 Public Access Block

S3 Encryption

GuardDuty

Inspector
```

Important principle:

```text
Configuration Observation
≠
Confirmed Vulnerability
```

Context matters.

---

# Terraform

## 44. Infrastructure as Code

Terraform allows:

```text
Desired Infrastructure
        ↓
Code
        ↓
Plan
        ↓
Review
        ↓
Apply
```

This helps shift security earlier in the deployment process.

---

# Secure Terraform

## 45. Preventive Controls

Day 44 examples included:

```text
Private Subnet

No Automatic Public IP

Restricted Security Group

S3 Block Public Access

SSE-KMS

KMS Rotation

IAM Least Privilege

Variable Validation
```

---

# Terraform State

## 46. State Security

Terraform state can contain:

```text
Resource IDs

ARNs

Infrastructure Details

Sensitive Values
```

Therefore:

```text
terraform.tfstate
→ Never publish
```

For collaborative environments consider:

```text
Remote State

Encryption

Access Control

State Locking

Audit Logging
```

---

# Terraform + boto3

## 47. Prevent and Detect

Terraform:

```text
Preventive Control
```

boto3:

```text
Detective Control
```

Together:

```text
Terraform
    ↓
Secure AWS Infrastructure
    ↓
boto3 Security Scanner
    ↓
Verification
```

---

# Complete Security Architecture

## 48. High-Level Architecture

```text
Internet
   |
   v
Route 53
   |
   v
CloudFront
   |
   +-- Shield
   |
   +-- AWS WAF
   |
   v
Application Load Balancer
   |
   v
Application Tier
   |
   v
Database Tier
```

Around the workload:

```text
IAM
Organizations
SCP
KMS
CloudTrail
Config
GuardDuty
Inspector
Security Hub
Central Logging
```

---

# Control Categories

## 49. Preventive Controls

Examples:

```text
IAM

SCP

Security Groups

NACL

S3 Block Public Access

KMS

Terraform Secure Defaults
```

---

## 50. Detective Controls

Examples:

```text
CloudTrail

AWS Config

GuardDuty

Inspector

Macie

Security Hub

CloudWatch
```

---

## 51. Responsive Controls

Examples:

```text
EventBridge

Lambda

Systems Manager

Step Functions

Incident Response Procedures
```

---

# Incident Scenario 1

## 52. Suspicious EC2 Activity

Scenario:

```text
GuardDuty reports suspicious
activity from an EC2 instance.
```

Investigation:

```text
1. Identify Account / Region

2. Review GuardDuty Finding

3. Identify EC2 Instance

4. Check Public Exposure

5. Review Security Groups

6. Review Inspector Findings

7. Review CloudTrail

8. Review IAM Role

9. Review Network Activity

10. Determine Containment Action
```

Do not immediately terminate the instance without considering:

```text
Evidence Preservation

Business Impact

Incident Response Procedure
```

---

# Incident Scenario 2

## 53. S3 Data Exposure

Scenario:

```text
Sensitive S3 bucket
may be publicly accessible.
```

Investigate:

```text
Block Public Access

Bucket Policy

ACL

Access Point

IAM

CloudTrail Data Events

Macie

KMS

Object Access
```

---

# Incident Scenario 3

## 54. Credential Compromise

Scenario:

```text
Suspicious IAM credential activity.
```

Investigate:

```text
CloudTrail

Principal ARN

Source IP

API History

AssumeRole Events

Access Key Age

Role Session

Resource Access

Cross-Account Activity
```

Possible response:

```text
Revoke / Disable Credentials

Restrict Sessions

Contain Permissions

Preserve Evidence

Investigate Impact
```

---

# Incident Scenario 4

## 55. Logging Disabled

Scenario:

```text
CloudTrail logging was stopped.
```

Investigate:

```text
CloudTrail Event

Principal

Account

Region

SCP

IAM Permission

Related API Activity
```

A logging failure or unauthorized logging modification should be treated as a security event.

---

# Incident Scenario 5

## 56. Unapproved Region

Scenario:

```text
Resources appear in an
unapproved AWS Region.
```

Review:

```text
Organizations SCP

CloudTrail

IAM Principal

Resource Type

Security Service Coverage
```

Remember:

```text
No GuardDuty Finding
```

may simply mean:

```text
GuardDuty is not enabled
in that Region.
```

---

# Architecture Review Questions

## 57. Identity

Ask:

```text
Who can access the account?

Are temporary credentials used?

Is MFA enforced?

Are permissions least privilege?

Is cross-account access controlled?
```

---

## 58. Network

Ask:

```text
Which resources are internet reachable?

Are administrative ports public?

Are databases private?

Are security groups least privilege?

Is network segmentation appropriate?
```

---

## 59. Data

Ask:

```text
What sensitive data exists?

Is it encrypted?

Who can decrypt it?

How are secrets stored?

Is public access prevented?
```

---

## 60. Logging

Ask:

```text
Is CloudTrail enabled?

Are logs centralized?

Can workload administrators delete logs?

Are logs protected and retained?
```

---

## 61. Detection

Ask:

```text
Is GuardDuty enabled?

Is Inspector coverage complete?

Is sensitive S3 data monitored?

Are findings centralized?

Are alerts actionable?
```

---

## 62. Governance

Ask:

```text
Are accounts separated?

Are OUs designed around controls?

Are SCPs applied?

Are security services centrally managed?

Are approved Regions defined?
```

---

## 63. Automation

Ask:

```text
Can security checks be automated?

Are APIs paginated correctly?

Are automation credentials temporary?

Are remediation actions safe?
```

---

## 64. Infrastructure as Code

Ask:

```text
Are secure defaults defined?

Are Terraform plans reviewed?

Is Terraform state protected?

Are secrets excluded from code?

Can security configuration drift be detected?
```

---

# Interview Questions

## 65. IAM

### Question

What is the difference between an IAM role trust policy and a permission policy?

### Answer

```text
Trust Policy
→ Defines who can assume the role.

Permission Policy
→ Defines what the role can do
after it is assumed.
```

---

## 66. SCP

### Question

Does an SCP grant AWS permissions?

### Answer

```text
No.

An SCP defines the maximum
permissions available to principals
in member accounts.

IAM permissions are still required.
```

---

## 67. Security Group vs NACL

### Question

What is the difference?

### Answer

```text
Security Group
→ Stateful
→ Resource / ENI
→ Allow Rules

NACL
→ Stateless
→ Subnet
→ Allow + Deny Rules
```

---

## 68. CloudTrail vs Config

### Question

What is the difference?

### Answer

```text
CloudTrail
→ Who performed an API action?

AWS Config
→ What configuration changed?
```

---

## 69. GuardDuty vs Inspector

### Question

What is the difference?

### Answer

```text
GuardDuty
→ Threat Detection

Inspector
→ Vulnerability Management
```

---

## 70. KMS

### Question

Why does an application sometimes need both S3 and KMS permissions?

### Answer

For SSE-KMS protected objects:

```text
S3 Permission
→ Access Object

KMS Permission
→ Decrypt Data Key / Object
```

Both access layers may be required.

---

## 71. Terraform

### Question

Why should Terraform state not be committed to Git?

### Answer

State can contain:

```text
Resource IDs

Infrastructure Information

Sensitive Values

Secrets
```

Therefore state should be protected and stored securely.

---

## 72. Public IP

### Question

Does a public IP automatically mean an EC2 instance is vulnerable?

### Answer

No.

Actual exposure depends on:

```text
Route

Internet Gateway

Security Group

NACL

Host Firewall

Application
```

A public IP is a security review signal, not proof of vulnerability.

---

# Security Investigation Workflow

## 73. Investigation Mental Model

Use:

```text
Identity
   ↓
Permission
   ↓
Network
   ↓
Resource
   ↓
Data
   ↓
Activity
   ↓
Impact
```

Questions:

```text
Who?

What permission?

What resource?

From where?

What changed?

What data?

What impact?
```

---

# AWS Security Service Decision Matrix

## 74. Which Service?

| Question | Primary Service |
|---|---|
| Who called this API? | CloudTrail |
| What configuration changed? | AWS Config |
| Is malicious activity occurring? | GuardDuty |
| Does the workload have known vulnerabilities? | Inspector |
| Does S3 contain sensitive data? | Macie |
| Can I centrally view security findings? | Security Hub |
| How do I protect HTTP requests? | AWS WAF |
| How do I protect against DDoS? | AWS Shield |
| How do I manage encryption keys? | AWS KMS |
| How do I store application secrets? | Secrets Manager |
| How do I control organization-wide permission boundaries? | SCP |
| How do I automate AWS APIs? | boto3 / AWS CLI |
| How do I define infrastructure as code? | Terraform |

---

# AWS Security Architecture Review

## 75. Final Architecture

```text
AWS Organizations
       |
       +-- Management Account
       |
       +-- Security OU
       |     |
       |     +-- Security Tooling
       |     |
       |     +-- Log Archive
       |
       +-- Infrastructure OU
       |     |
       |     +-- Network
       |     |
       |     +-- Shared Services
       |
       +-- Workloads OU
             |
             +-- Production
             |
             +-- NonProduction
```

Security services:

```text
Identity
→ IAM Identity Center / IAM / STS

Governance
→ Organizations / SCP

Network
→ VPC / SG / NACL / WAF / Shield

Data
→ KMS / Secrets Manager / S3 Controls

Audit
→ CloudTrail / Config / CloudWatch

Detection
→ GuardDuty / Inspector / Macie

Aggregation
→ Security Hub

Automation
→ AWS CLI / boto3

Infrastructure
→ Terraform
```

---

# Prevent, Detect, Respond

## 76. Final Security Model

```text
Prevent
│
├── IAM
├── SCP
├── Security Groups
├── S3 BPA
├── KMS
└── Terraform

        ↓

Detect
│
├── CloudTrail
├── Config
├── GuardDuty
├── Inspector
├── Macie
└── Security Hub

        ↓

Respond
│
├── Investigation
├── EventBridge
├── Lambda
├── Systems Manager
└── Incident Response Process
```

---

# Repository Review

## 77. What This Repository Demonstrates

The repository now demonstrates:

```text
AWS Fundamentals

Identity Security

Network Security

Compute Security

Storage Security

Encryption

Logging

Threat Detection

Multi-Account Governance

Security Architecture

Security Investigation

Python Automation

Security Scanning

Infrastructure as Code

Secure Terraform Configuration
```

---

# What I Should Be Able to Explain

## 78. Interview Readiness

After completing this repository, I should be able to explain:

```text
Why multi-account architecture is used

How SCP differs from IAM

How cross-account AssumeRole works

How AWS network exposure is evaluated

How S3 public access works

How KMS permissions work

How logs should be centralized

How GuardDuty, Inspector, Macie,
and Security Hub differ

How to investigate AWS security events

How boto3 can automate security checks

How Terraform can enforce secure defaults

How preventive and detective controls
work together
```

---

# Future Study

## 79. Next Areas

Possible next topics:

```text
AWS Security Specialty

Cloud Security Detection Engineering

SIEM

Amazon Security Lake

Incident Response

Container Security

EKS Security

CI/CD Security

DevSecOps

Policy as Code

Advanced Terraform

AWS Control Tower

Cloud Security Posture Management

Threat Modeling
```

---

# Security Checklist

```text
[ ] Strong identity foundation is implemented

[ ] Temporary credentials are preferred

[ ] MFA is enforced where appropriate

[ ] Least privilege is applied

[ ] Cross-account access is controlled

[ ] Network exposure is understood

[ ] Sensitive administrative ports are restricted

[ ] Data is encrypted appropriately

[ ] KMS permissions are reviewed

[ ] Secrets are not stored in source code

[ ] CloudTrail is available for investigations

[ ] Configuration changes can be tracked

[ ] Logs are centralized and protected

[ ] GuardDuty coverage is verified

[ ] Inspector coverage is verified

[ ] Sensitive data monitoring is considered

[ ] Security findings are centralized

[ ] Multi-account boundaries are used appropriately

[ ] SCP guardrails are applied carefully

[ ] Security services use delegated administration where appropriate

[ ] Automation uses read-only operations first

[ ] Pagination is considered in security automation

[ ] Terraform credentials are not hard-coded

[ ] Terraform state is protected

[ ] Terraform plans are reviewed

[ ] Secure infrastructure defaults are defined

[ ] Runtime configuration is verified after deployment

[ ] Incident response procedures are prepared
```

---

## Key Takeaways

- AWS cloud security requires multiple security layers working together.
- Identity is the foundation of AWS security.
- Temporary credentials and least privilege reduce credential risk.
- Network exposure requires evaluating routes, public addresses, Security Groups, NACLs, and workloads together.
- Encryption requires both data encryption and secure key management.
- CloudTrail, AWS Config, and CloudWatch provide complementary visibility.
- GuardDuty, Inspector, Macie, and Security Hub solve different security problems.
- Multi-account architecture reduces blast radius and improves separation of duties.
- SCPs provide organization-level permission guardrails but do not grant permissions.
- Security logs should be centralized and protected from workload compromise.
- AWS CLI and boto3 enable repeatable security investigations and automation.
- Terraform shifts security controls earlier by defining secure infrastructure as code.
- Terraform state must be treated as sensitive information.
- Preventive, detective, and responsive controls should work together.
- A security finding must always be interpreted in business and technical context.
- Cloud security is a continuous process of prevention, visibility, detection, investigation, and improvement.

---

## Reflection

Over the past 45 days, I studied AWS cloud security from fundamental architecture through security automation and Infrastructure as Code.

I started with AWS accounts, IAM, VPC networking, EC2, S3, EBS, and RDS security. I then studied logging and monitoring with CloudTrail, CloudWatch, and AWS Config, followed by encryption, secrets management, and threat detection services such as GuardDuty, Inspector, Macie, Security Hub, AWS WAF, and Shield.

I also learned how multi-account architecture, AWS Organizations, SCPs, centralized security services, and centralized logging can reduce blast radius and improve governance.

In the final phase, I moved from individual AWS console concepts to security operations and automation. I practiced AWS CLI investigation workflows, used Python and boto3 to build security checks, and used Terraform to define secure AWS infrastructure as code.

The most important lesson is that cloud security is not based on a single service. Strong security requires identity, network, data protection, logging, detection, governance, automation, and incident response to work together as one architecture.

My next goal is to continue converting this knowledge into hands-on security projects and use the repository as a foundation for Cloud Security Engineer roles.
