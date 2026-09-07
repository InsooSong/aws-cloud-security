# AWS Cloud Security

> Hands-on learning notes for AWS and Cloud Security.

This repository documents my AWS learning journey with a focus on cloud security architecture, identity and access management, networking, encryption, logging, monitoring, threat detection, and security automation.

---

# Learning Objectives

- Understand AWS core architecture and services
- Learn identity and access management in AWS
- Build secure AWS network architectures
- Understand data protection and encryption
- Implement logging and monitoring
- Learn cloud threat detection techniques
- Understand major AWS security services
- Practice cloud security automation
- Build a practical foundation for cloud security engineering

---

# Roadmap

## Phase 1 — AWS Fundamentals & IAM

- [x] Day 1 — AWS Fundamentals & Shared Responsibility Model
- [x] Day 2 — AWS IAM Fundamentals
- [x] Day 3 — IAM Users, Groups, Roles & Policies
- [x] Day 4 — IAM Policy Evaluation
- [ ] Day 5 — IAM Security Best Practices

## Phase 2 — AWS Networking

- [ ] Day 6 — VPC Fundamentals
- [ ] Day 7 — Public & Private Subnets
- [ ] Day 8 — Route Tables & Internet Gateway
- [ ] Day 9 — NAT Gateway
- [ ] Day 10 — Security Groups
- [ ] Day 11 — Network ACLs
- [ ] Day 12 — VPC Security Review

## Phase 3 — Compute & Storage Security

- [ ] Day 13 — EC2 Fundamentals & Security
- [ ] Day 14 — EC2 Security Hardening
- [ ] Day 15 — S3 Fundamentals
- [ ] Day 16 — S3 Access Control & Security
- [ ] Day 17 — EBS Encryption
- [ ] Day 18 — RDS Security
- [ ] Day 19 — Compute & Storage Security Review

## Phase 4 — Logging & Monitoring

- [ ] Day 20 — AWS CloudTrail
- [ ] Day 21 — Amazon CloudWatch
- [ ] Day 22 — AWS Config
- [ ] Day 23 — Centralized Logging
- [ ] Day 24 — Logging & Monitoring Review

## Phase 5 — Data Protection & Threat Detection

- [ ] Day 25 — AWS KMS Fundamentals
- [ ] Day 26 — KMS Keys & Encryption
- [ ] Day 27 — AWS Secrets Manager
- [ ] Day 28 — Amazon GuardDuty
- [ ] Day 29 — AWS Security Hub
- [ ] Day 30 — Amazon Inspector
- [ ] Day 31 — Amazon Macie
- [ ] Day 32 — AWS WAF & Shield
- [ ] Day 33 — Security Services Review

## Phase 6 — AWS Security Architecture

- [ ] Day 34 — AWS Organizations
- [ ] Day 35 — Service Control Policies
- [ ] Day 36 — Multi-Account Security Architecture
- [ ] Day 37 — Centralized Security & Logging
- [ ] Day 38 — AWS Security Architecture Review

## Phase 7 — Security Automation

- [ ] Day 39 — AWS CLI Fundamentals
- [ ] Day 40 — AWS CLI for Security Operations
- [ ] Day 41 — Python & boto3 Fundamentals
- [ ] Day 42 — Security Automation with boto3
- [ ] Day 43 — Terraform Fundamentals for AWS
- [ ] Day 44 — Terraform Security Configuration
- [ ] Day 45 — AWS Cloud Security Final Review

---

# Day 1 — AWS Fundamentals & Cloud Security Overview

## Topic

AWS Fundamentals, Global Infrastructure, and Shared Responsibility Model

---

## Objectives

- Understand AWS global infrastructure
- Understand Regions and Availability Zones
- Understand the AWS Shared Responsibility Model
- Learn the basic categories of AWS services
- Understand AWS accounts as security boundaries
- Identify major AWS security services
- Develop a basic cloud security perspective

---

## 1. AWS Global Infrastructure

AWS operates cloud infrastructure around the world using Regions and Availability Zones.

### Region

A Region is a geographical area where AWS operates infrastructure.

Examples:

```text
ap-northeast-1 → Tokyo
ap-northeast-2 → Seoul
us-east-1      → N. Virginia
```

Choosing a Region can affect:

- Data residency
- Compliance requirements
- Network latency
- Disaster recovery strategy
- Service availability

From a security perspective, Region selection is important because organizations may have legal or regulatory requirements regarding where data is stored and processed.

---

## 2. Availability Zone

Each AWS Region contains multiple Availability Zones.

An Availability Zone is one or more physically separated data centers within a Region.

The basic infrastructure hierarchy can be understood as:

```text
AWS
└── Region
    └── Availability Zone
        └── Data Center
```

Using multiple Availability Zones can improve:

- High availability
- Fault tolerance
- Resilience
- Disaster recovery capability

Availability Zones are designed to be isolated from failures in other Availability Zones while being connected through high-bandwidth, low-latency networking.

---

## 3. AWS Shared Responsibility Model

Security responsibilities in AWS are divided between AWS and the customer.

