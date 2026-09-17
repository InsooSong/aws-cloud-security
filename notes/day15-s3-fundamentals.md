# Day 15 — Amazon S3 Fundamentals

## Topic

Amazon S3 Fundamentals and Object Storage Architecture

---

## Objectives

- Understand what Amazon S3 is
- Understand the difference between object and block storage
- Learn the relationship between buckets, objects, and keys
- Understand basic S3 object operations
- Learn how S3 object URLs and prefixes work
- Understand S3 Versioning
- Learn the purpose of S3 storage classes
- Understand basic S3 encryption concepts
- Understand basic S3 access control concepts
- Identify common S3 security risks
- Build a security-focused mental model for S3

---

## 1. What is Amazon S3?

Amazon Simple Storage Service (Amazon S3) is an object storage service.

S3 stores data as objects inside buckets.

Conceptually:

```text
Amazon S3
   ↓
Bucket
   ↓
Object
```

Examples of data stored in S3 include:

- Images
- Documents
- Application files
- Backups
- Log files
- Videos
- Static website files
- Security logs
- Data lake objects

---

## 2. Object Storage

S3 uses an object storage model.

An object typically consists of:

```text
Object
│
├── Data
├── Key
└── Metadata
```

Unlike a traditional file system, S3 does not operate as a normal directory-based disk.

Instead, each object is identified by a unique key inside a bucket.

---

## 3. Object Storage vs Block Storage

Amazon S3 and Amazon EBS solve different storage problems.

### Amazon S3

```text
Object Storage
```

Common use cases:

- Backups
- Documents
- Logs
- Static files
- Data lakes
- Archives

### Amazon EBS

```text
Block Storage
```

Common use cases:

- EC2 operating system disk
- Application disk
- Database storage

A simple comparison:

| Amazon S3 | Amazon EBS |
|---|---|
| Object storage | Block storage |
| Accessed through APIs | Attached to compute resources |
| Stores objects | Stores blocks |
| Very large-scale storage | Disk-like storage for EC2 |
| Common for files, logs, backups | Common for OS and application disks |

---

## 4. S3 Bucket

A bucket is a container for S3 objects.

Conceptually:

```text
S3
└── Bucket
    ├── Object A
    ├── Object B
    └── Object C
```

Example:

```text
security-training-bucket
```

A bucket can contain many objects.

---

## 5. Bucket Naming

S3 bucket names must follow AWS naming requirements.

Bucket names are globally unique within the relevant S3 namespace.

Examples:

```text
company-security-logs

application-backups-2026

cloud-security-training
```

Bucket names should not contain sensitive information.

Avoid names such as:

```text
customer-password-backups

confidential-merger-files
```

because bucket names may appear in URLs, logs, or configuration.

---

## 6. S3 Object

An object is the actual data stored in S3.

Example:

```text
report.pdf

image.jpg

security.log

backup.tar.gz
```

Each object has:

```text
Data

Key

Metadata
```

and may also have properties such as:

```text
Version ID

Storage Class

Encryption Information

Tags
```

---

## 7. Object Key

An object key uniquely identifies an object inside a bucket.

Example:

```text
logs/2026/09/security.log
```

The full logical structure is:

```text
Bucket:
company-security-logs

Key:
logs/2026/09/security.log
```

Together:

```text
s3://company-security-logs/logs/2026/09/security.log
```

---

## 8. Prefixes

S3 does not use traditional folders in the same way as a normal file system.

However, keys can use prefixes that look like directories.

Example:

```text
logs/
logs/2026/
logs/2026/09/
logs/2026/09/security.log
```

Conceptually:

```text
Bucket
│
└── logs/
    └── 2026/
        └── 09/
            └── security.log
```

The console presents these prefixes in a folder-like interface.

---

## 9. Example S3 Structure

```text
security-data
│
├── logs/
│   ├── cloudtrail/
│   └── application/
│
├── reports/
│   ├── monthly/
│   └── incident/
│
└── backups/
    ├── database/
    └── configuration/
```

These appear as folders, but the underlying model is based on object keys and prefixes.

---

## 10. Basic S3 Operations

Common S3 actions include:

```text
PutObject

GetObject

DeleteObject

ListBucket
```

Conceptually:

```text
Upload Object
→ PutObject

Download Object
→ GetObject

Delete Object
→ DeleteObject

List Objects
→ ListBucket
```

These API actions are also used when defining IAM permissions.

---

## 11. Bucket vs Object Permissions

Bucket-level and object-level operations can require different permissions.

Example:

```text
s3:ListBucket
```

applies to the bucket.

Example:

```text
s3:GetObject
```

