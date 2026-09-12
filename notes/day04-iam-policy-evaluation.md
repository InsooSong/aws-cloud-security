# Day 4 — IAM Policy Evaluation

## Topic

AWS IAM Policy Evaluation Logic and Effective Permissions

---

## Objectives

- Understand how AWS evaluates authorization requests
- Understand implicit deny and explicit deny
- Understand how Allow and Deny interact
- Learn the difference between identity-based and resource-based policies
- Understand permissions boundaries
- Understand Service Control Policies (SCPs)
- Learn how multiple policy types affect effective permissions
- Analyze common IAM permission conflicts

---

## 1. AWS Authorization Request Flow

When a principal sends a request to AWS, AWS evaluates whether the requested action should be allowed or denied.

A simplified flow is:

```text
Principal
   ↓
Authentication
   ↓
Request Context
   ↓
Applicable Policies
   ↓
Policy Evaluation
   ↓
Allow or Deny
```

AWS considers information such as:

- Principal
- Requested action
- Requested resource
- Request conditions
- Applicable IAM policies
- Resource-based policies
- Permissions boundaries
- AWS Organizations policies
- Session policies

The final result is called the effective permission.

---

## 2. Default Behavior — Implicit Deny

AWS follows a deny-by-default security model.

```text
Default
→ Deny
```

If no policy explicitly allows an action, the request is denied.

This is called:

```text
Implicit Deny
```

Example:

An IAM user has no policy allowing:

```text
s3:DeleteObject
```

The user attempts to delete an S3 object.

Result:

```text
No Allow
↓
Implicit Deny
↓
Access Denied
```

There does not need to be an explicit Deny statement.

The absence of Allow is enough to deny the request.

---

## 3. Explicit Allow

A request can be allowed when an applicable policy explicitly grants permission.

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

This policy explicitly allows:

```text
s3:GetObject
```

for objects inside:

```text
example-bucket
```

Simplified evaluation:

```text
Default Deny
   ↓
Explicit Allow Found
   ↓
No Explicit Deny
   ↓
Allow
```

---

## 4. Explicit Deny

An explicit Deny overrides an Allow.

Example:

Policy A:

```json
{
  "Effect": "Allow",
  "Action": "s3:*",
  "Resource": "*"
}
```

Policy B:

```json
{
  "Effect": "Deny",
  "Action": "s3:DeleteObject",
  "Resource": "*"
}
```

The user attempts:

```text
s3:DeleteObject
```

Evaluation:

```text
Policy A
→ Allow

Policy B
→ Deny
```

Final result:

```text
Explicit Deny
→ DENY
```

The important rule is:

```text
Explicit Deny overrides Allow.
```

---

## 5. Basic Policy Evaluation Logic

A simplified decision process can be represented as:

```text
Request
   ↓
Is there an applicable Explicit Deny?
   │
   ├── Yes → DENY
   │
   └── No
        ↓
Is there an applicable Allow?
   │
   ├── Yes → ALLOW
   │
   └── No → IMPLICIT DENY
```

Therefore:

```text
No Allow
→ Deny

Allow
→ Allow

Allow + Explicit Deny
→ Deny
```

---

## 6. Implicit Deny vs Explicit Deny

Implicit Deny and Explicit Deny both result in denied access, but they are different concepts.

### Implicit Deny

Occurs when no applicable policy grants permission.

```text
No Allow
→ Implicit Deny
```

### Explicit Deny

Occurs when a policy contains an applicable:

```json
"Effect": "Deny"
```

Example:

```text
Policy A → Allow

Policy B → Explicit Deny

Final → Deny
```

Explicit Deny has higher priority than an Allow.

---

## 7. Identity-Based Policies

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
Identity-Based Policy
   ↓
