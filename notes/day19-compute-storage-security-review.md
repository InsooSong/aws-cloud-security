# Day 19 — Compute & Storage Security Review

## Topic

AWS Compute and Storage Security Architecture Review

---

## Objectives

- Review EC2 security fundamentals
- Review EC2 security hardening
- Review S3 access control and data protection
- Review EBS encryption and KMS integration
- Review RDS security architecture
- Connect identity, network, data, and monitoring controls
- Apply defense-in-depth principles
- Identify common cloud security misconfigurations
- Practice security architecture review
- Build a systematic troubleshooting and review process

---

## 1. Phase 3 Security Overview

During this phase, I studied four major AWS areas:

```text
Amazon EC2
Amazon EBS
Amazon S3
Amazon RDS
```

Each service has different security responsibilities.

A useful security framework is:

```text
Identity
   ↓
Network
   ↓
Compute / Service
   ↓
Data Protection
   ↓
Logging
   ↓
Monitoring
```

Security should be evaluated across all of these layers rather than looking at only one AWS service.

---

## 2. EC2 Security Review

Amazon EC2 provides virtual servers in AWS.

Because EC2 gives customers control over the guest operating system, customers have significant security responsibilities.

Important areas include:

```text
AMI Security

Operating System Patching

Security Groups

IAM Roles

IMDSv2

EBS Encryption

Secrets Management

Logging and Monitoring
```

A basic EC2 security model is:

```text
Private EC2
   │
   ├── Least-Privilege Security Group
   ├── IAM Role
   ├── IMDSv2
   ├── Patched OS
   ├── Encrypted EBS
   └── Centralized Logging
```

---

## 3. EC2 Hardening Review

EC2 hardening reduces unnecessary attack surface.

Important controls include:

```text
Remove unnecessary services

Remove unnecessary packages

Restrict administrative access

Avoid public SSH / RDP

Use Systems Manager where appropriate

Patch the operating system

Protect local accounts

Use host firewalls

Collect system logs
```

A useful principle is:

```text
If it is not required,
remove or disable it.
```

---

## 4. EC2 Identity Security

Applications running on EC2 may need access to AWS services.

Poor design:

```text
EC2
 ↓
Hard-Coded Access Key
 ↓
AWS Service
```

Better:

```text
EC2
 ↓
IAM Role
 ↓
Temporary Credentials
 ↓
AWS Service
```

The IAM role should provide only the required permissions.

Example:

```text
Application
requires:

s3:GetObject

on:

arn:aws:s3:::application-data/*
```

It should not automatically receive:

```text
AdministratorAccess
```

---

## 5. EC2 Network Security

Network exposure should be minimized.

Risky:

```text
EC2
Public IP
+
TCP 22
0.0.0.0/0
```

Better architecture:

```text
Internet
   ↓
Application Load Balancer
   ↓
Private EC2
```

Administrative access may use:

```text
AWS Systems Manager
```

where appropriate.

This can reduce the need for direct inbound SSH or RDP.

---

## 6. EBS Security Review

Amazon EBS provides persistent block storage for EC2.

Sensitive data on EBS should be protected through encryption.

Conceptually:

```text
EC2
 ↓
Encrypted EBS
 ↓
AWS KMS
```

Encryption can protect:

```text
Root Volumes

Data Volumes

Snapshots

EBS Storage I/O
```

---

## 7. EBS and AWS KMS

EBS encryption uses AWS KMS.

Simplified model:

```text
KMS Key
   ↓
Protects Data Key
   ↓
Data Key
   ↓
Encrypts EBS Data
```

This is an example of:

```text
Envelope Encryption
```

The KMS key and EBS data key serve different purposes.

---

## 8. EBS Encryption by Default

EBS Encryption by Default helps prevent newly created unencrypted volumes.

Conceptually:

```text
New EBS Volume
      ↓
Encryption by Default
      ↓
Encrypted Volume
```

Important:

```text
Encryption by Default
≠
Automatic encryption of existing volumes
```

