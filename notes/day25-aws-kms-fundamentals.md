# Day 25 — AWS KMS Fundamentals

## Topic

AWS Key Management Service Fundamentals, KMS Keys, Envelope Encryption, and Access Control

---

## Objectives

- Understand the purpose of AWS KMS
- Understand what a KMS key is
- Compare customer managed, AWS managed, and AWS owned keys
- Understand symmetric and asymmetric KMS keys
- Understand envelope encryption
- Understand data keys
- Learn how key policies work
- Understand IAM policies and KMS permissions
- Understand KMS grants
- Learn the role of aliases
- Understand key rotation
- Understand single-Region and multi-Region keys
- Review AWS service integrations with KMS
- Identify common KMS security risks

---

## 1. What Is AWS KMS?

AWS Key Management Service (AWS KMS) is a managed service for creating and controlling cryptographic keys.

KMS keys can be used to protect data in AWS services and applications.

Conceptually:

```text
Application / AWS Service
          |
          v
       AWS KMS
          |
          v
       KMS Key
          |
          v
     Protect Data
```

AWS KMS integrates with many AWS services, including:

```text
Amazon EBS

Amazon S3

Amazon RDS

AWS Secrets Manager

Amazon CloudWatch Logs

Amazon SNS

Amazon SQS
```

KMS provides centralized key management and access control.

---

## 2. Why Key Management Matters

Encryption is only as secure as the keys protecting the data.

Poor key management can create risks such as:

```text
Unauthorized Decryption

Key Leakage

Excessive Permissions

Accidental Key Deletion

Loss of Data Access
```

A good key management system should control:

```text
Who can use a key?

Who can manage a key?

Which data can the key protect?

When should the key rotate?

When can the key be disabled or deleted?

How is key usage audited?
```

AWS KMS provides mechanisms to manage these requirements.

---

## 3. KMS Key

A KMS key is a logical cryptographic key resource managed by AWS KMS.

Conceptually:

```text
KMS Key
│
├── Key ID
├── ARN
├── Key Policy
├── Key Material
├── Key State
├── Key Usage
└── Metadata
```

A KMS key is not simply a password or plaintext encryption key.

It is an AWS resource with:

```text
Identity

Permissions

Lifecycle

Cryptographic Material

Auditability
```

---

## 4. KMS Key ARN

Every KMS key has an ARN.

Example:

```text
arn:aws:kms:ap-northeast-1:111122223333:key/example-key-id
```

A KMS key ARN identifies:

```text
Service

Region

AWS Account

Key ID
```

IAM policies and resource policies can reference the key ARN.

---

## 5. KMS Key Types by Ownership

AWS KMS-related encryption keys can be divided into three important categories:

```text
Customer Managed Keys

AWS Managed Keys

AWS Owned Keys
```

These have different levels of customer control.

---

## 6. Customer Managed Keys

A customer managed key is created and controlled by the customer.

Conceptually:

```text
Customer
   |
   v
Create KMS Key
   |
   v
Customer Managed Key
```

Customers control:

```text
Key Policy

IAM Permissions

Grants

Rotation Configuration

Enable / Disable

Aliases

Tags

Deletion Scheduling
```

Customer managed keys provide the highest level of customer control.

They are appropriate when organizations need:

- Fine-grained permissions
- Custom key policies
- Cross-account usage
- Key lifecycle control
- Specific compliance requirements
- Detailed access control

---

## 7. AWS Managed Keys

AWS managed keys are created and managed by AWS services in the customer's account.

Examples may use aliases such as:

```text
aws/ebs

aws/rds

aws/s3
```

Conceptually:

```text
AWS Service
     |
     v
AWS Managed Key
     |
     v
Customer Resource
```

Customers can:

```text
View the key

View the key policy

Audit supported key usage
```

but cannot:

```text
Change the key policy

Delete the key

Manually rotate the key

Directly control its lifecycle
```

AWS managed keys are convenient when custom key management is not required.

---

## 8. AWS Owned Keys

AWS owned keys are owned and managed entirely by AWS services.

Conceptually:

```text
AWS Service
     |
     v
AWS Owned Key
     |
     v
Encrypted Customer Resource
```

These keys:

