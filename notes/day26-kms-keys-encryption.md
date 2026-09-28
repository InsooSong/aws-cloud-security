# Day 26 — KMS Keys & Encryption

## Topic

AWS KMS Cryptographic Operations, Key Policies, Grants, Cross-Account Access, and Service Integration

---

## Objectives

- Understand the difference between Encrypt and GenerateDataKey
- Understand the Decrypt operation
- Understand envelope encryption in detail
- Understand encryption context
- Learn how encryption context can restrict permissions
- Understand Key Policies and IAM Policies
- Understand KMS Grants
- Understand cross-account KMS access
- Learn how kms:ViaService works
- Understand ReEncrypt
- Review KMS integration with EBS, S3, and RDS
- Understand CloudTrail auditing for KMS
- Identify common KMS security misconfigurations

---

# Cryptographic Operations

## 1. Encrypt

The AWS KMS Encrypt operation encrypts small amounts of plaintext directly using a KMS key.

Conceptually:

```text
Plaintext
   |
   v
AWS KMS Encrypt
   |
   v
KMS Key
   |
   v
Ciphertext
```

The Encrypt API supports plaintext up to:

```text
4,096 bytes
```

Therefore, Encrypt is appropriate for relatively small pieces of sensitive data.

Examples:

```text
Small Secret

Identifier

Short Configuration Value
```

For large files or application datasets, envelope encryption should normally be used instead.

---

## 2. Why Not Encrypt Large Data Directly?

AWS KMS is primarily a key management system.

It is not intended to directly encrypt large application files.

Poor design:

```text
10 GB File
   |
   v
KMS Encrypt
```

This will not work because the Encrypt API has a small plaintext size limit.

Better:

```text
Large File
   |
   v
Data Key
   |
   v
Local Encryption
```

while:

```text
KMS Key
   |
   v
Protect Data Key
```

This is envelope encryption.

---

## 3. GenerateDataKey

GenerateDataKey creates a unique symmetric data key.

It returns:

```text
Plaintext Data Key

+

Encrypted Data Key
```

Conceptually:

```text
Application
     |
     v
GenerateDataKey
     |
     v
AWS KMS
     |
     +-----------------------+
     |                       |
     v                       v
Plaintext Data Key     Encrypted Data Key
```

The plaintext data key is used to encrypt application data.

The encrypted copy is stored for later use.

---

## 4. GenerateDataKey Workflow

Example:

```text
1. Application calls GenerateDataKey.

2. AWS KMS creates a data key.

3. AWS KMS returns:

   Plaintext Data Key

   Encrypted Data Key

4. Application encrypts data locally.

5. Application deletes the plaintext data key from memory.

6. Application stores:

   Encrypted Data

   +

   Encrypted Data Key
```

Conceptually:

```text
KMS Key
   |
   v
Encrypted Data Key
        |
        v
Stored with
        |
        v
Encrypted Application Data
```

---

## 5. Plaintext Data Key

The plaintext data key should exist only as long as needed.

Conceptually:

```text
GenerateDataKey
      |
      v
Plaintext Data Key
      |
      v
Encrypt Data
      |
      v
Erase from Memory
```

It should not normally be stored permanently.

Poor design:

```text
Encrypted File
+
Plaintext Data Key
```

This defeats the purpose of encryption.

---

## 6. Encrypted Data Key

The encrypted data key can be safely stored with the encrypted application data.

Example:

```text
encrypted-file.bin

encrypted-data-key.bin
```

The encrypted data key cannot be used directly until AWS KMS decrypts it.

---

## 7. Decrypt

The Decrypt operation uses a KMS key to decrypt ciphertext that was protected by KMS.

For envelope encryption, Decrypt normally decrypts:

```text
Encrypted Data Key
```

rather than the large application data itself.

Conceptually:

```text
Encrypted Data
+
Encrypted Data Key
        |
        v
KMS Decrypt
        |
        v
Plaintext Data Key
        |
        v
Decrypt Application Data
```

After decryption:

```text
Plaintext Data Key
→ Remove from memory
```

---

## 8. Envelope Encryption

The complete encryption flow is:

```text
                   AWS KMS
                      |
                      v
                GenerateDataKey
                      |
             +--------+--------+
             |                 |
             v                 v
      Plaintext Key      Encrypted Key
             |
             v
      Encrypt Data
             |
             v
      Encrypted Data
             |
             +---------+
                       |
                       v
              Store Together

Encrypted Data
+
Encrypted Data Key
```