Existing unencrypted resources require a migration process.

---

## 9. EBS Snapshot Security

Snapshots can contain sensitive data.

Review:

```text
Is the snapshot encrypted?

Which KMS key protects it?

Who can access it?

Is it shared externally?

Is cross-account sharing required?
```

A secure backup architecture should protect both:

```text
Production Storage

and

Backup Storage
```

---

## 10. S3 Security Review

Amazon S3 stores objects inside buckets.

A basic S3 security model is:

```text
Application
    ↓
IAM Role
    ↓
Private S3 Bucket
    │
    ├── Block Public Access
    ├── Bucket Policy
    ├── Encryption
    ├── Versioning
    └── Lifecycle
```

S3 should generally be treated as:

```text
Private by Default
```

and access should be granted only when required.

---

## 11. S3 Access Control Review

Important S3 access controls include:

```text
IAM Policies

Bucket Policies

Block Public Access

Object Ownership

Access Points
```

A policy should answer:

```text
Who?
→ Principal

Can do what?
→ Action

To what?
→ Resource

Under what conditions?
→ Condition
```

Example:

```text
Application Role
→ s3:GetObject
→ Required Prefix Only
```

---

## 12. S3 Public Exposure

One of the most important S3 risks is unintended public access.

Risky architecture:

```text
Sensitive S3 Bucket
      ↓
Public Policy
      ↓
Internet
```

Controls include:

```text
Block Public Access

Least-Privilege Bucket Policy

IAM Access Analyzer

Policy Review
```

Public access should only exist when there is a documented requirement.

---

## 13. S3 Data Protection

S3 data protection includes:

```text
Encryption
Versioning
Lifecycle
Backup / Replication Strategy
```

Versioning can help recover from:

```text
Accidental deletion

Accidental overwrite

Certain destructive actions
```

Encryption protects stored data, but does not replace access control.

```text
Encryption
+
Access Control
```

are both required.

---

## 14. RDS Security Review

Amazon RDS is a managed relational database service.

AWS manages more of the underlying infrastructure than with a database installed directly on EC2.

However, the customer still manages:

```text
Network Access

Database Users

Database Privileges

Encryption

Authentication

Backup Requirements

Logging

Monitoring
```

---

## 15. RDS Network Security

A common secure architecture is:

```text
Internet
   ↓
Load Balancer
   ↓
Private Application
   ↓
Private RDS
```

Database Security Group:

```text
PostgreSQL:
TCP 5432
Source: APP-SG
```

or:

```text
MySQL:
TCP 3306
Source: APP-SG
```

The database generally does not need:

```text
0.0.0.0/0
```

access.

---

## 16. AWS IAM vs Database Permissions

These are separate authorization layers.

```text
AWS IAM
→ Manage AWS RDS resources
```

Examples:

```text
rds:DescribeDBInstances

rds:ModifyDBInstance
```

Database permissions control:

```text
SELECT

INSERT

UPDATE

DELETE
```

An IAM administrator does not automatically receive database table permissions.

This distinction is important when troubleshooting database access.

---

## 17. Database Credential Security

Poor design:

```text
Application
 ↓
Hard-Coded Database Password
 ↓
RDS
```

Better approaches include:

```text
Application
 ↓
IAM Role
 ↓
Secrets Manager
 ↓
Database Credentials
```

or, where supported and appropriate:

```text
Application
 ↓
IAM DB Authentication
 ↓
Temporary Authentication Token
 ↓
RDS
```

Database privileges should still follow least privilege.

---

## 18. RDS Data Protection

Important controls include:

```text
Encryption at Rest

TLS in Transit

Encrypted Snapshots

Automated Backups

Backup Retention

Deletion Protection
```

Conceptually:

```text
Application
   │
   │ TLS
   ↓
Encrypted RDS
   ↓
Encrypted Backup
```

Encryption should protect both active data and recovery data.

---

## 19. Multi-AZ vs Backup

