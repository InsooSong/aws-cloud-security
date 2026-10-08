# Day 35 — Service Control Policies

## Topic

AWS Organizations Service Control Policies, Permission Guardrails, Policy Inheritance, Explicit Deny, and Organization-Wide Security Controls

---

## Objectives

- Understand the purpose of Service Control Policies
- Understand that SCPs do not grant permissions
- Understand the relationship between SCPs and IAM policies
- Learn how SCP inheritance works
- Understand Allow and Deny strategies
- Understand FullAWSAccess
- Learn how Explicit Deny affects permissions
- Understand how SCPs affect root users in member accounts
- Understand the management account exception
- Understand the service-linked role exception
- Learn common security SCP patterns
- Understand Region restriction strategies
- Learn how to protect logging and security services
- Understand how to safely test and deploy SCPs
- Compare SCPs and Resource Control Policies
- Practice designing organization-wide security guardrails

---

# SCP Fundamentals

## 1. What Is a Service Control Policy?

A Service Control Policy, or SCP, is an AWS Organizations policy that defines permission guardrails for member accounts.

Conceptually:

```text
AWS Organization
       |
       v
      SCP
       |
       v
Maximum Available Permissions
       |
       v
Member Account
```

SCPs can be attached to:

```text
Root

Organizational Unit

AWS Account
```

---

## 2. SCP Does Not Grant Permissions

This is the most important SCP concept.

```text
SCP
≠
IAM Permission Policy
```

An SCP cannot give a user permission to perform an AWS action.

Example:

```text
SCP:
Allow ec2:RunInstances
```

but:

```text
IAM Policy:
No EC2 Permission
```

Result:

```text
Access Denied
```

The IAM principal still needs an IAM policy that grants the permission.

---

## 3. IAM and SCP Together

A simplified permission model:

```text
IAM Permission
      ∩
SCP Permission
      =
Effective Permission
```

Example:

```text
IAM:
Allow ec2:*

SCP:
Allow ec2:Describe*

Result:

Only allowed EC2 Describe operations
```

---

## 4. SCP as Maximum Permission

Think of an SCP as:

```text
Permission Ceiling
```

Example:

```text
SCP Maximum:
EC2
S3
CloudWatch
```

An administrator in the member account cannot grant:

```text
IAM

Organizations

Unapproved Services
```

if they fall outside that ceiling.

---

# Permission Evaluation

## 5. Basic Evaluation

Suppose:

```text
IAM Policy
→ Allow s3:GetObject

SCP
→ Allow s3:GetObject
```

Result:

```text
Allowed
```

But:

```text
IAM
→ Allow s3:GetObject

SCP
→ Deny s3:GetObject
```

Result:

```text
Denied
```

---

## 6. Explicit Deny

AWS authorization follows an important rule:

```text
Explicit Deny
>
Allow
```

Conceptually:

```text
IAM Allow
+
SCP Deny
=
DENY
```

Even:

```text
AdministratorAccess
```

cannot override an applicable SCP Explicit Deny.

---

## 7. Implicit Deny

If an allow-list style SCP does not allow an action, that action is unavailable.

Example:

```text
SCP:

Allow:
s3:*
ec2:*
```

Request:

```text
rds:CreateDBInstance
```

Result:

```text
Implicitly Denied
```

because RDS is outside the allowed permission boundary.

---

# FullAWSAccess

## 8. Default FullAWSAccess Policy

When SCPs are enabled, AWS Organizations provides a default SCP:

```text
FullAWSAccess
```

Conceptually:

```json
{
  "Effect": "Allow",
  "Action": "*",
  "Resource": "*"
}
```

This means the SCP layer itself does not initially restrict AWS actions.

---

## 9. FullAWSAccess Does Not Grant Administrator Access

Important:

```text
FullAWSAccess SCP
≠
AdministratorAccess IAM Policy
```

It only means:

```text
SCP Layer
→ Does Not Restrict Actions
```

The principal still needs IAM authorization.

---

## 10. Be Careful Removing FullAWSAccess

If using an allow-list SCP strategy, removing `FullAWSAccess` without replacing it with appropriate Allow statements can make many or all AWS actions unavailable.

Therefore:

```text
Do Not Remove FullAWSAccess
Without Understanding the Result
```

---

# Policy Inheritance

## 11. SCP Hierarchy

SCPs can apply at multiple organization levels.

