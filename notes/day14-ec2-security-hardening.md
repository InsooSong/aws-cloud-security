# Day 14 — EC2 Security Hardening

## Topic

Amazon EC2 Security Hardening and Secure Instance Operations

---

## Objectives

- Understand the purpose of EC2 hardening
- Reduce direct administrative exposure
- Use AWS Systems Manager for secure instance management
- Enforce IMDSv2
- Apply least-privilege IAM roles
- Harden operating system configuration
- Improve patch and vulnerability management
- Protect EBS volumes and snapshots
- Secure secrets and application credentials
- Improve logging and monitoring
- Reduce unnecessary services and software
- Build a practical EC2 hardening checklist

---

## 1. What is EC2 Hardening?

Security hardening is the process of reducing unnecessary functionality, permissions, exposure, and configuration risk.

The goal is to reduce the attack surface.

Conceptually:

```text
Default EC2
    ↓
Remove Unnecessary Access
    ↓
Restrict Permissions
    ↓
Patch and Harden OS
    ↓
Protect Data
    ↓
Enable Logging
    ↓
Hardened EC2
```

Hardening should address multiple layers:

```text
Identity
Network
Operating System
Application
Storage
Credentials
Monitoring
```

---

## 2. Reduce the Attack Surface

A secure EC2 instance should expose only what is required.

Ask:

```text
Does this port need to be open?

Does this service need to run?

Does this package need to be installed?

Does this instance need a public IP?

Does this user need administrative access?
```

A useful principle is:

```text
If it is not required,
remove or disable it.
```

---

## 3. Avoid Direct Internet Administration

Directly exposing administrative services increases risk.

Examples:

```text
SSH
TCP 22

RDP
TCP 3389
```

Risky configuration:

```text
TCP 22
Source: 0.0.0.0/0
```

or:

```text
TCP 3389
Source: 0.0.0.0/0
```

This allows connection attempts from anywhere on the Internet.

---

## 4. Prefer Systems Manager Session Manager

AWS Systems Manager Session Manager can provide administrative access without exposing inbound SSH or RDP.

Conceptually:

```text
Administrator
      ↓
IAM Authentication
      ↓
Systems Manager
      ↓
EC2
```

Potential benefits include:

- No inbound TCP 22 required
- No inbound TCP 3389 required
- IAM-based access control
- Centralized access
- Session logging options
- Reduced public exposure

---

## 5. Session Manager Architecture

A hardened management design may look like:

```text
Administrator
      ↓
IAM
      ↓
AWS Systems Manager
      ↓
SSM Agent
      ↓
Private EC2
```

The EC2 instance can remain in a private subnet.

This reduces the need for:

```text
Public IPv4

Bastion Host

Inbound SSH

Inbound RDP
```

depending on the architecture.

---

## 6. IAM Role for Systems Manager

EC2 instances managed through Systems Manager require appropriate IAM permissions.

Conceptually:

```text
EC2
 ↓
IAM Role
 ↓
Systems Manager Permissions
```

The role should contain only required permissions.

Avoid attaching:

```text
AdministratorAccess
```

simply to make Systems Manager work.

Least privilege still applies.

---

## 7. Enforce IMDSv2

The EC2 Instance Metadata Service provides instance information and temporary IAM role credentials.

A hardened EC2 configuration should prefer:

```text
IMDSv2
```

over older metadata access methods.

Conceptually:

```text
Application
   ↓
IMDSv2 Session Token
   ↓
Instance Metadata
```

IMDSv2 uses a session-oriented request flow.

---

## 8. Why IMDSv2 Matters

If an application contains an SSRF vulnerability, an attacker may attempt to access instance metadata.

Example:

```text
Attacker
   ↓
SSRF
   ↓
Application
   ↓
Instance Metadata
   ↓
IAM Credentials
```

Using IMDSv2 helps reduce certain metadata exploitation scenarios.

However:

```text
IMDSv2
≠
Complete SSRF Protection
```

Application security and least-privilege IAM roles are still required.

---

## 9. Limit Metadata Access

Metadata access should be limited to workloads that actually require it.

Security questions:

```text
Does this application need instance metadata?

Does it need IAM role credentials?

Can metadata access be restricted?

Is IMDSv2 required?
```