Multi-AZ and backups solve different problems.

### Multi-AZ

```text
Primary
   ↓
Standby
```

Main purpose:

```text
Availability
Failover
Resilience
```

### Backup

Main purpose:

```text
Data Recovery
Point-in-Time Recovery
Historical Restore
```

Therefore:

```text
Multi-AZ
≠
Backup
```

Both may be required.

---

## 20. Security Responsibility Comparison

| Area | EC2 | S3 | EBS | RDS |
|---|---|---|---|---|
| OS Hardening | Customer | N/A | N/A | AWS manages underlying OS |
| IAM | Customer | Customer | Customer | Customer |
| Network Access | Customer | Customer | Primarily through EC2 | Customer |
| Encryption | Customer configures | Customer configures | Customer configures | Customer configures |
| Patch OS | Customer | AWS | AWS | AWS manages infrastructure |
| Data Access | Customer | Customer | Customer | Customer |
| Backup Strategy | Customer | Customer | Customer | Shared / customer configures |
| Logging | Customer | Customer | Customer | Customer configures relevant logs |

The exact responsibility depends on the specific feature and configuration.

---

## 21. Defense in Depth

A secure AWS workload should not depend on one security control.

Example:

```text
Internet
   ↓
Load Balancer
   ↓
Security Group
   ↓
Private EC2
   ↓
IAM Role
   ↓
Private S3 / RDS
   ↓
Encrypted Storage
   ↓
Logging and Monitoring
```

Security layers may include:

```text
Identity

Network

Operating System

Application

Storage

Encryption

Backup

Logging

Monitoring
```

This is:

```text
Defense in Depth
```

---

## 22. Example Secure Application Architecture

```text
                         Internet
                             │
                             ↓
                  Application Load Balancer
                             │
                        ALB-SG
                             │
                             ↓
                     Private EC2
                             │
              ┌──────────────┼──────────────┐
              │              │              │
              ↓              ↓              ↓
           APP-SG         IAM Role       Encrypted EBS
              │              │
              │              ├────→ S3
              │              │
              │              └────→ Secrets Manager
              │
              ↓
          Private RDS
              │
            DB-SG
              │
              ↓
          KMS Encryption
```

Supporting controls:

```text
S3
├── Block Public Access
├── Versioning
└── Encryption

RDS
├── Automated Backups
├── Encryption
├── TLS
└── Deletion Protection

EC2
├── IMDSv2
├── Patching
└── Systems Manager
```

---

## 23. Threat Scenario — Compromised EC2

Suppose an attacker exploits an application running on EC2.

Potential path:

```text
Application Vulnerability
        ↓
EC2 Compromise
        ↓
IAM Role Credentials
        ↓
AWS Resources
```

Impact depends heavily on:

```text
IAM Role Permissions
```

If the role has:

```text
AdministratorAccess
```

the impact can be severe.

If the role only has:

```text
s3:GetObject
on one required prefix
```

the potential cloud-side impact is much smaller.

This demonstrates the importance of least privilege.

---

## 24. Threat Scenario — Exposed S3 Bucket

Scenario:

```text
Bucket Policy
     ↓
Public Read
     ↓
Sensitive Data Exposure
```

Review:

```text
Block Public Access

Bucket Policy

IAM Policies

Access Analyzer

Data Classification
```

The correct response is not simply to encrypt the bucket.

Encryption does not fix excessive authorization.

---

## 25. Threat Scenario — Database Credential Leak

Scenario:

```text
GitHub
  ↓
Hard-Coded DB Password
  ↓
Attacker
  ↓
RDS
```

Risk can be reduced through:

```text
Secrets Manager

Credential Rotation

Private RDS

Security Group Restrictions

Least-Privilege DB User
```

A leaked credential is less useful if network and privilege controls also limit its use.

---

## 26. Threat Scenario — Lost EBS Snapshot

Scenario:

```text
EBS Snapshot
     ↓
Incorrect Sharing
     ↓
External Account
```