```text
Are not resources in the customer's AWS account

Cannot be viewed by the customer

Cannot have their key policy changed by the customer

Cannot be directly audited as a customer KMS resource
```

They provide simple, transparent encryption for supported AWS services.

---

## 9. Key Type Comparison

| Feature | Customer Managed | AWS Managed | AWS Owned |
|---|---|---|---|
| Customer creates key | Yes | No | No |
| Customer controls policy | Yes | No | No |
| Customer controls lifecycle | Yes | No | No |
| Visible in customer account | Yes | Yes | No |
| Customer CloudTrail visibility | Yes | Yes | Limited / not exposed as customer key activity |
| Custom cross-account design | Yes | Limited | No customer control |
| Management responsibility | Customer | AWS service | AWS service |

A useful model:

```text
More Control
    ↑
Customer Managed
AWS Managed
AWS Owned
    ↓
More Convenience
```

---

## 10. When to Use Customer Managed Keys

Customer managed keys are useful when security requirements include:

```text
Custom Key Policies

Cross-Account Access

Separation of Duties

Key Lifecycle Management

Detailed Auditing

Specific Compliance Controls
```

Example:

```text
Sensitive Production Database
       |
       v
Customer Managed KMS Key
```

This allows the organization to define precisely who can use and manage the key.

---

## 11. Symmetric Encryption Keys

The most common KMS keys are symmetric encryption keys.

Conceptually:

```text
Same Key Material
      |
      +-- Encrypt
      |
      +-- Decrypt
```

AWS services integrated with KMS commonly use symmetric encryption KMS keys.

Examples include:

```text
EBS Encryption

S3 SSE-KMS

RDS Encryption

Secrets Manager
```

---

## 12. Asymmetric KMS Keys

AWS KMS also supports asymmetric key pairs for supported use cases.

Conceptually:

```text
Asymmetric Key Pair
│
├── Public Key
└── Private Key
```

Depending on the key specification, asymmetric keys can be used for:

```text
Encryption / Decryption

Digital Signing / Verification
```

The private key remains protected within AWS KMS.

The public key can be downloaded for supported use cases.

---

## 13. Symmetric vs Asymmetric

### Symmetric

```text
Same secret key material
→ Encryption and Decryption
```

Common use:

```text
AWS Service Data Encryption
```

### Asymmetric

```text
Public Key
+
Private Key
```

Common use:

```text
Digital Signatures

Special Application Encryption
```

For most AWS service encryption scenarios:

```text
Symmetric KMS Key
```

is the common choice.

---

## 14. Key Usage

A KMS key has a defined cryptographic purpose.

Examples include:

```text
ENCRYPT_DECRYPT

SIGN_VERIFY

GENERATE_VERIFY_MAC
```

A key created for one purpose cannot simply be used for an unrelated cryptographic operation.

For example:

```text
SIGN_VERIFY
```

is not used as a normal EBS encryption key.

---

## 15. Envelope Encryption

Envelope encryption is one of the most important KMS concepts.

Instead of encrypting large amounts of application data directly with a KMS key:

```text
Large Data
    |
    X
Encrypt Everything Directly with KMS Key
```

AWS commonly uses:

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
Encrypt Application Data
```

This model is called:

```text
Envelope Encryption
```

---

## 16. Why Envelope Encryption?

KMS keys are designed to protect cryptographic key material.

Applications often need to encrypt large amounts of data efficiently.

Therefore:

```text
KMS Key
→ Protect smaller data key

Data Key
→ Encrypt actual data
```

This provides:

```text
Centralized Key Control

Efficient Data Encryption

Scalable Encryption

Separation of Key Hierarchy
```

---

## 17. Data Keys

A data key is cryptographic key material used to encrypt application data.

Conceptually:

```text
AWS KMS
   |
   v
Generate Data Key
   |
   +---------------------+
   |                     |
   v                     v
Plaintext Data Key   Encrypted Data Key
   |                     |
   v                     |
Encrypt Data              |
   |                     |
   v                     |
Delete Plaintext Key      |
                         |
                         v
                 Store with Ciphertext
```

The encrypted data key can be stored with the encrypted data.

---

## 18. Envelope Encryption Process

Simplified encryption process:

```text
1. Application requests a data key.

2. AWS KMS returns:
   - Plaintext data key
   - Encrypted copy of data key

