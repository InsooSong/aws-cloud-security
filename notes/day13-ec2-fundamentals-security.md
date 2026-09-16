# Day 13 — EC2 Fundamentals & Security

## Topic

Amazon EC2 Fundamentals and Basic Security Architecture

---

## Objectives

- Understand what Amazon EC2 is
- Understand EC2 instance components
- Learn the relationship between AMIs and EC2 instances
- Understand instance types
- Understand EC2 networking
- Learn the role of Security Groups
- Understand IAM Roles for EC2
- Understand EC2 storage options
- Learn basic EC2 security responsibilities
- Identify common EC2 security risks
- Build a security-focused mental model for EC2

---

## 1. What is Amazon EC2?

Amazon Elastic Compute Cloud (EC2) provides virtual servers in AWS.

An EC2 instance can run operating systems and applications in the same way as a traditional server.

Conceptually:

```text
AWS
 ↓
Amazon EC2
 ↓
Virtual Machine
 ↓
Operating System
 ↓
Application
```

Common EC2 use cases include:

- Web servers
- Application servers
- Development environments
- Security tools
- Batch workloads
- Backend services
- Self-managed databases
- Custom software workloads

---

## 2. EC2 and the Shared Responsibility Model

Amazon EC2 is an Infrastructure as a Service (IaaS) service.

Because customers control the operating system and applications, they have significant security responsibility.

Conceptually:

```text
AWS Responsibility

Physical Data Center
Hardware
Networking Infrastructure
Hypervisor

----------------------------

Customer Responsibility

Guest Operating System
OS Patching
Applications
IAM Permissions
Security Groups
Data Protection
Instance Configuration
```

EC2 therefore requires more customer-side security management than many fully managed AWS services.

---

## 3. EC2 Instance Components

An EC2 instance depends on several AWS components.

```text
EC2 Instance
│
├── AMI
├── Instance Type
├── VPC
├── Subnet
├── Security Group
├── IAM Role
├── Storage
└── Key / Management Method
```

Each component can affect security.

---

## 4. Amazon Machine Image

An Amazon Machine Image (AMI) is a template used to launch EC2 instances.

An AMI can contain:

- Operating system
- Installed software
- Configuration
- Application components

Conceptually:

```text
AMI
 ↓
Launch
 ↓
EC2 Instance
```

Examples include:

```text
Amazon Linux
Ubuntu
Red Hat Enterprise Linux
Windows Server
```

---

## 5. AMI Security Considerations

The AMI becomes the starting point for an EC2 instance.

Therefore, the AMI should be trusted and maintained.

Security questions include:

```text
Who created this AMI?

Is the operating system supported?

Are known vulnerabilities patched?

Does the AMI contain unnecessary software?

Does the image contain credentials or secrets?
```

A compromised or poorly configured AMI can create insecure instances from the moment they are launched.

---

## 6. Instance Types

EC2 instance types define the hardware resources available to the instance.

Examples:

```text
General Purpose

Compute Optimized

Memory Optimized

Storage Optimized

Accelerated Computing
```

A simplified example:

```text
t3.micro

m7i.large

c7i.large

r7i.large
```

Instance type selection mainly affects:

- CPU
- Memory
- Network performance
- Storage capabilities
- Cost

It is primarily a performance and cost decision, but resource sizing can also affect availability and security operations.

---

## 7. EC2 Networking

An EC2 instance is launched into a subnet inside a VPC.

Conceptually:

```text
VPC
 ↓
Subnet
 ↓
EC2
```

The instance normally receives:

```text
Private IPv4 Address
```

Depending on the architecture, it may also receive:

```text
Public IPv4 Address

or

Elastic IP
```

Network exposure depends on multiple components.

---

## 8. Public EC2 Instance

A directly Internet-accessible EC2 instance typically requires:

```text
Public Subnet

Public IPv4 / Elastic IP

Route to Internet Gateway

Security Group Rules

Network ACL Rules
```

Conceptually:

```text
Internet
   ↓
Internet Gateway
   ↓
Public Route Table
   ↓
Public Subnet
   ↓
Security Group
   ↓
EC2
```

Public placement should only be used when direct Internet connectivity is actually required.

---

## 9. Private EC2 Instance

A private EC2 instance can run without direct inbound Internet access.

Example:

```text
Internet
   ↓
Application Load Balancer
   ↓
Private EC2
```

For outbound Internet access:

```text
Private EC2
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

This reduces direct exposure of the instance.

---

## 10. Security Groups for EC2

Security Groups act as stateful virtual firewalls for EC2 network interfaces.

Example:

```text
Internet
   ↓
Security Group
   ↓
EC2
```

A secure configuration should allow only required traffic.

Example:

```text
HTTPS

TCP 443

Source:
0.0.0.0/0
```

may be appropriate for a public web service.

But:

```text
SSH

