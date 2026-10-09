# Day 37 — Centralized Security & Logging

## Topic

Centralized Logging, Security Monitoring, Log Archive Architecture, Organization Trails, AWS Config Aggregation, and Security Operations

---

## Objectives

- Understand why centralized logging is important
- Understand the roles of Security Tooling and Log Archive accounts
- Learn how organization-wide CloudTrail logging works
- Understand organization trails
- Understand AWS Config aggregation
- Learn how security services use delegated administration
- Understand centralized GuardDuty administration
- Understand centralized Inspector administration
- Understand centralized Macie administration
- Understand Security Hub centralization
- Learn how EventBridge supports security automation
- Understand cross-account log delivery
- Learn how S3 protects centralized logs
- Understand log immutability and retention
- Understand KMS considerations for centralized logging
- Understand multi-Region logging
- Learn modern CloudWatch log centralization concepts
- Design an end-to-end centralized security operations architecture

---

# Centralized Logging Fundamentals

## 1. Why Centralize Logs?

In a multi-account AWS environment, logs are generated across:

```text
Accounts

Regions

Applications

Security Services

Networks
```

Without centralization:

```text
Account A
→ Logs

Account B
→ Logs

Account C
→ Logs
```

Security teams must investigate each location separately.

With centralization:

```text
Account A ──┐
Account B ──┼──> Central Log Platform
Account C ──┘
```

This improves:

```text
Investigation

Audit

Compliance

Threat Detection

Retention

Forensic Readiness
```

---

## 2. Security Goals of Central Logging

Central logging should provide:

```text
Confidentiality

Integrity

Availability

Retention

Searchability

Access Control
```

The most important security objective is:

```text
Compromised Workload
→ Cannot Destroy Evidence
```

---

# Security Tooling vs Log Archive

## 3. Security Tooling Account

The Security Tooling account is used for:

```text
Detection

Analysis

Investigation

Security Administration

Automation
```

Possible services:

```text
GuardDuty

Inspector

Macie

Security Hub

AWS Config Aggregator

EventBridge

Lambda / Automation
```

---

## 4. Log Archive Account

The Log Archive account is used for:

```text
Long-Term Log Storage

Audit Evidence

Compliance Retention

Forensic Evidence
```

Possible data:

```text
CloudTrail Logs

AWS Config History

VPC Flow Logs

WAF Logs

DNS Logs

Application Logs

Operating System Logs
```

---

## 5. Why Separate Them?

Conceptually:

```text
Security Tooling
→ Read / Analyze

Log Archive
→ Preserve
```

A security analyst may need:

```text
s3:GetObject
```

but not:

```text
s3:DeleteObject
```

The separation reduces the chance that operational security users can destroy audit evidence.

---

# Central Logging Architecture

## 6. High-Level Flow

```text
Production ───────┐
Development ──────┤
Network ──────────┤
Shared Services ──┼──> Central Logs
Security ─────────┘
                       |
                       v
                 Log Archive
                       |
                       v
                Security Analysis
```

---

## 7. Common Log Sources

Typical centralized logs include:

```text
AWS CloudTrail

AWS Config

VPC Flow Logs

AWS WAF Logs

Route 53 DNS Logs

CloudFront Logs

Load Balancer Logs

Network Firewall Logs

Operating System Logs

Application Logs

Database Logs
```

Each log answers different security questions.

---

# CloudTrail Organization Trail

## 8. Organization Trail

An organization trail is a CloudTrail trail that records supported activity across accounts in an AWS Organization.

Conceptually:

```text
AWS Organization
       |
       v
Organization Trail
       |
       +-- Account A
       +-- Account B
       +-- Account C
       |
       v
Central S3 Bucket
```

This provides a consistent organization-wide audit trail.

---

## 9. Why Organization Trail?

Without one:

```text
Each Account
→ Configure CloudTrail Manually
```

Potential result:

```text
Account Forgotten

Logging Disabled

Inconsistent Retention
```

With organization-level logging:

```text
Central Governance
→ Consistent Audit Coverage
```

---

## 10. Multi-Region Trail

A multi-Region trail can collect management events from multiple AWS Regions.

Conceptually:

```text
Tokyo ───────┐
Singapore ───┤
Virginia ────┼──> Organization Trail
Frankfurt ───┘
```

This reduces the risk that activity in an unexpected Region goes unlogged.

---

## 11. Organization Trail Destination

A strong pattern is:

```text
Organization Trail
       |
       v
S3 Bucket
       |
       v
Log Archive Account
```

The workload account should not own the authoritative audit logs.

---

## 12. Trail Management vs Log Storage

A useful separation:

```text
Security Tooling
→ Manage Trail

Log Archive
→ Store Logs
```

This separates:

```text
Control Plane

from

Evidence Storage
```

---

# CloudTrail Event Types

## 13. Management Events

Examples:

```text
CreateUser

RunInstances

PutBucketPolicy

CreateRole

AuthorizeSecurityGroupIngress
```

These answer:

```text
Who changed AWS resources?
```

---

## 14. Data Events

Examples:

```text
S3 GetObject

S3 PutObject

Lambda Invoke
```

Data events can be high-volume and may add additional cost.

Enable them strategically for:

```text
Sensitive S3 Buckets

Critical Lambda Functions
```

---

# AWS Config Centralization

## 15. AWS Config

AWS Config provides:

```text
Resource Configuration

Configuration History

Compliance Evaluation
```

Conceptually:

```text
AWS Resource
      |
      v
AWS Config
      |
      v
Configuration History
```

---

## 16. Config Aggregator

A Config Aggregator can collect AWS Config information across:

```text
Accounts

Regions
```

Conceptually:

```text
Account A Config ──┐
Account B Config ──┼──> Config Aggregator
Account C Config ──┘
```

This gives a central view of:

```text
Resource Inventory

Compliance

Configuration State
```

---

## 17. CloudTrail vs Config

Remember:

```text
CloudTrail
→ Who performed an API action?

AWS Config
→ What did the resource configuration become?
```

Together:

```text
Config
→ Security Group became public

CloudTrail
→ User X changed it
```

---

# GuardDuty Centralization

## 18. GuardDuty Delegated Administrator

A Security Tooling account can act as the GuardDuty delegated administrator.

Conceptually:

```text
AWS Organizations
       |
       v
Security Tooling
       |
       v
GuardDuty Administrator
       |
       +-- Prod
       +-- Dev
       +-- Network
```

This provides centralized threat visibility.

---

## 19. GuardDuty Findings

GuardDuty findings can identify:

```text
Credential Compromise

Malicious Network Activity

Suspicious API Behavior

Runtime Threats

S3 Threats
```

Central administration allows security teams to investigate findings without relying on each workload team.

---

# Inspector Centralization

## 20. Inspector Delegated Administration

Amazon Inspector can also use centralized administration.

Conceptually:

```text
Member Accounts
      |
      +-- EC2
      +-- ECR
      +-- Lambda
      |
      v
Inspector
      |
      v
Security Tooling
```

This provides organization-wide vulnerability visibility.

---

## 21. Coverage Matters

Central administration should answer:

```text
Which Accounts Are Covered?

Which Regions Are Covered?

Which Resources Are Scanned?

Which Accounts Have Gaps?
```

Remember:

```text
No Finding
≠
No Vulnerability

if

Resource Was Not Scanned
```

---

# Macie Centralization

## 22. Macie Administrator

Macie can provide centralized sensitive-data visibility across member accounts.

Conceptually:

```text
S3 Buckets
Across Organization
      |
      v
Amazon Macie
      |
      v
Security Tooling
```

This helps security teams identify:

```text
PII

Credentials

Financial Data

Sensitive Business Data
```

across the organization.

---

# Security Hub Centralization

## 23. Security Hub

Security Hub can receive and prioritize security signals from multiple services.

Conceptually:

```text
GuardDuty ──┐
Inspector ──┤
Macie ──────┼──> Security Hub
CSPM ───────┘
```

This creates a unified security view.

---

## 24. Security Hub CSPM

Security Hub CSPM focuses on:

```text
Security Standards

Controls

Misconfigurations

Security Posture
```

Examples:

```text
Public S3

Unencrypted EBS

Open Security Group

Logging Misconfiguration
```

---

# Security Signal Flow

## 25. End-to-End Security Signal

Example:

```text
GuardDuty
      |
      v
Finding
      |
      v
Security Hub
      |
      v
EventBridge
      |
      v
Automation / Notification
```

---

# EventBridge

## 26. Security Automation

Amazon EventBridge can route security events.

Conceptually:

```text
Security Finding
      |
      v
EventBridge
      |
      +-- SNS
      |
      +-- Lambda
      |
      +-- Step Functions
      |
      +-- Systems Manager
```

This enables:

```text
Alerting

Ticket Creation

Automated Investigation

Containment
```

---

## 27. Notification Example

```text
GuardDuty
Critical Finding
      |
      v
Security Hub
      |
      v
EventBridge
      |
      v
SNS
      |
      v
Security Team
```

---

## 28. Automated Response Example

```text
Compromised EC2
      |
      v
GuardDuty
      |
      v
EventBridge
      |
      v
Lambda / SSM
      |
      v
Isolation Security Group
```

Automatic response should be carefully tested.

---

# S3 as a Central Log Repository

## 29. Why S3?

Amazon S3 is commonly used for centralized long-term log storage because it supports:

```text
High Durability

Encryption

Versioning

Object Lock

Lifecycle Management

Fine-Grained Access Control
```

---

## 30. Central Log Bucket

Conceptually:

```text
Organization
     |
     v
Central Logging
     |
     v
S3
     |
     v
Log Archive Account
```

---

# Log Integrity

## 31. S3 Versioning

Versioning helps preserve previous versions of objects.

Conceptually:

```text
Log Object
    |
    +-- Version 1
    +-- Version 2
```

This can reduce the impact of accidental overwrite or deletion.

---

## 32. S3 Object Lock

S3 Object Lock can provide WORM-style protection.

WORM means:

```text
Write Once
Read Many
```

Conceptually:

```text
Log Written
    |
    v
Retention Period
    |
    X
Delete / Overwrite
```

depending on the configured retention mode.

---

## 33. Why Immutability Matters

Scenario:

```text
Attacker
   |
   v
Compromised Admin
   |
   v
Delete Evidence
```

Immutable storage reduces this risk.

Goal:

```text
Compromise Workload
≠
Destroy Investigation Evidence
```

---

# Log Confidentiality

## 34. Logs Can Contain Sensitive Data

Logs may include:

```text
User Names

IP Addresses

Request Paths

Resource Names

Identifiers

Authentication Context
```

Therefore logs themselves must be protected.

---

## 35. KMS Encryption

Central log buckets can use AWS KMS.

Conceptually:

```text
Log
 |
 v
S3
 |
 v
SSE-KMS
 |
 v
KMS Key
```

Access must account for both:

```text
S3 Permission

+

KMS Permission
```

---

## 36. KMS Key Administration

A dedicated KMS key can provide:

```text
Key Policy Control

Auditability

Separation of Duties

Cross-Account Permissions
```

Avoid granting broad:

```text
kms:Decrypt
```

permissions to workload administrators.

---

# S3 Bucket Policy

## 37. Log Writer vs Reader

A central log bucket can separate:

```text
Log Delivery
→ Write

Security Analyst
→ Read

Workload Administrator
→ No Delete
```

Conceptually:

```text
Member Account
    |
    v
Write Only
    |
    v
Log Archive S3
```

---

## 38. Least Privilege

Do not grant:

```text
s3:*
```

to log-producing workloads.

Grant only required delivery operations.

Similarly, analysts generally do not need:

```text
s3:DeleteObject
```

