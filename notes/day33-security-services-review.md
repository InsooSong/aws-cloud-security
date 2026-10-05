# Day 33 — Security Services Review

## Topic

AWS Security Services Review — Data Protection, Threat Detection, Vulnerability Management, Sensitive Data Discovery, Web Protection, and Security Operations

---

## Objectives

- Review AWS KMS
- Review AWS Secrets Manager
- Review Amazon GuardDuty
- Review AWS Security Hub and Security Hub CSPM
- Review Amazon Inspector
- Review Amazon Macie
- Review AWS WAF
- Review AWS Shield
- Understand the role of each security service
- Compare preventive, detective, and protective controls
- Practice selecting the correct AWS security service for different scenarios
- Correlate multiple security services during incident investigations
- Build an end-to-end cloud security architecture

---

# Phase 5 Overview

## 1. Security Services Covered

During this phase, I studied:

```text
Day 25
→ AWS KMS Fundamentals

Day 26
→ KMS Keys & Encryption

Day 27
→ AWS Secrets Manager

Day 28
→ Amazon GuardDuty

Day 29
→ AWS Security Hub

Day 30
→ Amazon Inspector

Day 31
→ Amazon Macie

Day 32
→ AWS WAF & Shield
```

These services protect different parts of an AWS environment.

---

## 2. Security Service Map

A useful high-level model is:

```text
Data Protection
├── AWS KMS
└── AWS Secrets Manager

Threat Detection
└── Amazon GuardDuty

Vulnerability Management
└── Amazon Inspector

Sensitive Data Security
└── Amazon Macie

Web Application Protection
├── AWS WAF
└── AWS Shield

Security Posture and Finding Management
├── AWS Security Hub
└── Security Hub CSPM
```

---

# AWS KMS Review

## 3. AWS KMS

AWS KMS manages cryptographic keys.

Question:

```text
How should encryption keys be controlled?
```

Typical use cases:

```text
EBS Encryption

S3 SSE-KMS

RDS Encryption

Secrets Manager Encryption

Application Encryption
```

Core concepts:

```text
KMS Key

Key Policy

IAM Policy

Grant

Data Key

Envelope Encryption

Encryption Context

Rotation
```

---

## 4. KMS Mental Model

```text
KMS Key
   |
   v
Protect Data Key
   |
   v
Data Key
   |
   v
Encrypt Actual Data
```

The KMS key generally protects the data key.

The data key encrypts the actual application data.

---

## 5. KMS Security Questions

When reviewing KMS:

```text
Which key protects the data?

Who can use the key?

Who can administer the key?

Are usage and administration separated?

Can another account use the key?

Is rotation configured appropriately?

What happens if the key is disabled?

What happens if the key is deleted?
```

---

# Secrets Manager Review

## 6. AWS Secrets Manager

Secrets Manager stores and manages sensitive credentials.

Question:

```text
Where should applications securely obtain credentials?
```

Examples:

```text
Database Passwords

API Keys

OAuth Tokens

Application Credentials
```

---

## 7. Secure Secret Architecture

```text
Application
     |
     v
IAM Role
     |
     v
Secrets Manager
     |
     v
KMS
     |
     v
Secret
```

Avoid:

```text
Hard-Coded Passwords

Secrets in GitHub

Secrets in Dockerfiles

Secrets in AMIs
```

---

## 8. Secret Rotation

Important labels:

```text
AWSCURRENT

AWSPREVIOUS

AWSPENDING
```

Rotation concept:

```text
Create
  ↓
Set
  ↓
Test
  ↓
Finish
```

Rotation should update both:

```text
Secrets Manager

and

Target Service
```

---

# GuardDuty Review

## 9. Amazon GuardDuty

GuardDuty is a managed threat detection service.

Question:

```text
Is suspicious or potentially malicious activity occurring?
```

GuardDuty analyzes telemetry such as:

```text
CloudTrail Management Events

VPC Network Activity

DNS Activity

S3 Data Activity

Runtime Events

RDS Login Activity

Lambda Network Activity
```

depending on enabled protection plans.

---

## 10. GuardDuty Mental Model

```text
AWS Telemetry
     |
     v
GuardDuty
     |
     v
Threat Detection
     |
     v
Finding
```