s3:GetObject
```

The policy defines what actions the identity is permitted to perform.

Example:

```json
{
  "Effect": "Allow",
  "Action": "s3:GetObject",
  "Resource": "arn:aws:s3:::security-logs/*"
}
```

---

## 8. Resource-Based Policies

Resource-based policies are attached directly to AWS resources.

Examples include:

```text
S3 Bucket Policy
KMS Key Policy
SQS Queue Policy
SNS Topic Policy
```

A resource-based policy defines:

```text
Which Principal
   ↓
Can perform which Action
   ↓
On this Resource
```

Example S3 bucket policy:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": "arn:aws:iam::111122223333:role/SecurityRole"
      },
      "Action": "s3:GetObject",
      "Resource": "arn:aws:s3:::security-logs/*"
    }
  ]
}
```

The important difference is:

```text
Identity-Based Policy
→ Attached to an identity

Resource-Based Policy
→ Attached to a resource
```

---

## 9. Identity-Based + Resource-Based Policies

Within the same AWS account, permissions from identity-based policies and resource-based policies can work together.

Conceptually:

```text
Identity-Based Policy
        +
Resource-Based Policy
        ↓
Effective Permissions
```

If an applicable policy allows the request and there is no applicable explicit Deny, the request may be allowed.

Example:

```text
IAM Policy
→ Allow s3:GetObject

Bucket Policy
→ No explicit Deny

Result
→ Allow
```

However:

```text
IAM Policy
→ Allow

Bucket Policy
→ Explicit Deny

Result
→ Deny
```

Explicit Deny still overrides Allow.

---

## 10. Permissions Boundary

A permissions boundary defines the maximum permissions that an IAM user or role can receive through identity-based policies.

It does not grant permissions by itself.

Conceptually:

```text
Identity-Based Policy
        ∩
Permissions Boundary
        ↓
Effective Permissions
```

The effective permissions are the intersection of both.

Example:

Identity-based policy:

```text
Allow:
s3:*
ec2:*
```

Permissions boundary:

```text
Allow:
s3:*
```

Effective permissions:

```text
s3:*
```

The EC2 permissions cannot be used because they are outside the permissions boundary.

---

## 11. Permissions Boundary Example

Suppose a developer is allowed to create IAM roles.

Without additional restrictions:

```text
Developer
   ↓
Create IAM Role
   ↓
Potentially assign excessive permissions
```

A permissions boundary can restrict the maximum permissions of roles created by that developer.

Example concept:

```text
Developer-created Role
       │
       ├── Identity Policy
       │     Administrator-like permissions
       │
       └── Permissions Boundary
             Limited permissions
```

Effective permissions:

```text
Only permissions allowed by BOTH
```

This can help organizations safely delegate IAM administration.

---

## 12. AWS Organizations Service Control Policies

A Service Control Policy (SCP) is an AWS Organizations policy used to limit the maximum available permissions in member accounts.

Conceptually:

```text
AWS Organization
     ↓
Organizational Unit
     ↓
SCP
     ↓
AWS Account
     ↓
IAM Identity
```

An SCP does not directly grant permissions.

Instead, it defines the maximum permissions that can be available.

Example:

```text
IAM Policy
→ Allow EC2 and S3

SCP
→ Allow only S3

Effective Permission
→ S3
```

---

## 13. SCP Example — Region Restriction

An organization may want workloads to operate only in approved AWS Regions.

Conceptually:

```text
Organization
   ↓
SCP
   ↓
Deny actions outside approved Regions
```

Example security objective:

```text
Approved Regions:

ap-northeast-1
ap-northeast-2
```

Requests outside those Regions may be blocked by an SCP.

This provides centralized governance across multiple AWS accounts.

---

## 14. Permissions Boundary vs SCP

Both mechanisms limit permissions, but their scope is different.

| Permissions Boundary | SCP |
|---|---|
| Applies to IAM users or roles | Applies through AWS Organizations |
| Controls maximum permissions of IAM entities | Controls maximum permissions available in accounts/OUs |
| Managed inside an AWS account | Managed at organization level |
| Does not grant permissions | Does not grant permissions |