---

# SCP Protection

## 39. Protect Logging with SCPs

SCPs can prevent workload administrators from weakening centralized logging.

Examples:

```text
Deny CloudTrail StopLogging

Deny CloudTrail DeleteTrail

Protect AWS Config

Protect Security Services
```

This connects directly to Day 35.

---

## 40. Defense in Depth

Central logging should not rely on one control.

Use:

```text
Separate Account

IAM

SCP

S3 Bucket Policy

KMS Key Policy

Versioning

Object Lock

Monitoring
```

together.

---

# Log Retention

## 41. Retention Requirements

Different logs may require different retention periods.

Examples:

```text
Operational Logs
→ Shorter

Security Logs
→ Longer

Compliance Logs
→ Policy-Driven
```

Retention should reflect:

```text
Legal Requirements

Compliance

Incident Investigation Needs

Cost
```

---

## 42. S3 Lifecycle

S3 Lifecycle can transition older logs to lower-cost storage.

Conceptually:

```text
New Logs
→ S3 Standard
      |
      v
Older Logs
→ Glacier Storage Class
      |
      v
Expiration
```

according to retention requirements.

---

# Multi-Region Logging

## 43. Regional Security Services

Many AWS security services are Regional.

Examples:

```text
GuardDuty

Inspector

AWS Config

Security Hub CSPM
```

Therefore:

```text
One Region Enabled
≠
Organization Fully Covered
```

---

## 44. Multi-Region Design

Conceptually:

```text
Tokyo Security ───────┐
Singapore Security ───┼──> Central Security View
Virginia Security ────┘
```

Coverage should match the Regions where workloads can operate.

---

## 45. Region Restrictions

SCPs can reduce complexity by restricting workloads to approved Regions.

Example:

```text
Approved:

ap-northeast-1

ap-northeast-3
```

Then security services need coverage primarily in those allowed Regions.

---

# CloudWatch Centralization

## 46. CloudWatch Logs

CloudWatch Logs can collect:

```text
Application Logs

Operating System Logs

Lambda Logs

Service Logs
```

These logs usually originate in the workload account and Region.

---

## 47. Cross-Account Centralization

CloudWatch can centralize logs across accounts and Regions.

Conceptually:

```text
Account A Logs ──┐
Account B Logs ──┼──> Central Monitoring
Account C Logs ──┘
```

This enables security and operational teams to analyze data from a central location.

---

## 48. Centralization Rules

Modern CloudWatch logging supports organization-aware centralization rules.

Conceptually:

```text
Source Accounts
      |
      v
Centralization Rule
      |
      v
Destination Account
```

Centralization rules can define:

```text
Source Accounts

Regions

Log Groups

Destination
```

---

## 49. Important Limitation

Centralization typically processes:

```text
New Log Events
```

after the rule is created.

Existing historical logs are not automatically copied by simply creating a new centralization rule.

Therefore:

```text
Centralization Enabled Today
≠
Automatic Historical Backfill
```

---

# CloudWatch Unified Security Data

## 50. Modern Centralized Observability

Modern AWS security architectures can also use centralized CloudWatch capabilities for:

```text
Operational Data

Security Data

Compliance Data
```

in a dedicated monitoring account.

Conceptually:

```text
AWS Accounts
    |
    v
CloudWatch Central Collection
    |
    v
Monitoring Account
```

---

## 51. OCSF

Some modern AWS security data services use:

```text
Open Cybersecurity Schema Framework
```

or:

```text
OCSF
```

to normalize security telemetry.

Conceptually:

```text
Different Security Logs
       |
       v
OCSF
       |
       v
Common Schema
```

This improves cross-source analysis.

---

# Security Lake

## 52. Amazon Security Lake

Amazon Security Lake can centralize security data in a purpose-built security data lake.

Conceptually:

```text
CloudTrail
VPC Flow
DNS
Security Sources
      |
      v
Security Lake
      |
      v
Normalized Security Data
```

It can store supported security data in:

```text
OCSF
```

format.

---

## 53. When Security Lake Helps

Security Lake can be useful for:

```text
Large-Scale Security Analytics

SIEM Integration

Threat Hunting

Long-Term Security Data

Cross-Source Correlation
```

It is not required for every AWS environment.

---

# Monitoring the Logging System

## 54. Logging Infrastructure Is Security-Critical

It is not enough to monitor workloads.

Also monitor:

```text
Logging Configuration

Log Delivery Failures

Bucket Policies

KMS Policies

CloudTrail Status

Config Status
```

---

## 55. Logging Failure Is a Security Event

Example:

```text
CloudTrail Stops
```

Possible reasons:

```text
Misconfiguration

Operational Failure

Malicious Activity
```

Therefore:

```text
Logging Failure
→ Alert
```

---

# Centralized Security Investigation

## 56. Scenario — Public Security Group

AWS Config detects:

```text
TCP 22
0.0.0.0/0
```

Investigation:

```text
AWS Config
→ What changed?

CloudTrail
→ Who changed it?

VPC Flow Logs
→ Was it accessed?

OS Logs
→ Was authentication successful?

GuardDuty
→ Was suspicious activity detected?
```

---

## 57. Scenario — Credential Compromise

GuardDuty detects:

```text
Potential Credential Compromise
```

Investigation:

```text
GuardDuty
      |
      v
CloudTrail
      |
      v
API Timeline
      |
      v
Security Hub
      |
      v
Related Findings
```

Then verify:

```text
Secrets Access

KMS Activity

S3 Access

EC2 Creation

IAM Changes
```

---

## 58. Scenario — Sensitive Data Access

Macie:

```text
PII in S3
```

GuardDuty:

```text
Suspicious S3 Access
```

CloudTrail:

```text
GetObject
```

Central security team correlates:

```text
Sensitive Data

+

Suspicious Access

=

Potential Data Exfiltration
```

---

# Incident Response Architecture

## 59. Security Operations Flow

```text
Collect
   |
   v
Centralize
   |
   v
Detect
   |
   v
Correlate
   |
   v
Alert
   |
   v
Investigate
   |
   v
Contain
   |
   v
Remediate
```

---

## 60. Evidence vs Detection

Remember:

```text
Log Archive
→ Evidence

Security Tooling
→ Detection and Investigation
```

Both are required.

---

# Access Design

## 61. Security Analyst Access

A Security Analyst may need:

```text
Read Security Findings

Read Logs

Run Queries

Assume Investigation Roles
```

but generally not:

```text
Delete Logs

Modify Production Applications

Change Organization Policies
```

---

## 62. Log Administrator Access

Log administrators may need:

```text
Retention

Lifecycle

Bucket Configuration

Log Pipeline Administration
```

but should not automatically be able to:

```text
Modify Production Resources
```

---

# Cost Considerations

## 63. Central Logging Costs

Costs can include:

```text
Log Ingestion

CloudWatch Storage

S3 Storage

KMS Requests

CloudTrail Data Events

Cross-Region Transfer

Security Lake

Analytics Queries
```

Therefore:

```text
Collect Everything Forever
```

is not always the correct design.

---

## 64. Risk-Based Logging

Use stronger logging for:

```text
Production

Sensitive Data

Privileged IAM

Critical Applications

Internet-Facing Workloads
```

Balance:

```text
Security Value

Compliance

Cost

Operational Requirements
```

---

# Common Misconfigurations

## 65. Logs Stored Only Locally

Poor:

```text
Production Logs
→ Production Account Only
```

If production is compromised:

```text
Logs May Be Deleted
```

Better:

```text
Production
→ Central Log Archive
```

---

## 66. Security Analysts Can Delete Logs

Poor:

```text
SecurityAnalyst
→ s3:*
```

Better:

```text
Read / Query
```

without delete permissions.

---

## 67. Central Bucket Is Public

A log bucket should never rely on public access.

Use:

```text
S3 Block Public Access

Restrictive Bucket Policy

Least Privilege
```

---

## 68. KMS Key Too Broad

Poor:

```text
kms:Decrypt

Principal:
*
```

Better:

```text
Approved Security Roles

Approved Logging Services
```

---

## 69. Only One Region Monitored

Scenario:

```text
Security Monitoring:
Tokyo Only

Workload:
Virginia
```

Result:

```text
Visibility Gap
```

Match security coverage to allowed workload Regions.

---

## 70. No Alert on Logging Failure

If:

```text
CloudTrail Stops
```

and nobody notices:

```text
Audit Visibility Lost
```

Monitoring infrastructure itself must be monitored.

---

## 71. Historical Logs Assumed to Be Backfilled

A common misconception:

```text
Create CloudWatch Centralization Rule
→ All Historical Logs Copied
```

Incorrect.

Plan separately for historical data migration if required.

---

# Hands-on Practice

## 72. Architecture Drawing

Draw:

```text
Member Accounts
      |
      +-- CloudTrail
      +-- Config
      +-- Flow Logs
      +-- WAF
      |
      v
Central Logging
      |
      v
Log Archive
```

Then separately:

```text
GuardDuty
Inspector
Macie
Security Hub
      |
      v
Security Tooling
```

---

## 73. Organization Trail Review

If available:

```text
AWS Console
      |
      v
CloudTrail
      |
      v
Trails
```

Review:

```text
Organization Trail?

Multi-Region?

S3 Destination?

Management Events?

Data Events?
```

Do not modify production logging solely for practice.

---

## 74. Config Aggregator Review

Navigate:

```text
AWS Config
   |
   v
Aggregators
```

Review:

```text
Accounts

Regions

Resource Counts

Compliance
```

---

## 75. Security Coverage Exercise

Create a table:

```text
Service      Account Coverage    Region Coverage

GuardDuty

Inspector

Macie

Security Hub

AWS Config
```

Identify any potential gaps.

---

## 76. Central Log Bucket Review

If a test bucket exists, review:

```text
Block Public Access

Versioning

Encryption

Lifecycle

Object Lock

Bucket Policy
```

Ask:

```text
Who can write?

Who can read?

Who can delete?
```

---

## 77. EventBridge Exercise

Design:

```text
GuardDuty
High Severity
      |
      v
EventBridge
      |
      v
SNS
```

Then extend:

```text
Critical Finding
      |
      v
Automation
      |
      v
Contain Resource
```

---

## 78. Optional CLI Practice

List CloudTrail trails:

```bash
aws cloudtrail describe-trails
```

Check trail status:

```bash
aws cloudtrail get-trail-status \
  --name <trail-name>
```

List Config aggregators:

```bash
aws configservice describe-configuration-aggregators
```

Check GuardDuty detectors:

```bash
aws guardduty list-detectors
```

List delegated administrators:

```bash
aws organizations list-delegated-administrators
```

Do not publish real:

```text
Account IDs

Bucket Names

Trail Names

Organization IDs

Security Role ARNs
```

to a public repository.

---

# Architecture Exercise

## 79. Centralized Security Architecture

```text
                      AWS Organization
                             |
        +--------------------+--------------------+
        |                                         |
        v                                         v
   Member Accounts                           Security OU
        |                                         |
        |                           +-------------+-------------+
        |                           |                           |
        v                           v                           v
 CloudTrail / Config         Security Tooling              Log Archive
 Flow / WAF / DNS               Account                      Account
        |                           |                           |
        |                           +-- GuardDuty              |
        |                           +-- Inspector               |
        |                           +-- Macie                   |
        |                           +-- Security Hub            |
        |                           +-- EventBridge             |
        |                                                       |
        +-----------------------------------------------------> S3
                                                                |
                                                                +-- Versioning
                                                                +-- Object Lock
                                                                +-- KMS
                                                                +-- Lifecycle
```

---

## 80. Security Operations Architecture

