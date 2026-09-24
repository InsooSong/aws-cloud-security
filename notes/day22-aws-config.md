# Day 22 — AWS Config

## Topic

AWS Config Fundamentals, Resource Configuration Tracking, Compliance, and Remediation

---

## Objectives

- Understand the purpose of AWS Config
- Understand Configuration Recorders
- Understand Configuration Items
- Learn how configuration history works
- Understand AWS Config Rules
- Compare Managed Rules and Custom Rules
- Understand compliance states
- Learn how remediation works
- Understand Conformance Packs
- Understand multi-account and multi-Region aggregation
- Compare AWS Config, CloudTrail, and CloudWatch
- Practice reviewing AWS resource compliance

---

## 1. What Is AWS Config?

AWS Config is a service that records and evaluates the configuration of supported AWS resources.

It helps answer questions such as:

```text
What resources exist?

How are they configured?

How were they configured in the past?

Did the configuration change?

Does the current configuration comply with security requirements?
```

Conceptually:

```text
AWS Resource
     |
     v
Configuration Change
     |
     v
AWS Config
     |
     +-- Configuration History
     |
     +-- Compliance Evaluation
     |
     +-- Remediation
```

AWS Config is useful for:

- Security auditing
- Configuration management
- Compliance monitoring
- Governance
- Troubleshooting
- Change analysis

---

## 2. AWS Config vs CloudTrail vs CloudWatch

These services provide different types of visibility.

### AWS CloudTrail

CloudTrail records supported AWS API activity.

Question:

```text
Who changed the resource?
```

Example:

```text
Who changed this Security Group?
```

### AWS Config

AWS Config records supported resource configuration state.

Question:

```text
What changed?
```

Example:

```text
When did this Security Group start allowing TCP 22 from 0.0.0.0/0?
```

### Amazon CloudWatch

CloudWatch monitors metrics and logs.

Question:

```text
What is happening to the resource?
```

Example:

```text
Is CPU utilization unusually high?
```

A useful model:

```text
CloudTrail
→ WHO changed it?

AWS Config
→ WHAT changed?

CloudWatch
→ WHAT is happening?
```

These services complement each other.

---

## 3. Example Security Investigation

Suppose an EC2 Security Group suddenly allows:

```text
TCP 22

Source:
0.0.0.0/0
```

AWS Config can help determine:

```text
Previous Configuration

Current Configuration

Time of Configuration Change

Compliance State
```

CloudTrail can then help determine:

```text
Who made the change?

Which API operation was used?

Where did the request originate?
```

Conceptually:

```text
Security Group Exposure
        |
        +---- AWS Config
        |       |
        |       +-- What changed?
        |       +-- When did configuration change?
        |
        +---- CloudTrail
                |
                +-- Who changed it?
                +-- Which API was called?
```

This is a common investigation pattern.

---

## 4. Configuration Recorder

The Configuration Recorder records configuration changes for resource types in scope.

Conceptually:

```text
AWS Resource
     |
     v
Configuration Recorder
     |
     v
Configuration Item
```

Examples of resources that AWS Config can record include supported:

```text
EC2 Instances

Security Groups

EBS Volumes

S3 Buckets

RDS Resources

IAM Resources

VPC Components
```

Supported resource types can vary by AWS Region.

---

## 5. Resource Recording Scope

AWS Config can be configured to record:

```text
All Supported Resource Types

or

Selected Resource Types
```

Example:

```text
AWS Config

Record:
EC2
S3
RDS
Security Groups
```

instead of recording every supported resource.

The appropriate scope depends on:

- Security requirements
- Compliance requirements
- Resource inventory needs
- Cost
- Regional architecture

---

## 6. Recording Frequency

AWS Config supports different recording frequencies for supported resources.

Two important models are:

```text
Continuous Recording

Daily Recording
```

### Continuous Recording

AWS Config records a new Configuration Item when a supported recorded resource changes.

Conceptually:

```text
Resource Changes
      |
      v
New Configuration Item
```

### Daily Recording

AWS Config records the most recent configuration state during the daily recording period when the configuration differs from the previously recorded state.

Conceptually:

```text
Multiple Changes
during Day
      |
      v
Latest Relevant State
      |
      v
Configuration Item
```

Continuous recording provides more granular change history but can generate more configuration items.

---

## 7. Configuration Item

A Configuration Item represents a point-in-time view of a resource configuration.