applies to objects.

Conceptually:

```text
Bucket
→ ListBucket

Object
→ GetObject
→ PutObject
→ DeleteObject
```

This distinction becomes important when designing IAM and bucket policies.

---

## 12. S3 ARN Examples

Bucket ARN:

```text
arn:aws:s3:::example-bucket
```

Object ARN:

```text
arn:aws:s3:::example-bucket/*
```

These represent different resource scopes.

Example policy concept:

```text
ListBucket
→ Bucket ARN

GetObject
→ Object ARN
```

---

## 13. S3 and AWS Regions

S3 buckets are created in an AWS Region.

Example:

```text
ap-northeast-1
→ Tokyo
```

Region selection can affect:

- Data residency
- Compliance
- Latency
- Architecture
- Disaster recovery

The bucket name identifies the bucket, while the bucket itself belongs to a selected AWS Region.

---

## 14. S3 Durability and Availability

S3 is designed for highly durable object storage.

However, durability and security are different concepts.

A durable object can still be:

```text
Accidentally Deleted

Publicly Exposed

Incorrectly Authorized

Overwritten

Encrypted with Incorrect Key Policies
```

Therefore:

```text
Durability
≠
Security
```

S3 security still requires proper access control, versioning, encryption, and monitoring.

---

## 15. S3 Versioning

S3 Versioning allows multiple versions of the same object to be retained.

Without versioning:

```text
report.txt
   ↓
Upload new report.txt
   ↓
Previous object replaced
```

With versioning:

```text
report.txt
│
├── Version 1
├── Version 2
└── Version 3
```

This can help protect against accidental overwrite or deletion.

---

## 16. Version ID

When versioning is enabled, objects receive version IDs.

Conceptually:

```text
report.txt

Version ID:
A

Version ID:
B

Version ID:
C
```

A specific version can be retrieved if needed.

This provides recovery options.

---

## 17. Delete Marker

In a versioning-enabled bucket, deleting an object normally creates a delete marker rather than immediately destroying every previous version.

Conceptually:

```text
Object
│
├── Version 1
├── Version 2
└── Delete Marker
```

The object appears deleted in normal requests, but older versions may still exist.

This can help recover accidentally deleted objects.

---

## 18. Versioning Security Benefits

Versioning can help reduce the impact of:

- Accidental deletion
- Accidental overwrite
- Application errors
- Some destructive security incidents

Example:

```text
Attacker / User
      ↓
Overwrite Object
      ↓
Old Version Still Available
```

However:

```text
Versioning
≠
Backup Strategy by itself
```

Additional controls may still be required.

---

## 19. S3 Storage Classes

S3 provides different storage classes for different access patterns.

Common examples include:

```text
S3 Standard

S3 Intelligent-Tiering

S3 Standard-IA

S3 One Zone-IA

S3 Glacier Instant Retrieval

S3 Glacier Flexible Retrieval

S3 Glacier Deep Archive
```

Each storage class has different characteristics related to:

- Cost
- Access frequency
- Retrieval time
- Availability
- Minimum storage duration

---

## 20. S3 Standard

S3 Standard is commonly used for frequently accessed data.

Example workloads:

```text
Application Data

Frequently Accessed Files

Web Content

Active Logs
```

It is the default storage class for many S3 objects.

---

## 21. S3 Intelligent-Tiering

S3 Intelligent-Tiering is designed for data with changing or unpredictable access patterns.

Conceptually:

```text
Object
   ↓
Access Pattern Changes
   ↓
Automatic Tier Optimization
```

This can help optimize storage costs without manually predicting access frequency.

---

## 22. Infrequent Access Classes

Examples:

```text
S3 Standard-IA

S3 One Zone-IA
```

These are designed for data accessed less frequently.

Potential examples:

```text
Backups

Older Reports

Recovery Data
```

The correct class depends on durability, availability, access, and cost requirements.

---

## 23. S3 Glacier Classes

Glacier storage classes are commonly used for archive workloads.

Examples:

```text
Glacier Instant Retrieval

Glacier Flexible Retrieval

Glacier Deep Archive
```

Potential use cases:

```text
Long-Term Backups

Compliance Archives

Historical Logs

Old Security Data
```

Retrieval characteristics differ by class.

---

## 24. Lifecycle Management

S3 Lifecycle rules can automatically move or expire objects.

Example:

```text
Day 0
S3 Standard

     ↓

Day 30
Standard-IA

     ↓

Day 90
Glacier

     ↓

Day 365
Delete
```

This can help manage large amounts of data automatically.

Lifecycle design should consider both cost and retention requirements.

---

