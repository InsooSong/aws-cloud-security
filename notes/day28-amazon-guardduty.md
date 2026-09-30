# Day 28 — Amazon GuardDuty

## Topic

Amazon GuardDuty Fundamentals, Threat Detection, Findings, Protection Plans, and Security Response

---

## Objectives

- Understand the purpose of Amazon GuardDuty
- Understand GuardDuty foundational threat detection
- Learn which telemetry GuardDuty analyzes
- Understand GuardDuty Findings
- Understand finding severity levels
- Learn common GuardDuty finding categories
- Understand Extended Threat Detection and attack sequences
- Learn S3 Protection
- Understand Runtime Monitoring
- Learn EKS, RDS, and Lambda protection
- Understand Malware Protection features
- Understand GuardDuty multi-account architecture
- Learn how EventBridge can automate responses
- Understand suppression and finding management
- Practice investigating GuardDuty findings
- Identify common GuardDuty operational mistakes

---

# GuardDuty Fundamentals

## 1. What Is Amazon GuardDuty?

Amazon GuardDuty is a managed threat detection service.

It continuously analyzes security-relevant telemetry from AWS environments to identify potentially malicious or suspicious activity.

Conceptually:

```text
AWS Environment
      |
      +-- CloudTrail
      |
      +-- VPC Flow Logs
      |
      +-- DNS Logs
      |
      +-- Additional Protection Data
      |
      v
Amazon GuardDuty
      |
      v
Threat Detection
      |
      v
Finding
```

GuardDuty can help identify activity such as:

```text
Compromised Credentials

Suspicious API Activity

Malicious Network Communication

Cryptocurrency Mining

Data Exfiltration

Privilege Escalation

Malware

Suspicious Database Login Activity

Container Runtime Threats
```

---

## 2. GuardDuty Is a Detection Service

GuardDuty primarily provides:

```text
Detection

Analysis

Security Findings
```

It does not automatically mean:

```text
Finding
→ Threat Automatically Blocked
```

A complete workflow requires:

```text
Detect
   ↓
Alert
   ↓
Investigate
   ↓
Contain
   ↓
Remediate
```

Automated response can be added using other AWS services.

---

## 3. Why GuardDuty Matters

Without GuardDuty, security engineers may need to manually analyze:

```text
CloudTrail Events

VPC Flow Logs

DNS Queries

Runtime Events

Service Logs
```

Example:

```text
Millions of Events
       |
       v
Manual Analysis
       |
       v
Potential Threat
```

GuardDuty changes the model:

```text
Telemetry
    |
    v
GuardDuty Analysis
    |
    v
Security Finding
    |
    v
Security Investigation
```

---

# Foundational Threat Detection

## 4. Foundational Data Sources

When GuardDuty is enabled, foundational threat detection begins analyzing supported AWS telemetry.

Important foundational sources include:

```text
AWS CloudTrail Management Events

VPC Flow Logs

Route 53 Resolver DNS Query Logs
```

These provide visibility into:

```text
AWS API Activity

Network Communication

DNS Resolution
```

---

## 5. CloudTrail Management Events

GuardDuty analyzes CloudTrail management activity to identify suspicious AWS API usage.

Examples:

```text
CreateUser

AttachRolePolicy

PutRolePolicy

RunInstances

StopLogging

DisableKey
```

Potential detections include:

```text
Credential Misuse

Reconnaissance

Privilege Escalation

Persistence

Defense Evasion
```

---

## 6. Credential Compromise Example

Scenario:

```text
IAM Access Key
      |
      v
Stolen
      |
      v
Used from Unusual Location
      |
      v
Unusual API Calls
```

GuardDuty may analyze:

```text
API Behavior

IP Reputation

Usage Patterns

Resource Activity
```

and generate a finding when behavior appears suspicious.

---

## 7. VPC Flow Logs

GuardDuty analyzes network flow information for threat detection.

Conceptually:

```text
EC2
 |
 v
Network Communication
 |
 v
VPC Flow Telemetry
 |
 v
GuardDuty
```

Possible detections include communication with:

```text
Known Malicious IPs

Command-and-Control Infrastructure

Cryptocurrency Mining Infrastructure

Suspicious Scanners
```