TCP 22

Source:
0.0.0.0/0
```

creates unnecessary exposure in many environments.

---

## 11. EC2 Management Access

Traditionally, Linux EC2 instances may be managed using SSH.

Example:

```text
Administrator
    ↓
SSH 22
    ↓
EC2
```

Windows instances may use:

```text
RDP 3389
```

However, exposing management ports directly to the Internet increases the attack surface.

A more secure architecture may use:

```text
AWS Systems Manager Session Manager
```

instead of direct SSH or RDP access where appropriate.

---

## 12. AWS Systems Manager Session Manager

Session Manager provides interactive access to supported EC2 instances without requiring direct inbound SSH or RDP connectivity.

Conceptually:

```text
Administrator
      ↓
AWS Systems Manager
      ↓
IAM Authorization
      ↓
EC2
```

Potential benefits include:

- No inbound SSH port required
- No inbound RDP port required
- IAM-based access control
- Centralized access management
- Session logging options
- Reduced public network exposure

---

## 13. SSH Key Pairs

EC2 Linux instances can use key pairs for SSH authentication.

Conceptually:

```text
Private Key
→ Administrator

Public Key
→ EC2 Instance
```

The private key must be protected.

Important rules:

```text
Never publish the private key

Do not commit it to GitHub

Restrict file permissions

Remove unused keys

Protect backups
```

A private SSH key should be treated as a sensitive credential.

---

## 14. IAM Role for EC2

An EC2 workload may need access to other AWS services.

A poor design is:

```text
EC2
 ↓
Hard-coded AWS Access Key
 ↓
Amazon S3
```

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

EC2 uses an instance profile to provide the role to the instance.

This avoids storing permanent AWS credentials on the server.

---

## 15. EC2 Instance Role Example

Suppose an application needs to read from S3.

Required permission:

```text
s3:GetObject
```

Architecture:

```text
EC2
 ↓
IAM Role
 ↓
S3 Read Policy
 ↓
Amazon S3
```

Instead of:

```text
EC2
 ↓
AdministratorAccess
```

the role should follow least privilege.

---

## 16. Instance Metadata Service

EC2 provides instance metadata that workloads can access from inside the instance.

Metadata can contain information about:

- Instance identity
- Network configuration
- IAM role credentials
- Instance details

This service is commonly referred to as:

```text
Instance Metadata Service
```

or:

```text
IMDS
```

---

## 17. IMDS Security

Because IAM role credentials can be obtained through instance metadata, metadata access is security-sensitive.

AWS provides:

```text
IMDSv2
```

which uses a session-oriented request model.

IMDSv2 provides stronger protection than the older IMDSv1 model against certain metadata-related attack scenarios.

A security-focused EC2 configuration should prefer:

```text
IMDSv2
```

and restrict metadata access where appropriate.

---

## 18. Metadata Attack Scenario

Suppose a vulnerable web application allows Server-Side Request Forgery (SSRF).

Conceptually:

```text
Attacker
   ↓
Vulnerable Application
   ↓
Instance Metadata
   ↓
IAM Credentials
```

If an attacker obtains EC2 role credentials, the impact depends on the permissions assigned to the role.

This demonstrates why both:

```text
IMDS Security

and

Least-Privilege IAM Role
```

are important.

---

## 19. EC2 Storage

EC2 can use several storage options.

Common examples include:

```text
Amazon EBS

Instance Store

Amazon EFS
```

The most common persistent block storage for EC2 is Amazon EBS.

Conceptually:

```text
EC2
 ↓
EBS Volume
```

---

## 20. Amazon EBS

Amazon Elastic Block Store provides block storage volumes for EC2.

EBS volumes may contain:

- Operating system files
- Application files
- Logs
- Business data
- Sensitive information

Therefore, storage security is important.

---

## 21. EBS Encryption

EBS volumes can be encrypted.

Conceptually:

```text
EC2
 ↓
Encrypted EBS Volume
 ↓
AWS KMS
```

Encryption can protect:

- Data at rest
- Disk snapshots
- Data moving between EC2 and EBS infrastructure

Encryption keys are managed through AWS KMS.

EBS encryption will be studied in more detail later.

---

## 22. EBS Snapshots

EBS snapshots provide point-in-time backups of EBS volumes.

Conceptually:

```text
EBS Volume
 ↓
Snapshot
```

Security concerns include:

```text
Who can access the snapshot?

Is the snapshot encrypted?

Is the snapshot shared externally?

Does the snapshot contain sensitive data?
```

Snapshot permissions should be carefully managed.

---

## 23. Operating System Security

Because EC2 customers manage the guest operating system, OS security is a customer responsibility.

Important areas include:

- Patch management
- User accounts
- File permissions
- Running services
- Host firewall
- Malware protection
- Logging
- Secure configuration
- Vulnerability management

An EC2 instance should be treated like a traditional server from an operating system security perspective.

---

## 24. Patch Management

Operating systems and installed software require regular updates.

Conceptually:

```text
Vulnerability
   ↓