Review:

```text
Snapshot Permissions

Encryption

KMS Key Policy

Cross-Account Access
```

Backup data requires the same security attention as production data.

---

## 27. Common Security Anti-Patterns

### Anti-Pattern 1

```text
AdministratorAccess
everywhere
```

Better:

```text
Least Privilege
```

### Anti-Pattern 2

```text
0.0.0.0/0
on management or database ports
```

Better:

```text
Required Sources Only
```

### Anti-Pattern 3

```text
Hard-Coded Credentials
```

Better:

```text
IAM Roles
Secrets Manager
Temporary Credentials
```

### Anti-Pattern 4

```text
Unencrypted Sensitive Storage
```

Better:

```text
KMS-backed Encryption
```

### Anti-Pattern 5

```text
No Backup / Recovery Testing
```

Better:

```text
Backup
+
Restore Testing
```

### Anti-Pattern 6

```text
Security Without Logging
```

Better:

```text
Prevent
+
Detect
+
Respond
```

---

## 28. Security Review Method

When reviewing an AWS workload, use a consistent order.

### Step 1 — Understand the Architecture

```text
What services are used?
```

### Step 2 — Identify Data

```text
What sensitive data exists?
```

### Step 3 — Review Identity

```text
Who can access each resource?
```

### Step 4 — Review Network

```text
Which network paths exist?
```

### Step 5 — Review Encryption

```text
Is data protected at rest and in transit?
```

### Step 6 — Review Recovery

```text
Can the workload recover from deletion or failure?
```

### Step 7 — Review Logging

```text
Can important actions be investigated?
```

### Step 8 — Review Monitoring

```text
Can suspicious or abnormal behavior be detected?
```

---

## 29. Troubleshooting Security Access

A useful troubleshooting model is:

```text
Identity
   ↓
Permission
   ↓
Network Path
   ↓
Security Control
   ↓
Service Configuration
   ↓
Encryption / KMS
   ↓
Application
```

Example:

```text
EC2 cannot read S3 object
```

Check:

```text
IAM Role

s3:GetObject

Bucket Policy

Object ARN

KMS Permission

Network Path / VPC Endpoint

Application Configuration
```

---

## 30. Troubleshooting RDS Connectivity

Problem:

```text
Application cannot connect to RDS.
```

Check:

```text
Application
   ↓
DNS / Endpoint
   ↓
Route
   ↓
Security Group
   ↓
Database Port
   ↓
TLS
   ↓
Authentication
   ↓
Database Privileges
```

Do not immediately open the database Security Group to:

```text
0.0.0.0/0
```

just to make the connection work.

---

## 31. Logging Review

Different logs answer different questions.

### CloudTrail

```text
Who changed the AWS resource?
```

Examples:

```text
Modified Security Group

Deleted Snapshot

Changed Bucket Policy

Modified RDS
```

### Operating System Logs

```text
What happened inside EC2?
```

### Database Logs

```text
What happened inside RDS?
```

### VPC Flow Logs

```text
What network communication occurred?
```

A complete investigation may require multiple log sources.

---

## 32. Hands-on Architecture Review

For today's practice, design or review this architecture:

```text
Internet
   ↓
ALB
   ↓
Private EC2
   ↓
Private RDS

Private EC2
   ↓
Amazon S3
```

For each component, document:

```text
Identity Control

Network Control

Encryption

Backup / Recovery

Logging

Monitoring
```

Example:

| Resource | Identity | Network | Data | Recovery |
|---|---|---|---|---|
| EC2 | IAM Role | APP-SG | Encrypted EBS | AMI / Snapshot |
| S3 | IAM + Bucket Policy | Private access | S3 Encryption | Versioning |
| EBS | IAM/KMS | Attached through EC2 | KMS Encryption | Snapshot |
| RDS | IAM / DB User | DB-SG | KMS + TLS | Backup / Snapshot |

---

## 33. Optional Security Review Exercise

Find at least one security risk in each configuration.