## 25. Security Log Retention Example

Example security log lifecycle:

```text
Recent Logs
→ S3 Standard

Older Logs
→ Glacier

Long-Term Archive
→ Deep Archive
```

This can reduce storage cost while preserving data required for investigations or compliance.

---

## 26. S3 Encryption

S3 supports encryption for stored objects.

Conceptually:

```text
Object
   ↓
Encryption
   ↓
Stored Data
```

Encryption protects data at rest.

Common S3 server-side encryption options include:

```text
SSE-S3

SSE-KMS
```

Different encryption methods provide different levels of key management and control.

---

## 27. SSE-S3

With SSE-S3:

```text
S3
 ↓
AWS Managed S3 Encryption
 ↓
Object
```

AWS manages the encryption keys used by S3.

This provides server-side encryption without requiring the customer to manage individual encryption keys.

---

## 28. SSE-KMS

With SSE-KMS:

```text
S3
 ↓
AWS KMS
 ↓
KMS Key
 ↓
Encrypted Object
```

SSE-KMS provides additional key management and access control options.

It can also provide additional auditing capabilities through AWS KMS and CloudTrail.

KMS will be studied in more detail later.

---

## 29. Encryption in Transit

Data transferred to and from S3 should use secure transport.

Conceptually:

```text
Client
   ↓
HTTPS / TLS
   ↓
Amazon S3
```

This protects data in transit.

Security therefore includes both:

```text
At Rest
+
In Transit
```

---

## 30. Basic S3 Access Control

S3 access can be controlled through multiple mechanisms.

Examples include:

```text
IAM Policies

Bucket Policies

Block Public Access

Access Points

ACLs
```

Modern S3 security design generally emphasizes IAM and bucket policies while minimizing unnecessary ACL use.

Access control will be studied in detail on Day 16.

---

## 31. IAM Policy

IAM policies can define what an identity can do with S3.

Example:

```text
IAM Role
   ↓
s3:GetObject
   ↓
Specific Bucket
```

Example:

```text
Application
→ Read only required objects
```

rather than:

```text
Application
→ s3:*
→ *
```

Least privilege should be applied.

---

## 32. Bucket Policy

A bucket policy is a resource-based policy attached directly to an S3 bucket.

Conceptually:

```text
S3 Bucket
   ↓
Bucket Policy
   ↓
Who can access?
What actions?
Under what conditions?
```

Bucket policies can be used for:

- Cross-account access
- Service access
- Security conditions
- Resource-level restrictions

---

## 33. Block Public Access

Amazon S3 provides Block Public Access settings.

Conceptually:

```text
Public Access Configuration
        ↓
Block Public Access
        ↓
Prevent Unintended Public Exposure
```

For most private data:

```text
Block Public Access
→ Enabled
```

should be the expected starting point.

---

## 34. Public S3 Exposure

A major S3 security risk is unintended public access.

Example:

```text
Sensitive Bucket
     ↓
Public Policy
     ↓
Internet
```

Possible exposed data:

- Customer information
- Backups
- Logs
- Credentials
- Internal documents

Public access should only exist when there is a specific requirement.

---

## 35. New Bucket Security Defaults

New S3 buckets are designed with restrictive public access defaults.

A useful security mindset is:

```text
Private by Default
      ↓
Grant Only Required Access
```

rather than:

```text
Public First
      ↓
Try to Restrict Later
```

Secure defaults help reduce accidental exposure.

---

## 36. Object Ownership

S3 also has object ownership settings that determine how ownership and ACL behavior work.

A modern S3 architecture commonly avoids relying heavily on ACL-based permission management.

Conceptually:

```text
Centralized Policy-Based Access
```

is usually easier to manage than:

```text
Many Individual Object ACLs
```

Object Ownership and ACL behavior will be studied further on Day 16.

---

## 37. Common Misconfiguration — Public Bucket

Risky:

```text
Sensitive Data
+
Public Bucket Policy
```

Example result:

```text
Anonymous Internet User
→ Read Objects
```

Public exposure should be reviewed carefully.

---

## 38. Common Misconfiguration — Broad IAM Permission

Risky:

```text
Action:
s3:*

Resource:
*
```

This may allow far more access than required.

Better:

```text
Required Actions
+
Required Bucket
+
Required Objects
```

Example:

```text
s3:GetObject

arn:aws:s3:::application-data/*
```

---

## 39. Common Misconfiguration — No Versioning

For important data:

```text
No Versioning
```

can increase the impact of accidental overwrites or deletions.

Versioning can provide an additional recovery mechanism.

---

## 40. Common Misconfiguration — Poor Lifecycle Design