Reducing unnecessary metadata access can reduce risk.

---

## 10. Least-Privilege IAM Role

An EC2 instance should receive only the AWS permissions required by its workload.

Bad:

```text
EC2
 ↓
AdministratorAccess
```

Better:

```text
EC2
 ↓
ApplicationRole
 ↓
s3:GetObject
 ↓
Required Bucket Only
```

Example:

```text
Required:

s3:GetObject

Resource:

arn:aws:s3:::application-data/*
```

This reduces the impact if the instance is compromised.

---

## 11. Avoid Long-Term AWS Credentials

Do not store long-term AWS credentials on EC2 unless absolutely necessary.

Avoid:

```text
~/.aws/credentials

Environment Variables

Source Code

Shell Scripts

Configuration Files
```

containing permanent access keys.

Prefer:

```text
EC2 IAM Role
      ↓
Temporary Credentials
```

---

## 12. Protect SSH Private Keys

If SSH keys are used, private keys must be protected.

Important practices:

- Never commit private keys to GitHub
- Restrict local file permissions
- Do not share private keys between users
- Remove unused keys
- Rotate access when personnel change
- Avoid unnecessary copies

Example Linux permissions:

```bash
chmod 600 private-key.pem
```

The private key should only be readable by the owner.

---

## 13. Operating System Patching

The guest operating system is the customer's responsibility.

A hardened EC2 instance should receive regular security updates.

Conceptually:

```text
Known Vulnerability
       ↓
Security Update
       ↓
Patch
       ↓
Reduced Exposure
```

Patching should include:

- Operating system
- Kernel
- Libraries
- Installed packages
- Application dependencies

---

## 14. Patch Management Strategy

A practical lifecycle may look like:

```text
Inventory
   ↓
Identify Missing Patches
   ↓
Test
   ↓
Patch
   ↓
Reboot if Required
   ↓
Validate
```

Patching should not simply mean:

```text
Run updates once
```

It should be a recurring operational process.

---

## 15. AWS Systems Manager Patch Manager

AWS Systems Manager includes capabilities that can help automate patch management.

Conceptually:

```text
Fleet of EC2 Instances
        ↓
Systems Manager
        ↓
Patch Policies / Operations
        ↓
Consistent Patching
```

This can help manage larger EC2 environments more consistently.

---

## 16. Vulnerability Management

Patching and vulnerability management are related but not identical.

A vulnerability management workflow may include:

```text
Discover
   ↓
Assess
   ↓
Prioritize
   ↓
Remediate
   ↓
Verify
```

Tools such as Amazon Inspector can help identify vulnerabilities in supported workloads.

---

## 17. Remove Unnecessary Services

Unused network services increase attack surface.

Check running services:

```text
Web Server

SSH

Database

FTP

Telnet

Development Services
```

Only required services should remain enabled.

Example:

```text
Application Server

Required:
Application Service

Not Required:
FTP
Telnet
Local Database
```

Disable or remove unnecessary software.

---

## 18. Remove Unnecessary Packages

Every installed package can potentially introduce:

- Vulnerabilities
- Dependencies
- Maintenance burden
- Misconfiguration risk

A hardened image should contain only required software.

Conceptually:

```text
Minimal OS
+
Required Packages
+
Application
```

instead of:

```text
Full Development Environment
+
Unused Tools
+
Unused Services
```

---

## 19. Secure User Accounts

Review local operating system accounts.

Ask:

```text
Is this user required?

Does this user need login access?

Does this user need sudo?

Is the account still active?

Are default accounts secured?
```

Remove unused accounts and minimize privileged access.

---

## 20. Privileged Access

Avoid giving unnecessary users unrestricted administrative privileges.

Linux example:

```text
root
```

or:

```text
sudo ALL
```

should be carefully controlled.

A better approach is:

```text
Named User
 ↓
Required sudo commands only
```

where practical.

Administrative actions should be auditable.

---

## 21. Disable Password Authentication When Appropriate

For Linux systems using SSH, password authentication may be disabled when stronger authentication methods are used.

Conceptually:

```text
Password Login
→ Disabled

Key-Based / Controlled Access
→ Enabled
```

