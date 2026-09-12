# Day 3 — IAM Users, Groups, Roles & Policies

## Topic

AWS IAM Users, User Groups, Roles, and Policies

---

## Objectives

- Understand IAM users and their use cases
- Understand IAM user groups
- Understand IAM roles and role assumption
- Understand how IAM policies define permissions
- Learn the difference between users and roles
- Learn the difference between AWS managed, customer managed, and inline policies
- Understand temporary security credentials
- Apply the Principle of Least Privilege to IAM design

---

## 1. IAM User

An IAM user is an identity created inside an AWS account.

An IAM user can represent a person or workload that requires AWS credentials.

An IAM user may have:

- Console password
- Access keys
- Permissions
- Group memberships
- MFA configuration

Basic structure:

```text
AWS Account
│
└── IAM User
    │
    ├── Password
    ├── Access Key
    └── Permissions
```

IAM users can use long-term credentials.

Examples:

```text
Console Access
→ Username + Password + MFA

Programmatic Access
→ Access Key ID + Secret Access Key
```

Because IAM users may use long-term credentials, they must be carefully managed.

Security considerations include:

- Avoid unnecessary IAM users
- Enable MFA when appropriate
- Avoid unnecessary access keys
- Remove unused credentials
- Apply least privilege
- Do not share credentials

---

## 2. IAM User Group

An IAM user group is a collection of IAM users.

Groups make permission management easier when multiple users require similar permissions.

Example:

```text
Developers
│
├── Alice
├── Bob
└── Charlie
```

Instead of attaching the same permissions individually:

```text
Alice   → Policy
Bob     → Policy
Charlie → Policy
```

A policy can be attached to the group:

```text
Developers
    │
    └── Developer Policy
         │
         ├── Alice
         ├── Bob
         └── Charlie
```

This simplifies permission administration.

---

## 3. IAM Group Characteristics

IAM groups have several important characteristics.

```text
IAM Group
→ Contains IAM users
→ Can have policies attached
→ Cannot be used to sign in
→ Cannot be assumed like a role
```

A group is not an identity that can directly access AWS resources.

Instead, it is used to organize users and manage their permissions.

Example:

```text
SecurityTeam
│
├── User A
├── User B
└── User C

SecurityTeam
└── SecurityAudit Policy
```

Each user in the group receives the permissions provided through the group policy.

---

## 4. IAM Role

An IAM role is an identity that can be assumed temporarily.

Unlike an IAM user, a role does not normally have long-term credentials such as a permanent password or access key.

Instead:

```text
Identity
   ↓
Assume Role
   ↓
Temporary Credentials
   ↓
AWS Resources
```

IAM roles are commonly used by:

- AWS services
- Applications
- Federated users
- Users from another AWS account
- Administrators requiring temporary elevated access

---

## 5. IAM User vs IAM Role

The difference between users and roles is important.

| IAM User | IAM Role |
|---|---|
| Represents an identity | Represents an assumable identity |
| Can have long-term credentials | Uses temporary credentials |
| Can have console credentials | Normally does not use a permanent password |
| Can have access keys | Does not require permanent access keys |
| Used when persistent identity is required | Used for temporary or delegated access |

Example:

```text
IAM User

Administrator
   ↓
Username + Password + MFA
   ↓
AWS
```

Role example:

```text
Administrator
   ↓
Assume Role
   ↓
Temporary Credentials
   ↓
Production Account
```

---

## 6. IAM Role for AWS Services

AWS services can use IAM roles to access other AWS resources.

Example:

```text
EC2 Instance
     ↓
IAM Role
     ↓
Temporary Credentials
     ↓
Amazon S3
```

Without a role, an application might store credentials directly:

```text
EC2
 ↓
Access Key stored in application
 ↓
Amazon S3
```

This creates additional security risks.

Using a role is safer:

```text
EC2
 ↓
IAM Role
 ↓
Temporary Credentials
 ↓
Amazon S3
```

The application does not need to store permanent AWS credentials.

---

## 7. Role Assumption

A role is accessed through a process called role assumption.

Conceptually:

```text
User / Service / External Identity
              ↓
         Assume Role
              ↓
      Temporary Credentials
              ↓
        AWS Resources
```