Example:

```text
Root
 |
 v
Workloads OU
 |
 v
Production OU
 |
 v
Account
```

The account is affected by relevant SCPs throughout the hierarchy.

---

## 12. Effective Permission Path

Conceptually:

```text
Root SCP
   ∩
Parent OU SCP
   ∩
Child OU SCP
   ∩
Account SCP
   ∩
IAM Permission
       =
Effective Permission
```

A required permission must survive all applicable permission boundaries.

---

## 13. Deny Inheritance

Example:

```text
Root
→ Deny organizations:LeaveOrganization
```

Then:

```text
Production OU

Development OU

Security OU
```

all inherit the restriction.

A child OU cannot override the parent Deny with:

```text
Allow organizations:LeaveOrganization
```

because:

```text
Explicit Deny Wins
```

---

## 14. Parent Restriction Cannot Be Expanded

Example:

```text
Root:
Allow EC2 + S3
```

Child OU:

```text
Allow EC2 + S3 + RDS
```

Effective permissions do not suddenly gain RDS.

Why?

Because the parent did not permit it.

Conceptually:

```text
Parent Maximum
      ∩
Child Maximum
      =
Effective Maximum
```

---

# Deny-List Strategy

## 15. Deny-List Model

A common approach keeps:

```text
FullAWSAccess
```

and adds explicit Deny policies.

Example:

```text
Allow:
Everything

Deny:
Specific Dangerous Actions
```

Conceptually:

```text
FullAWSAccess
      |
      v
Everything Available
      |
      v
Specific Denies
```

---

## 16. Deny-List Example

Example requirement:

```text
Users must not disable CloudTrail.
```

SCP concept:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Deny",
      "Action": [
        "cloudtrail:StopLogging",
        "cloudtrail:DeleteTrail"
      ],
      "Resource": "*"
    }
  ]
}
```

Even if:

```text
IAM Administrator
```

tries to disable CloudTrail:

```text
SCP Deny
→ Access Denied
```

---

## 17. Advantages of Deny-List Strategy

Benefits:

```text
Simple Initial Deployment

New AWS Services Continue to Work

Lower Operational Friction
```

Potential disadvantage:

```text
Anything Not Explicitly Denied
May Be Available
```

assuming IAM permits it.

---

# Allow-List Strategy

## 18. Allow-List Model

A stricter strategy defines which services or actions may be used.

Example:

```text
Allow:

EC2

S3

CloudWatch
```

Everything outside the allowed set is unavailable.

---

## 19. Allow-List Example

Conceptual SCP:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ec2:*",
        "s3:*",
        "cloudwatch:*"
      ],
      "Resource": "*"
    }
  ]
}
```

If a user requests:

```text
lambda:CreateFunction
```

Result:

```text
Denied
```

unless Lambda is also allowed through every applicable SCP layer.

---

## 20. Advantages of Allow Lists

Benefits:

```text
Strong Least Privilege

Explicit Service Approval

Smaller Attack Surface
```

Challenges:

```text
Operational Complexity

New Services Require Updates

Dependencies Can Be Missed

Potential Application Breakage
```

---

# Deny vs Allow Strategy

## 21. Comparison

```text
Deny List
→ Everything available except prohibited actions

Allow List
→ Only explicitly approved actions available
```

Deny lists are often easier to operate.

Allow lists provide stronger restrictions but require significantly more governance.

---

# Member Account Root User

## 22. SCPs Affect Root Users in Member Accounts

A very important point:

```text
Member Account Root User
```

is affected by applicable SCPs.

Example:

```text
SCP
→ Deny s3:DeleteBucket
```

Then:

```text
Member Account Root
→ Cannot Delete Bucket
```

through that denied action.

---

## 23. Root Is Not Above SCPs

A common misconception:

```text
Root User
→ Can Ignore SCP
```

Incorrect for member accounts.

Correct:

```text
Member Account Root
→ Subject to SCP
```

This makes SCPs powerful organization-level guardrails.

---

# Management Account Exception

## 24. SCPs Do Not Restrict the Management Account

SCPs apply to:

```text
Member Accounts
```

but not to:

```text
Management Account
```

Conceptually:

```text
Management Account
       |
       X
      SCP
```

This is another reason workloads should not be placed in the management account.

---

## 25. Security Implication

Suppose an SCP protects CloudTrail:

```text
Deny:
cloudtrail:StopLogging
```

Member accounts:

```text
Protected by SCP
```

Management account:

```text
Not Restricted by SCP
```

Therefore, management account security must rely strongly on:

```text
IAM

Root Protection

MFA

Minimal Access

Monitoring

Operational Discipline
```

---

# Delegated Administrators

## 26. SCPs Affect Delegated Administrator Accounts

A delegated administrator is still:

```text
A Member Account
```

Therefore:

```text
Delegated Administrator
→ Subject to SCP
```

Example:

```text
Security Tooling Account
```

may administer GuardDuty for the organization while still being restricted by organization SCPs.

---

# Service-Linked Roles

## 27. SCPs Do Not Restrict Service-Linked Roles

AWS service-linked roles are special roles used by AWS services.

Conceptually:

```text
AWS Service
      |
      v
Service-Linked Role
```

SCP restrictions do not apply to actions performed through service-linked roles.

---

## 28. Why This Matters

Suppose:

```text
SCP
→ Deny Some AWS Action
```

An AWS service using its service-linked role may still need to perform that operation.

AWS excludes service-linked roles from SCP restrictions so integrated AWS services can operate correctly.

---

# Common Security Guardrails

## 29. Prevent Leaving the Organization

An organization may prohibit member accounts from leaving.

Concept:

```text
Deny:
organizations:LeaveOrganization
```

This prevents an account administrator from escaping organization governance.

---

## 30. Protect CloudTrail

Important security control:

```text
Deny:

cloudtrail:StopLogging

cloudtrail:DeleteTrail
```

Goal:

```text
Prevent Workload Administrators
from Removing Audit Visibility
```

---

## 31. Protect AWS Config

Concept:

```text
Deny:

config:StopConfigurationRecorder

config:DeleteConfigurationRecorder

config:DeleteDeliveryChannel
```

Goal:

```text
Preserve Configuration Visibility
```

---

## 32. Protect GuardDuty

A security organization may restrict actions that weaken threat detection.

Conceptually:

```text
Deny:

GuardDuty Disable / Delete Actions
```

The exact actions should be validated against the current GuardDuty API and organizational design.

Goal:

```text
Workload Administrator
→ Cannot Disable Central Threat Detection
```

---

## 33. Protect Security Services

Conceptually:

```text
Workload Account Admin

Cannot:

Disable Logging

Disable Threat Detection

Destroy Security Configuration
```

but:

```text
Central Security Role
```

may need approved administrative permissions.

This requires careful use of policy conditions and exceptions.

---

# Exceptions

## 34. Why Exceptions Are Needed

Suppose:

```text
Deny cloudtrail:StopLogging
```

for everyone.

The central security automation may legitimately need to replace or modify a trail.

Therefore, some SCPs need exceptions for approved roles.

---

## 35. ArnNotLike Exception

Conceptual pattern:

```json
{
  "Effect": "Deny",
  "Action": [
    "cloudtrail:StopLogging",
    "cloudtrail:DeleteTrail"
  ],
  "Resource": "*",
  "Condition": {
    "ArnNotLike": {
      "aws:PrincipalArn": [
        "arn:aws:iam::*:role/ApprovedSecurityRole"
      ]
    }
  }
}
```

Meaning:

```text
Deny the action

unless

the approved security role is making the request
```

Conditions must be tested carefully.

---

# Region Restrictions

## 36. Why Restrict Regions?

Organizations may approve only selected AWS Regions.

Reasons include:

```text
Compliance

Data Residency

Operational Support

Cost Control

Security Monitoring Coverage
```

Example approved Regions:

```text
ap-northeast-1

ap-northeast-3
```

---

## 37. RequestedRegion Condition

A common Region restriction pattern uses:

```text
aws:RequestedRegion
```

Conceptually:

```text
Request Region
      |
      v
Approved?
   +--+--+
   |     |
  Yes    No
   |     |
 Allow  Deny
```

---

## 38. Region Restriction Example

Conceptual:

```json
{
  "Effect": "Deny",
  "NotAction": [
    "iam:*",
    "route53:*",
    "cloudfront:*",
    "organizations:*"
  ],
  "Resource": "*",
  "Condition": {
    "StringNotEquals": {
      "aws:RequestedRegion": [
        "ap-northeast-1"
      ]
    }
  }
}
```