A finding is:

```text
A Security Signal
```

not automatically:

```text
A Confirmed Incident
```

---

## 11. GuardDuty Investigation

When a finding appears:

```text
Finding Type
    ↓
Severity
    ↓
Affected Resource
    ↓
Principal / IP / Domain
    ↓
CloudTrail
    ↓
Network / Runtime Evidence
    ↓
Scope
    ↓
Containment
```

---

# Security Hub Review

## 12. AWS Security Hub

AWS Security Hub provides a unified security experience that correlates and prioritizes security signals.

It can receive security information from services such as:

```text
GuardDuty

Inspector

Macie

Security Hub CSPM
```

Conceptually:

```text
GuardDuty ──┐
Inspector ──┤
Macie ──────┼──> Security Hub
CSPM ───────┘
                 |
                 v
          Prioritized Security View
```

---

## 13. Security Hub CSPM

Security Hub CSPM focuses on cloud security posture management.

Question:

```text
Does the AWS environment follow security standards and best practices?
```

Examples:

```text
S3 Public Access

EBS Encryption

RDS Encryption

CloudTrail Configuration

IAM Security

Security Group Exposure
```

---

## 14. Security Hub vs Security Hub CSPM

A useful distinction:

```text
Security Hub
→ Correlate and prioritize security signals

Security Hub CSPM
→ Evaluate security posture and controls
```

Together:

```text
Threats

Vulnerabilities

Sensitive Data

Misconfigurations
       |
       v
Unified Security View
```

---

# Inspector Review

## 15. Amazon Inspector

Inspector is a vulnerability management service.

Question:

```text
What known vulnerabilities exist in my workloads?
```

Main resources:

```text
EC2

ECR

Lambda
```

---

## 16. Inspector Mental Model

```text
Workload
   |
   v
Inspector
   |
   v
Vulnerability
   |
   v
Risk Context
   |
   v
Finding
   |
   v
Remediation
```

---

## 17. Vulnerability Priority

Do not prioritize only by:

```text
CVSS
```

Use context:

```text
CVSS

EPSS

Exploit Availability

Internet Exposure

Resource Criticality

Data Sensitivity
```

A useful formula:

```text
Technical Severity
+
Exploitability
+
Exposure
+
Business Impact
=
Remediation Priority
```

---

# Macie Review

## 18. Amazon Macie

Macie discovers sensitive data in Amazon S3.

Question:

```text
Where is sensitive data stored?
```

Possible sensitive data:

```text
Credentials

Financial Data

PII

PHI

Organization-Specific Data
```

---

## 19. Macie Mental Model

```text
Amazon S3
    |
    v
Macie
    |
    v
Sensitive Data Discovery
    |
    v
Finding
```

Important concepts:

```text
Managed Data Identifiers

Custom Data Identifiers

Allow Lists

Automated Discovery

Discovery Jobs
```

---

## 20. Macie Risk Context

Compare:

```text
Sensitive Data
+
Private Bucket
+
Encryption
```

with:

```text
Sensitive Data
+
Public Bucket
+
External Access
```

The second requires much higher priority.

---

# AWS WAF Review

## 21. AWS WAF

AWS WAF protects web applications at the HTTP/HTTPS layer.

Question:

```text
Should this web request be allowed?
```

Possible inspection:

```text
IP

URI

Query String

Headers

Body

Cookies
```

---

## 22. WAF Architecture

```text
Internet
   |
   v
CloudFront / ALB / API Gateway
   |
   v
AWS WAF
   |
   v
Web ACL
   |
   v
Application
```

Important controls:

```text
Managed Rules

Rate-Based Rules

IP Sets

SQL Injection Rules

XSS Rules

Bot Control

CAPTCHA

Challenge
```

---

## 23. Safe WAF Deployment

Important operational model:

```text
New Rule
   |
   v
Count
   |
   v
Analyze
   |
   v
Tune
   |
   v
Block / Challenge
```

Avoid immediately blocking production traffic without validation.

---

# AWS Shield Review

## 24. AWS Shield

AWS Shield provides DDoS protection.

Question:

```text
How should Internet-facing resources handle DDoS attacks?
```

---

## 25. Shield Standard