---

## 8. DNS Logs

DNS queries can reveal suspicious activity.

Example:

```text
Compromised EC2
      |
      v
DNS Query
      |
      v
Known Malicious Domain
```

GuardDuty can use Route 53 Resolver DNS query telemetry to identify suspicious domain communication.

Potential examples:

```text
Command-and-Control Domains

Cryptocurrency Mining Domains

Malware Infrastructure
```

---

# GuardDuty Findings

## 9. What Is a Finding?

A GuardDuty Finding is a notification describing a potential security issue.

Conceptually:

```text
Suspicious Activity
      |
      v
GuardDuty Detection
      |
      v
Finding
```

A Finding can contain:

```text
Finding Type

Severity

Affected Resource

Account

Region

Time

Network Information

API Information

Evidence

Recommended Investigation Context
```

---

## 10. Finding Type

GuardDuty finding types use descriptive names.

Example:

```text
Recon:EC2/PortProbeUnprotectedPort
```

The name provides information about:

```text
Threat Purpose

Affected Resource

Detected Activity
```

Another conceptual example:

```text
UnauthorizedAccess:IAMUser/...
```

can indicate suspicious IAM credential usage.

---

## 11. Resource Types

GuardDuty findings can involve resources such as:

```text
EC2 Instance

IAM Credentials

S3 Bucket

S3 Object

EKS Cluster

ECS Cluster

Container

RDS Database

Lambda Function
```

The exact finding information depends on the resource type.

---

# Severity

## 12. Severity Levels

GuardDuty assigns a numeric severity value from:

```text
1.0
to
10.0
```

Current severity categories are:

```text
Low

Medium

High

Critical
```

---

## 13. Low Severity

Range:

```text
1.0 – 3.9
```

Low severity generally represents suspicious activity with lower immediate impact.

Example:

```text
Reconnaissance

Port Scanning

Failed Attack Attempt
```

Low does not mean:

```text
Ignore Forever
```

It may still provide useful context during investigation.

---

## 14. Medium Severity

Range:

```text
4.0 – 6.9
```

Medium findings may indicate suspicious behavior that differs from expected activity.

Examples may include:

```text
Unusual API Usage

Potential Credential Abuse

Unexpected Behavioral Changes
```

Investigation should determine whether the behavior was authorized.

---

## 15. High Severity

Range:

```text
7.0 – 8.9
```

High findings may indicate that a resource or credential is actively being used for unauthorized activity.

These findings should receive high priority.

Examples could involve:

```text
Credential Compromise

Data Exfiltration

Compromised EC2 Activity
```

---

## 16. Critical Severity

Range:

```text
9.0 – 10.0
```

Critical findings can indicate an active or recent attack sequence involving potentially compromised resources.

Examples include:

```text
Compromised Credentials

Ransomware-Related Activity

Multi-Step Attack Sequence
```

Critical findings should be triaged immediately.

---

# Finding Investigation

## 17. Finding Details

When reviewing a finding, investigate:

```text
Finding Type

Severity

Account

Region

Affected Resource

First Seen

Last Seen

Count

Action

Source IP

Destination

User Identity

Resource Role
```

Not every finding contains all fields.

The available information depends on the finding type.

---

## 18. Investigation Questions

For every GuardDuty finding, ask:

```text
What was detected?

Which resource is affected?

What is the severity?

When did it begin?

Is the activity still occurring?

Was this expected?

Which identity was involved?

Which IP or domain was involved?

What happened before the finding?

What happened after the finding?
```

---

## 19. GuardDuty Is a Starting Point

A finding is not always enough to determine the entire incident.

Example:

```text
GuardDuty Finding
       |
       v
Potential Credential Compromise
```

Investigation should continue with:

```text
CloudTrail

AWS Config

VPC Flow Logs

CloudWatch

Application Logs

OS Logs
```

---

# Extended Threat Detection

## 20. Attack Sequences

Modern GuardDuty can correlate multiple signals into attack sequence findings.

Instead of:

```text
Event A

Event B

Event C
```

being reviewed independently, GuardDuty can correlate them:

```text
Event A
   ↓
Event B
   ↓
Event C
   ↓
Attack Sequence
```

This can provide higher-confidence threat detection.