3. Application encrypts data using plaintext data key.

4. Application removes plaintext data key from memory.

5. Application stores:
   - Encrypted data
   - Encrypted data key
```

Conceptually:

```text
KMS Key
   ↓
Encrypted Data Key
   ↓
Stored with
   ↓
Encrypted Data
```

---

## 19. Envelope Decryption Process

When data needs to be decrypted:

```text
Encrypted Data Key
       |
       v
AWS KMS Decrypt
       |
       v
Plaintext Data Key
       |
       v
Decrypt Application Data
```

After use:

```text
Plaintext Data Key
→ Remove from memory
```

The KMS key itself does not leave AWS KMS.

---

## 20. Why Not Store Plaintext Data Keys?

If plaintext data keys are permanently stored:

```text
Encrypted Data
+
Plaintext Encryption Key
```

then encryption provides little protection.

A secure model stores:

```text
Encrypted Data
+
Encrypted Data Key
```

The plaintext data key should exist only when required for cryptographic operations.

---

## 21. Key Policies

Every KMS key has a key policy.

A key policy is a resource-based policy attached directly to the KMS key.

Conceptually:

```text
KMS Key
   |
   v
Key Policy
   |
   v
Who Can Use / Manage Key?
```

Key policies are a primary mechanism for controlling access to KMS keys.

---

## 22. Key Policy Structure

A simplified key policy looks similar to other AWS resource policies.

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/ApplicationRole"
      },
      "Action": [
        "kms:Encrypt",
        "kms:Decrypt"
      ],
      "Resource": "*"
    }
  ]
}
```

The policy defines:

```text
Who
→ Principal

Can do what
→ Action

Under which conditions
→ Condition
```

---

## 23. KMS Key Policy vs IAM Policy

KMS authorization is slightly different from many AWS services.

A key policy controls the KMS key itself.

IAM policies can also grant permissions, but the key policy must allow the appropriate IAM-based delegation.

Conceptually:

```text
Key Policy
     |
     v
Allows IAM Delegation
     |
     v
IAM Policy
     |
     v
Principal Uses Key
```

Therefore:

```text
IAM Allow
```

alone may not be sufficient if the KMS key policy does not permit the required access model.

---

## 24. Key Administrators vs Key Users

A good KMS design separates:

```text
Key Administration

from

Key Usage
```

### Key Administrator

May manage:

```text
Key Policy

Enable / Disable

Rotation

Aliases

Deletion
```

### Key User

May perform:

```text
Encrypt

Decrypt

GenerateDataKey
```

Conceptually:

```text
Security Administrator
→ Manage Key

Application
→ Use Key
```

This follows separation of duties.

---

## 25. Least Privilege for KMS

Avoid broad permissions such as:

```text
kms:*
```

for normal applications.

Instead, grant only required actions.

Example application:

```text
kms:Decrypt

kms:GenerateDataKey
```

against:

```text
Specific KMS Key
```

not:

```text
All KMS Keys
```

A useful principle is:

```text
Required Principal

+

Required KMS Actions

+

Required Key

+

Required Conditions
```

---

## 26. KMS Grants

A grant is another KMS authorization mechanism.

Conceptually:

```text
KMS Key
   |
   v
Grant
   |
   v
Principal / AWS Service
   |
   v
Allowed Operations
```

Grants are often used by AWS services that integrate with KMS.

Examples can include:

```text
EBS

RDS

Other AWS Services
```

They can provide temporary or delegated permission without modifying the main key policy.

---

## 27. Grant Example

Suppose AWS EBS needs to use a KMS key.

Conceptually:

```text
EC2 / EBS Operation
        |
        v
KMS Grant
        |
        v
Customer Managed Key
```

The grant might allow required cryptographic operations for the service.

A grant should follow least privilege:

```text
Specific Principal

Specific Operations

Specific Constraints
```

---

## 28. Encryption Context

An encryption context is additional non-secret contextual information that can be cryptographically associated with ciphertext.

Conceptually:

```text
Data
+
Encryption Context
       |
       v
Encryption
```

Example context:

```text
Department = Security

Environment = Production
```

When decrypting, the required encryption context must match.

This can help bind encrypted data to its intended context.

---

## 29. Encryption Context Is Not Secret

Important:

```text
Encryption Context
≠
Secret
```

