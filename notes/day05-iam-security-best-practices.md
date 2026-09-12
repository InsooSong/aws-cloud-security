# Day 5 — IAM Security Best Practices

## Topic

AWS IAM Security Best Practices and Secure Access Management

---

## Objectives

- Understand IAM security best practices
- Protect the AWS root user
- Understand the importance of MFA
- Prefer temporary credentials over long-term credentials
- Understand when to use IAM roles
- Apply the Principle of Least Privilege
- Understand secure access key management
- Learn the purpose of IAM Identity Center
- Understand IAM Access Analyzer
- Review and remove unused IAM permissions and credentials

---

## 1. IAM Security Strategy

AWS IAM security is not only about granting permissions.

A secure IAM design should answer several questions:

```text
Who needs access?

How should the identity authenticate?

What permissions are required?

How long should the access exist?

Can temporary credentials be used?

Can permissions be reduced?

Is the access being monitored?
```

A useful security model is:

```text
Identity
   ↓
Strong Authentication
   ↓
Temporary Credentials
   ↓
Least Privilege
   ↓
Monitoring and Review
```

---

## 2. Protect the AWS Root User

The AWS account root user has highly privileged access to the AWS account.

Because of this, the root user should not be used for normal daily administration.

Recommended approach:

```text
Root User
→ Use only when root-level access is required

Normal Administration
→ IAM Identity Center / IAM Roles / Administrative Identity
```

Important root user security practices include:

- Enable MFA
- Use a strong and unique password
- Do not use the root user for daily tasks
- Do not create unnecessary root access keys
- Protect account recovery mechanisms
- Monitor root user activity

The root user should be treated as an emergency or account-level administrative identity.

---

## 3. Multi-Factor Authentication

Multi-Factor Authentication (MFA) adds another authentication factor in addition to a password.

```text
Password
+
MFA
```

MFA helps reduce the risk of account compromise when a password is exposed.

MFA is especially important for:

- AWS root users
- Privileged administrators
- IAM users with console access
- Sensitive environments

A compromised password alone should not be enough to access a highly privileged AWS identity.

---

## 4. Prefer Temporary Credentials

Long-term credentials create additional security risks because they remain valid until they are rotated, disabled, or deleted.

Examples of long-term credentials include:

```text
IAM User Password

Access Key ID
+
Secret Access Key
```

Temporary credentials automatically expire.

Conceptually:

```text
Identity
   ↓
Assume Role
   ↓
Temporary Credentials
   ↓
AWS Resources
```

Temporary credentials typically include:

```text
Access Key ID
Secret Access Key
Session Token
Expiration
```

Because temporary credentials expire automatically, they reduce the risk associated with long-lived credentials.

---

## 5. Human Access to AWS

For human users, centralized and federated access is generally preferable to creating large numbers of individual IAM users.

Conceptually:

```text
Employee
   ↓
Identity Provider
   ↓
IAM Identity Center
   ↓
AWS Account
   ↓
IAM Role
   ↓
Temporary Credentials
```

This approach provides:

- Centralized identity management
- Temporary credentials
- Easier access removal
- Consistent permissions
- Better multi-account access management

IAM users may still be required for certain use cases, but they should not automatically be the default choice for every human user.

---

## 6. IAM Identity Center

AWS IAM Identity Center can be used to centrally manage workforce access to AWS accounts and applications.

Conceptually:

```text
Organization Users
       ↓
IAM Identity Center
       ↓
Permission Sets
       ↓
AWS Accounts
```

Example:

```text
Security Engineer
       ↓
IAM Identity Center
       ↓
SecurityAudit Permission Set
       ↓
Development Account
Production Account
Security Account
```

Benefits include:

- Centralized user access
- Multi-account management
- Temporary credentials
- Easier onboarding and offboarding
- Integration with external identity providers

---

## 7. Workload Access

Applications and AWS services often require access to other AWS resources.

A poor security design is:

```text
EC2 Application
      ↓
Hard-coded Access Key
      ↓
Amazon S3
```

Problems include:

- Credential exposure
- Difficult rotation
- Long credential lifetime
- Risk of accidental GitHub exposure

A better design is:

```text
EC2
 ↓
IAM Role
 ↓
Temporary Credentials
 ↓
Amazon S3
```

AWS workloads should use IAM roles whenever possible.

Examples:

```text
EC2
→ IAM Role

Lambda
→ Execution Role

ECS Task
→ Task Role
```

---

## 8. Never Hard-Code AWS Credentials

AWS credentials should never be embedded directly into:

- Source code
- Configuration files
- Docker images
- Shell scripts
- Git repositories
- Public GitHub repositories

Bad example:

```python
aws_access_key_id = "ACCESS_KEY"
aws_secret_access_key = "SECRET_KEY"
```

Better approach:

```text
Application
   ↓
IAM Role
   ↓
Temporary Credentials
```