Security Patch
   ↓
Update Instance
```

Unpatched systems may expose known vulnerabilities.

Patch management can be performed through various approaches, including automation and AWS management services.

---

## 25. Reduce Unnecessary Services

A server should run only required services.

Example:

```text
Required:

HTTPS

Application Service
```

Unnecessary:

```text
Unused FTP

Unused Telnet

Unused Database Service

Unused Development Tools
```

Reducing unnecessary services decreases the attack surface.

---

## 26. Principle of Least Functionality

A useful server security principle is:

```text
Install and run only what is required.
```

This reduces:

- Attack surface
- Patch burden
- Misconfiguration risk
- Unnecessary network exposure

This complements the Principle of Least Privilege.

---

## 27. Secrets on EC2

Applications may require secrets such as:

- Database passwords
- API tokens
- Application secrets
- Certificates

Poor design:

```text
Password hard-coded
inside source code
```

or:

```text
Secret stored
in Git repository
```

Better approaches may use:

```text
AWS Secrets Manager

AWS Systems Manager Parameter Store
```

along with IAM roles.

---

## 28. Example Secret Access

Conceptually:

```text
EC2 Application
      ↓
IAM Role
      ↓
Secrets Manager
      ↓
Database Credential
```

This reduces the need to store credentials directly inside the EC2 image or application source code.

---

## 29. Logging and Monitoring

EC2 security requires visibility.

Useful data can include:

```text
Operating System Logs

Application Logs

CloudWatch Metrics

CloudTrail API Activity

VPC Flow Logs
```

Different logging sources answer different questions.

---

## 30. CloudTrail vs EC2 Logs

AWS CloudTrail records AWS API activity.

Example:

```text
Who started the instance?

Who modified the Security Group?

Who terminated the instance?
```

Operating system logs answer different questions:

```text
Who logged into Linux?

Which process failed?

What application error occurred?
```

Both layers are important.

---

## 31. CloudWatch

Amazon CloudWatch can collect:

- Metrics
- Logs
- Alarms

Example metrics include:

```text
CPU Utilization

Network In / Out

Status Check Failures
```

Additional OS-level metrics may require the CloudWatch agent.

Monitoring helps detect abnormal behavior and availability problems.

---

## 32. EC2 Status Checks

EC2 provides status checks that can help identify infrastructure or instance-level problems.

Conceptually:

```text
EC2 Status Checks

├── System Status
└── Instance Status
```

These can help differentiate between:

```text
AWS Infrastructure Problem

and

Guest Operating System Problem
```

---

## 33. Common Misconfiguration — Open SSH

Risky:

```text
TCP 22
Source: 0.0.0.0/0
```

This allows SSH connection attempts from anywhere on the Internet.

Better options include:

```text
Trusted IP Range

VPN

Bastion Host

AWS Systems Manager
```

depending on requirements.

---

## 34. Common Misconfiguration — Open RDP

Risky:

```text
TCP 3389
Source: 0.0.0.0/0
```

This exposes Windows remote administration directly to the Internet.

Administrative access should be restricted.

---

## 35. Common Misconfiguration — Administrator IAM Role

Poor design:

```text
EC2
 ↓
IAM Role
 ↓
AdministratorAccess
```

If the instance is compromised, the attacker may gain excessive AWS permissions.

Better:

```text
EC2
 ↓
Least-Privilege Role
 ↓
Only Required API Actions
```

---

## 36. Common Misconfiguration — Hard-Coded Credentials

Risky:

```text
AWS_ACCESS_KEY_ID
AWS_SECRET_ACCESS_KEY
```

stored in:

```text
Source Code

Configuration File

AMI

Shell Script
```

Better:

```text
IAM Role
→ Temporary Credentials
```

---

## 37. Common Misconfiguration — Unencrypted Storage

Sensitive data stored on unencrypted EBS volumes creates additional risk.

A better design uses:

```text
Encrypted EBS

+
KMS
```

where required.

Encryption should be part of the architecture rather than an afterthought.

---

## 38. Common Misconfiguration — Outdated AMI

Launching instances from an old AMI may result in:

```text
Unpatched OS

Old Libraries

Known Vulnerabilities

Deprecated Software
```

AMI lifecycle management should therefore be part of EC2 security.

---

## 39. Common Misconfiguration — Excessive Public Exposure

An EC2 instance may accidentally become highly exposed through a combination of:

```text
Public IP

Public Subnet

Open Security Group

Weak Application Security
```

Security should be evaluated as a complete architecture rather than one setting at a time.

---

## 40. EC2 Security Layers

A secure EC2 architecture includes multiple layers.

```text
Network
   ↓