A Configuration Item can contain information such as:

```text
Resource Type

Resource ID

AWS Region

Configuration

Relationships

Tags

Capture Time
```

Conceptually:

```text
EC2 Instance

Time A
→ Configuration Item A

Time B
→ Configuration Item B

Time C
→ Configuration Item C
```

These items allow AWS Config to build resource history.

---

## 8. Configuration History

Configuration History contains previous Configuration Items for a resource.

Example:

```text
Security Group

09:00
TCP 443
0.0.0.0/0

        ↓

11:30
TCP 22
0.0.0.0/0
TCP 443
0.0.0.0/0

        ↓

13:00
TCP 443
0.0.0.0/0
```

AWS Config can show how the resource changed over time.

This is useful for:

- Security investigation
- Configuration troubleshooting
- Audit evidence
- Change analysis

---

## 9. Resource Relationships

AWS Config can record relationships between supported AWS resources.

Example:

```text
EC2 Instance
     |
     +-- Security Group
     |
     +-- Subnet
     |
     +-- VPC
     |
     +-- EBS Volume
```

Resource relationships can help security engineers understand the impact of configuration changes.

For example:

```text
Security Group Misconfiguration
        |
        v
Which EC2 instances use this Security Group?
```

---

## 10. Configuration Snapshot

A Configuration Snapshot provides a picture of recorded resource configurations.

Conceptually:

```text
AWS Account

EC2
S3
RDS
EBS
VPC
IAM
   |
   v
Configuration Snapshot
```

A snapshot can help review the configuration state of recorded resources.

Potential uses include:

- Inventory review
- Audit
- Security assessment
- Troubleshooting

---

## 11. Delivery Channel

AWS Config can deliver configuration information to configured destinations.

Conceptually:

```text
AWS Config
    |
    +-- Amazon S3
    |
    +-- Amazon SNS
```

Configuration history and snapshots can be delivered to an S3 bucket.

SNS can be used for supported configuration notifications.

The destination resources should also follow appropriate security controls.

---

## 12. AWS Config Rules

AWS Config Rules evaluate resource configurations against defined conditions.

Conceptually:

```text
AWS Resource
     |
     v
AWS Config Rule
     |
     v
Compliance Evaluation
     |
     +-- COMPLIANT
     |
     +-- NON_COMPLIANT
```

Example requirement:

```text
All EBS volumes must be encrypted.
```

Rule logic:

```text
EBS Volume
     |
     v
Encrypted?
     |
 +---+---+
 |       |
Yes      No
 |       |
 v       v
COMPLIANT NON_COMPLIANT
```

---

## 13. AWS Managed Rules

AWS provides predefined Config Rules called Managed Rules.

Examples can evaluate conditions such as:

```text
Are EBS volumes encrypted?

Is an S3 bucket publicly accessible?

Are required tags present?

Is unrestricted SSH access allowed?

Is RDS storage encrypted?
```

Managed Rules allow organizations to start compliance evaluation without creating evaluation logic from scratch.

---

## 14. Example Managed Rule

A security requirement:

```text
EBS volumes must be encrypted.
```

Conceptually:

```text
EBS Volume
     |
     v
AWS Config Managed Rule
     |
     v
Encryption Check
     |
 +---+---+
 |       |
Yes      No
 |       |
 v       v
COMPLIANT NON_COMPLIANT
```

If the volume is unencrypted:

```text
Compliance Status:
NON_COMPLIANT
```

This allows security teams to identify resources that violate policy.

---

## 15. Custom Rules

If AWS Managed Rules do not cover a requirement, organizations can create Custom Rules.

Custom rules can use supported mechanisms such as:

```text
AWS Lambda

or

AWS CloudFormation Guard
```

Example organization requirement:

```text
Production EC2 instances must use
a specific approved instance configuration.
```

Conceptually:

```text
Resource Configuration
        |
        v
Custom Rule Logic
        |
        v
Compliance Result
```

Custom rules allow organizations to implement environment-specific controls.

---

## 16. Compliance Status

AWS Config Rules evaluate resources and produce compliance states.

The two most important states are:

```text
COMPLIANT

NON_COMPLIANT
```

### COMPLIANT

The resource satisfies the rule.

Example:

```text
EBS Encryption:
Enabled
```

### NON_COMPLIANT

The resource violates the rule.

Example:

```text
EBS Encryption:
Disabled
```

Other evaluation states may exist depending on the rule and evaluation condition.

A NON_COMPLIANT state means the configuration does not satisfy the defined rule.

It does not automatically mean that the resource has been compromised.

---

## 17. Compliance Is Configuration-Based

AWS Config compliance evaluates resource configuration.

Example:

```text
Security Group:

TCP 22
0.0.0.0/0
```

A Config Rule may classify this as:

```text
NON_COMPLIANT
```

because the configuration violates the defined security requirement.

However:

```text
NON_COMPLIANT
≠
Confirmed Attack
```

It means:

```text
Configuration Policy Violation
```

Security investigation may still be required.

---

## 18. Rule Evaluation Triggers

AWS Config Rules can evaluate resources based on supported trigger mechanisms.

Common concepts include:

```text
Configuration Change

Periodic Evaluation
```

### Configuration Change

Evaluation occurs when a relevant resource configuration changes.

Conceptually:

```text
Resource Changes
     |
     v
Config Rule
     |
     v
Evaluation
```

### Periodic Evaluation

The rule evaluates according to a configured frequency.

Conceptually:

```text
Scheduled Evaluation
       |
       v
Config Rule
       |
       v
Resource Evaluation
```

The appropriate trigger depends on the security requirement.

---

## 19. Example — Public SSH Detection

Security requirement:

```text
SSH must not be open to the Internet.
```

Misconfiguration:

```text
Security Group

TCP 22

Source:
0.0.0.0/0
```

AWS Config workflow:

```text
Security Group Changed
        |
        v
AWS Config Records Change
        |
        v
Config Rule Evaluates Resource
        |
        v
NON_COMPLIANT
```

Security team can then investigate and remediate the configuration.

---

## 20. Example — S3 Security

Security requirement:

```text
S3 buckets must not allow unintended public access.
```

AWS Config can evaluate relevant S3 configurations.

Conceptually:

```text
S3 Bucket
    |
    v
Config Rule
    |
    v
Public Access Evaluation
    |
 +--+--+
 |     |
Safe  Violation
 |     |
 v     v
COMPLIANT
      NON_COMPLIANT
```

This supports continuous cloud security posture monitoring.

---

## 21. Example — RDS Encryption

Security requirement:

```text
RDS storage must be encrypted.
```

Conceptually:

```text
RDS Instance
      |
      v
AWS Config Rule
      |
      v
Storage Encrypted?
      |
   +--+--+
   |     |
  Yes    No
   |     |
   v     v
COMPLIANT
      NON_COMPLIANT
```

This can help identify databases that do not meet data protection requirements.

---

## 22. Remediation

AWS Config can associate remediation actions with noncompliant resources.

AWS Config remediation uses AWS Systems Manager Automation documents.

Conceptually:

```text
Config Rule
    |
    v
NON_COMPLIANT
    |
    v
Remediation
    |
    v
Systems Manager Automation
    |
    v
Configuration Corrected
```

Remediation can be:

```text
Manual

or

Automatic
```

depending on the configuration.

---

## 23. Automatic Remediation

Example:

```text
S3 Bucket
     |
     v
NON_COMPLIANT
     |
     v
Automatic Remediation
     |
     v
Security Configuration Changed
```

Automatic remediation can reduce response time.

However, automatic changes should be carefully tested.

Potential risks include:

```text
Application Outage

Unexpected Permission Change

Incorrect Resource Modification

Business Process Impact
```

Automation should not be enabled blindly.

---

## 24. Manual Remediation

For sensitive resources, manual remediation may be more appropriate.

Conceptually:

```text
NON_COMPLIANT
     |
     v
Security Engineer Review
     |
     v
Validate Risk
     |
     v
Approve Change
     |
     v
Remediate
```

This provides human validation before modifying critical resources.

The correct approach depends on:

- Resource criticality
- Security severity
- Business impact
- Confidence in automation

---

## 25. Prevent vs Detect vs Remediate

AWS Config is primarily useful for detecting configuration drift and policy violations.

Conceptually:

```text
Prevent
→ IAM / SCP / Guardrails

Detect
→ AWS Config Rule

Remediate
→ Systems Manager Automation
```

Example:

```text
Resource Becomes Misconfigured
        |
        v
AWS Config Detects
        |
        v
NON_COMPLIANT
        |
        v
Remediation
```

