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
- [ ] Day 3 — IAM Users, Groups, Roles & Policies
- [ ] Day 4 — IAM Policy Evaluation
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

## Vocabulary

| Word | Meaning |
|---|---|
| Assume Role | The process of obtaining temporary permissions from an IAM role |
| Authentication | The process of verifying an identity |
| Authorization | The process of determining what an identity can access |
| Availability Zone | An isolated infrastructure location within an AWS Region |
| Configuration | Settings that determine how a system or service operates |
| Credential | Information used to prove an identity |
| Identity | A user, service, or entity that can interact with AWS resources |
| Infrastructure | The underlying computing, networking, and physical resources |
| Least Privilege | Granting only the minimum permissions required |
| Permission | Authorization to perform a specific action |
| Privilege | A level of access or authority granted to an identity |
| Region | A geographical area where AWS operates cloud infrastructure |
| Resilience | The ability of a system to continue operating or recover from failures |
| Responsibility | A duty or obligation to manage or protect something |
| Temporary Credential | A credential that expires after a limited period |