The KMS key never needs to directly process the large application data.

---

## 9. Envelope Decryption

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
Encrypted Application Data
       |
       v
Plaintext Application Data
```

After use:

```text
Plaintext Data Key
→ Remove from memory
```

---

# Encryption Context

## 10. What Is Encryption Context?

Encryption Context is a set of non-secret key-value pairs that can be included with supported symmetric KMS cryptographic operations.

Example:

```text
AppName = PaymentService

Environment = Production
```

Conceptually:

```text
Data
+
Encryption Context
       |
       v
AWS KMS
       |
       v
Ciphertext
```

The encryption context becomes cryptographically associated with the ciphertext.

---

## 11. Encryption Context as AAD

AWS KMS uses encryption context as:

```text
Additional Authenticated Data
```

or:

```text
AAD
```

It is not itself encrypted.

Instead, it is cryptographically bound to the encrypted data.

If encryption uses:

```text
AppName = PaymentService
```

then decryption must use the same encryption context.

---

## 12. Encryption Context Must Match

Example encryption:

```text
AppName = ExampleApp
```

Decrypt with:

```text
AppName = ExampleApp
```

Result:

```text
Success
```

But:

```text
AppName = OtherApp
```

may result in:

```text
Decrypt Failure
```

The encryption context must match exactly for supported cryptographic operations.

---

## 13. Encryption Context Is Not Secret

Very important:

```text
Encryption Context
≠
Secret
```

Encryption context values may appear in CloudTrail.

Therefore, never put:

```text
Password

API Token

Credit Card Number

Private Personal Data
```

inside encryption context.

Better:

```text
Application = Billing

Environment = Production

ResourceType = Backup
```

---

## 14. Encryption Context Example

A security application encrypts data with:

```json
{
  "AppName": "SecurityPortal",
  "Environment": "Production"
}
```

Conceptually:

```text
Sensitive Data
+
SecurityPortal
+
Production
       |
       v
Encryption
```

To decrypt:

```text
AppName = SecurityPortal

Environment = Production
```

must be provided again.

---

## 15. Encryption Context in Policies

Encryption context can also be used as an authorization condition.

Example requirement:

```text
ApplicationRole

may decrypt only when

AppName = SecurityPortal
```

Key policy example:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111122223333:role/ApplicationRole"
  },
  "Action": "kms:Decrypt",
  "Resource": "*",
  "Condition": {
    "StringEquals": {
      "kms:EncryptionContext:AppName": "SecurityPortal"
    }
  }
}
```

This combines:

```text
Identity

+

Cryptographic Context
```

for stronger access control.

---

# Key Policy

## 16. Key Policy Review

Every KMS key has exactly one Key Policy.

Conceptually:

```text
KMS Key
   |
   v
Key Policy
   |
   v
Access Decision
```

The Key Policy is the primary resource policy controlling access to the KMS key.

---

## 17. IAM Policy Is Not Always Enough

For KMS, an IAM Allow does not automatically mean access is permitted.

Conceptually:

```text
IAM Policy
Allow kms:Decrypt
       |
       X
       |
Key Policy does not permit IAM delegation
```

Result:

```text
Access Denied
```

The key policy must support the intended authorization model.

---

## 18. Enabling IAM Policies

A common key policy pattern allows the AWS account to use IAM policies for KMS access management.

Conceptually:

```text
Key Policy
      |
      v
Enable IAM Delegation
      |
      v
IAM Role Policy
      |
      v
KMS Access
```

This allows IAM administrators to delegate permitted KMS operations.

---

## 19. Key Administrator

Example responsibilities:

```text
Create Alias

Update Key Policy

Enable Key

Disable Key

Configure Rotation

Schedule Key Deletion
```

Key administrators should not automatically receive:

```text
kms:Decrypt
```

unless required.

---

## 20. Key User

A key user may need:

```text
kms:Encrypt

kms:Decrypt

kms:GenerateDataKey

kms:DescribeKey
```

depending on the application.

A key user normally should not need:

```text
kms:ScheduleKeyDeletion

kms:PutKeyPolicy
```

---

## 21. Separation of Duties

A secure design separates:

```text
Key Administrator
       |
       v
Manage Key

Application
       |
       v
Use Key
```