The global-service exception list must be carefully reviewed and maintained.

---

## 39. Why Not Simply Deny Every Action Outside a Region?

Some AWS services are:

```text
Global Services
```

Examples can include:

```text
IAM

CloudFront

Route 53

Organizations
```

A poorly designed Region restriction may unexpectedly break these services.

Always test Region SCPs before production deployment.

---

# Restrict Resource Creation

## 40. Restrict Unapproved Instance Types

Organizations may restrict expensive or unapproved EC2 instance types.

Conceptually:

```text
Developer
   |
   v
Launch EC2
   |
   v
Approved Instance Type?
```

This can help with:

```text
Cost Governance

Architecture Standards

Security Baselines
```

---

## 41. Restrict Public Resources

SCPs may be used as part of controls intended to reduce public exposure.

However:

```text
SCP
```

alone is not always the best tool for resource-side access.

Modern AWS Organizations also provides:

```text
Resource Control Policies
```

for resource access guardrails.

---

# SCP vs RCP

## 42. SCP

SCP asks:

```text
What may principals in my member accounts do?
```

Conceptually:

```text
IAM Principal
     |
     v
SCP
     |
     v
AWS Action
```

---

## 43. RCP

RCP asks:

```text
What access may resources in my organization accept?
```

Conceptually:

```text
Principal
     |
     v
Organization Resource
     |
     v
RCP
```

This is particularly useful when controlling access from:

```text
External Principals
```

to organization-owned resources.

---

## 44. SCP and RCP Together

Modern permission evaluation can involve:

```text
IAM Policy

Resource Policy

Permissions Boundary

SCP

RCP
```

Conceptually:

```text
All Applicable Permission Boundaries
              |
              v
       Effective Permission
```

---

# Security Architecture Example

## 45. Organization Structure

```text
Root
│
├── Security OU
│   ├── Security Tooling
│   └── Log Archive
│
├── Infrastructure OU
│   └── Network
│
└── Workloads OU
    ├── Production
    └── Development
```

---

## 46. Root-Level Guardrails

Possible root-level controls:

```text
Prevent Leaving Organization

Protect Core Logging

Restrict Dangerous Root-Level Operations
```

Root-level SCPs affect a very large scope.

They should be minimal and thoroughly tested.

---

## 47. Production OU Guardrails

Production may require:

```text
Approved Regions Only

No Logging Disable

No Security Service Disable

Restricted Networking Changes

Restricted Resource Sharing
```

---

## 48. Development OU Guardrails

Development may allow more flexibility:

```text
More AWS Services

More Resource Creation

Experimentation
```

while still preventing:

```text
Leaving Organization

Disabling Central Security

Using Prohibited Regions
```

---

# Testing SCPs

## 49. Do Not Test First at the Root

Poor:

```text
Create SCP
   |
   v
Attach to Root
   |
   v
Entire Organization Breaks
```

Better:

```text
Create Test OU
      |
      v
Attach SCP
      |
      v
Move Test Account
      |
      v
Validate
      |
      v
Expand Gradually
```

---

## 50. Test Account Strategy

Create or use:

```text
Sandbox / Policy-Test Account
```

Then validate:

```text
Expected Allowed Actions

Expected Denied Actions

AWS Service Dependencies

Automation

Security Services
```

before wider rollout.

---

## 51. Service Last Accessed Data

IAM service last accessed data can help determine which AWS services accounts are actually using.

Conceptually:

```text
Service Usage Data
      |
      v
Identify Unused Services
      |
      v
Refine SCP
```

This can support least privilege.

---

## 52. CloudTrail for SCP Design

CloudTrail can help identify:

```text
Which APIs are currently used?

Which services are needed?

Which calls fail after SCP deployment?
```

This reduces guesswork when tightening organization guardrails.

---

# Troubleshooting

## 53. AccessDenied After SCP Change

When a user unexpectedly receives:

```text
AccessDenied
```

check:

```text
IAM Policy

Permissions Boundary

Resource Policy

SCP

RCP

Session Policy

Explicit Deny
```

Do not assume the problem is IAM alone.

---

## 54. Troubleshooting Path

```text
Who is the principal?
       |
       v
Which action?
       |
       v
Which resource?
       |
       v
IAM Allows?
       |
       v
Permissions Boundary Allows?
       |
       v
All Parent SCPs Allow?
       |
       v
RCP Allows?
       |
       v
Any Explicit Deny?
```