Do not store:

```text
Passwords

Tokens

Sensitive Personal Data
```

inside the encryption context.

It should contain non-secret contextual information.

---

## 30. Aliases

KMS aliases provide friendly names for KMS keys.

Example:

```text
alias/prod-database

alias/security-logs

alias/application-data
```

Instead of remembering:

```text
1234abcd-example-key-id
```

applications or administrators can reference a meaningful alias where supported.

---

## 31. Alias vs KMS Key

An alias is not the key itself.

Conceptually:

```text
alias/prod-data
       |
       v
KMS Key A
```

Later:

```text
alias/prod-data
       |
       v
KMS Key B
```

The alias can be associated with another compatible KMS key.

This can simplify key replacement workflows.

---

## 32. Key States

A KMS key can have different states.

Examples include:

```text
Enabled

Disabled

PendingDeletion

PendingImport
```

The exact state depends on the key type and lifecycle.

A disabled key cannot normally be used for cryptographic operations.

---

## 33. Disabling a KMS Key

Disabling a customer managed key can affect resources that depend on it.

Example:

```text
Encrypted Resource
      |
      v
Customer Managed Key
      |
      v
Key Disabled
      |
      v
Required Cryptographic Operation Fails
```

Before disabling a key, identify:

```text
EBS Volumes

RDS Databases

S3 Objects

Secrets

Applications
```

that depend on it.

---

## 34. Key Deletion

Customer managed keys can be scheduled for deletion.

Conceptually:

```text
Schedule Key Deletion
        |
        v
Waiting Period
        |
        v
KMS Key Deleted
```

Deleting a key can make encrypted data permanently inaccessible.

Therefore:

```text
Key Deletion
```

is a high-risk administrative operation.

It should require strong access controls and change management.

---

## 35. Crypto-Shredding

Destroying the encryption key can effectively make encrypted data unrecoverable.

Conceptually:

```text
Encrypted Data
+
Encryption Key
→ Data Accessible

Encrypted Data
+
Key Destroyed
→ Data Cannot Be Decrypted
```

This concept is sometimes called:

```text
Crypto-Shredding
```

Because of this, key deletion must be treated carefully.

---

## 36. Key Rotation

Key rotation replaces the cryptographic key material associated with a KMS key while retaining the logical KMS key identity.

Conceptually:

```text
KMS Key
│
├── Old Key Material
└── New Key Material
```

AWS KMS retains previous key material as required so previously encrypted data can still be decrypted.

---

## 37. Customer Managed Key Rotation

For supported customer managed symmetric encryption KMS keys with AWS-generated key material, AWS KMS supports:

```text
Automatic Rotation

On-Demand Rotation
```

Automatic rotation can use a configurable rotation period.

Conceptually:

```text
KMS Key
   |
   v
Rotation
   |
   v
New Cryptographic Material
```

The KMS key ID and ARN remain the same.

---

## 38. AWS Managed Key Rotation

AWS managed KMS keys are rotated automatically by AWS KMS.

The customer does not configure their rotation schedule.

Conceptually:

```text
AWS Managed Key
       |
       v
AWS-Controlled Rotation
```

This reduces customer management responsibility.

---

## 39. Rotation Does Not Re-Encrypt Everything

Important:

```text
KMS Key Rotation
≠
Automatically re-encrypt all existing data
```

Previous versions of key material remain available for decryption.

Example:

```text
Old Ciphertext
→ Old Key Material

New Ciphertext
→ New Key Material
```

AWS KMS selects the appropriate key material during decryption.

---

## 40. Single-Region Keys

By default, a KMS key is associated with one AWS Region.

Example:

```text
ap-northeast-1
        |
        v
KMS Key
```

The key cannot automatically be used as the same key resource in another Region.

This is important for:

```text
Backup

Disaster Recovery

Multi-Region Applications
```

---

## 41. Multi-Region Keys

AWS KMS also supports Multi-Region keys.

Conceptually:

```text
Tokyo
Multi-Region Primary Key
        |
        v
Replicate
        |
        v
Singapore
Multi-Region Replica Key
```

Related Multi-Region keys share compatible key material and key ID characteristics.

This allows ciphertext encrypted with one related key to be decrypted using a related key in another Region.

---

## 42. Multi-Region Keys Are Separate Resources