This means compromising the application does not automatically allow the attacker to:

```text
Delete Key

Disable Key

Change Key Policy
```

---

# KMS Grants

## 22. What Is a Grant?

A KMS Grant is another authorization mechanism.

Conceptually:

```text
KMS Key
   |
   v
Grant
   |
   v
Grantee Principal
   |
   v
Specific Operations
```

Grants are evaluated together with:

```text
Key Policies

IAM Policies
```

---

## 23. Why Use Grants?

Grants are useful when permissions are needed temporarily or dynamically.

Example:

```text
AWS Service
     |
     v
Create Grant
     |
     v
Perform Encryption Operation
     |
     v
Retire Grant
```

AWS services integrated with KMS frequently use grants.

---

## 24. Example Grant Operations

A grant can allow selected operations such as:

```text
Encrypt

Decrypt

GenerateDataKey

ReEncrypt

DescribeKey
```

The exact operations depend on the use case.

---

## 25. Grant Constraints

Grants can include constraints.

Example:

```text
EncryptionContextEquals
```

or:

```text
EncryptionContextSubset
```

Conceptually:

```text
Grant
 |
 +-- Principal
 |
 +-- Operations
 |
 +-- Encryption Context Constraint
```

This makes the grant more restrictive.

---

# ReEncrypt

## 26. What Is ReEncrypt?

ReEncrypt allows ciphertext encrypted under one KMS key to be re-encrypted under another KMS key.

Conceptually:

```text
Ciphertext
Encrypted by Key A
        |
        v
AWS KMS ReEncrypt
        |
        v
Ciphertext
Encrypted by Key B
```

This avoids requiring the application to directly handle the plaintext between separate Decrypt and Encrypt operations.

---

## 27. ReEncrypt Use Case

Example:

```text
Old KMS Key

        ↓

Encrypted Data

        ↓

ReEncrypt

        ↓

New KMS Key
```

Possible use cases:

```text
Key Migration

Cross-Account Architecture

Changing Encryption Ownership
```

---

# Cross-Account KMS

## 28. Cross-Account KMS Access

A KMS key in Account A may be used by an authorized principal in Account B.

Conceptually:

```text
Account B
Application Role
       |
       v
Account A
KMS Key
```

This requires permissions on both sides.

---

## 29. Cross-Account Permission Model

### Account A — Key Owner

Key policy must allow the external account or principal.

```text
KMS Key Policy
→ Allow Account B
```

### Account B — Caller

IAM policy must grant the role permission to use the key.

```text
Application Role
→ IAM Policy
→ Allow KMS Operation
```

Therefore:

```text
Key Policy
+
IAM Policy
=
Cross-Account Access
```

Neither side alone is sufficient.

---

## 30. Cross-Account Example

Account A owns:

```text
arn:aws:kms:ap-northeast-1:111122223333:key/example
```

Account B role:

```text
arn:aws:iam::444455556666:role/ApplicationRole
```

Key policy concept:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::444455556666:role/ApplicationRole"
  },
  "Action": [
    "kms:Decrypt",
    "kms:DescribeKey"
  ],
  "Resource": "*"
}
```

Account B must also grant its role the corresponding IAM permissions.

---

## 31. Cross-Account Limitations

Not every KMS administrative action works cross-account.

Cross-account access is primarily intended for operations such as:

```text
Cryptographic Operations

CreateGrant

DescribeKey

Grant Management
```

Granting an external principal actions such as:

```text
ScheduleKeyDeletion
```

does not make those cross-account administrative operations valid.

---

# kms:ViaService

## 32. What Is kms:ViaService?

`kms:ViaService` is a KMS condition key that can limit key usage to requests coming through a specific AWS service.

Conceptually:

```text
Application Role
      |
      v
Amazon EBS
      |
      v
AWS KMS
```

Policy condition:

```text
Allow key use
only through EBS
```

---

## 33. ViaService Example

Conceptual condition:

```json
{
  "Condition": {
    "StringEquals": {
      "kms:ViaService": "ec2.ap-northeast-1.amazonaws.com"
    }
  }
}
```

This can limit KMS usage to supported requests coming through Amazon EBS in the specified Region.

---

## 34. Why ViaService Is Useful

Without the condition:

```text
Application Role
→ Direct KMS Decrypt
```

may be allowed.

With:

```text
kms:ViaService = EBS
```

the intent can become:

```text
Application Role
→ Use Key only through EBS
```

This reduces unnecessary direct KMS usage.

---

## 35. ViaService and Least Privilege

A useful model is:

```text
Principal
   +