---

## 21. Why Attack Sequences Matter

A single API call may not be clearly malicious.

Example:

```text
ListBuckets
```

may be normal.

Another event:

```text
GetObject
```

may also be normal.

But:

```text
Unusual Credential Use
      ↓
Reconnaissance
      ↓
Privilege Escalation
      ↓
Sensitive Data Access
      ↓
Data Exfiltration
```

is much more suspicious.

Attack sequence correlation helps identify this broader pattern.

---

## 22. Attack Sequence Examples

GuardDuty currently supports attack sequence findings involving areas such as:

```text
IAM Credentials

Amazon S3 Data

Amazon EC2 Instance Groups

Amazon EKS

Amazon ECS
```

Examples conceptually include:

```text
AttackSequence:IAM/CompromisedCredentials

AttackSequence:S3/CompromisedData

AttackSequence:EC2/CompromisedInstanceGroup
```

These can receive Critical severity.

---

# Protection Plans

## 23. GuardDuty Protection Plans

Beyond foundational threat detection, GuardDuty provides optional protection plans.

Important examples include:

```text
S3 Protection

Runtime Monitoring

EKS Audit Logs

RDS Protection

Lambda Protection
```

Other GuardDuty security capabilities can include:

```text
Malware Protection

AI Protection

Custom Detection Rules
```

Enable only the protection required by the environment and threat model.

---

# S3 Protection

## 24. S3 Protection

S3 Protection analyzes:

```text
AWS CloudTrail S3 Data Events
```

including object-level API activity.

Conceptually:

```text
Application
     |
     v
S3 Object API
     |
     v
CloudTrail Data Event
     |
     v
GuardDuty S3 Protection
```

---

## 25. S3 Threat Detection

Potential detections include:

```text
Suspicious Object Access

Potential Data Exfiltration

Potential Data Destruction

Suspicious API Patterns

Public Access Changes
```

Example:

```text
Compromised Credential
      |
      v
大量 GetObject Requests
      |
      v
Sensitive S3 Data
```

GuardDuty may identify this as suspicious depending on context.

---

# Runtime Monitoring

## 26. Runtime Monitoring

Runtime Monitoring provides deeper visibility into supported compute workloads.

Currently supported resource types include:

```text
Amazon EKS

Amazon ECS on AWS Fargate

Amazon EC2
```

It uses a GuardDuty security agent.

---

## 27. Runtime Telemetry

The GuardDuty security agent can provide visibility into behavior such as:

```text
Process Execution

File Access

Command-Line Arguments

Network Connections
```

Conceptually:

```text
EC2 / Container
       |
       v
GuardDuty Security Agent
       |
       v
Runtime Events
       |
       v
GuardDuty
```

---

## 28. Why Runtime Monitoring Is Different

Foundational GuardDuty can see activity such as:

```text
AWS API

DNS

Network Flow
```

Runtime Monitoring can additionally see:

```text
Inside the Workload
```

Example:

```text
Malicious Process

Suspicious Shell Command

Privilege Escalation

Unexpected File Activity
```

This provides deeper workload visibility.

---

# EKS Protection

## 29. EKS Audit Logs

GuardDuty can analyze EKS Kubernetes audit activity.

Conceptually:

```text
Kubernetes API
      |
      v
EKS Audit Logs
      |
      v
GuardDuty
```

Possible suspicious behaviors include:

```text
Unauthorized Kubernetes API Calls

Suspicious Pod Activity

Privilege Escalation

Unexpected Cluster Administration
```

---

## 30. EKS Runtime Monitoring

Runtime Monitoring can also inspect supported EKS runtime behavior.

Conceptually:

```text
Container
   |
   v
GuardDuty Agent
   |
   v
Runtime Events
```

This can help detect activity such as:

```text
Container Compromise

Suspicious Process Execution

Privilege Escalation

Container-to-Host Attack
```

---

# RDS Protection

## 31. RDS Protection

RDS Protection analyzes supported RDS login activity.

Conceptually:

```text
Client
   |
   v
Database Login
   |
   v
RDS Login Activity
   |
   v
GuardDuty
```

Potential threats may include:

```text
Suspicious Database Authentication

Credential Abuse

Unexpected Login Patterns
```