Example:

```text
Security Logs
→ Deleted after 7 days
```

when the organization needs:

```text
1 Year Investigation History
```

Lifecycle policies should match:

- Security requirements
- Compliance requirements
- Recovery requirements
- Cost requirements

---

## 41. Common Misconfiguration — Sensitive Bucket Name

Avoid placing sensitive information directly in bucket names.

Poor example:

```text
company-secret-acquisition-project
```

Better:

```text
project-data-prod-01
```

Bucket naming should avoid unnecessarily exposing business context.

---

## 42. S3 Security Layers

A useful S3 security model is:

```text
Identity
   ↓
IAM

Resource Access
   ↓
Bucket Policy

Public Exposure
   ↓
Block Public Access

Data Protection
   ↓
Encryption

Data Recovery
   ↓
Versioning

Retention
   ↓
Lifecycle

Visibility
   ↓
Logging / Monitoring
```

---

## 43. Example Secure S3 Architecture

```text
Application
    ↓
IAM Role
    ↓
Private S3 Bucket
    │
    ├── Block Public Access
    ├── Versioning
    ├── Encryption
    └── Lifecycle Policy
```

This combines several security and operational controls.

---

## 44. S3 Security Questions

When reviewing an S3 bucket, ask:

```text
What data is stored here?

Who needs access?

Is public access required?

Is Block Public Access enabled?

Which IAM policies allow access?

Does a bucket policy exist?

Is versioning enabled?

Is encryption enabled?

How long should objects be retained?

Are old objects archived or deleted appropriately?

Does the bucket contain sensitive data?
```

---

## 45. Hands-on Practice

For today's practice, open the Amazon S3 console.

Review:

```text
Buckets

Objects

Properties

Permissions

Management
```

For one test bucket or the bucket creation workflow, identify:

```text
Bucket Name

AWS Region

Object Ownership

Block Public Access

Versioning

Default Encryption

Lifecycle Configuration
```

Do not enable public access for practice unless there is a specific need.

---

## 46. Optional Practice

Create a test bucket with a non-sensitive name.

Example:

```text
cloud-security-lab-<unique-value>
```

Review the default settings.

Check:

```text
Block Public Access

Object Ownership

Versioning

Encryption
```

Upload a non-sensitive test file.

Example:

```text
test.txt
```

Then identify:

```text
Bucket

Object Key

Object Size

Storage Class

Encryption
```

Delete test resources when they are no longer required.

---

## Security Checklist

When reviewing an S3 bucket, I should ask:

```text
Is the bucket public?

Is public access actually required?

Is Block Public Access enabled?

Are IAM permissions least-privilege?

Does the bucket policy contain broad access?

Is versioning required?

Is encryption enabled?

Is HTTPS used for data transfer?

Are lifecycle rules appropriate?

Are retention requirements defined?

Are old versions managed?

Does the bucket name expose sensitive information?

Are important objects recoverable after accidental deletion?
```

---

## Key Takeaways

- Amazon S3 is an object storage service.
- S3 stores objects inside buckets.
- Each object is identified by a key.
- Prefixes provide folder-like organization but are part of the object key.
- Bucket-level and object-level operations use different permissions.
- S3 Versioning preserves multiple versions of objects.
- Versioning can help recover from accidental deletion or overwrite.
- Storage classes support different access and cost requirements.
- Lifecycle rules automate object transitions and expiration.
- S3 supports encryption at rest and secure transport in transit.
- IAM policies and bucket policies control S3 access.
- Block Public Access helps prevent unintended public exposure.
- Least privilege should be applied to S3 permissions.
- S3 security requires access control, encryption, recovery, retention, and monitoring.

---

## Reflection

Today I learned that Amazon S3 is based on an object storage model rather than a traditional file system.

Objects are stored inside buckets and identified by unique keys. Prefixes may look like directories, but they are part of the object naming structure.

I also learned that S3 security is not only about whether a bucket is public or private.

Versioning can improve recoverability, encryption protects stored data, lifecycle rules help manage retention, and IAM and bucket policies define who can access the data.

From a security perspective, the default approach should be to keep S3 data private and grant only the minimum access required.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Bucket | A container used to store objects in Amazon S3 |
| Lifecycle | Rules that automatically transition or expire S3 objects |
| Object | Data stored in S3 together with its key and metadata |
| Object Key | The unique identifier of an object inside a bucket |
| Object Storage | A storage model that stores data as individually identified objects |
| Prefix | A portion of an object key used to organize objects |
| Storage Class | A storage tier designed for a particular access pattern |
| Versioning | A feature that preserves multiple versions of an object |
