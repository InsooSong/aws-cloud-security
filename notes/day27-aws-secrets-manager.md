# Day 27 — AWS Secrets Manager

## Topic

AWS Secrets Manager Fundamentals, Rotation, Versioning, Resource Policies, and Secure Secret Access

---

## Objectives

- Understand the purpose of AWS Secrets Manager
- Understand how secrets are stored and encrypted
- Learn how IAM controls access to secrets
- Understand secret versions and staging labels
- Learn how automatic rotation works
- Understand managed rotation and Lambda-based rotation
- Learn how Secrets Manager integrates with AWS KMS
- Understand resource-based policies
- Understand cross-account secret access
- Review RDS credential management
- Compare Secrets Manager and Systems Manager Parameter Store
- Identify common secrets management misconfigurations

---

# Secrets Manager Fundamentals

## 1. What Is AWS Secrets Manager?

AWS Secrets Manager is a managed service for storing and managing sensitive credentials and secrets.

Examples include:

```text
Database Passwords

API Keys

OAuth Tokens

Private Keys

Application Credentials
```

Conceptually:

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
Secret Value
```

Secrets Manager helps reduce the need to store credentials directly inside:

```text
Source Code

Configuration Files

Environment Files

AMI Images

Git Repositories
```

---

## 2. Why Secrets Management Matters

Poor design:

```text
Application
    |
    v
Hard-Coded Password
    |
    v
Source Code
```

Risks include:

```text
Credential Leakage

Git Exposure

Unauthorized Access

Difficult Rotation

Operational Errors
```

Better:

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
Retrieve Secret at Runtime
```

This separates:

```text
Application Code

from

Sensitive Credentials
```

---

## 3. Secret Structure

A Secrets Manager secret can contain:

```text
Secret Name

Secret Value

Versions

Staging Labels

KMS Encryption

Resource Policy

Tags

Rotation Configuration
```

Example secret value:

```json
{
  "username": "app_user",
  "password": "example-password"
}
```

Real secret values should never be committed to GitHub.

---

## 4. Secret Value Formats

Secrets can store:

```text
Plain String

or

JSON Key-Value Structure
```

Example:

```json
{
  "username": "security_app",
  "password": "example",
  "host": "database.example.internal",
  "port": 5432
}
```

JSON format can make it easier for applications to retrieve multiple related values.

---

# Encryption

## 5. Secrets Manager and AWS KMS

Secrets Manager encrypts stored secret values using AWS KMS.

Conceptually:

```text
Secret
   |
   v
Secrets Manager
   |
   v
AWS KMS
   |
   v
Encrypted Secret
```

A secret can use:

```text
AWS Managed KMS Key

or

Customer Managed KMS Key
```

---

## 6. AWS Managed Key

Secrets Manager can use the AWS managed key:

```text
aws/secretsmanager
```

This is convenient for standard same-account use cases.

Conceptually:

```text
Secret
   |
   v
aws/secretsmanager
```

The customer does not directly manage the key policy.

---

## 7. Customer Managed KMS Key

A customer managed key may be useful when requirements include:

```text
Custom Key Policies

Cross-Account Access

Stronger Separation of Duties

More Granular Access Control
```

Conceptually:

```text
Secrets Manager
      |
      v
Customer Managed KMS Key
      |
      v
Secret Encryption
```

The application may require both:

```text
Secrets Manager Permission

+

KMS Permission
```

depending on the configuration.

---

# IAM Access

## 8. Secret Access with IAM

Applications should access secrets using IAM roles.

Example:

```text
EC2 Application
      |
      v
IAM Role
      |
      v
secretsmanager:GetSecretValue
      |
      v
Specific Secret
```

Poor:

```text
secretsmanager:*
Resource: *
```

Better:

```text
secretsmanager:GetSecretValue
Resource:
Specific Secret ARN
```

---

## 9. Example IAM Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "arn:aws:secretsmanager:ap-northeast-1:111122223333:secret:prod/database/example-*"
    }
  ]
}
```

This allows read access to a specific secret.

It does not automatically allow:

```text
DeleteSecret

UpdateSecret

RotateSecret
```

---

## 10. Least Privilege

A good secrets policy should define:

```text
Who?

Which Secret?

Which Action?

Under What Conditions?
```

Example:

```text
ApplicationRole