---

## 32. Database Threat Example

Scenario:

```text
Database User
      |
      v
Unusual External Source
      |
      v
Repeated Authentication
```

GuardDuty can use login behavior to help identify potential database credential compromise.

This complements:

```text
RDS Logs

CloudTrail

Application Logs
```

---

# Lambda Protection

## 33. Lambda Protection

Lambda Protection analyzes Lambda network activity.

Conceptually:

```text
Lambda Function
      |
      v
Network Activity
      |
      v
GuardDuty
```

This can help identify suspicious outbound communication from Lambda functions.

---

## 34. Lambda Threat Example

Scenario:

```text
Compromised Dependency
       |
       v
Lambda Function
       |
       v
Malicious External Server
```

GuardDuty may detect suspicious network behavior associated with the function.

---

# Malware Protection

## 35. Malware Protection for EC2

GuardDuty Malware Protection for EC2 can scan EBS volumes associated with EC2 instances or container workloads running on EC2.

Conceptually:

```text
Suspicious EC2 Finding
       |
       v
Malware Scan
       |
       v
EBS Volume Analysis
```

This can help identify malicious files associated with a potentially compromised instance.

---

## 36. Malware Protection for S3

Malware Protection for S3 can scan objects uploaded to selected S3 buckets.

Conceptually:

```text
New S3 Object
      |
      v
Malware Scan
      |
      +-- Clean
      |
      +-- Malicious
```

This can help prevent malicious uploaded files from entering downstream workflows.

---

## 37. Malware Protection for Backup

GuardDuty can also integrate with AWS Backup to scan supported backup resources.

Examples include:

```text
EBS Snapshots

EC2 AMIs

S3 Recovery Points
```

Potential use:

```text
Backup
   |
   v
Malware Scan
   |
   v
Validate Before Restore
```

This helps reduce the risk of restoring infected backup data.

---

# AI Protection

## 38. GuardDuty AI Protection

GuardDuty AI Protection extends threat detection to supported AWS AI workloads.

It can analyze activity associated with services such as:

```text
Amazon Bedrock

Amazon Bedrock AgentCore

Amazon SageMaker AI
```

Data can include relevant CloudTrail data events and management events.

---

## 39. AI Threat Examples

Potential detections can include:

```text
Anomalous Model Invocation

Unexpected Source IP

Unusual API Usage

Unusual Model Access

Prompt Attack Signals
```

Conceptually:

```text
AI Application
     |
     v
Model Invocation
     |
     v
CloudTrail Data Event
     |
     v
GuardDuty AI Protection
```

---

# Custom Detection Rules

## 40. Custom Detection Rules

GuardDuty Custom Detection Rules provide AWS-maintained detection rules for activity that may be abnormal specifically within an organization's environment.

Example:

```text
Sharing an AMI
```

may be legitimate in one account but forbidden in another.

A Custom Detection Rule can identify that organization-specific activity.

---

## 41. Live vs Dry Run

Custom Detection Rules can operate in:

```text
Dry Run

or

Live
```

### Dry Run

```text
Activity Matched
      |
      v
CloudWatch Metrics
```

No GuardDuty finding is generated.

This is useful for understanding expected signal volume.

### Live

```text
Activity Matched
      |
      v
GuardDuty Finding
```

---

## 42. Why Dry Run Matters

Before enabling a rule in production:

```text
Enable Dry Run
      |
      v
Measure Activity
      |
      v
Evaluate Noise
      |
      v
Enable Live
```

This can reduce:

```text
False Positives

Alert Fatigue
```

---

# Finding Management

## 43. Finding Status

GuardDuty findings can be managed during investigation.

Conceptually:

```text
New Finding
    |
    v
Investigate
    |
    +-- Legitimate
    |
    +-- Suspicious
    |
    +-- Confirmed Threat
```

Security teams should document how findings are triaged and closed.

---

## 44. Finding Aggregation

GuardDuty can aggregate repeated occurrences of the same finding type.

Instead of generating unlimited separate findings:

```text
Same Threat

Same Resource

Repeated Activity
```

GuardDuty may update an existing finding with:

```text
Count

First Seen

Last Seen
```

This helps reduce duplicate alert volume.