This can reduce password brute-force risk.

However, access design should consider operational and recovery requirements.

---

## 22. Host Firewall

Security Groups are important, but the operating system can also use a host firewall.

Examples:

```text
nftables

iptables

firewalld

Windows Defender Firewall
```

Conceptually:

```text
Network
   ↓
Security Group
   ↓
Host Firewall
   ↓
Application
```

This adds another security layer.

---

## 23. File Permissions

Sensitive files should use appropriate permissions.

Examples:

```text
SSH Keys

Configuration Files

Application Secrets

Log Files

Certificates
```

Linux example:

```bash
chmod 600 sensitive-file
```

Permissions should follow least privilege.

---

## 24. Protect Configuration Files

Configuration files may contain sensitive information.

Examples:

```text
Database Connection Strings

API Endpoints

Certificates

Tokens

Passwords
```

Avoid storing secrets in plaintext configuration whenever possible.

Separate:

```text
Configuration
```

from:

```text
Secrets
```

---

## 25. Secrets Manager

AWS Secrets Manager can store sensitive application credentials.

Conceptually:

```text
EC2 Application
      ↓
IAM Role
      ↓
Secrets Manager
      ↓
Secret
```

Benefits can include:

- Centralized secret storage
- IAM-based access
- Reduced hard-coded credentials
- Secret rotation capabilities

---

## 26. Parameter Store

AWS Systems Manager Parameter Store can also be used for configuration and sensitive parameters.

Conceptually:

```text
Application
   ↓
IAM Role
   ↓
Parameter Store
```

Sensitive values can be protected using encryption where appropriate.

The correct service depends on requirements.

---

## 27. EBS Encryption

A hardened EC2 environment should protect data at rest.

Conceptually:

```text
EC2
 ↓
Encrypted EBS Volume
 ↓
AWS KMS
```

Encryption can protect:

- Root volumes
- Data volumes
- Snapshots created from encrypted volumes

---

## 28. Encrypted by Default

Organizations can enable EBS encryption by default.

Conceptually:

```text
New EBS Volume
       ↓
Automatically Encrypted
```

This reduces the risk of accidentally creating unencrypted volumes.

Security defaults are valuable because they reduce dependence on manual configuration.

---

## 29. Snapshot Security

EBS snapshots may contain sensitive data.

Review:

```text
Encryption

Sharing Permissions

External Access

Unused Snapshots
```

A snapshot should not be made publicly accessible unless there is a deliberate and justified requirement.

---

## 30. Logging

A hardened system should produce useful logs.

Examples:

```text
Authentication Logs

System Logs

Application Logs

Security Logs

Audit Logs
```

Logs help answer:

```text
Who accessed the system?

What changed?

What failed?

Was suspicious activity present?
```

---

## 31. CloudWatch Agent

The CloudWatch Agent can collect additional system-level information.

Examples:

```text
Memory Usage

Disk Usage

Application Logs

System Logs
```

Default EC2 metrics do not provide all operating system information.

The agent can improve visibility.

---

## 32. CloudTrail

CloudTrail records AWS API activity.

Useful EC2-related events include:

```text
RunInstances

StartInstances

StopInstances

TerminateInstances

ModifyInstanceAttribute

AuthorizeSecurityGroupIngress
```

This helps identify AWS-side configuration changes.

---

## 33. OS Logging vs CloudTrail

These logs serve different purposes.

```text
CloudTrail
→ AWS control plane activity
```

Examples:

```text
Who changed the Security Group?

Who terminated the instance?
```

Compared with:

```text
Operating System Logs
→ Activity inside the instance
```

Examples:

```text
Who logged in?

Which process crashed?

Which sudo command was executed?
```

Both are important.

---

## 34. Audit Logging

Linux systems can use audit capabilities to track security-relevant events.

Examples may include:

```text
Authentication Events

Privilege Use

File Changes

Process Execution
```

Audit logging can support investigations and compliance requirements.

---

## 35. Time Synchronization

Accurate system time is important for:

- Log correlation
- Authentication
- Incident investigation
- Certificate validation
- Distributed applications

Logs from multiple systems are much harder to investigate if timestamps are inconsistent.

---

## 36. Build Hardened AMIs