Temporary credentials normally include:

```text
Access Key ID

Secret Access Key

Session Token
```

These credentials expire after a limited period.

This reduces the risks associated with long-term credentials.

---

## 8. IAM Policy

An IAM policy is a document that defines permissions.

A policy determines:

```text
What actions can be performed

Which resources can be accessed

Under which conditions access is allowed
```

Policies are usually written in JSON.

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::example-bucket/*"
    }
  ]
}
```

This policy allows the following action:

```text
s3:GetObject
```

on objects inside:

```text
arn:aws:s3:::example-bucket/*
```

---

## 9. IAM Policy Structure

A basic IAM policy contains several important elements.

### Version

```json
"Version": "2012-10-17"
```

Defines the policy language version.

---

### Statement

```json
"Statement": []
```

Contains one or more permission statements.

---

### Effect

```json
"Effect": "Allow"
```

Possible values include:

```text
Allow
Deny
```

---

### Action

Defines which API operations are affected.

Example:

```json
"Action": "s3:GetObject"
```

Multiple actions can also be specified:

```json
"Action": [
  "s3:GetObject",
  "s3:ListBucket"
]
```

---

### Resource

Defines which AWS resource the policy applies to.

Example:

```json
"Resource": "arn:aws:s3:::example-bucket/*"
```

---

### Condition

Policies can optionally include conditions.

Conceptually:

```text
Allow Action
      ↓
Only if Condition is satisfied
```

Examples of conditions can include:

- Source IP
- MFA usage
- Resource tags
- Time
- Requested Region

Conditions will be studied in more detail later.

---

## 10. Identity-Based Policies

Identity-based policies are attached to IAM identities.

They can be attached to:

```text
IAM User
IAM Group
IAM Role
```

Example:

```text
IAM Role
   ↓
S3ReadOnly Policy
   ↓
Amazon S3
```

The policy defines what the identity is allowed to do.

---

## 11. AWS Managed Policies

AWS managed policies are policies created and maintained by AWS.

Examples include:

```text
ReadOnlyAccess
SecurityAudit
AmazonS3ReadOnlyAccess
```

Advantages:

- Easy to use
- Maintained by AWS
- Useful for common permission requirements

However, AWS managed policies may sometimes grant more permissions than a specific workload actually requires.

Therefore, they should still be evaluated from a least-privilege perspective.

---

## 12. Customer Managed Policies

Customer managed policies are policies created and maintained by the AWS customer.

Example:

```text
CompanyS3ReadOnlyPolicy
```

A customer managed policy can be designed specifically for an organization's requirements.

Example:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::company-security-logs",
        "arn:aws:s3:::company-security-logs/*"
      ]
    }
  ]
}
```

Advantages include:

- More precise permissions
- Reusable across multiple identities
- Easier centralized management
- Better support for least privilege

---

## 13. Inline Policies

An inline policy is embedded directly into one IAM identity.

Example:

```text
IAM User
   │
   └── Inline Policy
```

or:

```text
IAM Role
   │
   └── Inline Policy
```

Unlike managed policies, an inline policy has a one-to-one relationship with the identity.

Conceptually:

```text
Managed Policy

Policy
├── Role A
├── Role B
└── Role C
```

Compared with:

```text
Inline Policy

Role A
└── Policy
```

Inline policies can be useful when permissions must remain tightly associated with a specific identity.

However, reusable customer managed policies are often easier to manage when the same permissions are required by multiple identities.

---

## 14. Managed Policy vs Inline Policy

| Managed Policy | Inline Policy |
|---|---|
| Separate AWS resource | Embedded in one identity |
| Can be reused | Cannot be reused directly |
| Easier centralized management | Tightly coupled to identity |
| Can be attached to multiple identities | Associated with a single identity |

---

## 15. IAM Permission Relationships

IAM permissions can come from multiple places.

Example:

```text
IAM User
│
├── Directly Attached Policy
│
└── IAM Group
    └── Group Policy
```

A role can also receive permissions:

```text
IAM Role
│
├── Managed Policy
└── Inline Policy
```

The effective permissions of an identity depend on all applicable policies.

Detailed policy evaluation rules will be studied on Day 4.

---

## 16. Principle of Least Privilege

Permissions should be limited to only what is required.

Bad example:

```text
Application
→ AdministratorAccess
```

Better:

```text
Application
→ s3:GetObject
→ Only required bucket
```

Even better security design may include:

```text
Required Actions
+
Required Resources
+
Required Conditions
```

Example:

```text
Allow only:
s3:GetObject

On:
security-report-bucket

From:
Required workload
```

Least privilege helps reduce the impact of:

- Credential compromise
- Application vulnerabilities
- Human error
- Insider threats
- Misconfiguration

---

## 17. Example — Application Access to S3

Suppose an EC2 application needs to read files from an S3 bucket.

A poor design would be:

```text
EC2
│
├── Hard-coded Access Key
└── AdministratorAccess
        ↓
       S3
```

Problems:

- Long-term credentials
- Credential exposure risk
- Excessive permissions
- Difficult credential rotation

A better design is:

```text
EC2
│
└── IAM Role
      │
      └── S3 Read Policy
             │
             └── Required Bucket
```

The role receives temporary credentials automatically.

Permissions can also be restricted to only:

```text
s3:GetObject
```

for the required bucket.

---

## 18. Example — Cross-Account Access

IAM roles can also provide access between AWS accounts.

Example:

```text
Development Account
        │
        │ Assume Role
        ↓
Production Account
        │
        └── ReadOnly Role
```

The user does not need to create another permanent IAM user in the production account.

This allows access to be:

- Temporary
- Auditable
- Centrally controlled
- Restricted by role permissions

---

## 19. Hands-on Practice

For today's practice, I explored the following sections in the AWS IAM console:

- Users
- User groups
- Roles
- Policies

I compared the purpose of each IAM component.

### IAM User

```text
Long-term identity
```

### IAM Group

```text
Permission management for multiple users
```

### IAM Role

```text
Temporary and delegated access
```

### IAM Policy

```text
Defines permissions
```

I also reviewed several AWS managed policies to understand how permissions are represented using JSON.

---

## Security Checklist

When designing IAM permissions, I should ask:

```text
Does this identity really need a permanent IAM user?

Can an IAM role be used instead?

Does this identity need all of these actions?

Can permissions be restricted to specific resources?

Can temporary credentials be used?

Are access keys stored securely?

Is MFA required for privileged access?
```

---

## Key Takeaways

- IAM users can use long-term AWS credentials.
- IAM groups simplify permission management for multiple users.
- IAM roles provide temporary and delegated access.
- IAM policies define what actions an identity can perform.
- IAM roles are generally preferred for AWS workloads instead of hard-coded access keys.
- Temporary credentials reduce risks associated with permanent credentials.
- AWS managed policies are maintained by AWS.
- Customer managed policies provide more control over permissions.
- Inline policies are directly associated with a single IAM identity.
- Least privilege should be applied to users, roles, workloads, and policies.
- Permissions should be limited by action, resource, and conditions whenever possible.

---

## Reflection

Today I learned that IAM users, groups, roles, and policies serve different purposes.

An IAM user represents a persistent identity, while an IAM role is designed for temporary or delegated access.

IAM groups do not directly access AWS resources. Instead, they simplify permission management by grouping users with similar responsibilities.

Policies define the actual permissions granted to identities.

I also learned that IAM roles and temporary credentials are important security mechanisms because they reduce the need to store long-term AWS credentials in applications and servers.

When designing IAM permissions, I should focus not only on whether access works, but also on whether the permissions are limited to exactly what is required.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Assume Role | The process of obtaining temporary credentials from an IAM role |
| Delegation | Granting another identity permission to perform actions |
| Group | A collection of IAM users used for permission management |
| Inline Policy | A policy embedded directly in one IAM identity |
| Least Privilege | Granting only the permissions required for a task |
| Managed Policy | A reusable IAM policy managed separately from an identity |
| Policy | A document that defines AWS permissions |
| Role | An IAM identity that provides temporary permissions |
| Temporary Credential | A credential that automatically expires |
| User | An IAM identity that can have long-term AWS credentials |