---

## 45. Suppression Rules

Suppression rules can automatically archive findings that match defined conditions.

Example:

```text
Known Security Scanner
       |
       v
Expected Port Scan
       |
       v
Suppression Rule
       |
       v
Auto Archive
```

Suppression should be used carefully.

Poor suppression can create security blind spots.

---

## 46. When to Suppress

Reasonable candidates may include:

```text
Authorized Penetration Testing

Known Vulnerability Scanner

Expected Security Automation
```

Before suppressing:

```text
Validate Activity

Restrict Rule Conditions

Document Reason

Review Periodically
```

---

# EventBridge Integration

## 47. GuardDuty and EventBridge

GuardDuty findings can be sent to Amazon EventBridge.

Conceptually:

```text
GuardDuty Finding
       |
       v
EventBridge
       |
       +-- SNS
       |
       +-- Lambda
       |
       +-- Step Functions
       |
       +-- Systems Manager
```

This can support automated security workflows.

---

## 48. Notification Example

```text
High Severity Finding
       |
       v
EventBridge
       |
       v
SNS
       |
       v
Security Team
```

This ensures high-priority findings reach responders quickly.

---

## 49. Automated Containment Example

Example:

```text
GuardDuty
Detects Compromised EC2
       |
       v
EventBridge
       |
       v
Lambda / Automation
       |
       v
Isolation Security Group
```

Other actions could include:

```text
Disable Credentials

Tag Resource

Create Incident Ticket

Capture Forensic Data
```

Automatic containment should be tested carefully before production use.

---

# Multi-Account GuardDuty

## 50. Multi-Account Architecture

Large organizations commonly centralize GuardDuty administration.

Conceptually:

```text
AWS Organizations
       |
       v
Delegated GuardDuty Administrator
       |
       +-- Production
       |
       +-- Development
       |
       +-- Shared Services
       |
       +-- Security
```

This supports centralized finding management.

---

## 51. Delegated Administrator

A security account can be designated as GuardDuty delegated administrator.

Conceptually:

```text
Management Account
      |
      v
Delegates GuardDuty
      |
      v
Security Account
      |
      v
Manage Member Accounts
```

This reduces the need to operate GuardDuty independently in every account.

---

## 52. Auto-Enable

Organizations can configure GuardDuty features to automatically enable for appropriate member accounts.

This helps reduce gaps caused by:

```text
New AWS Account Created

GuardDuty Forgotten

Protection Plan Not Enabled
```

A security baseline should define which GuardDuty features are required.

---

# Investigation Scenario

## 53. Compromised IAM Credential

Scenario:

```text
GuardDuty Finding

Potential IAM Credential Compromise
```

Investigation:

```text
Step 1
Review Finding

Step 2
Identify Access Key / Principal

Step 3
Check CloudTrail

Step 4
Identify API Activity

Step 5
Check Resource Changes

Step 6
Determine Scope

Step 7
Contain Credential

Step 8
Remediate Changes
```

---

## 54. CloudTrail Investigation

Search the relevant time period for actions performed by the affected identity.

Look for:

```text
IAM Changes

EC2 Creation

S3 Access

KMS Operations

Secrets Access

CloudTrail Changes
```

Build a timeline.

---

## 55. Credential Containment

Depending on the identity type:

```text
IAM Access Key
→ Disable / Rotate

Temporary Credential
→ Revoke Relevant Sessions Where Applicable

User Password
→ Reset

Role
→ Review Trust and Permissions
```

Do not simply delete evidence before investigation.

---

## 56. Compromised EC2 Scenario

Scenario:

```text
GuardDuty
       |
       v
Suspicious EC2 Network Activity
```

Investigate:

```text
Affected Instance

Public IP

Security Groups

IAM Role

VPC Flow Activity

DNS Queries

Processes

Files

CloudTrail Activity
```

---

## 57. EC2 Containment

Potential response:

```text
Affected EC2
      |
      v
Isolation Security Group
```

Then:

```text
Preserve Evidence

Review IAM Credentials

Inspect Volumes

Perform Malware Scan

Determine Entry Point
```

Termination may destroy useful forensic evidence.

---

# Findings and Context

## 58. False Positive Considerations