---

## 55. AdministratorAccess but AccessDenied

Scenario:

```text
IAM Policy:
AdministratorAccess
```

but:

```text
AccessDenied
```

Possible cause:

```text
SCP
→ Explicit Deny
```

Remember:

```text
AdministratorAccess
≠
Bypass Organization Guardrails
```

---

## 56. Service Works in Management but Not Member Account

Possible explanation:

```text
Management Account
→ SCP Not Applied

Member Account
→ SCP Applied
```

This difference is important when troubleshooting.

---

# Common Mistakes

## 57. Treating SCP as IAM Policy

Incorrect:

```text
SCP Allow
→ Permission Granted
```

Correct:

```text
SCP Allow
+
IAM Allow
→ Potentially Allowed
```

---

## 58. Attaching Untested SCP to Root

Risk:

```text
Entire Organization Impact
```

AWS security guardrails should be rolled out gradually.

---

## 59. Too Many Explicit Denies

A very large deny policy can become difficult to:

```text
Understand

Maintain

Troubleshoot
```

Use clear policy ownership and documentation.

---

## 60. Allow List Without Understanding Dependencies

Example:

```text
Allow:
EC2 only
```

but EC2 workflow requires:

```text
KMS

IAM PassRole

SSM

CloudWatch
```

Result:

```text
Application Failure
```

Evaluate service dependencies.

---

## 61. Assuming SCP Protects Management Account

Incorrect:

```text
Root SCP
→ Protects Management Account
```

Correct:

```text
Management Account
→ Not Restricted by SCP
```

Management account requires separate strict operational security.

---

## 62. Assuming SCP Restricts Service-Linked Roles

Incorrect:

```text
SCP
→ Blocks All Service-Linked Roles
```

Correct:

```text
Service-Linked Roles
→ Not Restricted by SCP
```

---

# Hands-on Practice

## 63. Practice — Review SCPs

Navigate:

```text
AWS Organizations
      |
      v
Policies
      |
      v
Service Control Policies
```

Review:

```text
FullAWSAccess

Custom SCPs

Attached Targets
```

Do not modify production organization policies solely for practice.

---

## 64. Practice — Identify Attachments

For each SCP, determine whether it is attached to:

```text
Root

OU

Account
```

Then draw:

```text
Root
 |
 +-- Policy A
 |
 +-- Production OU
       |
       +-- Policy B
       |
       +-- Account
```

Determine which policies apply to the account.

---

## 65. Practice — Permission Evaluation

Scenario:

```text
Root SCP:
FullAWSAccess

Production SCP:
Deny s3:DeleteBucket

IAM:
AdministratorAccess
```

Question:

```text
Can user delete S3 bucket?
```

Answer:

```text
No
```

Reason:

```text
Explicit SCP Deny
```

---

## 66. Practice — Allow-List Evaluation

Scenario:

```text
Root:
Allow *

OU:
Allow ec2:* and s3:*

IAM:
Allow lambda:CreateFunction
```

Result:

```text
Lambda CreateFunction
→ Denied
```

because the OU SCP does not include Lambda.

---

## 67. Practice — Design Logging Protection

Requirement:

```text
Workload administrators
must not disable CloudTrail.
```

Design conceptually:

```text
Deny:
cloudtrail:StopLogging
cloudtrail:DeleteTrail
```

Then determine whether an approved central security role needs an exception.

---

## 68. Practice — Region Restriction

Requirement:

```text
Workloads should operate only in:

Tokyo

Osaka
```

Design:

```text
aws:RequestedRegion

Allow:
ap-northeast-1
ap-northeast-3
```

Then identify global AWS services that require exceptions.

---

## 69. Optional CLI Practice

List SCPs:

```bash
aws organizations list-policies \
  --filter SERVICE_CONTROL_POLICY
```

Describe a policy:

```bash
aws organizations describe-policy \
  --policy-id <policy-id>
```

List targets:

```bash
aws organizations list-targets-for-policy \
  --policy-id <policy-id>
```

List policies attached to an OU or account:

```bash
aws organizations list-policies-for-target \
  --target-id <target-id> \
  --filter SERVICE_CONTROL_POLICY
```

Do not publish real:

```text
Organization IDs

Account IDs

OU IDs

Policy IDs

Internal Security Policy Details
```

to a public GitHub repository.