Conceptually:

```text
Permissions Boundary
→ Identity-level guardrail

SCP
→ Organization/account-level guardrail
```

---

## 15. Effective Permissions

Effective permissions are the permissions that remain after AWS evaluates all applicable policy types.

A simplified model can be represented as:

```text
Identity-Based Policy
        │
        ├──── Permissions Boundary
        │
        ├──── SCP
        │
        └──── Other Applicable Policies
                   ↓
          Effective Permissions
```

A useful mental model is:

```text
IAM Policy
→ What the identity may be granted

Permissions Boundary
→ Maximum permission for the identity

SCP
→ Maximum permission allowed by the organization

Explicit Deny
→ Overrides applicable Allow
```

---

## 16. Example — Allow and Deny Conflict

Assume the following policies apply.

### Identity Policy

```text
Allow:
s3:GetObject
s3:PutObject
s3:DeleteObject
```

### Permissions Boundary

```text
Allow:
s3:GetObject
s3:PutObject
```

### SCP

```text
Allow:
s3:*
```

Effective permissions are:

```text
s3:GetObject
s3:PutObject
```

`s3:DeleteObject` is outside the permissions boundary.

Therefore:

```text
DeleteObject
→ Denied
```

---

## 17. Example — Explicit Deny

Assume:

### IAM Policy

```text
Allow:
s3:*
```

### Bucket Policy

```text
Deny:
s3:DeleteObject
```

The user attempts:

```text
s3:DeleteObject
```

Evaluation:

```text
Identity Policy
→ Allow

Bucket Policy
→ Explicit Deny
```

Final result:

```text
DENY
```

This demonstrates one of the most important IAM rules:

```text
Explicit Deny overrides Allow.
```

---

## 18. Example — No Explicit Allow

Assume a user has permission:

```text
s3:GetObject
```

The user attempts:

```text
ec2:TerminateInstances
```

There is no applicable Allow.

Result:

```text
Implicit Deny
→ Access Denied
```

This demonstrates the AWS default-deny model.

---

## 19. Cross-Account Access

Cross-account access allows a principal in one AWS account to access resources in another AWS account.

Example:

```text
Account A
   │
   │ IAM Role / User
   │
   ↓
Account B
   │
   └── Resource
```

For many cross-account access scenarios, permissions must be configured on both sides.

Conceptually:

```text
Account A
Identity Permission
        +
Account B
Resource Trust / Permission
        ↓
Cross-Account Access
```

Example:

```text
Account A IAM Role
→ Permission to access S3

Account B S3 Bucket Policy
→ Trusts Account A role
```

Both sides must be configured correctly.

---

## 20. Policy Evaluation Troubleshooting

When an AWS action returns:

```text
AccessDenied
```

I should investigate systematically.

### Step 1 — Identify the Principal

```text
Who made the request?
```

Examples:

- IAM user
- IAM role
- AWS service
- Federated identity

### Step 2 — Identify the Action

```text
Which API operation failed?
```

Example:

```text
s3:GetObject
```

### Step 3 — Identify the Resource

```text
Which resource was accessed?
```

Example:

```text
arn:aws:s3:::security-logs/example.log
```

### Step 4 — Check Identity Policies

```text
Is the action explicitly allowed?
```

### Step 5 — Check Resource Policies

```text
Does the resource policy allow or deny access?
```

### Step 6 — Check Boundaries

```text
Does a permissions boundary restrict the action?
```

### Step 7 — Check Organization Policies

```text
Does an SCP restrict the action?
```

### Step 8 — Check Explicit Deny

```text
Is there an applicable explicit Deny anywhere?
```

This approach is useful when troubleshooting AWS authorization issues.

---

## 21. Policy Evaluation Troubleshooting Flow

```text
AccessDenied
    ↓
Who is the Principal?
    ↓
What Action was requested?
    ↓
Which Resource?
    ↓
Identity Policy
    ↓
Resource Policy
    ↓
Permissions Boundary
    ↓
SCP
    ↓
Conditions
    ↓
Explicit Deny?
```