Security Group
   ↓
Operating System
   ↓
Application
   ↓
IAM Role
   ↓
Data
```

Supporting controls include:

```text
Logging

Monitoring

Patch Management

Encryption

Secrets Management
```

---

## 41. Example Secure EC2 Architecture

```text
Internet
   ↓
Application Load Balancer
   ↓
ALB-SG
   ↓
Private EC2
   ↓
APP-SG
   ↓
IAM Role
   ↓
AWS Services
```

Storage:

```text
EC2
 ↓
Encrypted EBS
 ↓
AWS KMS
```

Administration:

```text
Administrator
   ↓
IAM
   ↓
Systems Manager Session Manager
   ↓
EC2
```

This design avoids direct SSH exposure and unnecessary permanent credentials.

---

## 42. EC2 Security Review Questions

When reviewing an EC2 instance, ask:

```text
Does this instance need a public IP?

Does it need direct Internet inbound access?

Which Security Groups are attached?

Are management ports publicly exposed?

What IAM role is attached?

Are its IAM permissions excessive?

Is IMDSv2 enabled or required?

Is the operating system patched?

Are unnecessary services running?

Is storage encrypted?

Are secrets stored securely?

Are logs collected?

Is monitoring enabled?

Is the AMI trusted and maintained?
```

---

## 43. Hands-on Practice

For today's practice, open the Amazon EC2 console and review one instance or the instance launch workflow.

Identify:

```text
AMI

Instance Type

VPC

Subnet

Private IP

Public IP

Security Groups

IAM Role

Storage

Metadata Configuration
```

For each item, ask:

```text
What security risk could this configuration introduce?
```

---

## 44. Optional Architecture Exercise

Design an EC2 application server with these requirements:

```text
No direct Internet inbound access

Outbound software update access

Access to S3

Encrypted storage

Administrative access without public SSH
```

Possible architecture:

```text
Private EC2
   │
   ├── Private Subnet
   │
   ├── NAT Gateway for outbound access
   │
   ├── IAM Role for S3
   │
   ├── Encrypted EBS
   │
   └── Systems Manager Session Manager
```

This combines multiple AWS security controls.

---

## Security Checklist

When reviewing EC2 security, I should ask:

```text
Is the AMI trusted?

Is the operating system supported and patched?

Does the instance need a public IP?

Are Security Group rules least-privilege?

Are SSH or RDP ports publicly exposed?

Can Systems Manager replace direct management access?

Is an IAM role used instead of hard-coded credentials?

Does the role follow least privilege?

Is IMDSv2 used?

Are EBS volumes encrypted?

Are snapshots protected?

Are secrets stored securely?

Are unnecessary services disabled?

Are operating system and application logs collected?

Are CloudWatch and CloudTrail providing sufficient visibility?
```

---

## Key Takeaways

- Amazon EC2 provides customer-managed virtual servers in AWS.
- EC2 has significant customer security responsibility.
- AMIs define the initial operating system and software configuration.
- EC2 instances run inside VPC subnets.
- Public exposure depends on routing, addressing, and Security Groups.
- Private EC2 instances can reduce direct Internet exposure.
- Security Groups should follow least-privilege network access.
- IAM roles are preferred over hard-coded AWS credentials.
- EC2 workloads should use temporary credentials whenever possible.
- Instance Metadata Service access is security-sensitive.
- IMDSv2 provides stronger metadata protection than IMDSv1.
- Operating system patching and hardening are customer responsibilities.
- EBS encryption protects EC2 storage at rest.
- Secrets should not be stored in source code or AMIs.
- Logging and monitoring are essential for EC2 security.
- EC2 should be secured using defense in depth.

---

## Reflection

Today I learned that EC2 security involves much more than launching a virtual machine.

Because EC2 is an Infrastructure as a Service offering, the customer is responsible for securing the operating system, applications, network configuration, identities, and data.

I also learned that EC2 should be evaluated as a combination of multiple security layers.

Network exposure can be reduced through private subnets and restrictive Security Groups, AWS API permissions can be controlled with IAM roles, storage can be protected with EBS encryption, and administrative access can be reduced by using Systems Manager instead of exposing SSH or RDP directly.

The most important lesson is that EC2 security requires defense in depth across identity, network, operating system, application, data, and monitoring controls.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AMI | A template used to launch EC2 instances |
| EBS | Persistent block storage commonly used by EC2 |
| EC2 | AWS virtual compute service |
| IMDS | The EC2 Instance Metadata Service |
| IMDSv2 | A session-oriented version of the Instance Metadata Service |
| Instance Profile | The mechanism used to provide an IAM role to an EC2 instance |
| Instance Type | The compute, memory, network, and hardware configuration of an EC2 instance |
| Session Manager | A Systems Manager capability for managing instances without direct inbound SSH or RDP |