Instead of manually hardening every new instance, organizations can create hardened base images.

Conceptually:

```text
Trusted Base AMI
      ↓
Patch
      ↓
Harden
      ↓
Install Required Agents
      ↓
Create Hardened AMI
      ↓
Launch Instances
```

This improves consistency.

---

## 37. Immutable Infrastructure Concept

Another approach is to replace instances rather than manually changing them indefinitely.

Conceptually:

```text
Old Instance
     ↓
Create Updated Image
     ↓
Launch New Instance
     ↓
Replace Old Instance
```

Benefits may include:

- More predictable configuration
- Reduced configuration drift
- Easier rollback
- Consistent deployments

---

## 38. Configuration Drift

Configuration drift occurs when instances gradually become different from the intended baseline.

Example:

```text
Instance A
→ Patched

Instance B
→ Old configuration

Instance C
→ Manual firewall change
```

Over time, security becomes inconsistent.

Automation and hardened images can reduce configuration drift.

---

## 39. Security Baselines

A security baseline defines required configuration.

Example:

```text
IMDSv2 Required

EBS Encryption Enabled

No Public SSH

CloudWatch Agent Installed

SSM Agent Installed

Approved Packages Only

Required Logging Enabled
```

New instances can be checked against this baseline.

---

## 40. CIS Benchmarks

CIS Benchmarks provide security configuration guidance for operating systems and cloud environments.

Examples include recommendations related to:

- Account configuration
- Services
- Logging
- File permissions
- Authentication
- Network configuration

Benchmarks should be adapted to the organization's actual requirements.

Hardening should not blindly break required functionality.

---

## 41. Availability and Hardening

Security changes should consider availability.

Example:

```text
Disable Service
```

may improve security only if the service is actually unnecessary.

Similarly:

```text
Restrictive Firewall Rule
```

can cause an outage if required traffic is blocked.

A good hardening process includes:

```text
Change
 ↓
Test
 ↓
Validate
 ↓
Monitor
```

---

## 42. Example Hardened EC2 Architecture

```text
                      Administrator
                           │
                           ↓
                 Systems Manager
                           │
                           ↓
                    Private EC2
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ↓                ↓                ↓
      IAM Role       Encrypted EBS      CloudWatch
          │                                 │
          ↓                                 ↓
   AWS Services                          Monitoring
```

Network:

```text
Internet
   ↓
ALB
   ↓
Private EC2
```

No direct inbound administrative port is required.

---

## 43. Common Hardening Mistake — Security Through One Control

Example:

```text
Private Subnet
→ Therefore Secure
```

This is incorrect.

A private EC2 can still be compromised through:

- Vulnerable application
- Excessive IAM role
- Stolen credentials
- Unpatched OS
- Internal lateral movement
- Malicious package
- Poor secrets management

Hardening requires multiple layers.

---

## 44. Common Hardening Mistake — Permanent Administrator Access

Risky:

```text
User
→ Permanent Administrator Privileges
```

Better:

```text
Normal Access
   ↓
Temporary Privileged Access
   ↓
Audited Administrative Action
```

Privilege should be limited in both scope and duration.

---

## 45. Common Hardening Mistake — Manual Configuration Only

If every instance is manually configured:

```text
Instance A
→ Configuration 1

Instance B
→ Configuration 2

Instance C
→ Configuration 3
```

inconsistency becomes likely.

Better:

```text
Automation
+
Baseline
+
Image Management
```

---

## 46. Common Hardening Mistake — No Monitoring

A secure configuration without monitoring can still leave attacks undetected.

Hardening should include:

```text
Prevent

Detect

Respond
```

Example:

```text
Security Group
→ Prevent

CloudWatch / Logs
→ Detect

Incident Response
→ Respond
```

---

## 47. Hardening Review Questions

When reviewing an EC2 instance, ask:

```text
Does it need a public IP?

Are SSH or RDP exposed?

Can Session Manager be used?

Is IMDSv2 required?

Does the IAM role follow least privilege?

Are permanent AWS credentials stored locally?

Is the OS fully patched?

Are unnecessary services running?

Are unnecessary packages installed?

Are local users still required?

Are EBS volumes encrypted?

Are snapshots protected?

Are secrets stored outside source code?

Are system and application logs collected?

Is the instance following a defined security baseline?
```