```text
Shield Standard
```

provides baseline DDoS protection automatically.

Focus:

```text
Common Network

Transport-Layer Attacks
```

---

## 26. Shield Advanced

```text
Shield Advanced
```

provides enhanced DDoS protection for selected critical resources.

Capabilities can include:

```text
Advanced Detection

Event Visibility

Application-Layer Protection

SRT Support

Automatic Application-Layer Mitigation
```

---

# Service Selection

## 27. Scenario — Encrypt EBS

Requirement:

```text
EC2 EBS volumes contain sensitive data.

Need customer-controlled encryption key.
```

Choose:

```text
AWS KMS
```

Why:

```text
Centralized cryptographic key management
```

---

## 28. Scenario — Database Password

Requirement:

```text
EC2 application needs RDS password.

Password must not exist in source code.

Automatic rotation required.
```

Choose:

```text
AWS Secrets Manager
```

Supporting service:

```text
AWS KMS
```

---

## 29. Scenario — Stolen IAM Credentials

Requirement:

```text
IAM credentials are being used
from an unusual location
with unusual API activity.
```

Choose:

```text
Amazon GuardDuty
```

Then investigate:

```text
CloudTrail
```

---

## 30. Scenario — Critical CVE

Requirement:

```text
EC2 instances may contain
known software vulnerabilities.
```

Choose:

```text
Amazon Inspector
```

---

## 31. Scenario — Vulnerable Container Image

Requirement:

```text
Need continuous scanning
of images stored in ECR.
```

Choose:

```text
Amazon Inspector
```

Remediation:

```text
Update Dependency
      ↓
Rebuild Image
      ↓
Push to ECR
      ↓
Rescan
      ↓
Deploy
```

---

## 32. Scenario — Find PII

Requirement:

```text
Need to identify S3 objects
containing customer PII.
```

Choose:

```text
Amazon Macie
```

---

## 33. Scenario — Organization-Specific Sensitive Data

Requirement:

```text
Find employee IDs:

EMP-123456
```

Choose:

```text
Amazon Macie
+
Custom Data Identifier
```

---

## 34. Scenario — SQL Injection

Requirement:

```text
Block common SQL injection attempts
against a public web application.
```

Choose:

```text
AWS WAF
```

Possible control:

```text
AWS Managed Rules
```

---

## 35. Scenario — Credential Stuffing

Requirement:

```text
Thousands of automated login attempts
against /login.
```

Choose:

```text
AWS WAF
```

Possible controls:

```text
Rate-Based Rule

Bot Control

Challenge

CAPTCHA

Fraud Control
```

---

## 36. Scenario — Infrastructure DDoS

Requirement:

```text
Public service is receiving
large-scale network traffic.
```

Choose:

```text
AWS Shield
```

Critical workload:

```text
Shield Advanced
```

---

## 37. Scenario — Central Security View

Requirement:

```text
Security team needs to review:

GuardDuty threats

Inspector vulnerabilities

Macie sensitive-data risks

CSPM posture issues
```

Choose:

```text
AWS Security Hub
```

---

## 38. Scenario — Security Standards

Requirement:

```text
Evaluate AWS resources
against security best practices
and compliance controls.
```

Choose:

```text
Security Hub CSPM
```

---

# Prevent / Detect / Protect / Manage

## 39. Preventive and Protective Controls

Examples:

```text
AWS WAF

AWS Shield

KMS Policies

Secrets Manager Access Controls
```

Goal:

```text
Reduce the likelihood
or impact of an attack.
```

---

## 40. Detective Controls

Examples:

```text
GuardDuty

Inspector

Macie

Security Hub CSPM
```

Goal:

```text
Identify threats,
vulnerabilities,
sensitive data,
or misconfigurations.
```

---

## 41. Management and Aggregation

Example:

```text
AWS Security Hub
```

Goal:

```text
Centralize

Correlate

Prioritize

Respond
```

---

# Combined Incident Scenarios

## 42. Scenario — Vulnerable Public EC2

Environment:

```text
EC2

Public IP

Apache Critical CVE

IAM Role

Sensitive S3 Access
```

Signals:

```text
Inspector
→ Critical CVE

GuardDuty
→ Suspicious EC2 Network Activity
```