can:

GetSecretValue

only for:

ProductionDatabaseSecret
```

Not:

```text
All Roles

All Secrets

All Secrets Manager Actions
```

---

# Secret Versions

## 11. Secret Versioning

When a secret value changes, Secrets Manager creates a new version.

Conceptually:

```text
Secret
│
├── Version A
├── Version B
└── Version C
```

Secrets Manager uses staging labels to identify important versions.

---

## 12. AWSCURRENT

`AWSCURRENT` identifies the current active secret version.

Conceptually:

```text
Secret
│
├── Version A
│
└── Version B
      |
      └── AWSCURRENT
```

By default:

```text
GetSecretValue
```

returns the version labeled:

```text
AWSCURRENT
```

---

## 13. AWSPREVIOUS

When the current value changes, the previous active version can receive:

```text
AWSPREVIOUS
```

Example:

```text
Version A
→ AWSPREVIOUS

Version B
→ AWSCURRENT
```

This can help with troubleshooting or rollback scenarios.

---

## 14. AWSPENDING

During rotation, the new candidate version uses:

```text
AWSPENDING
```

Conceptually:

```text
Old Credential
→ AWSCURRENT

New Candidate
→ AWSPENDING
```

After successful rotation:

```text
New Candidate
→ AWSCURRENT
```

and the previous version becomes:

```text
AWSPREVIOUS
```

---

## 15. Version Flow

A useful model:

```text
Before Rotation

Version A
→ AWSCURRENT


During Rotation

Version A
→ AWSCURRENT

Version B
→ AWSPENDING


After Rotation

Version A
→ AWSPREVIOUS

Version B
→ AWSCURRENT
```

This makes credential transitions safer.

---

# Rotation

## 16. What Is Secret Rotation?

Rotation means periodically replacing a secret value.

Example:

```text
Old Password
     |
     v
Rotation
     |
     v
New Password
```

A complete rotation should update both:

```text
Secrets Manager

and

Target Service
```

Example:

```text
Database Password
```

must change in both the database and Secrets Manager.

---

## 17. Why Rotation Matters

Long-lived credentials increase risk.

Example:

```text
Credential Leaked
     |
     v
Still Valid for Years
```

Rotation reduces the useful lifetime of exposed credentials.

Conceptually:

```text
Credential Compromise
      |
      v
Rotation
      |
      v
Old Credential Invalid
```

Rotation does not replace proper access control, but it reduces credential exposure duration.

---

## 18. Automatic Rotation

Secrets Manager supports automatic rotation.

Conceptually:

```text
Secret
   |
   v
Rotation Schedule
   |
   v
Generate New Credential
   |
   v
Update Target Service
   |
   v
Update Secret Version
```

Rotation schedules can use:

```text
rate()

or

cron()
```

expressions.

---

## 19. Rotation Frequency

Rotation frequency depends on security and operational requirements.

Examples:

```text
Every 30 Days

Every 7 Days

Every Few Hours
```

Secrets Manager supports rotation schedules as frequently as every four hours.

More frequent rotation is not automatically better.

Consider:

```text
Application Compatibility

Database Connection Behavior

Operational Complexity

Availability
```

---

# Managed Rotation

## 20. Managed Rotation

Some AWS services support managed rotation.

Conceptually:

```text
Secrets Manager
      |
      v
AWS Managed Service Integration
      |
      v
Credential Rotation
```

Managed rotation does not require the customer to create a Lambda rotation function.

Examples include supported credentials for services such as:

```text
Amazon RDS

Amazon Aurora

Amazon DocumentDB

Amazon Redshift
```

---

## 21. RDS Managed Credentials

For supported RDS configurations:

```text
RDS
   |
   v
Secrets Manager
   |
   v
Managed Credential
   |
   v
Automatic Rotation
```

This can reduce the operational burden of maintaining database master credentials.

However, applications should normally use:

```text
Dedicated Least-Privilege Database Users
```

instead of master accounts where possible.

---

# Lambda Rotation

## 22. Lambda-Based Rotation

For other secrets, rotation can use an AWS Lambda function.

Conceptually:

```text
Secrets Manager
      |
      v
Rotation Trigger
      |
      v
Lambda Function
      |
      v
Target System
```

The Lambda function updates both:

```text
Target Credential