```text
Logs
   ↓
Centralize
   ↓
Preserve
   ↓
Analyze
   ↓
Detect
   ↓
Correlate
   ↓
Alert
   ↓
Investigate
   ↓
Respond
```

---

# Security Checklist

```text
[ ] Organization-wide CloudTrail logging is configured

[ ] Multi-Region logging is used where appropriate

[ ] Authoritative CloudTrail logs are stored outside workload accounts

[ ] AWS Config is enabled in required accounts and Regions

[ ] Config aggregation is centralized

[ ] GuardDuty is centrally administered

[ ] Inspector coverage is centrally reviewed

[ ] Macie administration is centralized where required

[ ] Security Hub provides centralized security visibility

[ ] EventBridge routes high-priority security findings

[ ] Central log storage resides in a dedicated account

[ ] S3 Block Public Access protects log buckets

[ ] Central log buckets use appropriate encryption

[ ] KMS permissions follow least privilege

[ ] S3 Versioning is enabled where required

[ ] Object Lock is considered for immutable evidence

[ ] Lifecycle and retention policies are defined

[ ] Workload administrators cannot delete central evidence

[ ] Security analysts do not receive unnecessary delete permissions

[ ] Security services cover all approved workload Regions

[ ] Logging infrastructure failures generate alerts

[ ] CloudWatch centralization scope is documented

[ ] Historical log migration requirements are considered separately

[ ] Logging costs and retention are periodically reviewed
```

---

## Key Takeaways

- Centralized logging provides consistent audit, investigation, and forensic visibility across AWS accounts.
- Security Tooling and Log Archive accounts serve different purposes.
- Security Tooling focuses on detection, analysis, and response.
- Log Archive focuses on durable and protected evidence storage.
- CloudTrail organization trails can provide consistent activity logging across organization accounts.
- Multi-Region logging reduces visibility gaps.
- AWS Config Aggregators provide centralized configuration and compliance views.
- GuardDuty, Inspector, and Macie can be centrally managed through delegated administration.
- Security Hub provides centralized security signal management.
- EventBridge can route findings into notification and remediation workflows.
- Central S3 log repositories should use strict access control, encryption, versioning, retention, and immutability controls.
- Workload administrators should not be able to delete authoritative central logs.
- Security monitoring must cover every approved workload Region.
- Logging infrastructure itself must be monitored.
- Modern CloudWatch capabilities can centralize logs and security telemetry across accounts and Regions.
- Security data normalization using OCSF can simplify cross-source security analytics.
- Centralized logging should balance security value, compliance requirements, and cost.

---

## Reflection

Today I learned how centralized logging and security monitoring provide organization-wide visibility across a multi-account AWS environment.

The most important lesson is that security analysis and evidence preservation should be separated. The Security Tooling account can manage threat detection and investigation, while the Log Archive account protects authoritative audit evidence.

I also learned that CloudTrail organization trails, AWS Config aggregation, delegated security administration, EventBridge automation, and centralized log storage work together to create a scalable security operations architecture.

From a cloud security perspective, centralized logging is not simply about collecting logs. The logs must be protected against deletion, encrypted, retained for the required period, monitored for delivery failures, and made available to the appropriate security analysts without giving them unnecessary administrative permissions.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Centralized Logging | Collecting logs from multiple accounts and Regions into centrally controlled locations |
| Config Aggregator | AWS Config resource that aggregates configuration and compliance data across accounts and Regions |
| Delegated Administrator | Member account centrally administering a supported AWS service |
| Forensic Readiness | Ability to preserve and analyze reliable evidence during an incident |
| Immutability | Property that prevents stored evidence from being modified or deleted |
| Log Archive | Dedicated account or repository for protected long-term log storage |
| Object Lock | S3 feature providing WORM-style retention protection |
| OCSF | Open Cybersecurity Schema Framework for normalized cybersecurity data |
| Organization Trail | CloudTrail trail that records supported activity across AWS Organization accounts |
| Security Telemetry | Logs and signals used for security monitoring and investigation |