```text
Security OF the Cloud
→ AWS Responsibility

Security IN the Cloud
→ Customer Responsibility
```

### AWS Responsibilities

AWS is responsible for protecting the infrastructure that runs AWS services.

Examples include:

- Physical data centers
- Physical security
- Hardware
- Storage infrastructure
- Networking infrastructure
- Virtualization infrastructure
- Underlying cloud platform

### Customer Responsibilities

Customers are responsible for securely configuring and operating their AWS resources.

Examples include:

- IAM configuration
- User permissions
- Credentials
- Operating system configuration
- Operating system patching
- Application security
- Security Groups
- Network ACLs
- Data classification
- Encryption configuration
- Logging configuration

---

## 4. Responsibility Depends on the Service

The customer's level of responsibility changes depending on the AWS service being used.

For example:

```text
EC2
→ Customer manages more of the operating environment

RDS
→ AWS manages more of the underlying infrastructure

S3
→ AWS manages the storage infrastructure
→ Customer manages data, permissions, and configuration
```

With Amazon EC2, customers are responsible for areas such as:

- Guest operating system
- OS patching
- Installed applications
- IAM permissions
- Network configuration
- Data protection

With managed services, AWS manages more of the underlying infrastructure, but customers are still responsible for secure access control, data protection, and service configuration.

---

## 5. Core AWS Service Categories

### Compute

```text
Amazon EC2
AWS Lambda
Amazon ECS
Amazon EKS
```

### Storage

```text
Amazon S3
Amazon EBS
Amazon EFS
```

### Database

```text
Amazon RDS
Amazon Aurora
Amazon DynamoDB
```

### Networking

```text
Amazon VPC
Amazon Route 53
Amazon CloudFront
Elastic Load Balancing
```

### Identity & Security

```text
AWS IAM
AWS KMS
AWS Secrets Manager
Amazon GuardDuty
AWS Security Hub
Amazon Inspector
Amazon Macie
AWS WAF
AWS Shield
```

### Logging & Monitoring

```text
AWS CloudTrail
Amazon CloudWatch
AWS Config
```

---

## 6. Core AWS Security Services

| Service | Main Purpose |
|---|---|
| AWS IAM | Controls identities and permissions |
| AWS KMS | Manages encryption keys |
| AWS Secrets Manager | Manages credentials and secrets |
| AWS CloudTrail | Records AWS API activity |
| Amazon CloudWatch | Monitors metrics, logs, and system activity |
| AWS Config | Tracks AWS resource configurations |
| Amazon GuardDuty | Detects suspicious and malicious activity |
| AWS Security Hub | Aggregates and manages security findings |
| Amazon Inspector | Identifies software vulnerabilities and exposure |
| Amazon Macie | Discovers sensitive data in Amazon S3 |
| AWS WAF | Protects web applications from malicious requests |
| AWS Shield | Provides protection against DDoS attacks |

---

## 7. AWS Account as a Security Boundary

An AWS account acts as an important security and resource boundary.

A single AWS account can contain resources such as:

```text
AWS Account
│
├── IAM
├── VPC
├── EC2
├── S3
├── RDS
├── CloudTrail
├── CloudWatch
└── KMS
```

In enterprise environments, organizations often use multiple AWS accounts.

Example:

```text
AWS Organization
│
├── Management Account
├── Security Account
├── Logging Account
├── Production Account
├── Development Account
└── Sandbox Account
```

Separating workloads into multiple accounts can improve:

- Security isolation
- Access control
- Logging
- Compliance
- Resource management
- Incident response

Later, this architecture can be managed using AWS Organizations and Service Control Policies.

---

## 8. Cloud Security Perspective

When evaluating an AWS resource, I can analyze security using five major perspectives:

```text
Identity
Network
Data
Logging
Detection
```

### Identity

Question:

```text
Who can access the resource?
```

Related AWS services:

```text
IAM
IAM Roles
IAM Policies
```

### Network

Question:

```text
From where can the resource be accessed?
```

Related AWS services:

```text
VPC
Security Groups
Network ACLs
```

### Data Protection

Question:

```text
How is the data protected?
```

Related AWS services:

```text
AWS KMS
Encryption
AWS Secrets Manager
```

### Logging

Question:

```text
Who performed an action and what happened?
```

Related AWS services:

```text
AWS CloudTrail
Amazon CloudWatch
AWS Config
```

### Detection

Question:

```text
Is suspicious activity occurring?
```

Related AWS services:

```text
Amazon GuardDuty
AWS Security Hub
Amazon Inspector
Amazon Macie
```

---

## 9. Example — EC2 Security Perspective

Amazon EC2 can be evaluated using the same security model.

```text
Amazon EC2
│
├── Identity
│   └── IAM
│
├── Network
│   ├── VPC
│   ├── Security Groups
│   └── Network ACLs
│
├── Data
│   ├── EBS Encryption
│   └── AWS KMS
│
├── Logging
│   ├── AWS CloudTrail
│   └── Amazon CloudWatch
│
└── Detection
    └── Amazon GuardDuty
```

Questions to consider:

- Who can manage the EC2 instance?
- Which networks can communicate with it?
- Is the attached storage encrypted?
- Who changed the EC2 configuration?
- Are there any suspicious activities related to the instance?

Thinking about AWS resources from these perspectives helps build a security-focused mindset rather than simply memorizing individual AWS services.

---

## 10. Hands-on Practice

For today's practice, I explored the AWS Management Console and located the following services:

- IAM
- EC2
- VPC
- S3
- CloudTrail
- CloudWatch
- KMS
- GuardDuty

The goal was to become familiar with where major AWS and security services are located and understand their basic roles.

### IAM

Controls identities, authentication, and permissions.

### KMS

Manages encryption keys used to protect data in AWS.

### CloudTrail

Records API calls and account activity for auditing and investigation.

### CloudWatch

Collects metrics, logs, and monitoring information from AWS resources and applications.

### GuardDuty

Analyzes AWS data sources to identify potentially malicious or suspicious activity.

---

## Key Takeaways

- AWS infrastructure is organized into Regions and Availability Zones.
- Multiple Availability Zones improve availability and resilience.
- AWS and customers share security responsibilities.
- AWS is responsible for security **of** the cloud.
- Customers are responsible for security **in** the cloud.
- Customer responsibility depends on the AWS service being used.
- AWS accounts provide important security and resource boundaries.
- Cloud security can be analyzed through identity, network, data, logging, and detection.
- Using cloud services does not automatically make a workload secure.
- Secure AWS environments require proper configuration, access control, monitoring, and data protection.

---

## Reflection

Before studying individual AWS security services, I need to understand how AWS infrastructure and security responsibilities are divided.

One important lesson from the Shared Responsibility Model is that using AWS does not automatically make an application secure.

AWS protects the underlying cloud infrastructure, while customers must securely configure their identities, networks, workloads, applications, and data.

I also learned that AWS security can be approached systematically by considering five areas:

```text
Identity
Network
Data
Logging
Detection
```

I will use these perspectives when studying individual AWS services and cloud architectures.

---

## Next Step

Day 2 will focus on AWS Identity and Access Management (IAM).

Topics will include:

- IAM fundamentals
- Authentication
- Authorization
- IAM users
- IAM groups
- IAM roles
- IAM policies
- Principle of least privilege

---

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

## Next Step

Day 3 will focus on IAM users, user groups, roles, and policies in more detail.

Topics will include:

- IAM users
- IAM user groups
- IAM roles
- Identity-based policies
- AWS managed policies
- Customer managed policies
- Inline policies
- Role assumption
- Temporary credentials

---

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

## Next Step

Day 4 will focus on IAM policy evaluation.

Topics will include:

- Explicit Allow
- Explicit Deny
- Implicit Deny
- Identity-based policies
- Resource-based policies
- Permission boundaries
- Service Control Policies
- Policy evaluation logic
- Conflicting permissions

---

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

## Next Step

Day 5 will focus on IAM security best practices.

Topics will include:

- Root user protection
- MFA
- Least privilege
- Temporary credentials
- IAM roles
- Access key management
- IAM Identity Center
- Credential rotation
- IAM Access Analyzer
- Permission review
- Privileged access
- IAM security checklist

---

## Vocabulary

| Word | Meaning |
|---|---|
| Assume Role | The process of obtaining temporary permissions from an IAM role |
| Authentication | The process of verifying an identity |
| Authorization | The process of determining what an identity can access |
| Availability Zone | An isolated infrastructure location within an AWS Region |
| Configuration | Settings that determine how a system or service operates |
| Credential | Information used to prove an identity |
| Delegation | Granting another identity permission to perform actions |
| Effective Permission | The final permissions available after all policies are evaluated |
| Explicit Deny | A policy statement that specifically denies an action |
| Group | A collection of IAM users used for permission management |
| Guardrail | A security control that limits what actions are possible |
| Identity | A user, service, or entity that can interact with AWS resources |
| Implicit Deny | Access denied because no applicable Allow exists |
| Infrastructure | The underlying computing, networking, and physical resources |
| Inline Policy | A policy embedded directly in one IAM identity |
| Least Privilege | Granting only the minimum permissions required |
| Managed Policy | A reusable IAM policy managed separately from an identity |
| Permission | Authorization to perform a specific action |
| Permissions Boundary | A policy that defines maximum permissions for an IAM user or role |
| Policy | A document that defines AWS permissions |
| Policy Evaluation | The process AWS uses to determine whether a request is allowed |
| Principal | An identity making a request to AWS |
| Privilege | A level of access or authority granted to an identity |
| Region | A geographical area where AWS operates cloud infrastructure |
| Request Context | Information AWS uses when evaluating an authorization request |
| Resilience | The ability of a system to continue operating or recover from failures |
| Resource-Based Policy | A policy attached directly to an AWS resource |
| Responsibility | A duty or obligation to manage or protect something |
| Role | An IAM identity that provides temporary permissions |
| SCP | An AWS Organizations policy that limits available permissions |
| Temporary Credential | A credential that expires after a limited period |
| User | An IAM identity that can have long-term AWS credentials |