Investigation:

```text
Security Hub
→ Correlate Findings

CloudTrail
→ IAM / API Activity

AWS Config
→ Network Configuration History

VPC Flow Logs
→ Network Activity

OS Logs
→ Host Activity
```

Priority:

```text
Very High
```

---

## 43. Scenario — Sensitive Data Exfiltration

Signals:

```text
Macie
→ PII in S3

GuardDuty
→ Suspicious S3 Data Access
```

Additional investigation:

```text
CloudTrail Data Events
→ GetObject Activity

AWS Config
→ Bucket Policy History

Security Hub
→ Centralized View
```

Potential conclusion:

```text
Sensitive Data Exposure
or
Data Exfiltration
```

---

## 44. Scenario — Compromised Credential and Secret Access

Signals:

```text
GuardDuty
→ Suspicious IAM Credential Usage

CloudTrail
→ GetSecretValue

Secrets Manager
→ Production DB Secret

RDS
→ Production Database
```

Investigation:

```text
Which Principal?

Which Secret?

Which Database?

Was Secret Retrieved?

Was Database Accessed?

What Other APIs Were Called?
```

Response may include:

```text
Disable Credential

Rotate Secret

Review DB Access

Review IAM Permissions

Preserve Evidence
```

---

## 45. Scenario — Public Web Attack

Signals:

```text
AWS WAF
→ High SQLi Match Count

GuardDuty
→ Suspicious Activity

Inspector
→ Vulnerable Web Server
```

Security response:

```text
WAF
→ Block / Challenge

Inspector
→ Patch Vulnerability

GuardDuty
→ Investigate Threat Activity

Security Hub
→ Correlate Findings
```

---

## 46. Scenario — DDoS plus Application Attack

Environment:

```text
CloudFront

AWS WAF

ALB

Application
```

Attack:

```text
Layer 3 / 4 Flood
+
Layer 7 HTTP Flood
```

Controls:

```text
Shield
→ Infrastructure DDoS Protection

AWS WAF
→ Application Request Filtering

Rate-Based Rules
→ Layer 7 Rate Control

Bot Control
→ Automated Client Management
```

---

# Security Architecture

## 47. Complete Security Architecture

```text
                         Internet
                            |
                            v
                      AWS Shield
                            |
                            v
                        AWS WAF
                            |
                            v
                        CloudFront
                            |
                            v
                            ALB
                            |
                            v
                     Private Compute
                            |
          +-----------------+----------------+
          |                 |                |
          v                 v                v
         S3                RDS              EBS
          |                 |                |
          +-----------------+----------------+
                            |
                            v
                         AWS KMS

Application Credentials
         |
         v
Secrets Manager

Security Visibility
         |
         +-- GuardDuty
         |
         +-- Inspector
         |
         +-- Macie
         |
         +-- Security Hub CSPM
         |
         v
     Security Hub
         |
         v
Security Operations
```

---

# Service Decision Matrix

## 48. Which Service?

| Security Requirement | AWS Service |
|---|---|
| Encryption key management | AWS KMS |
| Password / API key storage | Secrets Manager |
| Automatic secret rotation | Secrets Manager |
| Threat detection | GuardDuty |
| Compromised credential detection | GuardDuty |
| Runtime threat detection | GuardDuty |
| Vulnerability scanning | Inspector |
| EC2 package CVEs | Inspector |
| ECR image CVEs | Inspector |
| Lambda vulnerability scanning | Inspector |
| Sensitive S3 data discovery | Macie |
| Custom sensitive-data detection | Macie |
| Web request filtering | AWS WAF |
| SQLi / XSS filtering | AWS WAF |
| Bot management | AWS WAF |
| HTTP rate limiting | AWS WAF |
| DDoS protection | AWS Shield |
| Enhanced DDoS response | Shield Advanced |
| Security posture controls | Security Hub CSPM |
| Centralized security prioritization | Security Hub |

---

# Common Exam Traps

## 49. GuardDuty vs Inspector

```text
Known CVE
→ Inspector

Suspicious Exploitation Activity
→ GuardDuty
```

Do not confuse:

```text
Weakness

with

Attack Activity
```

---