For local development, credentials should also be managed securely rather than embedded in source code.

---

## 9. Access Key Security

Some use cases may still require long-term access keys.

When long-term credentials are required:

- Create them only when necessary
- Do not share them
- Never publish them
- Remove unused keys
- Review when they were last used
- Update or rotate them when required
- Disable credentials before deleting them if necessary
- Prefer temporary credentials whenever possible

A useful rule is:

```text
No Access Key
→ Better than unused Access Key

Temporary Credential
→ Better than unnecessary long-term credential
```

---

## 10. Credential Exposure Response

If an AWS access key is accidentally exposed, simply removing the key from the latest Git commit is not enough.

The exposed credential may already exist in:

```text
Git History
GitHub Cache
Forks
Logs
External Systems
```

Recommended response:

```text
Credential Exposed
      ↓
Disable / Revoke Credential
      ↓
Create Replacement if Required
      ↓
Investigate Usage
      ↓
Remove Secret from Repository
      ↓
Review Logs
```

Potentially exposed credentials should be treated as compromised.

---

## 11. Principle of Least Privilege

Least privilege means granting only the permissions necessary to perform a task.

Bad example:

```text
Application
→ AdministratorAccess
```

Better:

```text
Application
→ s3:GetObject
→ Specific Bucket
```

Even better:

```text
Required Action
+
Required Resource
+
Required Conditions
```

Example:

```text
Allow:
s3:GetObject

Resource:
security-report-bucket/*

Condition:
Required security context
```

Least privilege should be applied to:

- IAM users
- IAM roles
- Applications
- Administrators
- AWS services
- Cross-account access

---

## 12. Start Broad, Then Reduce Permissions

During initial development, managed policies may sometimes be useful for understanding or testing required access.

However, permissions should be reduced over time.

Conceptually:

```text
Initial Development
       ↓
AWS Managed Policy
       ↓
Observe Actual Usage
       ↓
Create More Restrictive Policy
       ↓
Least Privilege
```

The goal should be to move toward permissions that match actual requirements.

---

## 13. IAM Access Analyzer

IAM Access Analyzer helps identify and analyze access to AWS resources.

It can be used for tasks such as:

- Identifying external access
- Reviewing public access
- Reviewing cross-account access
- Validating IAM policies
- Generating policies based on access activity

Conceptually:

```text
AWS Resource
    ↓
Access Analyzer
    ↓
Analyze Access
    ↓
Security Finding
```

Example:

```text
S3 Bucket
   ↓
Accessible from external account
   ↓
IAM Access Analyzer
   ↓
Finding
```

This helps security teams identify unintended access.

---

## 14. Policy Validation

IAM Access Analyzer can also help validate IAM policies.

It can identify potential issues such as:

```text
Invalid Policy Elements

Security Warnings

Overly Broad Permissions

Policy Errors
```

Before deploying an IAM policy, it is useful to verify whether the policy behaves as intended.

A secure workflow can be:

```text
Create Policy
    ↓
Validate Policy
    ↓
Test Permissions
    ↓
Deploy
    ↓
Monitor Usage
```

---

## 15. Review Unused Permissions

IAM environments tend to accumulate unused permissions over time.

Examples include:

```text
Old IAM Users

Unused IAM Roles

Unused Access Keys

Old Policies

Unused Permissions

Former Employee Accounts
```

These increase the attack surface.

Regular reviews should identify:

```text
Is this identity still required?

Is this role still used?

When was this access key last used?

Are all attached permissions still necessary?

Can this policy be reduced?
```

---

## 16. Identity Lifecycle

IAM security should include the full identity lifecycle.

```text
Create
  ↓
Grant Access
  ↓
Use
  ↓
Review
  ↓
Reduce / Update
  ↓
Remove
```

For employees:

```text
Join Company
   ↓
Required Access Granted
   ↓
Role Changes
   ↓
Permissions Updated
   ↓
Employee Leaves
   ↓
Access Removed
```

This is especially important in enterprise cloud environments.

---

## 17. Privileged Access

Administrative permissions should be treated differently from normal access.

Instead of giving permanent administrator permissions:

```text
User
→ Permanent AdministratorAccess
```

A more secure design can use:

```text
Normal User
   ↓
Assume Privileged Role
   ↓
Temporary Administrator Access
```

Additional controls may include:

- MFA
- Short session duration
- Logging
- Approval processes
- Restricted conditions

This reduces permanent privileged access.

---

## 18. Use Policy Conditions

IAM policy conditions can further restrict when permissions can be used.

Conceptually:

```text
Allow Action
      ↓
Only When Condition Matches
```

Conditions may evaluate information such as:

- Source IP address
- MFA authentication
- AWS Region
- Resource tags
- Principal tags
- Network context

Example concept:

```text
Allow Administrative Action
        ↓
Only when MFA is present
```