This creates a governance feedback loop.

---

## 26. Configuration Drift

Configuration Drift occurs when the actual configuration differs from the intended security baseline.

Example:

```text
Expected:

SSH:
10.0.0.0/8

Actual:

SSH:
0.0.0.0/0
```

AWS Config can help detect changes that create drift.

Conceptually:

```text
Approved Baseline
       |
       v
Configuration Change
       |
       v
Drift
       |
       v
AWS Config Detection
```

Configuration drift is common when resources are manually modified.

---

## 27. Conformance Packs

A Conformance Pack is a collection of AWS Config Rules and remediation actions deployed together.

Conceptually:

```text
Conformance Pack
      |
      +-- Rule 1
      |
      +-- Rule 2
      |
      +-- Rule 3
      |
      +-- Remediation Actions
```

This helps organizations define a security or compliance baseline.

Examples could include:

```text
Encryption Requirements

Network Security Requirements

Logging Requirements

Access Control Requirements
```

---

## 28. Conformance Pack Example

Example security baseline:

```text
Cloud Security Baseline
│
├── EBS Encryption Required
├── RDS Encryption Required
├── S3 Public Access Restricted
├── SSH Exposure Restricted
└── Required Security Logging
```

Instead of deploying each rule individually:

```text
Deploy Conformance Pack
```

This improves consistency.

---

## 29. Conformance Packs and Organizations

Conformance Packs can also be deployed across AWS Organizations.

Conceptually:

```text
AWS Organization
      |
      +-- Production Account
      |
      +-- Development Account
      |
      +-- Security Account
      |
      v
Organization Conformance Pack
      |
      v
Common Security Baseline
```

This can help apply common governance requirements across multiple AWS accounts.

---

## 30. Multi-Account and Multi-Region Aggregation

AWS Config Aggregators can collect configuration and compliance information from multiple accounts and Regions.

Conceptually:

```text
Account A / Region A ----+
                         |
Account A / Region B ----+
                         |
Account B / Region A ----+----> AWS Config Aggregator
                         |
Account C / Region C ----+
                                   |
                                   v
                         Centralized Security View
```

This is useful for larger AWS environments.

---

## 31. Why Aggregators Matter

Without aggregation:

```text
Security Team
   |
   +-- Check Account A
   |
   +-- Check Account B
   |
   +-- Check Account C
   |
   +-- Check Multiple Regions
```

With an aggregator:

```text
Multiple Accounts / Regions
           |
           v
Centralized AWS Config View
```

This improves visibility into:

- Resource inventory
- Compliance status
- Configuration state
- Organization-wide security posture

---

## 32. Advanced Queries

AWS Config supports advanced queries against the current configuration state of supported resources.

Conceptually:

```text
AWS Config Resource Inventory
          |
          v
Advanced Query
          |
          v
Filtered Resources
```

Example questions:

```text
Which EC2 instances exist?

Which resources use a specific tag?

Which resources are in a specific Region?

Which resources have a specific configuration?
```

Advanced queries can help security teams search cloud inventory at scale.

---

## 33. Security Posture Management

AWS Config can contribute to Cloud Security Posture Management.

A useful model is:

```text
Inventory
    |
    v
Configuration
    |
    v
Compliance Rules
    |
    v
Find Violations
    |
    v
Remediate
    |
    v
Continuous Review
```

This helps answer:

```text
Are our AWS resources still configured securely?
```

---

## 34. AWS Config Does Not Prevent Every Misconfiguration

AWS Config usually evaluates configurations after they exist or at an evaluation interval.

Example:

```text
User Changes Security Group
        |
        v
Insecure Configuration Exists
        |
        v
AWS Config Evaluates
        |
        v
NON_COMPLIANT
```

Therefore:

```text
AWS Config
≠
Universal Preventive Control
```

Preventive controls may include:

```text
IAM Permissions

Service Control Policies

Infrastructure as Code Controls

Deployment Validation
```

AWS Config provides important detective and remediation capabilities.

---

## 35. AWS Config Does Not Replace CloudTrail

AWS Config tells you:

```text
Security Group changed.
```

CloudTrail may tell you:

```text
IAM Role A called
AuthorizeSecurityGroupIngress
at 10:35 UTC
from Source X.
```

Combined:

```text
AWS Config
→ What changed?

CloudTrail
→ Who changed it?
```

This combination is especially useful during incident investigations.