This method helps avoid randomly modifying IAM policies when troubleshooting access problems.

---

## 22. Hands-on Practice

For today's practice, I reviewed several IAM policies and analyzed whether different requests would be allowed or denied.

### Scenario 1

Policy:

```text
Allow:
s3:GetObject
```

Request:

```text
s3:GetObject
```

Result:

```text
ALLOW
```

---

### Scenario 2

Policy:

```text
Allow:
s3:GetObject
```

Request:

```text
s3:DeleteObject
```

Result:

```text
IMPLICIT DENY
```

---

### Scenario 3

Policies:

```text
Policy A:
Allow s3:*

Policy B:
Deny s3:DeleteObject
```

Request:

```text
s3:DeleteObject
```

Result:

```text
EXPLICIT DENY
```

---

### Scenario 4

Identity Policy:

```text
Allow:
s3:*
ec2:*
```

Permissions Boundary:

```text
Allow:
s3:*
```

Request:

```text
ec2:StartInstances
```

Result:

```text
DENY
```

The EC2 permission is outside the permissions boundary.

---

## 23. Security Perspective

IAM policy evaluation is important for cloud security because permissions may come from multiple sources.

A security engineer should not only ask:

```text
Does this IAM policy allow the action?
```

Instead, the full question should be:

```text
What are the effective permissions
after all applicable policies are evaluated?
```

Important areas to review include:

```text
Identity Policies
Resource Policies
Permissions Boundaries
SCPs
Session Policies
Policy Conditions
Explicit Denies
```

---

## Security Checklist

When reviewing IAM permissions, I should ask:

```text
Is there an explicit Allow?

Is there an explicit Deny?

Is access denied implicitly?

Does a resource-based policy affect access?

Does a permissions boundary limit the identity?

Does an SCP restrict the account?

Are policy conditions satisfied?

Are permissions broader than necessary?
```

---

## Key Takeaways

- AWS uses a deny-by-default authorization model.
- Requests without an applicable Allow are implicitly denied.
- Explicit Allow can grant permission when no applicable explicit Deny exists.
- Explicit Deny overrides applicable Allow.
- Identity-based policies define permissions for IAM identities.
- Resource-based policies define access directly on resources.
- Permissions boundaries define maximum permissions for IAM users and roles.
- SCPs define organization-level permission guardrails.
- Permissions boundaries and SCPs do not grant permissions by themselves.
- Effective permissions depend on all applicable policy types.
- AccessDenied errors should be investigated systematically rather than solved by granting broader permissions.

---

## Reflection

Today I learned that AWS permission evaluation is more complex than simply checking whether an IAM policy contains an Allow statement.

AWS uses a default-deny model, meaning that actions are denied unless permission is explicitly granted.

I also learned that an explicit Deny can override an Allow, making Deny an important security control.

Permissions boundaries and Service Control Policies provide additional guardrails by limiting the maximum permissions available to identities or AWS accounts.

When troubleshooting access problems, I should identify the principal, action, resource, and all applicable policies before changing permissions.

This approach helps maintain least privilege and prevents the common mistake of granting excessive permissions simply to resolve an AccessDenied error.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Effective Permission | The final permissions available after all policies are evaluated |
| Explicit Deny | A policy statement that specifically denies an action |
| Guardrail | A security control that limits what actions are possible |
| Implicit Deny | Access denied because no applicable Allow exists |
| Permissions Boundary | A policy that defines maximum permissions for an IAM user or role |
| Policy Evaluation | The process AWS uses to determine whether a request is allowed |
| Principal | An identity making a request to AWS |
| Request Context | Information AWS uses when evaluating an authorization request |
| Resource-Based Policy | A policy attached directly to an AWS resource |
| SCP | An AWS Organizations policy that limits available permissions |