### Scenario A

```text
EC2
Public IP

SSH:
0.0.0.0/0

IAM Role:
AdministratorAccess
```

Issues:

```text
Excessive network exposure

Excessive IAM permissions
```

---

### Scenario B

```text
S3 Bucket

Block Public Access:
Disabled

Bucket Policy:
Principal "*"

Action:
s3:GetObject
```

Issue:

```text
Potential public data exposure
```

---

### Scenario C

```text
RDS PostgreSQL

Publicly Accessible:
Yes

Security Group:
TCP 5432
0.0.0.0/0
```

Issue:

```text
Database exposed directly to the Internet
```

---

### Scenario D

```text
EBS Volume

Sensitive Data

Encrypted:
No
```

Issue:

```text
Sensitive persistent storage is unencrypted
```

---

## 34. Phase 3 Security Checklist

### EC2

```text
[ ] Public exposure is minimized
[ ] Security Groups follow least privilege
[ ] IAM role follows least privilege
[ ] IMDSv2 is used where appropriate
[ ] OS and applications are patched
[ ] Administrative access is restricted
[ ] EBS volumes are encrypted
[ ] Logs and monitoring are configured
```

### S3

```text
[ ] Block Public Access is configured
[ ] IAM permissions are least-privilege
[ ] Bucket policies are reviewed
[ ] Public access is intentional
[ ] Encryption is enabled
[ ] Versioning is considered
[ ] Lifecycle and retention are appropriate
[ ] External access is reviewed
```

### EBS

```text
[ ] Sensitive volumes are encrypted
[ ] Encryption by Default is reviewed
[ ] Correct KMS keys are used
[ ] Snapshots are encrypted
[ ] Snapshot sharing is restricted
[ ] KMS key dependencies are documented
```

### RDS

```text
[ ] Public accessibility is disabled unless required
[ ] DB Security Group is restricted
[ ] Database users follow least privilege
[ ] Credentials are securely managed
[ ] Encryption at rest is enabled
[ ] TLS is used where required
[ ] Backups are configured
[ ] Deletion protection is considered
[ ] Database logs are configured
[ ] Monitoring is enabled
```

---

## Key Takeaways

- Compute and storage security requires multiple security layers.
- EC2 requires strong OS, network, identity, and storage security.
- IAM roles are preferable to hard-coded AWS credentials.
- EBS encryption protects persistent EC2 storage.
- S3 should generally remain private unless public access is explicitly required.
- S3 Block Public Access provides an important public-exposure guardrail.
- S3 encryption does not replace authorization controls.
- RDS should normally use private network connectivity for internal workloads.
- AWS IAM permissions and database privileges are separate authorization layers.
- Multi-AZ provides availability, while backups provide data recovery.
- Encryption should protect both production data and backup data.
- Least privilege applies to IAM, networking, databases, and KMS.
- Logging and monitoring are required for investigation and detection.
- Secure AWS architecture should follow defense-in-depth principles.

---

## Reflection

During this phase, I learned that cloud security cannot be achieved by enabling one security feature.

EC2, S3, EBS, and RDS each have different security models, but they share common security principles.

Identity should follow least privilege, network exposure should be minimized, sensitive data should be encrypted, credentials should be managed securely, backups should be protected, and important activity should be logged and monitored.

I also learned that managed AWS services reduce some infrastructure responsibilities but do not remove the customer's responsibility for access control, data protection, and secure configuration.

The most important lesson from this phase is to evaluate AWS workloads as complete architectures rather than isolated services.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Attack Surface | The set of points that could potentially be attacked |
| Data at Rest | Data stored on persistent storage |
| Data in Transit | Data moving across a network |
| Data Protection | Controls that protect the confidentiality and integrity of data |
| Defense in Depth | Using multiple independent security layers |
| Least Privilege | Granting only the permissions necessary for a task |
| Recovery | Restoring a service or data after failure or loss |
| Security Posture | The overall security condition of a system or environment |