KMS Key
   +
Required Operation
   +
Required AWS Service
```

Example:

```text
ApplicationRole

can use

ProductionKey

only through

Amazon RDS
```

This provides stronger contextual authorization.

---

# AWS Service Integration

## 36. EBS Integration

From Day 17:

```text
EC2
 ↓
Encrypted EBS
 ↓
AWS KMS
```

EBS may use KMS operations such as:

```text
GenerateDataKey

Decrypt

CreateGrant
```

internally as part of encryption workflows.

Applications do not normally need to perform low-level disk encryption themselves.

---

## 37. S3 SSE-KMS

S3 can encrypt objects using SSE-KMS.

Conceptually:

```text
Application
      |
      v
Amazon S3
      |
      v
SSE-KMS
      |
      v
KMS Key
```

Permissions may involve:

```text
S3 Permission

+

KMS Permission
```

Example:

```text
s3:GetObject

+

kms:Decrypt
```

depending on the operation.

---

## 38. S3 Security Example

Application needs to read:

```text
s3://production-data/reports/*
```

Encrypted using:

```text
ProductionDataKey
```

The application should receive:

```text
s3:GetObject

on required prefix
```

and:

```text
kms:Decrypt

on ProductionDataKey
```

not:

```text
s3:*

kms:*
```

---

## 39. RDS Integration

RDS can use KMS for encryption at rest.

Conceptually:

```text
RDS
 ↓
Encrypted Storage
 ↓
KMS Key
```

Customer access to database records normally occurs through the database service.

Applications generally do not call:

```text
kms:Decrypt
```

for every database query.

The integrated AWS service performs the required KMS operations as part of its encryption architecture.

---

## 40. Service Integration Mental Model

A very important distinction:

```text
Direct KMS Application

Application
→ KMS API
```

versus:

```text
Integrated AWS Service

Application
→ AWS Service
→ KMS
```

These require different authorization designs.

---

# CloudTrail Auditing

## 41. KMS and CloudTrail

KMS API operations can be recorded through CloudTrail.

Important operations include:

```text
Encrypt

Decrypt

GenerateDataKey

ReEncrypt

CreateGrant

DisableKey

ScheduleKeyDeletion

PutKeyPolicy
```

Conceptually:

```text
KMS Operation
      |
      v
CloudTrail
      |
      v
Audit Record
```

---

## 42. Cryptographic vs Administrative Events

### Cryptographic Operations

```text
Encrypt

Decrypt

GenerateDataKey

ReEncrypt
```

Question:

```text
Who used the key?
```

### Administrative Operations

```text
PutKeyPolicy

DisableKey

ScheduleKeyDeletion

EnableKey
```

Question:

```text
Who changed the key?
```

Both are security relevant.

---

## 43. Monitoring Sensitive KMS Events

Potential high-value monitoring events include:

```text
DisableKey

ScheduleKeyDeletion

PutKeyPolicy

CreateGrant

RevokeGrant
```

Unexpected events should be investigated.

Example:

```text
ScheduleKeyDeletion
        |
        v
CloudTrail
        |
        v
Detection Rule
        |
        v
Security Alert
```

---

# Common Misconfigurations

## 44. Application Has kms:*

Risk:

```text
Application
    |
    v
kms:*
```

This may grant unnecessary administrative and cryptographic permissions.

Better:

```text
Required Operations

+

Specific Key
```

---

## 45. Decrypt Access to Every Key

Poor configuration:

```text
kms:Decrypt

Resource:
*
```

This increases the impact of compromised credentials.

Better:

```text
kms:Decrypt

Resource:
Specific Key ARN
```

---

## 46. No Encryption Context Restriction

Application A and Application B share a key.

Without contextual restrictions:

```text
App A
→ Key

App B
→ Key
```

Both may be able to perform broader cryptographic operations.

Where appropriate, encryption context conditions can add additional restrictions.

---

## 47. Cross-Account Policy Too Broad

Risky:

```text
External Account
→ Broad KMS Access
```

Better:

```text
Required External Role

Required Operations

Required Key

