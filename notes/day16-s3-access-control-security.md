# Day 16 — S3 Access Control & Security

## Topic

Amazon S3 Access Control, Bucket Policies, Block Public Access, and Secure Data Access

---

## Objectives

- Understand how Amazon S3 access control works
- Compare IAM policies and bucket policies
- Understand principals, actions, resources, and conditions
- Understand S3 Block Public Access
- Learn the role of Object Ownership and ACLs
- Understand cross-account S3 access
- Apply the Principle of Least Privilege
- Understand S3 Access Points
- Learn how IAM Access Analyzer helps identify external access
- Identify common S3 security misconfigurations

---

## 1. S3 Access Control Overview

Amazon S3 supports multiple access control mechanisms.

Common mechanisms include:

```text
IAM Policies

Bucket Policies

Block Public Access

Object Ownership

ACLs

S3 Access Points
```

A secure S3 design should use these controls together.

Conceptually:

```text
Identity
   ↓
IAM Policy
   ↓
S3 Resource
   ↑
Bucket Policy
   ↑
Block Public Access
```

The final access decision depends on all applicable policies and controls.

---

## 2. Identity-Based Policies

Identity-based policies are attached to IAM identities.

They can be attached to:

```text
IAM User

IAM Group

IAM Role
```

Example:

```text
Application Role
      ↓
IAM Policy
      ↓
Amazon S3
```

The policy defines what the identity is allowed to do.

---