---

## 36. AWS Config Does Not Replace CloudWatch

AWS Config evaluates configuration.

CloudWatch monitors operational data.

Example:

```text
AWS Config:

EC2 Security Group
→ NON_COMPLIANT
```

Compared with:

```text
CloudWatch:

EC2 CPU
→ 95%
```

Both are useful but answer different questions.

---

## 37. Security Investigation Workflow

Scenario:

A database becomes publicly accessible.

### Step 1 — AWS Config

Determine:

```text
When did the configuration change?

What was the previous state?

What is the current state?
```

### Step 2 — CloudTrail

Determine:

```text
Who made the change?

Which API was used?

Where did the request originate?
```

### Step 3 — CloudWatch / Logs

Determine:

```text
Was unusual activity observed?

Did application behavior change?

Were alerts generated?
```

Conceptually:

```text
AWS Config
     ↓
CloudTrail
     ↓
CloudWatch
     ↓
Security Investigation
```

---

## 38. Common AWS Config Misconfigurations

### Configuration Recorder Not Running

Problem:

```text
AWS Config Enabled
but
Recorder Stopped
```

Result:

```text
Configuration Changes
may not be recorded as intended.
```

Review recorder status regularly.

---

### Required Resources Not Recorded

Example:

```text
Security Group
→ Not Included in Recording Scope
```

A Config Rule cannot provide complete visibility if required configuration data is unavailable.

Recording scope should match security requirements.

---

### Only One Region Monitored

Example:

```text
Tokyo Region
→ AWS Config Enabled

Singapore Region
→ AWS Config Not Enabled
```

Resources created in another Region may fall outside the intended monitoring baseline.

Multi-Region environments require deliberate coverage.

---

### Rules Without Remediation Process

Example:

```text
NON_COMPLIANT

NON_COMPLIANT

NON_COMPLIANT
```

but nobody reviews or remediates the resources.

Detection without a response process provides limited value.

---

### Overly Aggressive Auto-Remediation

Example:

```text
Config Rule
    |
    v
Automatic Remediation
    |
    v
Production Configuration Changed
    |
    v
Service Outage
```

Automatic remediation should be tested before production deployment.

---

## 39. Example Cloud Security Architecture

```text
AWS Resources
      |
      v
AWS Config Recorder
      |
      v
Configuration Items
      |
      +------------------+
      |                  |
      v                  v
Configuration      Config Rules
History                 |
                        v
                   Compliance
                        |
                +-------+-------+
                |               |
                v               v
            COMPLIANT      NON_COMPLIANT
                                |
                                v
                           Remediation
```

Supporting services:

```text
CloudTrail
→ Who changed configuration?

CloudWatch
→ Monitor operational behavior

AWS Config
→ Track and evaluate configuration

Systems Manager
→ Remediation automation
```

---

## 40. Example Security Baseline

An organization may define:

```text
EC2
→ No unrestricted SSH

EBS
→ Encryption required

S3
→ Public access restricted

RDS
→ Encryption required

CloudTrail
→ Logging enabled
```

AWS Config Rules can evaluate these requirements.

Conceptually:

```text
Security Baseline
        |
        v
AWS Config Rules
        |
        v
AWS Resources
        |
        v
Compliance Dashboard
```

This provides continuous visibility into configuration compliance.

---

## 41. Hands-on Practice

### Practice A — Open AWS Config

Navigate to:

```text
AWS Management Console
        |
        v
AWS Config
```

Review:

```text
Dashboard

Resources

Rules

Conformance Packs
```

If AWS Config has not been enabled, review the setup workflow without enabling paid resources unless required.

---

## 42. Practice — Configuration Recorder

Review the recording configuration.

Identify:

```text
Recorder Status

Recording Scope

Recording Frequency

AWS Region
```

Ask:

```text
Which resource types are being recorded?

Are security-critical resources included?

Is continuous or daily recording used?
```

---

## 43. Practice — Resource Timeline

If recorded resources exist:

```text
AWS Config
   |
   v
Resources
   |
   v
Select Resource
   |
   v
Resource Timeline
```

Review:

```text
Current Configuration

Previous Configuration

Configuration Changes

Relationships
```

Try to identify at least one historical configuration change.

---

## 44. Practice — Config Rules

Navigate to:

```text
AWS Config
   |
   v
Rules
```

Review existing rules or browse available Managed Rules.