Conditions
```

Cross-account permissions should be reviewed regularly.

---

## 48. Direct KMS Usage When Only Service Access Is Required

Example:

Application only needs an encrypted EBS volume.

Poor design:

```text
Application Role
→ Direct kms:Decrypt
```

even though the use case only requires EBS integration.

Where supported, conditions such as:

```text
kms:ViaService
```

can reduce unnecessary direct key usage.

---

## 49. Sensitive Encryption Context

Poor:

```text
EncryptionContext:

Password = Secret123
```

The encryption context may be logged.

Better:

```text
Application = Billing

Environment = Production
```

---

## 50. Key Administrator Also Has Full Decrypt Access

Risk:

```text
Key Administrator
    |
    +-- PutKeyPolicy
    +-- ScheduleKeyDeletion
    +-- kms:Decrypt
```

This concentrates excessive privilege.

Better separation:

```text
Key Admin
→ Manage

Application / Data Role
→ Use
```

---

# Troubleshooting

## 51. AccessDenied on kms:Decrypt

Check:

```text
Which principal?

Which KMS key?

Is kms:Decrypt allowed?

Does the Key Policy allow the principal?

Does IAM Policy allow the action?

Is an Explicit Deny present?

Is Encryption Context required?

Is kms:ViaService required?

Is the key enabled?

Is cross-account access involved?
```

---

## 52. Encryption Context Error

Problem:

```text
Encrypt:
AppName = AppA

Decrypt:
AppName = AppB
```

Result:

```text
Decrypt Fails
```

Check that the encryption context exactly matches the original encryption operation.

---

## 53. EBS Encryption Failure

Possible checks:

```text
Is the KMS key enabled?

Does EBS have required access?

Does the principal have required permissions?

Does kms:ViaService allow EBS?

Are grants functioning correctly?
```

---

## 54. Cross-Account Failure

Check both:

```text
Key Owner Account
→ Key Policy
```

and:

```text
Caller Account
→ IAM Policy
```

Remember:

```text
One side alone
≠
Cross-Account KMS Access
```

---

# Hands-on Practice

## 55. Practice — Review a Key Policy

Open:

```text
AWS KMS
→ Customer Managed Keys
→ Select Key
→ Key Policy
```

Identify:

```text
Key Administrators

Key Users

Principal

Actions

Conditions
```

Ask:

```text
Who can manage the key?

Who can decrypt data?

Does the application have excessive permissions?
```

Do not modify a production key for practice.

---

## 56. Practice — Review CloudTrail

Open:

```text
CloudTrail
→ Event History
```

Search for available KMS operations.

Examples:

```text
CreateKey

Encrypt

Decrypt

GenerateDataKey

CreateGrant
```

If none exist, review the event structure conceptually.

Identify:

```text
userIdentity

eventName

eventTime

sourceIPAddress

awsRegion
```

---

## 57. Optional CLI Practice

### Encrypt a Small Test File

Create:

```bash
echo -n "cloud-security-test" > plaintext.txt
```

Encrypt:

```bash
aws kms encrypt \
  --key-id alias/example-key \
  --plaintext fileb://plaintext.txt \
  --query CiphertextBlob \
  --output text
```

The returned value is Base64 encoded ciphertext output.

Do not use sensitive data for testing.

---

## 58. Generate a Data Key

Conceptual CLI example:

```bash
aws kms generate-data-key \
  --key-id alias/example-key \
  --key-spec AES_256
```

The response can contain:

```text
Plaintext

CiphertextBlob

KeyId
```

Important:

The plaintext output is sensitive.

Do not:

```text
Save it to GitHub

Paste it into documentation

Leave it in terminal history
```

Use conceptual practice if handling plaintext keys is unnecessary.

---

## 59. Encryption Context CLI Concept

Encryption:

```bash
aws kms encrypt \
  --key-id alias/example-key \
  --plaintext fileb://plaintext.txt \
  --encryption-context AppName=SecurityLab
```

Decryption must use:

```text
AppName=SecurityLab
```

again.

Do not use confidential values as encryption context.

---

# Security Architecture Exercise

## 60. Design Scenario

Application requirements:

```text
Application runs on EC2

Data stored in S3

S3 uses SSE-KMS

Only the application may read data

KMS key should only be used through S3

Cross-account administrators must not decrypt data
```

Possible design:

```text
EC2 Application
      |
      v