Not every finding represents malicious activity.

Examples:

```text
Authorized Penetration Test

New Administrator Location

Security Scanner

New Automation

Unexpected but Legitimate Deployment
```

Investigate before concluding.

---

## 59. Expected Activity Can Still Be Risky

Example:

```text
Administrator Intentionally
Disables CloudTrail
```

The activity may be authorized but still violate policy.

Therefore distinguish:

```text
Authorized?

and

Secure?
```

These are separate questions.

---

# Troubleshooting

## 60. No GuardDuty Findings

No findings does not necessarily mean:

```text
No Threats
```

Check:

```text
Is GuardDuty Enabled?

Is Correct Region Selected?

Are Required Protection Plans Enabled?

Are Member Accounts Covered?

Is Runtime Agent Healthy?

Are Required Resources Supported?
```

---

## 61. Missing S3 Detection

Check:

```text
Is S3 Protection Enabled?

Is the activity covered by S3 Protection?

Was the required CloudTrail S3 data activity available to GuardDuty?
```

---

## 62. Missing Runtime Findings

Check:

```text
Is Runtime Monitoring Enabled?

Is Resource Type Supported?

Is GuardDuty Security Agent Installed?

Is Agent Healthy?

Are IAM Permissions Correct?
```

---

## 63. Too Many Findings

Investigate:

```text
Repeated Expected Activity?

Security Scanner?

Automation?

Misconfiguration?

Real Attack?
```

Possible solutions:

```text
Fix Root Cause

Tune Automation

Use Carefully Scoped Suppression
```

Do not suppress broad categories simply to reduce alert volume.

---

# Hands-on Practice

## 64. Practice — Explore GuardDuty

Open:

```text
AWS Console
   |
   v
Amazon GuardDuty
```

Review:

```text
Summary

Findings

Protection Plans

Settings
```

Identify whether GuardDuty is enabled in the Region.

---

## 65. Practice — Review Protection Plans

Navigate to:

```text
GuardDuty
   |
   v
Protection Plans
```

Review the status of:

```text
Foundational GuardDuty

S3 Protection

Runtime Monitoring

EKS Audit Logs

RDS Protection

Lambda Protection
```

Do not enable paid features solely for practice without reviewing cost.

---

## 66. Practice — Generate Sample Findings

GuardDuty can generate sample findings.

Use:

```text
GuardDuty
→ Settings / Sample Findings
```

or the available console workflow.

Sample findings contain fictitious information and are marked as sample data.

They can help you learn:

```text
Finding Type

Severity

Resource

Action

Evidence
```

without creating a real attack.

---

## 67. Sample Finding Exercise

Choose one sample finding.

Record:

```text
Finding Type:

Severity:

Affected Resource:

Region:

First Seen:

Last Seen:

Action:

Why It Is Suspicious:
```

Then write:

```text
Investigation Plan:

1.

2.

3.

4.

5.
```

---

## 68. Optional CLI Practice

List GuardDuty detectors:

```bash
aws guardduty list-detectors
```

Get detector details:

```bash
aws guardduty get-detector \
  --detector-id <detector-id>
```

List findings:

```bash
aws guardduty list-findings \
  --detector-id <detector-id>
```

Retrieve finding details:

```bash
aws guardduty get-findings \
  --detector-id <detector-id> \
  --finding-ids <finding-id>
```

Do not publish:

```text
Real Account IDs

Instance IDs

Finding IDs

Source IPs

Sensitive Finding Details
```

to a public GitHub repository.

---

# Architecture Exercise

## 69. Threat Detection Architecture

Design:

```text
AWS Accounts
      |
      +-- CloudTrail
      |
      +-- Network Activity
      |
      +-- DNS
      |
      +-- Runtime Telemetry
      |
      v
Amazon GuardDuty
      |
      v
Findings
      |
      v
EventBridge
      |
      +---------+----------+
      |                    |
      v                    v
     SNS              Automation
      |                    |
      v                    v
Security Team         Containment
```

---

## 70. Investigation Integration

A GuardDuty finding should connect back to the services learned in Phase 4.