---

## 48. Hands-on Practice

For today's practice, review an EC2 instance or launch configuration.

Check:

```text
Public IP

Security Groups

IAM Role

Metadata Options

EBS Encryption

SSM Availability

Operating System Version
```

If you have a test instance, also inspect:

```bash
uname -a

cat /etc/os-release

systemctl --type=service --state=running

ss -tulnp
```

These commands can help identify:

```text
OS Version

Running Services

Listening Ports
```

---

## 49. Optional Linux Hardening Review

On a Linux EC2 test instance:

### Check listening ports

```bash
ss -tulnp
```

Ask:

```text
Why is each port open?
```

### Check running services

```bash
systemctl --type=service --state=running
```

Ask:

```text
Is every service required?
```

### Check users

```bash
cat /etc/passwd
```

### Check sudo access

```bash
sudo -l
```

### Check SSH configuration

```bash
sudo sshd -T
```

Review the configuration carefully before making changes.

---

## 50. EC2 Hardening Checklist

### Identity

```text
[ ] IAM role follows least privilege
[ ] No unnecessary long-term AWS credentials
[ ] Administrative privileges are limited
```

### Network

```text
[ ] Public IP is required
[ ] Security Groups are least-privilege
[ ] SSH / RDP are not publicly exposed unnecessarily
[ ] Private subnet used where appropriate
```

### Metadata

```text
[ ] IMDSv2 is required where appropriate
[ ] Metadata access is limited
```

### Operating System

```text
[ ] OS is supported
[ ] Security patches are current
[ ] Unnecessary services are disabled
[ ] Unnecessary packages are removed
[ ] User accounts are reviewed
[ ] File permissions are appropriate
```

### Data

```text
[ ] EBS volumes are encrypted
[ ] Snapshots are protected
[ ] Sensitive files have restricted permissions
```

### Secrets

```text
[ ] Secrets are not hard-coded
[ ] Secrets Manager / Parameter Store used where appropriate
```

### Monitoring

```text
[ ] CloudTrail available
[ ] System logs collected
[ ] Application logs collected
[ ] CloudWatch monitoring configured
[ ] Security alerts are available
```

---

## Key Takeaways

- EC2 hardening reduces unnecessary attack surface.
- Direct SSH and RDP exposure should be minimized.
- Systems Manager Session Manager can reduce the need for inbound administrative ports.
- IMDSv2 should be preferred for stronger instance metadata protection.
- IAM roles should follow least privilege.
- Permanent AWS credentials should not be stored on EC2 when temporary credentials can be used.
- Operating systems and packages must be patched regularly.
- Unnecessary services and packages should be removed.
- EBS volumes and snapshots should be protected.
- Secrets should be stored securely outside application source code.
- Logging and monitoring are part of hardening, not optional extras.
- Hardened AMIs and automation can improve consistency.
- Security baselines help reduce configuration drift.
- Hardening should balance security, reliability, and application requirements.

---

## Reflection

Today I learned that EC2 hardening is a continuous process rather than a single configuration change.

A secure EC2 instance should minimize direct network exposure, use temporary AWS credentials, protect instance metadata, keep the operating system patched, remove unnecessary functionality, encrypt sensitive data, and produce useful security logs.

I also learned that automation is important because manually hardening every instance can lead to inconsistent configurations and configuration drift.

Using Systems Manager, hardened AMIs, security baselines, least-privilege IAM roles, and centralized monitoring can make EC2 security more consistent and scalable.

The overall goal is not simply to block attacks, but to reduce attack surface, detect suspicious activity, and limit the impact of a compromise.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Attack Surface | The total set of possible points that an attacker could target |
| Configuration Drift | Gradual differences between actual and intended system configuration |
| Hardening | Reducing security risk by removing unnecessary functionality and strengthening configuration |
| Host Firewall | A firewall running directly on an operating system |
| Immutable Infrastructure | Replacing systems with updated versions instead of modifying them continuously |
| Patch Management | The process of identifying, testing, and applying software updates |
| Privileged Access | Elevated access that allows administrative actions |
| Security Baseline | A defined set of required security configurations |
