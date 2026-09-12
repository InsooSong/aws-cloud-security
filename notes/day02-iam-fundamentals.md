# Day 2 — AWS IAM Fundamentals

## Topic

AWS Identity and Access Management (IAM) Fundamentals

---

## Objectives

- Understand the purpose of AWS IAM
- Understand authentication and authorization
- Learn the basic IAM components
- Understand the difference between IAM users and IAM roles
- Understand the Principle of Least Privilege
- Learn basic IAM security best practices
- Understand the security risks associated with AWS credentials

---

## 1. What is AWS IAM?

AWS Identity and Access Management (IAM) is a service used to control access to AWS resources.

IAM answers two fundamental security questions:

```text
Who are you?
→ Authentication

What are you allowed to do?
→ Authorization
```

IAM enables AWS administrators to control:

- Identities
- Authentication
- Permissions
- Access to AWS services
- Access to AWS resources

---

## 2. Authentication vs Authorization

Authentication verifies the identity of a user or system.

```text
Authentication
→ Who are you?
```

Examples include:

- Password
- Multi-Factor Authentication (MFA)
- Access keys
- Temporary credentials
- Federated authentication

Authorization determines what an authenticated identity is allowed to do.

```text
Authorization
→ What are you allowed to do?
```

Examples:

```text
Can this identity read an S3 object?

Can this identity start an EC2 instance?

Can this identity create an IAM user?
```

Authorization in AWS is mainly controlled through IAM policies.

---

## 3. Core IAM Components

IAM consists of several major components:

```text
IAM
│
├── Users
├── User Groups
├── Roles
└── Policies
```

### IAM User

An IAM user represents an identity with credentials that can be used to access AWS.

An IAM user can have:

- Console password
- Access keys
- Permissions
- Group memberships

IAM users are generally used when long-term credentials are required.

---

### IAM User Group

An IAM user group is a collection of IAM users.

Groups make it easier to manage permissions for multiple users.

Example:

```text
Developers Group
│
├── User A
├── User B
└── User C
```

Instead of assigning the same policy to each user individually, a policy can be attached to the group.

---

### IAM Role

An IAM role is an AWS identity that provides temporary permissions.

Unlike IAM users, roles are commonly assumed when permissions are needed temporarily.

Examples include:

```text
EC2
→ IAM Role
→ S3

Lambda
→ IAM Role
→ DynamoDB

Administrator
→ Assume Role
→ Production Account
```

IAM roles are commonly used for:

- AWS services
- Cross-account access
- Federated users
- Temporary privileged access

---

### IAM Policy

An IAM policy defines permissions.

Policies specify:

```text
What actions are allowed or denied

Which resources can be accessed

Under which conditions access is allowed
```

A simple policy example:

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

Important elements include:

```text
Effect
→ Allow or Deny

Action
→ AWS API action

Resource
→ AWS resource affected by the policy
```

IAM policy evaluation will be studied in more detail later.

---

## 4. AWS Root User

The root user is created when an AWS account is created.

The root user has access to almost all resources and account-level operations.

Because of its powerful permissions, the root user should not be used for normal daily administration.

Recommended approach:

```text
Root User
→ Account-level operations only

IAM identities
→ Daily AWS operations
```

Security recommendations for the root user include:

- Enable MFA
- Do not create root access keys
- Use the root user only when required
- Protect the root account credentials

---

## 5. Principle of Least Privilege

The Principle of Least Privilege means granting only the permissions required to perform a specific task.

```text
Required Task
      ↓
Required Permissions
      ↓
Grant Only Those Permissions
```

For example, if a user only needs to view logs, the user should not receive full administrator permissions.

Bad example:

```text
Log Viewer
→ AdministratorAccess
```

Better approach:

```text
Log Viewer
→ Read-only permissions for required logging services
```

Least privilege reduces the potential impact of:

- Credential compromise
- Human error
- Malicious insiders
- Misconfiguration

---

## 6. IAM Roles and Temporary Credentials

AWS services often need permission to access other AWS services.

For example, an EC2 instance may need to read objects from Amazon S3.

A poor approach would be storing long-term access keys on the server.

```text
EC2
→ Hard-coded Access Key
→ Amazon S3
```

A more secure approach is using an IAM role.

```text
EC2
→ IAM Role
→ Temporary Credentials
→ Amazon S3
```

Temporary credentials reduce the risks associated with long-term AWS credentials.

IAM roles are therefore an important security mechanism in AWS environments.

---

## 7. Multi-Factor Authentication

Multi-Factor Authentication (MFA) adds an additional authentication factor.

```text
Password
+
MFA
```

If a password is compromised, MFA provides another layer of protection.

MFA is especially important for:

- Root users
- Administrative identities
- Privileged users
- Sensitive AWS environments

---

## 8. AWS Access Keys

Access keys are credentials used for programmatic access to AWS.

They consist of:

```text
Access Key ID
Secret Access Key
```

Access keys can be used with:

- AWS CLI
- AWS SDKs
- APIs
- Automation tools

Access keys must be treated as sensitive credentials.

Important security practices:

- Never expose access keys publicly
- Never commit credentials to GitHub
- Never hard-code credentials in source code
- Remove unused credentials
- Rotate credentials when necessary
- Prefer IAM roles and temporary credentials when possible

```text
Never commit AWS credentials to GitHub.
```

If credentials are accidentally exposed, they should be disabled or revoked immediately and replaced with new credentials.

---

## 9. IAM Security Model

IAM can be viewed using a simple security flow:

```text
Identity
   ↓
Authentication
   ↓
IAM Policy
   ↓
Authorization
   ↓
AWS Resource
```

Example:

```text
IAM User
   ↓
Login with Password + MFA
   ↓
IAM Policy
   ↓
s3:GetObject
   ↓
Amazon S3 Object
```

This model helps explain how AWS determines whether an identity can perform an action.

---

## 10. Hands-on Practice

For today's practice, I explored the IAM service in the AWS Management Console.

I located the following IAM components:

- IAM Dashboard
- Users
- User groups
- Roles
- Policies
- Account settings

I also reviewed the security status of the AWS account and checked whether MFA is enabled for privileged access.

The main goal of today's practice was to understand how identities and permissions are organized in AWS.

---

## Key Takeaways

- IAM controls access to AWS services and resources.
- Authentication verifies identity.
- Authorization determines permissions.
- IAM users can represent identities with long-term credentials.
- IAM groups simplify permission management for multiple users.
- IAM roles provide temporary permissions.
- IAM policies define allowed and denied actions.
- The AWS root user should not be used for normal daily activities.
- MFA provides an additional layer of account protection.
- Least privilege should be applied when granting permissions.
- Long-term access keys should be avoided when temporary credentials can be used.
- AWS credentials must never be committed to public source code repositories.

---

## Reflection

IAM is one of the most important components of AWS security because almost every AWS resource requires some form of access control.

I learned that authentication and authorization are separate concepts.

Authentication verifies who an identity is, while authorization determines what that identity is allowed to do.

I also learned that IAM roles and temporary credentials are generally safer than storing long-term credentials in applications or servers.

The Principle of Least Privilege is especially important because overly broad permissions can significantly increase the impact of compromised credentials or configuration mistakes.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Assume Role | The process of obtaining temporary permissions from an IAM role |
| Authentication | The process of verifying an identity |
| Authorization | The process of determining what an identity can access |
| Credential | Information used to prove an identity |
| Least Privilege | Granting only the minimum permissions required |
| Permission | Authorization to perform a specific action |
| Privilege | A level of access or authority granted to an identity |
| Temporary Credential | A credential that expires after a limited period |