and

Secret Version
```

---

## 23. Rotation Workflow

Lambda rotation typically follows four logical steps:

```text
createSecret

setSecret

testSecret

finishSecret
```

Conceptually:

```text
Create New Secret
      |
      v
Update Target Service
      |
      v
Test New Credential
      |
      v
Promote New Version
```

---

## 24. createSecret

Purpose:

```text
Create a new pending secret value.
```

Conceptually:

```text
AWSPENDING
```

is created.

The new value is not yet the active credential.

---

## 25. setSecret

Purpose:

```text
Update the target system
with the new credential.
```

Example:

```text
Database
Old Password
   ↓
New Password
```

---

## 26. testSecret

Purpose:

```text
Verify the new credential works.
```

Example:

```text
Connect to Database

Authenticate

Run Minimal Test
```

If the test fails, the new credential should not become active.

---

## 27. finishSecret

Purpose:

```text
Promote the new version.
```

Conceptually:

```text
AWSPENDING
    ↓
AWSCURRENT
```

Previous current version becomes:

```text
AWSPREVIOUS
```

---

# Rotation Strategies

## 28. Single-User Rotation

Single-user rotation updates the credential of the same database user.

Conceptually:

```text
app_user
Password A
    ↓
Rotation
    ↓
app_user
Password B
```

This is simpler but may temporarily affect active connections depending on the application and database.

---

## 29. Alternating-Users Rotation

Another strategy alternates between two database users.

Conceptually:

```text
User A
Active

User B
Standby
```

Rotation:

```text
Update User B
Test
Switch
```

Next rotation:

```text
Update User A
Test
Switch
```

This can improve availability during credential rotation in supported scenarios.

---

# Resource-Based Policies

## 30. Secret Resource Policies

Secrets Manager supports resource-based policies.

Conceptually:

```text
Secret
   |
   v
Resource Policy
   |
   v
Who Can Access?
```

Resource policies can allow:

```text
Specific Roles

Specific Accounts

Cross-Account Access
```

---

## 31. Example Resource Policy

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/ApplicationRole"
      },
      "Action": "secretsmanager:GetSecretValue",
      "Resource": "*"
    }
  ]
}
```

Because the policy is attached directly to the secret:

```text
Resource = *
```

refers to that secret resource in the policy context.

---

## 32. BlockPublicPolicy

Secrets Manager can validate resource policies to help prevent overly broad public access.

Conceptually:

```text
Resource Policy
      |
      v
Validate
      |
      v
Public Access Risk?
```

When using APIs, the:

```text
BlockPublicPolicy
```

option can help prevent resource policies from granting broad public access.

---

## 33. Access Analyzer

IAM Access Analyzer can also help identify unintended external access to secrets.

Questions:

```text
Can another AWS account access this secret?

Was this access intentional?

Is the external principal trusted?
```

This supports secrets access reviews.

---

# Cross-Account Access

## 34. Cross-Account Secret Access

Example:

```text
Account A
Secret

Account B
Application Role
```

Application in Account B needs to retrieve the secret.

This requires multiple permissions.

---

## 35. Cross-Account Permission Model

Cross-account access requires:

```text
Secret Resource Policy
       +
Caller IAM Policy
       +
KMS Key Policy
```

Conceptually:

```text
Account B Role
      |
      v
IAM Policy
      |
      v
Account A Secret
      |
      +-- Resource Policy
      |
      +-- Customer Managed KMS Key
             |
             +-- Key Policy
```

All required layers must permit access.

---

## 36. Why Customer Managed KMS Key Is Required

The default AWS managed key:

```text
aws/secretsmanager
```

cannot be used for cross-account secret access.

For cross-account access:

```text
Customer Managed KMS Key
```

is required.

The external principal must have permission to use that key.

---

## 37. Cross-Account Example

Account A owns:

```text
ProductionDatabaseSecret
```

Account B has:

```text
ApplicationRole
```

Required permissions:

### Secret Resource Policy

```text
Allow Account B ApplicationRole
→ GetSecretValue
```

### Account B IAM Policy

```text
Allow
→ secretsmanager:GetSecretValue
```

### KMS Key Policy

```text
Allow ApplicationRole
→ kms:Decrypt
```

Without all required layers, access can fail.

---