---

# Architecture Exercise

## 70. Design Guardrails

Organization:

```text
Root
│
├── Security OU
├── Infrastructure OU
└── Workloads OU
    ├── Production
    └── Development
```

Requirements:

```text
All Accounts:
Cannot leave organization

All Workloads:
Cannot disable CloudTrail

Production:
Only approved Regions

Development:
More service flexibility
```

Possible design:

```text
Root SCP
→ Deny LeaveOrganization

Workloads OU SCP
→ Protect Logging

Production SCP
→ Region Restriction
```

---

## 71. Why Layer Policies?

Instead of one giant SCP:

```text
One Huge Policy
```

use logical guardrails:

```text
Organization Protection

Logging Protection

Region Restriction

Production Protection
```

This improves:

```text
Readability

Testing

Ownership

Troubleshooting
```

---

# Security Checklist

```text
[ ] SCPs are enabled only in an organization with all features

[ ] SCPs are understood as guardrails, not permission grants

[ ] FullAWSAccess behavior is understood

[ ] Root-level SCPs are minimal

[ ] New SCPs are tested in a test OU first

[ ] Explicit Deny is used deliberately

[ ] Allow-list strategies account for service dependencies

[ ] Management account protection does not rely on SCPs

[ ] Member account root users are governed by SCPs

[ ] Service-linked role exceptions are understood

[ ] Delegated administrator accounts are covered by appropriate SCPs

[ ] Core logging services are protected

[ ] Security service configuration is protected where appropriate

[ ] Region restrictions account for global services

[ ] Cross-account administrative exceptions are narrowly scoped

[ ] SCPs are documented

[ ] Service last accessed data is reviewed

[ ] CloudTrail is used to investigate policy impact

[ ] AccessDenied troubleshooting includes SCP evaluation

[ ] RCPs are considered when resource-side guardrails are required
```

---

## Key Takeaways

- Service Control Policies define maximum permission guardrails for AWS Organizations member accounts.
- SCPs never grant IAM permissions.
- IAM permissions must still explicitly allow an action.
- An applicable explicit SCP Deny overrides IAM Allow.
- Effective permissions depend on every applicable SCP in the organization hierarchy.
- FullAWSAccess means the SCP layer initially does not restrict AWS actions.
- Removing FullAWSAccess requires careful allow-list design.
- SCPs affect IAM users, IAM roles, and the root user of member accounts.
- SCPs do not restrict the management account.
- SCPs do not restrict service-linked roles.
- Delegated administrator accounts are still member accounts and are affected by SCPs.
- Deny-list strategies are easier to operate but provide broader default capability.
- Allow-list strategies provide stronger restrictions but require more maintenance.
- SCPs can help protect logging and security services from workload administrators.
- Region restrictions require careful treatment of global AWS services.
- SCPs should be tested in isolated accounts or OUs before broad deployment.
- Resource Control Policies complement SCPs by providing resource-side organization guardrails.

---

## Reflection

Today I learned that Service Control Policies are organization-level permission guardrails rather than normal IAM permission policies.

The most important lesson is that an SCP never grants permission. An IAM principal must still receive an IAM Allow, and the requested operation must also remain within every applicable SCP permission boundary.

I also learned that SCPs are powerful because they can restrict even highly privileged IAM administrators and the root user of member accounts.

However, SCPs do not apply to the management account or service-linked roles, so these exceptions must be understood when designing security architecture.

From a cloud security perspective, SCPs provide a strong mechanism for enforcing organization-wide preventive controls such as protecting security logging, restricting AWS Regions, preventing member accounts from leaving the organization, and limiting dangerous administrative operations.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Allow List | Model that permits only explicitly approved actions |
| Deny List | Model that permits broad access except explicitly prohibited actions |
| Explicit Deny | Policy decision that overrides applicable Allow permissions |
| FullAWSAccess | Default SCP that places no additional SCP restriction on AWS actions |
| Guardrail | Organization-wide boundary restricting what actions may be performed |
| Implicit Deny | Denial caused by the absence of a required Allow |
| Policy Inheritance | Application of organization policies through Root, OU, and account hierarchy |
| RCP | Organization policy that defines maximum permissions available to organization resources |
| SCP | AWS Organizations policy that defines maximum permission guardrails |
| Service-Linked Role | AWS service-specific IAM role that is not restricted by SCPs |