Although related Multi-Region keys share cryptographic properties, they remain separate KMS resources.

Each Region has its own:

```text
Key Policy

Alias

Tags

Enabled / Disabled State

Grant Configuration
```

Conceptually:

```text
Primary Key
→ Policy A

Replica Key
→ Policy B
```

Policies are not automatically synchronized.

---

## 43. Multi-Region Use Cases

Possible use cases include:

```text
Disaster Recovery

Multi-Region Applications

Client-Side Encryption

Global Applications

Cross-Region Data Processing
```

However, Multi-Region keys should only be used when the architecture requires them.

Single-Region keys provide stronger regional isolation for many workloads.

---

## 44. AWS Service Integration

Many AWS services integrate directly with KMS.

Example EBS:

```text
EC2
 ↓
Encrypted EBS
 ↓
KMS
```

Example S3:

```text
S3 Object
 ↓
SSE-KMS
 ↓
KMS
```

Example RDS:

```text
RDS
 ↓
Encrypted Storage
 ↓
KMS
```

This allows centralized management of encryption keys across multiple services.

---

## 45. EBS and KMS

From Day 17:

```text
EC2
 ↓
EBS Volume
 ↓
KMS Key
```

KMS controls can determine who can perform required encryption-related operations.

If the key becomes unavailable:

```text
Encrypted EBS Operations
```

may fail.

Therefore, key availability also affects workload availability.

---

## 46. S3 and KMS

S3 can use:

```text
SSE-KMS
```

for server-side encryption.

Conceptually:

```text
Application
 ↓
Amazon S3
 ↓
SSE-KMS
 ↓
KMS Key
```

Access to an SSE-KMS encrypted object may require:

```text
S3 Permission

+

KMS Permission
```

depending on the operation.

---

## 47. RDS and KMS

RDS supports KMS-based encryption at rest.

Conceptually:

```text
Application
 ↓
RDS
 ↓
Encrypted Storage
 ↓
KMS
```

KMS can protect:

```text
Database Storage

Backups

Snapshots

Related Encrypted Resources
```

according to the RDS encryption architecture.

---

## 48. Secrets Manager and KMS

Secrets Manager protects stored secrets using encryption.

Conceptually:

```text
Application Secret
       |
       v
Secrets Manager
       |
       v
AWS KMS
```

KMS permissions can therefore affect access to encrypted secrets.

This will be studied in more detail later.

---

## 49. CloudTrail and KMS

AWS KMS API activity can be audited using AWS CloudTrail.

Examples may include:

```text
Encrypt

Decrypt

GenerateDataKey

CreateKey

DisableKey

ScheduleKeyDeletion
```

Conceptually:

```text
KMS Operation
     |
     v
CloudTrail
     |
     v
Audit Event
```

This provides important visibility into key usage and administration.

---

## 50. Key Administration Events

Security-sensitive KMS management events include:

```text
CreateKey

PutKeyPolicy

DisableKey

EnableKey

ScheduleKeyDeletion

CancelKeyDeletion

CreateGrant
```

These operations should be monitored because they can affect:

```text
Data Confidentiality

Data Availability

Access Control
```

---

## 51. Decrypt Events

A `Decrypt` operation may be particularly important during investigations.

Questions include:

```text
Which principal requested decryption?

Which KMS key was used?

When did the request occur?

Was the request expected?

Which service or application was involved?
```

However, expected applications may generate large numbers of cryptographic operations.

Monitoring should consider workload behavior and volume.

---

## 52. Separation of Duties

Key administrators and data users should not automatically have the same permissions.

Example:

```text
Key Administrator

Can:
Manage Key

Cannot:
Decrypt Application Data
```

Application role:

```text
Can:
Use Required Cryptographic Operations

Cannot:
Delete or Disable Key
```

This reduces the impact of a compromised role.

---

## 53. Common Misconfiguration — kms:*

Risky:

```text
Action:
kms:*

Resource:
*
```

This may allow both:

```text
Key Administration

and

Key Usage
```

Better:

```text
Required Actions

Required Key

Required Conditions
```

---

## 54. Common Misconfiguration — All Keys

Example:

```text
Application Role
       |
       v
kms:Decrypt
       |
       v
All KMS Keys
```