# Multi-Region Secrets

## 38. Secret Replication

Secrets Manager supports secret replication to other AWS Regions.

Conceptually:

```text
Primary Secret
Tokyo
   |
   v
Replicate
   |
   v
Replica Secret
Singapore
```

Replica secrets remain associated with the primary secret.

This can support:

```text
Disaster Recovery

Multi-Region Applications

Regional Resilience
```

---

## 39. Multi-Region Considerations

When replicating secrets, consider:

```text
KMS Keys

Regional Applications

Access Policies

Rotation

Disaster Recovery
```

Do not replicate secrets to Regions where they are not needed.

This reduces unnecessary exposure.

---

# Secrets Manager vs Parameter Store

## 40. Systems Manager Parameter Store

Parameter Store provides centralized storage for configuration values.

Examples:

```text
AMI ID

Application Endpoint

Environment Name

Feature Configuration
```

It can also store encrypted values using:

```text
SecureString
```

and AWS KMS.

---

## 41. Secrets Manager vs Parameter Store

A simplified comparison:

| Secrets Manager | Parameter Store |
|---|---|
| Purpose-built for secrets | General configuration storage |
| Automatic rotation | No native automatic credential rotation |
| Secret version staging labels | Parameter versions |
| Cross-account secret access | Different access model |
| Strong secret lifecycle features | Simpler configuration management |
| API keys / passwords | Configuration values |

---

## 42. When to Use Secrets Manager

Use Secrets Manager when you need:

```text
Database Credentials

API Keys

OAuth Tokens

Automatic Rotation

Cross-Account Secret Access

Fine-Grained Secret Auditing
```

---

## 43. When to Use Parameter Store

Parameter Store may be appropriate for:

```text
Application Settings

Endpoint URLs

AMI IDs

Environment Variables

Static Configuration

Non-Rotating Secure Values
```

The choice depends on application requirements.

---

# Application Architecture

## 44. Secure Application Pattern

A common pattern:

```text
EC2 / ECS / Lambda
       |
       v
IAM Role
       |
       v
Secrets Manager
       |
       v
Secret
       |
       v
Database / API
```

The application does not need to embed the credential permanently.

---

## 45. Runtime Retrieval

An application can retrieve a secret when needed.

Conceptually:

```text
Application Starts
      |
      v
GetSecretValue
      |
      v
Secrets Manager
      |
      v
Use Credential
```

However, calling Secrets Manager for every application request can be inefficient.

Caching may be appropriate.

---

## 46. Secret Caching

Applications may cache secrets temporarily.

Conceptually:

```text
Secrets Manager
      |
      v
Application Cache
      |
      v
Application Requests
```

Benefits include:

```text
Reduced API Calls

Lower Latency

Lower Cost
```

But caches must support rotation.

Applications should not cache secrets indefinitely.

---

# Monitoring

## 47. CloudTrail

Secrets Manager API activity can be recorded in CloudTrail.

Important operations include:

```text
GetSecretValue

PutSecretValue

UpdateSecret

RotateSecret

DeleteSecret

PutResourcePolicy
```

Conceptually:

```text
Secret API Call
      |
      v
CloudTrail
      |
      v
Audit Event
```

---

## 48. Sensitive Monitoring Events

Important management events may include:

```text
DeleteSecret

UpdateSecret

RotateSecret

PutResourcePolicy

DeleteResourcePolicy
```

Unexpected changes should be investigated.

---

## 49. GetSecretValue Monitoring

`GetSecretValue` can be security relevant.

Questions:

```text
Which principal retrieved the secret?

Was access expected?

Was access from the expected application?

Did access occur at an unusual time?
```

High-volume applications may retrieve secrets frequently, so detection rules require context.

---

# Common Misconfigurations

## 50. Hard-Coded Secrets

Poor:

```text
DATABASE_PASSWORD="password123"
```

inside:

```text
Source Code

Dockerfile

GitHub

AMI
```

Better:

```text
IAM Role
→ Secrets Manager
```

---

## 51. Broad Secret Access

Poor:

```text
secretsmanager:GetSecretValue

Resource:
*
```

This allows the principal to retrieve many secrets.

Better:

```text
Specific Secret ARN
```

---

## 52. Application Can Modify Secrets

If an application only needs read access:

Poor:

```text
GetSecretValue

UpdateSecret

DeleteSecret

PutResourcePolicy
```

Better:

```text
GetSecretValue
```

only.

---

## 53. No Rotation

A long-lived database password may remain valid indefinitely.

Risk:

```text
Credential Leak
       |
       v
Long-Term Access
```

Rotation should be considered for credentials that support it.

---

## 54. Rotation Without Testing

Poor rotation design:

```text
Generate New Credential
       |
       v
Immediately Set Current
```

without confirming that the new credential works.

Better:

```text
Create
↓
Set
↓
Test
↓
Finish
```

---

## 55. Resource Policy Too Broad

Risky:

```text
Principal:
*
```

for secret access.

This can expose sensitive credentials.

Use:

```text
Specific Principal

Specific Account

Specific Role
```

---

## 56. Cross-Account Without KMS Planning

Scenario:

```text
Secret Resource Policy
→ Correct

IAM Policy
→ Correct

KMS
→ Default aws/secretsmanager
```

Result:

```text
Cross-Account Access Fails
```

Cross-account Secrets Manager access requires a suitable customer managed KMS key.

---

## 57. Secret Logged Accidentally

Applications should never log:

```text
Password

API Key

OAuth Token

Private Key

Secret Value
```

Example poor code:

```text
DEBUG:
Database password = ...
```

Logs often have wider access than secret stores.

---

## 58. Secret in Environment Variables

Environment variables may be convenient, but they can be exposed through:

```text
Process Inspection

Debug Logs

Crash Dumps

Application Diagnostics
```

Where practical, retrieve secrets securely and minimize their lifetime in memory.

---

# Troubleshooting

## 59. AccessDenied on GetSecretValue

Check:

```text
Which IAM Principal?

Does IAM allow GetSecretValue?

Is the correct Secret ARN used?

Does the Secret Resource Policy allow access?

Is cross-account access involved?

Does KMS allow decryption?

Is an Explicit Deny present?
```

---

## 60. Cross-Account Failure

Check all three:

```text
Caller IAM Policy

Secret Resource Policy

KMS Key Policy
```

Remember:

```text
All Required Layers
→ Must Allow
```

---

## 61. Rotation Failure

Check:

```text
Does the rotation function have permissions?

Can it reach the target database?

Does the target credential update successfully?

Can testSecret authenticate?

Is AWSPENDING left behind?

Are Security Groups correct?
```

Rotation failures should be investigated before retrying repeatedly.

---

## 62. Database Rotation Network Issue

If a Lambda rotation function cannot reach an RDS database:

```text
Lambda
   |
   X
RDS
```

Check:

```text
VPC

Subnets

Security Groups

Routes

DNS

Database Port
```

Secret management still depends on correct networking.

---

# Hands-on Practice

## 63. Practice — Review Secrets

Open:

```text
AWS Console
    |
    v
Secrets Manager
```

Review available secrets.

Identify:

```text
Secret Name

KMS Key

Rotation Status

Last Changed Date

Last Retrieved Date

Tags
```

Do not reveal secret values.

---

## 64. Practice — Review Versions

Open a test secret.

Review:

```text
Versions

AWSCURRENT

AWSPREVIOUS

AWSPENDING
```

If no rotation exists, identify which version currently has:

```text
AWSCURRENT
```

---

## 65. Practice — Review Permissions

Review:

```text
IAM Permissions

Resource Permissions

KMS Key
```

Ask:

```text
Who can retrieve the secret?

Who can modify it?

Who can rotate it?

Who can delete it?
```

---

## 66. Optional CLI Practice

### List Secrets

```bash
aws secretsmanager list-secrets
```

### Describe Secret

```bash
aws secretsmanager describe-secret \
  --secret-id example-secret
```

### List Secret Versions

```bash
aws secretsmanager list-secret-version-ids \
  --secret-id example-secret
```

Avoid running:

```text
GetSecretValue
```

against production secrets solely for practice.

---

## 67. GetSecretValue Example

In an authorized lab environment:

```bash
aws secretsmanager get-secret-value \
  --secret-id example-secret
```

Important:

This command can display secret material directly in the terminal.

Do not:

```text
Paste the result into GitHub

Take public screenshots

Save it in shell scripts

Expose it in terminal recordings
```

---