Conditions can provide an additional security layer beyond basic action and resource permissions.

---

## 19. Permission Guardrails

Organizations can use additional controls to limit maximum permissions.

Examples include:

```text
Permissions Boundaries
Service Control Policies
```

These controls do not grant permissions.

Instead, they establish boundaries.

Conceptually:

```text
Identity Policy
      ↓
Permissions Boundary
      ↓
SCP
      ↓
Effective Permissions
```

This supports centralized security governance.

---

## 20. IAM Security Monitoring

IAM security should also include monitoring.

Important events may include:

```text
Root User Login

IAM User Creation

Access Key Creation

Policy Changes

Role Changes

MFA Changes

Permission Escalation
```

AWS CloudTrail can record API activity related to IAM changes.

Conceptually:

```text
IAM Activity
     ↓
AWS CloudTrail
     ↓
Audit Logs
     ↓
Security Monitoring
```

Logging and monitoring will be studied in more detail later.

---

## 21. Example — Secure Human Access

Less secure design:

```text
Employee
   ↓
IAM User
   ↓
Permanent Access Key
   ↓
AdministratorAccess
```

Risks:

- Long-term credentials
- Excessive permissions
- Difficult access management
- Increased credential exposure risk

More secure design:

```text
Employee
   ↓
Identity Provider
   ↓
IAM Identity Center
   ↓
Assume Role
   ↓
Temporary Credentials
   ↓
Least-Privilege Permissions
```

---

## 22. Example — Secure Application Access

Less secure design:

```text
EC2 Application
       ↓
Access Key in Source Code
       ↓
AdministratorAccess
```

Better design:

```text
EC2 Application
       ↓
IAM Role
       ↓
Temporary Credentials
       ↓
Required AWS API Actions Only
```

This eliminates unnecessary long-term credentials and reduces permissions.

---

## 23. Hands-on Practice

For today's practice, I reviewed the IAM security configuration of my AWS account.

I checked the following areas:

### Root User

- MFA status
- Root user usage
- Root access keys

### IAM

- Existing IAM users
- Existing roles
- Existing access keys
- Attached policies
- Unused credentials

### IAM Access Analyzer

I explored IAM Access Analyzer and reviewed its purpose for identifying:

- External access
- Public access
- Cross-account access
- Policy validation

The goal was to understand how IAM security controls are applied in an AWS environment.

---

## 24. IAM Security Checklist

When reviewing an AWS environment, I should ask:

```text
Is the root user protected with MFA?

Is the root user used only when necessary?

Are human users using temporary credentials where possible?

Are workloads using IAM roles?

Are there unnecessary IAM users?

Are there unused access keys?

Are credentials stored in source code?

Are permissions based on least privilege?

Are privileged permissions permanent?

Can permissions be restricted with conditions?

Are old users and roles removed?

Has external access been reviewed?

Are IAM policies validated?

Are IAM changes logged?
```

---

## Key Takeaways

- The AWS root user should be protected and rarely used.
- MFA provides an important additional authentication layer.
- Temporary credentials are preferable to unnecessary long-term credentials.
- IAM roles should be used for AWS workloads whenever possible.
- Human workforce access can be centrally managed through IAM Identity Center.
- AWS credentials should never be hard-coded or committed to GitHub.
- Exposed credentials should be treated as compromised.
- Least privilege reduces the potential impact of security incidents.
- IAM Access Analyzer can help identify unintended access and validate policies.
- Unused users, roles, permissions, policies, and credentials should be regularly reviewed and removed.
- Privileged access should be limited and temporary where possible.
- IAM security requires continuous review, not only initial configuration.

---

## Reflection

Today I learned that secure IAM management requires more than simply creating users and assigning policies.

Long-term credentials increase security risk, so temporary credentials and IAM roles should be preferred whenever possible.

I also learned that human access and workload access should be managed differently. Human users can use centralized identity management and federation, while AWS workloads should use IAM roles.

The Principle of Least Privilege should be continuously applied because permissions that were originally required may become unnecessary over time.

IAM Access Analyzer and regular permission reviews can help identify excessive or unintended access.

IAM security therefore requires a continuous lifecycle of authentication, authorization, monitoring, review, and removal.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Access Analyzer | An IAM capability for analyzing resource and policy access |
| Credential Exposure | Accidental or unauthorized disclosure of credentials |
| Federation | Using an external identity system to access AWS |
| Guardrail | A control that limits the maximum permissions or actions available |
| Identity Lifecycle | The process of creating, managing, reviewing, and removing identities |
| Long-Term Credential | A credential that remains valid until changed or removed |
| Permission Review | The process of checking whether existing permissions are still required |
| Privileged Access | Access with elevated administrative permissions |
| Temporary Credential | A security credential that expires automatically |
| Workforce Identity | A human identity such as an employee or administrator |