Look for security-related rules involving:

```text
EBS Encryption

S3 Security

Security Groups

RDS Encryption
```

For one rule, identify:

```text
Rule Name

Scope

Trigger Type

Compliance Status

Noncompliant Resources
```

---

## 45. Optional CLI Practice

If AWS CLI is configured:

### Check Configuration Recorders

```bash
aws configservice describe-configuration-recorders
```

### Check Recorder Status

```bash
aws configservice describe-configuration-recorder-status
```

### List Config Rules

```bash
aws configservice describe-config-rules
```

### Review Compliance

```bash
aws configservice describe-compliance-by-config-rule
```

These commands can help inspect AWS Config from the command line.

Do not publish real account identifiers or sensitive configuration data to a public GitHub repository.

---

## 46. Optional Architecture Exercise

Design a basic compliance monitoring system.

Requirements:

```text
EBS must be encrypted.

RDS must be encrypted.

S3 must not be public.

SSH must not be publicly accessible.
```

Architecture:

```text
AWS Resources
      |
      v
AWS Config
      |
      v
Config Rules
      |
      v
Compliance Evaluation
      |
      +-- COMPLIANT
      |
      +-- NON_COMPLIANT
              |
              v
      Security Review
              |
              v
        Remediation
```

For each rule, decide whether remediation should be:

```text
Automatic

or

Manual
```

Explain why.

---

## 47. Security Checklist

When reviewing AWS Config, ask:

```text
[ ] Is AWS Config enabled in required Regions?

[ ] Is the Configuration Recorder running?

[ ] Are required resource types recorded?

[ ] Is the recording frequency appropriate?

[ ] Are configuration histories being retained?

[ ] Is the delivery S3 bucket protected?

[ ] Are security-critical Config Rules deployed?

[ ] Are noncompliant resources reviewed?

[ ] Is remediation defined?

[ ] Has automatic remediation been tested?

[ ] Are Conformance Packs used where appropriate?

[ ] Is multi-account aggregation required?

[ ] Are multiple Regions included?

[ ] Are configuration changes correlated with CloudTrail?

[ ] Are compliance violations integrated into the security response process?
```

---

## Key Takeaways

- AWS Config records the configuration state of supported AWS resources.
- Configuration Recorders capture configuration changes for resources in scope.
- Configuration Items represent point-in-time resource configurations.
- Configuration History shows how resource configuration changes over time.
- AWS Config Rules evaluate resource configurations against defined requirements.
- Managed Rules provide predefined AWS configuration checks.
- Custom Rules can implement organization-specific requirements.
- Resources can be classified as COMPLIANT or NON_COMPLIANT.
- A noncompliant resource represents a policy violation, not necessarily a security incident.
- AWS Config remediation can use Systems Manager Automation.
- Automatic remediation should be tested carefully.
- Conformance Packs group rules and remediation actions into reusable governance baselines.
- Aggregators provide centralized visibility across accounts and Regions.
- AWS Config complements CloudTrail and CloudWatch.
- AWS Config is primarily a detective and governance control rather than a universal preventive control.

---

## Reflection

Today I learned that AWS Config provides continuous visibility into AWS resource configurations.

The most important concept is the difference between CloudTrail, CloudWatch, and AWS Config.

CloudTrail helps identify who performed an AWS API action, CloudWatch monitors resource and application behavior, and AWS Config records and evaluates resource configuration.

I also learned that AWS Config Rules can identify resources that violate security requirements and classify them as noncompliant.

Remediation can then be performed manually or automatically through Systems Manager Automation.

From a cloud security perspective, AWS Config is valuable because it allows security teams to continuously compare actual cloud configurations against an expected security baseline and identify configuration drift.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Aggregator | A feature for centrally viewing configuration and compliance data across accounts and Regions |
| AWS Config | A service for recording and evaluating AWS resource configurations |
| Compliance | Whether a resource satisfies a defined configuration requirement |
| Config Rule | A rule that evaluates AWS resources against defined requirements |
| Configuration Drift | A difference between the intended and actual configuration |
| Configuration History | Historical configuration records for a resource |
| Configuration Item | A point-in-time representation of an AWS resource configuration |
| Conformance Pack | A collection of Config Rules and remediation actions |
| Configuration Recorder | A component that records configuration changes for selected resources |
| Remediation | An action that corrects a noncompliant configuration |