## 68. Optional Architecture Exercise

Requirements:

```text
EC2 Application

Private RDS

Database Password

Automatic Rotation

No Hard-Coded Credentials
```

Design:

```text
EC2
 |
 v
IAM Role
 |
 v
Secrets Manager
 |
 v
Database Secret
 |
 v
RDS
```

Data protection:

```text
Secret
→ KMS Encryption
```

Rotation:

```text
Secrets Manager
→ Managed Rotation / Lambda
→ RDS
```

---

## 69. Cross-Account Exercise

Scenario:

```text
Account A
→ Central Secrets Account

Account B
→ Application
```

Design access:

```text
Account B ApplicationRole
       |
       v
IAM Policy
       |
       v
Account A Secret
       |
       +-- Resource Policy
       |
       v
Customer Managed KMS Key
       |
       +-- Key Policy
```

Questions:

```text
Does the application need only GetSecretValue?

Can it modify the secret?

Can it access other secrets?

Can it use the KMS key for unrelated data?
```

Apply least privilege.

---

# Security Checklist

```text
[ ] Secrets are not hard-coded in source code

[ ] Secrets are not committed to GitHub

[ ] Applications use IAM roles

[ ] GetSecretValue is limited to required secrets

[ ] Applications do not receive unnecessary update or delete permissions

[ ] Secrets use appropriate KMS keys

[ ] Customer managed KMS keys are used when required

[ ] Rotation requirements are documented

[ ] Rotation is tested

[ ] Rotation failures are monitored

[ ] AWSCURRENT points to the correct secret version

[ ] Resource policies follow least privilege

[ ] BlockPublicPolicy / policy validation is used where appropriate

[ ] Cross-account access is intentional

[ ] Cross-account IAM, resource, and KMS policies are configured correctly

[ ] Secret values are excluded from logs

[ ] Secret caching does not prevent rotation

[ ] Sensitive Secrets Manager API activity is logged in CloudTrail
```

---

## Key Takeaways

- AWS Secrets Manager is purpose-built for storing and managing sensitive credentials.
- Applications should use IAM roles to retrieve secrets at runtime.
- Secrets are encrypted at rest using AWS KMS.
- Secret updates and rotations create new secret versions.
- AWSCURRENT identifies the active secret version.
- AWSPREVIOUS identifies the previous active version.
- AWSPENDING is used during rotation.
- Automatic rotation can reduce the lifetime of exposed credentials.
- Some AWS services support managed rotation without Lambda.
- Other secrets can use Lambda-based rotation.
- Rotation should update both Secrets Manager and the target service.
- Resource-based policies can control access directly on a secret.
- Cross-account access requires an IAM policy, a secret resource policy, and a suitable KMS key policy.
- The AWS managed key aws/secretsmanager cannot be used for cross-account secret access.
- Secrets Manager is generally preferable to Parameter Store for credentials requiring automatic rotation, cross-account access, and fine-grained auditing.
- Secret values should never appear in source code, GitHub, or logs.

---

## Reflection

Today I learned that AWS Secrets Manager provides more than encrypted credential storage.

It manages the full lifecycle of sensitive credentials, including versioning, access control, encryption, rotation, and auditing.

The most important concept is secret rotation. A secure rotation process must update both the stored secret and the credential in the target service, test the new credential, and only then make the new version current.

I also learned that staging labels such as AWSCURRENT, AWSPREVIOUS, and AWSPENDING help Secrets Manager safely manage multiple secret versions.

From a security engineering perspective, secret access should follow least privilege, cross-account access should be carefully controlled, and secret values should never be exposed through source code or application logs.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AWSCURRENT | Staging label identifying the current active secret version |
| AWSPENDING | Staging label used for a new secret version during rotation |
| AWSPREVIOUS | Staging label identifying the previous secret version |
| Managed Rotation | Rotation managed directly by a supported AWS service integration |
| Resource Policy | A policy attached directly to a secret controlling who can access it |
| Rotation | Periodically replacing a secret with a new value |
| Secret | Sensitive information such as a password, API key, or token |
| Secret Caching | Temporarily storing retrieved secrets to reduce repeated API calls |
| Secret Replication | Creating linked copies of a secret in other AWS Regions |
| Secrets Manager | AWS service for managing the lifecycle of sensitive secrets |