## 50. Macie vs GuardDuty S3 Protection

```text
Macie
→ What sensitive data exists?

GuardDuty S3 Protection
→ Is suspicious S3 access occurring?
```

Example:

```text
Credit Card Data Found
→ Macie

Unusual GetObject Activity
→ GuardDuty
```

---

## 51. KMS vs Secrets Manager

```text
KMS
→ Cryptographic Keys

Secrets Manager
→ Application Secrets
```

Secrets Manager itself can use KMS for encryption.

---

## 52. WAF vs Shield

```text
WAF
→ HTTP Request Inspection

Shield
→ DDoS Protection
```

For Layer 7 DDoS:

```text
Shield Advanced
+
AWS WAF
```

may be used together.

---

## 53. Security Hub vs GuardDuty

```text
GuardDuty
→ Creates threat findings

Security Hub
→ Correlates and prioritizes security signals
```

---

## 54. Security Hub vs CSPM

```text
Security Hub CSPM
→ Posture and controls

Security Hub
→ Unified risk and finding management
```

---

# Risk-Based Prioritization

## 55. Do Not Prioritize by One Number

Avoid:

```text
Highest Severity First
and nothing else
```

Instead consider:

```text
Severity

Exploitability

Exposure

Sensitive Data

Resource Criticality

Active Threat Evidence
```

---

## 56. Example

### Resource A

```text
Inspector:
Critical CVE

Private Development Instance

No Known Exploit

No Sensitive Data
```

### Resource B

```text
Inspector:
High CVE

Public Production Instance

Known Exploit

GuardDuty Finding

Sensitive S3 Access
```

Resource B may deserve higher operational priority.

---

# Multi-Account Security

## 57. Central Security Account

A mature AWS Organization can centralize security services.

Conceptually:

```text
AWS Organizations
        |
        v
Security Account
        |
        +-- GuardDuty Admin
        |
        +-- Inspector Admin
        |
        +-- Macie Admin
        |
        +-- Security Hub
        |
        +-- Security Hub CSPM
```

This improves:

```text
Visibility

Governance

Consistency

Separation of Duties
```

---

## 58. Coverage Matters

A security service is useful only where coverage exists.

Check:

```text
Accounts

Regions

Resource Types

Protection Plans

Scanning Coverage

Sensitive Data Discovery
```

A missing finding may mean:

```text
No Threat
```

or:

```text
No Coverage
```

These are very different.

---

# Security Operations Workflow

## 59. End-to-End Process

```text
Protect
   |
   v
Monitor
   |
   v
Detect
   |
   v
Aggregate
   |
   v
Prioritize
   |
   v
Investigate
   |
   v
Contain
   |
   v
Remediate
   |
   v
Verify
```

---

## 60. Example Workflow

```text
GuardDuty Finding
       |
       v
Security Hub
       |
       v
High Priority
       |
       v
CloudTrail Investigation
       |
       v
Affected EC2
       |
       v
Inspector Finding
       |
       v
Critical CVE
       |
       v
Contain Instance
       |
       v
Patch / Rebuild
       |
       v
Rescan
```

---

# Hands-on Practice

## 61. Practice — Service Identification

For each scenario, choose the best AWS service.

### Scenario A

```text
Find credit card numbers in S3.
```

Answer:

```text
Amazon Macie
```

### Scenario B

```text
Detect suspicious IAM credential activity.
```

Answer:

```text
Amazon GuardDuty
```

### Scenario C

```text
Scan ECR image for CVEs.
```

Answer:

```text
Amazon Inspector
```

### Scenario D

```text
Block SQL injection traffic.
```

Answer:

```text
AWS WAF
```

### Scenario E

```text
Protect a critical public service from DDoS attacks.
```

Answer:

```text
AWS Shield Advanced
```

### Scenario F

```text
Automatically rotate an RDS password.
```

Answer:

```text
AWS Secrets Manager
```

### Scenario G

```text
Control the encryption key for an EBS volume.
```

Answer:

```text
AWS KMS
```

### Scenario H

```text
Evaluate resources against security best practices.
```

Answer:

```text
Security Hub CSPM
```

### Scenario I

```text
Prioritize GuardDuty, Inspector, and Macie security signals centrally.
```