```text
GuardDuty
→ Something suspicious happened.

CloudTrail
→ What API activity occurred?

AWS Config
→ What configuration changed?

VPC Flow Logs
→ What network activity occurred?

CloudWatch / OS Logs
→ What happened in the workload?
```

This provides a complete investigation workflow.

---

# Security Checklist

```text
[ ] GuardDuty is enabled in required Regions

[ ] Required AWS accounts are covered

[ ] Delegated administrator is configured where appropriate

[ ] New organization accounts receive required GuardDuty configuration

[ ] Required protection plans are enabled

[ ] S3 Protection is enabled for sensitive S3 workloads where appropriate

[ ] Runtime Monitoring covers required compute workloads

[ ] RDS Protection is enabled where required

[ ] Lambda Protection is enabled where required

[ ] Finding severity is used for triage

[ ] Critical and High findings have defined response procedures

[ ] GuardDuty findings are sent to a monitoring workflow

[ ] EventBridge integrations are configured where required

[ ] Automated response actions are tested

[ ] Suppression rules are narrowly scoped

[ ] Suppression rules are reviewed periodically

[ ] GuardDuty findings are correlated with CloudTrail

[ ] Network findings are correlated with Flow Logs and DNS activity

[ ] Runtime findings are correlated with OS and application evidence

[ ] Malware Protection is considered for relevant workloads

[ ] Sample findings are used to validate monitoring pipelines

[ ] GuardDuty configuration and costs are periodically reviewed
```

---

## Key Takeaways

- Amazon GuardDuty is a managed AWS threat detection service.
- Foundational GuardDuty analyzes CloudTrail management events, VPC network telemetry, and DNS query telemetry.
- GuardDuty generates Findings rather than directly blocking every detected threat.
- Findings include severity, affected resources, activity details, and investigation context.
- GuardDuty severity ranges from Low to Critical.
- Critical findings can indicate correlated multi-step attack activity.
- Extended Threat Detection correlates multiple weak signals into attack sequence findings.
- S3 Protection analyzes S3 object-level API activity.
- Runtime Monitoring provides process, file, command, and network visibility inside supported workloads.
- RDS Protection analyzes supported database login activity.
- Lambda Protection analyzes Lambda network activity.
- Malware Protection can help detect malicious files in EC2, S3, and supported backup resources.
- AI Protection extends GuardDuty threat detection to supported AWS AI workloads.
- Custom Detection Rules can identify activity that is suspicious specifically for an organization's environment.
- EventBridge can connect GuardDuty findings to notifications and automated response workflows.
- Multi-account GuardDuty can be centrally administered using AWS Organizations.
- A GuardDuty finding should be correlated with CloudTrail, AWS Config, network telemetry, and workload logs during investigation.
- Suppression rules must be carefully scoped to avoid creating security blind spots.

---

## Reflection

Today I learned that Amazon GuardDuty converts large amounts of AWS security telemetry into actionable security findings.

Instead of manually reviewing CloudTrail events, network activity, DNS queries, and workload telemetry, GuardDuty analyzes these signals and identifies suspicious behavior.

The most important lesson is that a GuardDuty finding is the beginning of an investigation rather than the final conclusion.

A security engineer should validate the finding, identify the affected resource and identity, correlate it with CloudTrail and other logs, determine the scope of compromise, preserve evidence, and then contain and remediate the threat.

I also learned that modern GuardDuty extends beyond basic EC2 and IAM detection through protection plans such as S3 Protection, Runtime Monitoring, RDS Protection, Lambda Protection, and additional capabilities such as Extended Threat Detection and Custom Detection Rules.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Anomaly Detection | Identifying behavior that differs significantly from an expected baseline |
| Attack Sequence | A correlated series of suspicious actions representing a potential multi-stage attack |
| Finding | A notification describing a potential security threat |
| GuardDuty | AWS managed threat detection service |
| Indicator of Compromise | Evidence that may indicate a system or identity has been compromised |
| Protection Plan | An optional GuardDuty feature providing additional detection coverage |
| Runtime Monitoring | Monitoring process, file, command, and network behavior inside supported workloads |
| Suppression Rule | A rule that automatically archives selected GuardDuty findings |
| Threat Detection | The process of identifying potentially malicious activity |
| Threat Intelligence | Information about known malicious infrastructure and attacker behavior |