## 3. Identity-Based Policy Example

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::application-data/*"
    }
  ]
}
```

This allows:

```text
s3:GetObject
```

on objects inside:

```text
application-data
```

It does not automatically grant:

```text
s3:PutObject

s3:DeleteObject
```

This is an example of least-privilege access.

---

## 4. Bucket Policies

A bucket policy is a resource-based policy attached directly to an S3 bucket.

Conceptually:

```text
S3 Bucket
   ↓
Bucket Policy
```

A bucket policy can define:

```text
Principal

Action

Resource

Condition

Effect
```

Bucket policies are useful for:

- Cross-account access
- AWS service access
- Restricting network access
- Requiring secure transport
- Limiting access based on conditions

---

## 5. Bucket Policy Structure

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
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::application-data/*"
    }
  ]
}
```

Important elements:

```text
Effect
→ Allow or Deny

Principal
→ Who receives access

Action
→ What operation is allowed

Resource
→ Which S3 resource

Condition
→ Optional restrictions
```

---

## 6. IAM Policy vs Bucket Policy

The major difference is where the policy is attached.

### IAM Policy

```text
Identity
   ↓
Policy
   ↓
Resource
```

Attached to:

```text
User

Group

Role
```

### Bucket Policy

```text
Bucket
   ↓
Policy
   ↓
Principal
```

Attached directly to the S3 bucket.

A useful mental model:

```text
IAM Policy
→ What can this identity access?

Bucket Policy
→ Who can access this bucket?
```

---

## 7. Principal

The `Principal` identifies who can access the resource.

Examples may include:

```text
AWS Account

IAM Role

IAM User

AWS Service
```

Example:

```json
"Principal": {
  "AWS": "arn:aws:iam::111122223333:role/SecurityRole"
}
```

This identifies a specific role.

---

## 8. Avoid Public Principals

A bucket policy can use:

```json
"Principal": "*"
```

This represents a very broad principal.

Depending on the policy and Block Public Access settings, this may create public access.

Example risk:

```text
Principal: *

Action: s3:GetObject
```

This could expose objects publicly.

Public access should only be configured for an explicit and verified use case.

---

## 9. S3 Resource ARNs

Bucket and object ARNs are different.

Bucket:

```text
arn:aws:s3:::example-bucket
```

Objects:

```text
arn:aws:s3:::example-bucket/*
```

This distinction is important.

Example:

```text
s3:ListBucket
```

typically uses:

```text
Bucket ARN
```

while:

```text
s3:GetObject
```

uses:

```text
Object ARN
```

---

## 10. Example — List and Read Permission

Example policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:ListBucket",
      "Resource": "arn:aws:s3:::application-data"
    },
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::application-data/*"
    }
  ]
}
```

This allows:

```text
List bucket contents

Read objects
```

but does not allow:

```text
Delete objects

Upload objects
```

---

## 11. Principle of Least Privilege

S3 permissions should grant only the required actions.

Poor example:

```text
Action:
s3:*

Resource:
*
```

Better:

```text
Action:
s3:GetObject

Resource:
arn:aws:s3:::application-data/*
```

Even better access control may include:

```text
Required Actions

Required Resources

Required Conditions
```

---

## 12. Explicit Deny

Explicit Deny is a powerful security control.

Example:

```json
{
  "Effect": "Deny",
  "Principal": "*",
  "Action": "s3:*",
  "Resource": [
    "arn:aws:s3:::example-bucket",
    "arn:aws:s3:::example-bucket/*"
  ]
}
```

An applicable explicit Deny overrides an Allow.

This can be used to enforce security requirements.

---

## 13. Require HTTPS

A bucket policy can deny access when secure transport is not used.

Conceptually:

```text
HTTP Request
→ Deny

HTTPS Request
→ Allowed if other permissions allow it
```

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Principal": "*",
      "Action": "s3:*",
      "Resource": [
        "arn:aws:s3:::example-bucket",
        "arn:aws:s3:::example-bucket/*"
      ],
      "Condition": {
        "Bool": {
          "aws:SecureTransport": "false"
        }
      }
    }
  ]
}
```

This can enforce encrypted transport.

---

## 14. Block Public Access

S3 Block Public Access provides controls that help prevent unintended public access.

Conceptually:

```text
Bucket Policy / ACL
        ↓
Block Public Access
        ↓
Public Access Prevented
```

Block Public Access can be configured at different scopes, including:

```text
Organization

AWS Account

Bucket

Access Point
```

More restrictive effective settings can prevent public access even when a policy or ACL attempts to grant it.

---

## 15. Why Block Public Access Matters

Consider:

```text
Sensitive Bucket
     ↓
Accidental Public Policy
     ↓
Internet Exposure
```

Block Public Access adds another control:

```text
Sensitive Bucket
     ↓
Accidental Public Policy
     ↓
Block Public Access
     ↓
Access Blocked
```

This helps reduce accidental public exposure.

---

## 16. Secure Default

A good default for most S3 workloads is:

```text
Block Public Access
→ Enabled
```

Then explicitly grant only required private access.

Conceptually:

```text
Private by Default
      ↓
Grant Required Access
```

instead of:

```text
Public by Default
      ↓
Try to Restrict Access
```

---

## 17. Public Access Use Cases

Some workloads may intentionally require public content.

Examples could include:

```text
Public Static Content

Public Downloads
```

However, public S3 bucket access should be carefully evaluated.

Alternative architectures may use services such as:

```text
Amazon CloudFront
```

in front of private S3 content.

The architecture should minimize unnecessary direct bucket exposure.

---

## 18. Object Ownership

S3 Object Ownership helps control ownership and ACL behavior.

Modern S3 configurations commonly use:

```text
Bucket owner enforced
```

With this model:

```text
ACLs Disabled

Bucket Owner Owns Objects

Permissions Managed Through Policies
```

This simplifies access management.

---

## 19. Why Disable ACLs?

ACLs are an older S3 access control mechanism.

Using many access control systems simultaneously can make permissions harder to understand.

Example:

```text
IAM Policy
+
Bucket Policy
+
Object ACL
+
Bucket ACL
```

This can increase complexity.

A simpler model is often:

```text
IAM Policies
+
Bucket Policies
```

with ACLs disabled.

---

## 20. Access Control Lists

ACLs can grant permissions to buckets and objects.

Historically they were used for scenarios such as:

```text
Object Ownership

Cross-Account Object Access

Public Access
```

However, modern S3 security design usually prefers policy-based access where possible.

ACLs should only be used when a specific requirement exists.

---

## 21. Cross-Account Access

S3 can be accessed across AWS accounts.

Example:

```text
Account A
Application Role
      ↓
      ↓ Cross-Account
      ↓
Account B
S3 Bucket
```

For cross-account access, permissions generally need to exist on both sides.

---

## 22. Cross-Account Permission Model

Conceptually:

```text
Account A

IAM Role
   ↓
Identity Policy
   ↓
Allow S3 Access

        +

Account B

S3 Bucket
   ↓
Bucket Policy
   ↓
Trust Account A Role
```

Both sides must allow the request.

---

## 23. Cross-Account Example

Account A role:

```text
arn:aws:iam::111122223333:role/SecurityRole
```

Bucket in Account B:

```text
security-logs
```

Bucket policy concept:

```json
{
  "Effect": "Allow",
  "Principal": {
    "AWS": "arn:aws:iam::111122223333:role/SecurityRole"
  },
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::security-logs/*"
}
```

The role in Account A must also have identity permissions allowing the required S3 action.

---

## 24. Access Conditions

Bucket policies can apply conditions.

Examples include:

```text
Secure Transport

Source IP

VPC Endpoint

Principal ARN

Resource Tags
```

Conditions can reduce the scope of access.

Conceptually:

```text
Allow Action

Only If

Condition Matches
```

---

## 25. Restrict Access to a VPC Endpoint

A bucket can be configured so requests must come through an approved VPC endpoint.

Conceptually:

```text
Private Workload
      ↓
VPC Endpoint
      ↓
S3 Bucket
```

Bucket policy:

```text
Allow required access
only through approved endpoint
```

This can reduce reliance on public network paths.

---

## 26. S3 Access Points

S3 Access Points provide additional ways to manage access to shared S3 data.

Conceptually:

```text
Bucket
│
├── Application A Access Point
│
├── Application B Access Point
│
└── Analytics Access Point
```

Each access point can have its own policy.

This can simplify access management for large shared buckets.

---

## 27. Access Point Example

Suppose one bucket contains:

```text
Company Data
```

Several applications need different access.

Instead of one complex bucket policy:

```text
Bucket
└── Large Policy
```

use:

```text
Bucket
│
├── App-A Access Point
│     └── App-A Policy
│
├── App-B Access Point
│     └── App-B Policy
│
└── Analytics Access Point
      └── Analytics Policy
```

This can improve manageability.

---

## 28. VPC-Restricted Access Point

An S3 Access Point can be configured for VPC-only access.

Conceptually:

```text
VPC
 ↓
S3 Access Point
 ↓
S3 Bucket
```

This can restrict data access to a private network path.

It is useful for workloads that should not access the data through general Internet paths.

---

## 29. IAM Access Analyzer for S3

IAM Access Analyzer can help identify external access to S3 buckets.

It can detect access granted to:

```text
Public Internet

External AWS Accounts

Other Principals Outside the Zone of Trust
```

Possible access sources include:

```text
Bucket Policy

ACL

Access Point Policy

Multi-Region Access Point Policy
```

---

## 30. Access Analyzer Security Workflow

Conceptually:

```text
S3 Configuration
      ↓
IAM Access Analyzer
      ↓
External Access Finding
      ↓
Review
      ↓
Confirm or Remediate
```

Questions include:

```text
Was this external access intentional?

Is the principal trusted?

Is the permission broader than necessary?
```

---

## 31. Access Analyzer Is Not an Automatic Fix

A finding does not automatically mean:

```text
Security Incident
```

It means:

```text
External Access Exists
```

The security engineer should determine whether the access is:

```text
Expected

or

Unexpected
```

Then take appropriate action.

---

## 32. Common Misconfiguration — Public Read

Risky bucket policy:

```text
Principal: *

Action: s3:GetObject
```

This can make objects publicly readable if other controls do not block it.

Potential exposure:

```text
Backups

Logs

Internal Documents

Customer Data
```

Always verify whether public access is truly required.

---

## 33. Common Misconfiguration — Public Write

Even more dangerous:

```text
Principal: *

Action: s3:PutObject
```

This could allow unauthorized uploads.

Potential risks include:

- Malicious file upload
- Storage abuse
- Unexpected costs
- Content poisoning

Public write access should be avoided unless there is an exceptional, carefully controlled requirement.

---

## 34. Common Misconfiguration — Wildcard Permissions

Risky:

```text
Action:
s3:*

Resource:
*
```

This may allow:

```text
Read

Write

Delete

Bucket Management
```

across many S3 resources.

Permissions should be narrowed.

---

## 35. Common Misconfiguration — Incorrect Resource ARN

Example:

```text
Action:
s3:GetObject

Resource:
arn:aws:s3:::example-bucket
```

This targets the bucket itself rather than the objects.

Correct object scope:

```text
arn:aws:s3:::example-bucket/*
```

Bucket and object permissions must use the appropriate ARN.

---

## 36. Common Misconfiguration — ACL Complexity

A bucket may appear secure through IAM policies but still have unexpected ACL access.

Example:

```text
IAM Policy
→ Restricted

Bucket Policy
→ Restricted

Object ACL
→ External Access
```

This is one reason simplifying access control and disabling unnecessary ACL usage can improve security.

---

## 37. Common Misconfiguration — Cross-Account Access Left Behind

A bucket may have previously required access from another AWS account.

Later, that relationship may no longer be required.

Example:

```text
Old Partner Account
      ↓
Bucket Policy
      ↓
Still Allowed
```

Unused cross-account access should be removed.

---

## 38. Common Misconfiguration — No Secure Transport Enforcement

If an application does not enforce HTTPS, data may be transmitted insecurely.

A bucket policy can deny requests where:

```text
aws:SecureTransport = false
```

This helps enforce TLS.

---

## 39. Common Misconfiguration — Overly Broad VPC Access

Example:

```text
Entire VPC
→ Access all bucket objects
```

when only one application requires access.

A better design might use:

```text
Application Role

+

Specific S3 Access Point

+

Required Prefix
```

for more granular control.

---

## 40. Prefix-Level Access

Permissions can be limited to specific object paths.

Example:

```text
Bucket:
company-data
```

Objects:

```text
finance/

security/

marketing/
```

Security application needs:

```text
security/*
```

Policy can restrict access to:

```text
arn:aws:s3:::company-data/security/*
```

instead of the entire bucket.

---

## 41. Application Access Example

Suppose an EC2 application only needs to read:

```text
application-data/config/*
```

Secure model:

```text
EC2
 ↓
IAM Role
 ↓
s3:GetObject
 ↓
application-data/config/*
```

Not:

```text
EC2
 ↓
s3:*
 ↓
*
```

---

## 42. Logging Bucket Example

Suppose CloudTrail writes logs to S3.

Conceptually:

```text
CloudTrail
   ↓
S3 Logging Bucket
```

The bucket should:

```text
Allow CloudTrail delivery

Restrict unrelated writes

Block public access

Protect stored logs
```

Security logs should have stronger protection because attackers may attempt to modify or delete evidence.

---

## 43. Security Policy Layers

A useful S3 security model is:

```text
Organization Controls
        ↓
Account Controls
        ↓
Block Public Access
        ↓
Bucket Policy
        ↓
IAM Policy
        ↓
Access Point Policy
        ↓
Object Access
```

All applicable security controls should be considered.

---

## 44. Policy Evaluation Questions

When investigating S3 access, ask:

```text
Who is the Principal?

Which Action is requested?

Which Resource is accessed?

What does the IAM policy allow?

What does the bucket policy allow?

Is there an Explicit Deny?

Does Block Public Access apply?

Are ACLs enabled?

Is an Access Point involved?

Is the request cross-account?

Are policy Conditions satisfied?
```

---

## 45. Troubleshooting AccessDenied

Suppose:

```text
Application
→ S3
→ AccessDenied
```

Use a systematic process.

### Step 1

Identify:

```text
Principal
```

### Step 2

Identify:

```text
Action
```

Example:

```text
s3:GetObject
```

### Step 3

Identify:

```text
Resource ARN
```

### Step 4

Check:

```text
IAM Policy
```

### Step 5

Check:

```text
Bucket Policy
```

### Step 6

Check:

```text
Block Public Access
```

### Step 7

Check:

```text
KMS permissions
```

if SSE-KMS is involved.

### Step 8

Check:

```text
Cross-account configuration
```

if applicable.

---

## 46. Encryption and Access Control

Encryption does not replace access control.

Example:

```text
Encrypted S3 Object
+
Public Read Permission
```

can still expose data through authorized decryption paths depending on configuration.

Security requires:

```text
Access Control

+

Encryption
```

not one or the other.

---

## 47. SSE-KMS Permission Consideration

Objects encrypted with SSE-KMS introduce additional permission requirements.

Conceptually:

```text
Identity
 ↓
S3 Permission
 ↓
KMS Permission
 ↓
Encrypted Object
```

The principal may need both:

```text
S3 Access

and

KMS Key Access
```

depending on the operation.

This provides an additional control layer.

---

## 48. Defense in Depth for S3

A secure S3 architecture might use:

```text
Block Public Access

+

Least-Privilege IAM Role

+

Bucket Policy

+

Encryption

+

Versioning

+

Access Analyzer

+

Logging
```

No single control should be the only protection.

---

## 49. Example Secure Architecture

```text
Private EC2
    ↓
IAM Role
    ↓
VPC Endpoint
    ↓
S3 Access Point
    ↓
Private S3 Bucket
    │
    ├── Block Public Access
    ├── Bucket Policy
    ├── Versioning
    └── Encryption
```

This architecture minimizes public exposure and limits application permissions.

---

## 50. Hands-on Practice

For today's practice, open the S3 console and review one bucket.

Check:

```text
Permissions

Block Public Access

Bucket Policy

Object Ownership

ACL

Access Points
```

Ask:

```text
Can this bucket be accessed publicly?

Which identities can access it?

Are ACLs enabled?

Is the bucket policy required?

Could the policy be more restrictive?
```

---

## 51. Optional Policy Practice

Create a sample policy that allows only read access to one test prefix.

Example requirement:

```text
Bucket:
cloud-security-lab

Allowed Prefix:
reports/*
```

Required action:

```text
s3:GetObject
```

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::cloud-security-lab/reports/*"
    }
  ]
}
```

Do not use real sensitive bucket names or account information in GitHub examples.

---

## 52. Security Review Checklist

When reviewing S3 access control, ask:

```text
Is Block Public Access enabled?

Is public access actually required?

Does the bucket policy use Principal: *?

Are IAM permissions least-privilege?

Are wildcard actions required?

Are resource ARNs correct?

Is cross-account access still required?

Are ACLs necessary?

Is Object Ownership configured appropriately?

Are access conditions being used?

Can access be restricted through a VPC endpoint?

Would an S3 Access Point simplify access management?

Does IAM Access Analyzer show external access?

Is HTTPS enforced?

Are SSE-KMS permissions correctly restricted?
```

---

## Key Takeaways

- S3 access can be controlled through identity-based and resource-based policies.
- IAM policies define what identities can access.
- Bucket policies define access directly on S3 resources.
- Block Public Access helps prevent unintended public exposure.
- Public access should only exist for explicit use cases.
- Object Ownership can simplify access control by disabling ACL-based permissions.
- ACLs should generally be avoided unless a specific requirement exists.
- Cross-account access typically requires permissions on both the requesting identity and the target resource.
- Access Points can simplify access management for shared buckets.
- IAM Access Analyzer can identify public and external S3 access.
- Least privilege should be applied to actions, resources, principals, and conditions.
- Explicit Deny can enforce important security requirements.
- Encryption and access control should be used together.

---

## Reflection

Today I learned that S3 access control can involve multiple policy layers.

IAM policies control what an identity is allowed to do, while bucket policies control access directly on the S3 resource.

I also learned that Block Public Access provides an important guardrail against unintended public exposure and should remain enabled unless public access is explicitly required.

Modern S3 configurations can simplify permission management by using Object Ownership with ACLs disabled and relying mainly on policy-based access control.

For cross-account and shared-data environments, S3 Access Points and IAM Access Analyzer can help manage and review access more systematically.

The most important lesson is that S3 access should be private by default and permissions should be granted only to the identities, actions, and resources that actually require them.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Access Point | A dedicated S3 access endpoint with its own access policy |
| ACL | An older access control mechanism for S3 buckets and objects |
| Block Public Access | S3 controls that prevent unintended public access |
| Bucket Policy | A resource-based policy attached to an S3 bucket |
| Cross-Account Access | Access to a resource from a principal in another AWS account |
| External Access | Access granted outside the defined trusted account or organization |
| Object Ownership | S3 settings that control object ownership and ACL behavior |
| Principal | The identity or entity receiving access in a resource policy |