Answer:

```text
AWS Security Hub
```

---

# Architecture Exercise

## 62. Design a Secure Production Environment

Requirements:

```text
Public Web Application

EC2

RDS

S3 Customer Data

Database Credentials

DDoS Risk

Sensitive PII

Vulnerability Management

Threat Detection
```

Possible architecture:

```text
Internet
   |
   v
Shield
   |
   v
AWS WAF
   |
   v
CloudFront / ALB
   |
   v
Private EC2
   |
   +----------> Private RDS
   |
   +----------> Private S3
```

Security services:

```text
KMS
→ Encrypt EBS / RDS / S3

Secrets Manager
→ Database Credentials

Inspector
→ EC2 Vulnerabilities

Macie
→ S3 Sensitive Data

GuardDuty
→ Threat Detection

Security Hub CSPM
→ Posture Controls

Security Hub
→ Central Prioritization
```

---

# Security Checklist

```text
[ ] Sensitive data is encrypted with appropriate KMS controls

[ ] Application credentials are stored in Secrets Manager

[ ] Secret rotation is configured where required

[ ] GuardDuty covers required accounts and Regions

[ ] Required GuardDuty protection plans are enabled

[ ] Inspector scanning covers EC2, ECR, and Lambda where required

[ ] Inspector coverage gaps are reviewed

[ ] Macie covers required S3 data

[ ] Automated sensitive data discovery is configured where appropriate

[ ] WAF protects public web applications

[ ] WAF rules are tested before blocking production traffic

[ ] Rate-based and bot controls are used where appropriate

[ ] Shield protection is understood and configured for critical workloads

[ ] Security Hub CSPM evaluates required security controls

[ ] Security Hub receives the required security signals

[ ] Multi-account security administration is centralized where appropriate

[ ] Findings have clear owners

[ ] Critical findings have defined response procedures

[ ] Security service coverage is reviewed periodically
```

---

## Key Takeaways

- AWS security services solve different security problems.
- AWS KMS manages cryptographic keys.
- Secrets Manager manages sensitive credentials and secret rotation.
- GuardDuty detects suspicious and potentially malicious activity.
- Inspector identifies software vulnerabilities and unintended network exposure.
- Macie discovers sensitive data in Amazon S3.
- AWS WAF protects web applications by inspecting HTTP and HTTPS requests.
- AWS Shield provides DDoS protection.
- Security Hub CSPM evaluates security posture and configuration controls.
- Security Hub correlates and prioritizes security signals across multiple services.
- A security finding should be evaluated with resource criticality, exposure, exploitability, and business context.
- Coverage is as important as finding severity.
- Security tools are most effective when integrated into a complete investigation and response process.
- No single AWS security service provides complete cloud security.
- Defense in depth requires preventive, detective, protective, and responsive controls.

---

## Reflection

During this phase, I learned that AWS security services are designed to solve different security problems and should be used together as part of a defense-in-depth architecture.

AWS KMS and Secrets Manager protect encryption keys and application credentials. Amazon GuardDuty detects suspicious activity, Amazon Inspector identifies vulnerabilities, and Amazon Macie discovers sensitive data stored in S3.

AWS WAF and AWS Shield provide preventive protection for Internet-facing applications, while Security Hub CSPM evaluates security posture and Security Hub provides centralized security prioritization.

The most important lesson is that selecting the correct security service depends on the security question being asked.

Instead of memorizing individual AWS services, I should identify whether the problem is related to encryption, secrets, threats, vulnerabilities, sensitive data, web attacks, DDoS protection, posture management, or centralized security operations.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Attack Surface | All points through which a system could potentially be attacked |
| Coverage | The extent to which security services monitor the intended environment |
| Data Classification | Categorizing data based on sensitivity |
| Defense in Depth | Using multiple security controls at different layers |
| Remediation | Correcting or reducing a security weakness or threat |
| Risk Prioritization | Ranking security issues according to likelihood and impact |
| Security Posture | Overall security configuration and condition of an environment |
| Security Signal | Information that may indicate a security issue |
| Threat Detection | Identifying suspicious or malicious behavior |
| Vulnerability Management | Finding, prioritizing, and remediating security weaknesses |