This can increase the impact of application compromise.

Better:

```text
kms:Decrypt
       |
       v
Specific Application Key
```

---

## 55. Common Misconfiguration — Key User Can Delete Key

Poor separation:

```text
Application Role

kms:Decrypt
kms:Encrypt
kms:ScheduleKeyDeletion
```

The application does not normally need administrative key deletion permissions.

Separate:

```text
Key Usage

from

Key Administration
```

---

## 56. Common Misconfiguration — Accidental Key Deletion

Scenario:

```text
KMS Key Deleted
       |
       v
Encrypted Data Remains
       |
       v
Data Cannot Be Decrypted
```

Key deletion can result in permanent data loss.

Deletion permissions should be highly restricted.

---

## 57. Common Misconfiguration — Key Disabled

Scenario:

```text
Production Key
      |
      v
Disabled
      |
      v
Application Failure
```

Security administrators should understand key dependencies before disabling a key.

---

## 58. Common Misconfiguration — Overly Broad Key Policy

Risky:

```text
Principal:
*

Actions:
kms:Decrypt
```

This may grant broader access than intended depending on conditions and policy context.

Key policies should explicitly identify:

```text
Required Principals

Required Actions

Required Conditions
```

---

## 59. Common Misconfiguration — No Monitoring

If KMS administrative changes are not monitored:

```text
DisableKey

ScheduleKeyDeletion

PutKeyPolicy
```

may go unnoticed.

Security-sensitive KMS operations should be included in logging and monitoring strategies.

---

## 60. Security Architecture Example

```text
                         Application
                              |
                              v
                           IAM Role
                              |
                              v
                         AWS Service
                    /         |         \
                   /          |          \
                  v           v           v
                EBS          S3          RDS
                  \           |           /
                   \          |          /
                    +---------+---------+
                              |
                              v
                         AWS KMS
                              |
                    +---------+---------+
                    |                   |
                    v                   v
               Key Policy            CloudTrail
                    |                   |
                    v                   v
             Access Control          Auditing
```

---

## 61. KMS Security Review Questions

When reviewing a KMS environment, ask:

```text
Who owns the key?

Is this a customer managed, AWS managed, or AWS owned key?

Who can administer the key?

Who can use the key?

Are administration and usage separated?

Does the application need Encrypt?

Does it need Decrypt?

Does it need GenerateDataKey?

Is access limited to a specific key?

Is the key policy least-privilege?

Are IAM policies least-privilege?

Are grants restricted?

Is rotation required?

Is the key single-Region or multi-Region?

What resources depend on the key?

What happens if the key is disabled?

What happens if the key is deleted?

Is key activity logged?
```

---

## 62. Hands-on Practice

### Practice A — Review KMS Keys

Open:

```text
AWS Management Console
        |
        v
AWS KMS
```

Review:

```text
AWS Managed Keys

Customer Managed Keys
```

Identify:

```text
Key ID

Alias

Key Manager

Key Usage

Key Spec

Region

Key State
```

Do not publish real key IDs or account information in GitHub.

---

## 63. Practice — Review AWS Managed Keys

Look for AWS managed aliases such as:

```text
aws/ebs

aws/rds

aws/s3
```

depending on which services have created keys in the account.

Compare:

```text
Customer Managed Key

vs

AWS Managed Key
```

Ask:

```text
Can I edit the key policy?

Can I disable the key?

Can I schedule deletion?

Who manages rotation?
```

---

## 64. Practice — Review a Key Policy

If a customer managed key is available, inspect its key policy.

Identify:

```text
Principal

Effect

Action

Condition
```

Ask:

```text
Who administers the key?

Who can use the key?

Does the policy enable IAM-based permissions?

Are any permissions too broad?
```

Do not modify production key policies for practice.

---

## 65. Practice — Review Rotation

For a suitable customer managed key, review:

```text
Key Rotation
```

Identify:

```text
Automatic Rotation Enabled?

Rotation Period?

Previous Rotations?
```

Do not enable or modify rotation in a production environment solely for practice.

---

## 66. Optional CLI Practice

If AWS CLI is configured:

### List KMS Keys

```bash
aws kms list-keys
```

### List Aliases

```bash
aws kms list-aliases
```

### Describe a Key

```bash
aws kms describe-key \
  --key-id alias/example-key
```