IAM Role
      |
      v
Amazon S3
      |
      v
Customer Managed KMS Key
```

Controls:

```text
IAM Role
→ s3:GetObject

KMS Key Policy
→ Application Role

KMS Permission
→ kms:Decrypt

Condition
→ kms:ViaService = S3
```

This combines identity and contextual restrictions.

---

## 61. Cross-Account Design Exercise

Scenario:

```text
Account A
→ Security Log Archive

Account B
→ Security Analysis Application
```

Account B needs to decrypt specific archived data.

Design:

```text
Account A
KMS Key Policy
→ Allow Account B Analysis Role

Account B
IAM Policy
→ Allow kms:Decrypt on Account A key
```

Restrict access to:

```text
Specific Role

Specific Key

Required Operation
```

---

## Security Checklist

```text
[ ] Applications use Encrypt directly only for small data where appropriate

[ ] Large data uses envelope encryption

[ ] GenerateDataKey permissions are restricted

[ ] Plaintext data keys are not stored

[ ] Encryption context does not contain secrets

[ ] Encryption context restrictions are used where appropriate

[ ] Key policies follow least privilege

[ ] IAM policies follow least privilege

[ ] Key administration and usage are separated

[ ] Grants contain only required operations

[ ] Grant constraints are used where appropriate

[ ] Cross-account access requires both key and IAM policies

[ ] Cross-account permissions are reviewed regularly

[ ] kms:ViaService is used where appropriate

[ ] Applications do not receive unnecessary direct KMS access

[ ] Specific KMS key ARNs are used where possible

[ ] Key state and dependencies are monitored

[ ] Sensitive KMS administrative events are monitored

[ ] KMS CloudTrail logs are available for investigation
```

---

## Key Takeaways

- KMS Encrypt directly supports only small plaintext payloads.
- GenerateDataKey is commonly used for envelope encryption.
- GenerateDataKey returns both plaintext and encrypted data keys.
- Plaintext data keys should be removed from memory after use.
- Encryption Context provides additional authenticated contextual information.
- Encryption Context is not secret and may appear in CloudTrail.
- Matching Encryption Context is required when decrypting ciphertext that used it.
- Every KMS key has a Key Policy.
- IAM permission alone might not grant KMS access unless the Key Policy supports it.
- Key administrators and key users should be separated.
- Grants provide delegated KMS permissions without modifying the primary policy.
- ReEncrypt can move ciphertext protection between KMS keys without exposing plaintext to the application.
- Cross-account KMS access requires authorization in both accounts.
- kms:ViaService can restrict key use to requests through supported AWS services.
- AWS services such as EBS, S3, and RDS integrate with KMS differently from direct application KMS calls.
- CloudTrail provides visibility into both cryptographic and administrative KMS activity.
- KMS access should always follow least privilege.

---

## Reflection

Today I learned how applications and AWS services actually interact with AWS KMS.

The most important concept is that KMS is primarily used to protect cryptographic keys rather than directly encrypt large amounts of application data.

GenerateDataKey enables envelope encryption by returning both a plaintext data key and an encrypted copy of that key.

I also learned that Encryption Context can provide additional integrity and authorization controls, but it must never contain secrets because it can appear in CloudTrail.

KMS authorization can involve Key Policies, IAM Policies, Grants, and conditions such as kms:ViaService.

From a security engineering perspective, I should not only ask whether data is encrypted, but also who can use the KMS key, through which service the key can be used, whether cross-account access exists, and whether cryptographic and administrative operations are properly monitored.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AAD | Additional Authenticated Data used to provide integrity and context |
| Cross-Account Access | Access to a KMS key from a principal in another AWS account |
| Cryptographic Operation | An operation such as Encrypt, Decrypt, GenerateDataKey, or ReEncrypt |
| Decrypt | A KMS operation that converts KMS-protected ciphertext into plaintext |
| Encrypt | A KMS operation that converts small plaintext data into ciphertext |
| Encryption Context | Non-secret authenticated information cryptographically associated with ciphertext |
| GenerateDataKey | A KMS operation that creates plaintext and encrypted copies of a data key |
| Grant Constraint | A condition that limits when permissions in a KMS Grant apply |
| ReEncrypt | A KMS operation that re-encrypts ciphertext under another KMS key |
| ViaService | A KMS condition that restricts key usage to requests through specified AWS services |