### Get Key Policy

```bash
aws kms get-key-policy \
  --key-id alias/example-key \
  --policy-name default
```

### Check Rotation Status

```bash
aws kms get-key-rotation-status \
  --key-id alias/example-key
```

Only use authorized keys in your own environment.

Do not publish real account IDs, key ARNs, or sensitive policies to a public repository.

---

## 67. Optional Envelope Encryption Exercise

Conceptually design an application that encrypts a sensitive file.

Architecture:

```text
Application
    |
    v
GenerateDataKey
    |
    +---------------------+
    |                     |
    v                     v
Plaintext Data Key   Encrypted Data Key
    |
    v
Encrypt File
    |
    v
Delete Plaintext Key
```

Store:

```text
Encrypted File

+

Encrypted Data Key
```

When decrypting:

```text
Encrypted Data Key
       |
       v
KMS Decrypt
       |
       v
Plaintext Data Key
       |
       v
Decrypt File
```

The important concept is:

```text
KMS Key
→ Protects Data Key

Data Key
→ Protects Data
```

---

## 68. Security Checklist

```text
[ ] Appropriate KMS key type is selected

[ ] Customer managed keys are used where granular control is required

[ ] Key administrators are identified

[ ] Key users are identified

[ ] Key administration and usage are separated

[ ] Key policies follow least privilege

[ ] IAM policies follow least privilege

[ ] Applications do not receive kms:* unnecessarily

[ ] Applications only access required KMS keys

[ ] Grants are appropriately restricted

[ ] Encryption context is used where appropriate

[ ] Sensitive information is not stored in encryption context

[ ] Key aliases are clearly defined

[ ] Key rotation requirements are documented

[ ] Key dependencies are documented

[ ] Key deletion permissions are highly restricted

[ ] KMS API activity is logged with CloudTrail

[ ] Important KMS changes are monitored

[ ] Multi-Region keys are used only when required
```

---

## Key Takeaways

- AWS KMS provides centralized management of cryptographic keys.
- Customer managed keys provide the greatest level of customer control.
- AWS managed keys are created and managed by AWS services in the customer's account.
- AWS owned keys are managed entirely by AWS and are not customer KMS resources.
- Symmetric encryption keys are commonly used by AWS service integrations.
- Envelope encryption uses a KMS key to protect data keys.
- Data keys perform the actual encryption of application data.
- Every KMS key has a key policy.
- KMS access may involve key policies, IAM policies, and grants.
- Key administrators and key users should be separated.
- KMS permissions should follow least privilege.
- Aliases provide friendly names for KMS keys.
- Disabling or deleting a KMS key can affect access to encrypted data.
- Key rotation changes cryptographic material without changing the logical KMS key identity.
- Multi-Region keys support specific cross-Region cryptographic use cases.
- CloudTrail provides visibility into KMS management and cryptographic operations.
- Key management affects both data confidentiality and system availability.

---

## Reflection

Today I learned that AWS KMS is not simply an encryption service but a centralized key management and access control system.

The most important concept is envelope encryption. A KMS key generally protects a data key, while the data key performs the actual encryption of application data.

I also learned that key ownership models provide different levels of control. Customer managed keys provide granular control over key policies, permissions, lifecycle, and rotation, while AWS managed and AWS owned keys reduce management responsibility.

From a security engineering perspective, KMS permissions should be treated carefully because access to a KMS key may determine whether sensitive data can be decrypted.

Key administration and key usage should therefore be separated, permissions should follow least privilege, and key lifecycle operations such as disabling or deleting keys should be tightly controlled.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Alias | A friendly name associated with a KMS key |
| AWS Managed Key | A KMS key created and managed by an AWS service in the customer's account |
| AWS Owned Key | A key owned and managed entirely by an AWS service |
| Customer Managed Key | A KMS key created and controlled by the customer |
| Data Key | Cryptographic key material used to encrypt application data |
| Envelope Encryption | Encrypting data with a data key that is protected by another key |
| Grant | A KMS authorization mechanism that delegates specific key permissions |
| Key Policy | A resource policy that controls access to a KMS key |
| Key Rotation | Replacing cryptographic key material while retaining the logical KMS key |
| KMS Key | A logical cryptographic key resource managed by AWS KMS |
