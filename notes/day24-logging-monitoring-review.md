# Day 24 — Logging & Monitoring Review

## Topic

AWS Logging, Monitoring, Detection, and Security Investigation Review

---

## Objectives

- Review AWS CloudTrail
- Review Amazon CloudWatch
- Review AWS Config
- Review centralized logging architecture
- Understand the relationship between logs, metrics, and configuration history
- Understand detection and alerting workflows
- Practice security event correlation
- Build a systematic incident investigation process
- Review common logging and monitoring misconfigurations
- Design a basic AWS security monitoring architecture

---

## 1. Phase 4 Overview

During this phase, I studied:

```text
Day 20
→ AWS CloudTrail

Day 21
→ Amazon CloudWatch

Day 22
→ AWS Config

Day 23
→ Centralized Logging
```

Each service answers a different security question.

```text
CloudTrail
→ Who performed the action?

AWS Config
→ What configuration changed?

CloudWatch
→ What is happening to the system?

Centralized Logging
→ Where can logs be analyzed together?
```

Together, these services provide important visibility for AWS security operations.

---

## 2. Security Monitoring Lifecycle

A useful security monitoring model is:

```text
Collect
   ↓
Centralize
   ↓
Analyze
   ↓
Detect
   ↓
Alert
   ↓
Investigate
   ↓
Respond
   ↓
Improve
```

Logging alone is not sufficient.

A mature security process must convert logs into useful detection and investigation capabilities.

---

## 3. Collect

The first step is collecting useful security data.

Possible AWS sources include:

```text
CloudTrail

CloudWatch Logs

AWS Config

VPC Flow Logs

Application Logs

Operating System Logs

RDS Logs

WAF Logs

Load Balancer Logs

DNS Logs
```

Not every environment requires every log source.

The required logs depend on:

- Architecture
- Threat model
- Compliance
- Incident response needs
- Cost

---

## 4. Centralize

Logs distributed across many AWS accounts are difficult to investigate.

Without centralization:

```text
Production
→ Logs

Development
→ Logs

Shared Services
→ Logs

Security Team
→ Search Each Account
```

With centralization:

```text
Production ─────┐
Development ────┼──> Central Logging
Shared Services ┘
```

This improves:

```text
Visibility

Investigation

Correlation

Governance

Audit
```

---

## 5. Protect

Security logs are evidence.

They should be protected from:

```text
Unauthorized Reading

Modification

Deletion

Retention Changes

Public Exposure
```

Possible controls include:

```text
Dedicated Log Archive Account

S3 Block Public Access

Encryption

Versioning

Object Lock

Least-Privilege IAM

Restricted Delete Permissions
```

A logging system is not secure if an attacker can easily delete its evidence.

---

## 6. Analyze

Collected logs must be searchable.

Examples:

```text
CloudTrail Event History

CloudWatch Logs Insights

CloudTrail Lake

Athena / S3-based Analysis

Security Analytics Platforms
```

The analysis method depends on:

- Data volume
- Query complexity
- Retention
- Investigation requirements
- Cost

---

## 7. Detect

Detection identifies potentially important security activity.

Examples:

```text
Root User Activity

IAM Policy Changes

Security Group Changes

Failed Authentication Attempts

Unexpected API Calls

Logging Disabled

KMS Key Changes

Public Resource Exposure
```

A detection event should be treated as:

```text
Signal
```

not automatically as:

```text
Confirmed Incident
```

Investigation is still required.

---

## 8. Alert

Important detections should reach the appropriate team.

Conceptually:

```text
Security Event
      |
      v
Detection
      |
      v
Alarm / Rule
      |
      v
Notification
      |
      v
Security Team
```

Possible notification mechanisms may include:

```text
Amazon SNS

EventBridge

Incident Management Systems

Security Operations Platforms
```

An alert should provide enough context for investigation.

---

## 9. Investigate

When an alert occurs, security engineers should determine:

```text
What happened?

Who performed the action?

When did it happen?

Where did it originate?

Which resources were affected?

Was the activity authorized?

What happened before and after the event?

Was data accessed?

Was persistence created?
```

This requires correlation across multiple data sources.

---

# CloudTrail Review

## 10. CloudTrail Purpose

AWS CloudTrail records supported AWS account activity and API operations.

It helps answer:

```text
Who?

Did What?

When?

From Where?

Against Which AWS Resource?
```

Conceptually:

```text
IAM Identity
      |
      v
AWS API
      |
      v
CloudTrail Event
```

CloudTrail is one of the most important AWS security investigation data sources.

---

## 11. CloudTrail Event Types

Important event categories include:

```text
Management Events

Data Events

Insights Events

Network Activity Events
```

### Management Events

Examples:

```text
CreateUser

AttachRolePolicy

RunInstances

AuthorizeSecurityGroupIngress
```

These mainly represent AWS resource management activity.

### Data Events

Examples:

```text
S3 GetObject

S3 PutObject

Lambda Invoke
```

These represent supported operations performed on resource data.

---

## 12. Event History

CloudTrail Event History provides recent management event history.

Use cases include:

```text
Who changed this Security Group?

Who terminated this EC2 instance?

Who modified this IAM policy?
```

Event History is useful for recent investigations.

Longer-term or broader logging requires an appropriate Trail or Event Data Store.

---

## 13. Important CloudTrail Fields

When investigating an event, review:

```text
eventTime

eventName

eventSource

userIdentity

sourceIPAddress

awsRegion

requestParameters

responseElements

errorCode
```

A useful mental model is:

```text
Who?
→ userIdentity

What?
→ eventName

Which Service?
→ eventSource

When?
→ eventTime

Where?
→ sourceIPAddress / awsRegion

Result?
→ responseElements / errorCode
```

---

## 14. CloudTrail Investigation Example

Scenario:

```text
Security Group
TCP 22
0.0.0.0/0
```

appears unexpectedly.

Search for:

```text
AuthorizeSecurityGroupIngress
```

Then review:

```text
userIdentity

eventTime

sourceIPAddress

requestParameters
```

CloudTrail can help determine who requested the change.

---

# CloudWatch Review

## 15. CloudWatch Purpose

Amazon CloudWatch provides monitoring and observability for AWS workloads.

Important features include:

```text
Metrics

Logs

Alarms

Logs Insights

Metric Filters

Dashboards
```

CloudWatch helps answer:

```text
What is happening to the workload?
```

---

## 16. Metrics

Metrics are numerical measurements over time.

Examples:

```text
CPUUtilization

NetworkIn

NetworkOut

DatabaseConnections

ErrorCount
```

Metrics can help identify:

```text
Performance Problems

Availability Problems

Unexpected Activity

Resource Exhaustion
```

However:

```text
Abnormal Metric
≠
Confirmed Attack
```

---

## 17. CloudWatch Logs

CloudWatch Logs stores log events.

Structure:

```text
Log Group
   |
   v
Log Stream
   |
   v
Log Events
```

Possible sources include:

```text
EC2

Applications

Lambda

CloudTrail

RDS

VPC Flow Logs
```

---

## 18. Logs Insights

CloudWatch Logs Insights can search and analyze logs.

Example:

```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```

Search for errors:

```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

Security engineers can use Logs Insights during investigations.

---

## 19. CloudWatch Alarms

CloudWatch Alarms evaluate metrics.

Conceptually:

```text
Metric
  ↓
Threshold
  ↓
Alarm Evaluation
  ↓
ALARM
  ↓
Action
```

Important configuration includes:

```text
Period

Evaluation Periods

Datapoints to Alarm

Threshold

Missing Data Treatment
```

---

## 20. Metric Filters

Metric Filters convert matching CloudWatch log events into numerical metrics.

Example:

```text
Authentication Failed
       |
       v
Metric Filter
       |
       v
FailedLoginCount
       |
       v
Alarm
```

This connects:

```text
Logs
→ Metrics
→ Alarm
→ Alert
```

---

# AWS Config Review

## 21. AWS Config Purpose

AWS Config records and evaluates AWS resource configurations.

It helps answer:

```text
What is the current configuration?

What was the previous configuration?

When did it change?

Does it meet the security baseline?
```

---

## 22. Configuration Recorder

The Configuration Recorder tracks supported AWS resources that are included in its recording scope.

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

The recording configuration determines which resources AWS Config tracks.

---

## 23. Configuration Item

A Configuration Item is a point-in-time representation of a supported resource configuration.

Example:

```text
Security Group

10:00
SSH Restricted

12:00
SSH Public

14:00
SSH Restricted
```

These records build the Configuration History.

---

## 24. Config Rules

AWS Config Rules evaluate resources against defined requirements.

Example:

```text
Requirement:

EBS volumes must be encrypted.
```

Evaluation:

```text
EBS Volume
    |
    v
Encrypted?
    |
 +--+--+
 |     |
Yes    No
 |     |
 v     v
COMPLIANT
     NON_COMPLIANT
```

---

## 25. Compliance

Important states include:

```text
COMPLIANT

NON_COMPLIANT
```

NON_COMPLIANT means:

```text
The resource does not satisfy
the defined configuration requirement.
```

It does not automatically mean:

```text
The resource is compromised.
```

---

## 26. Remediation

AWS Config can associate remediation with noncompliant resources.

Conceptually:

```text
NON_COMPLIANT
      |
      v
AWS Config
      |
      v
Systems Manager Automation
      |
      v
Remediation
```

Remediation can be:

```text
Manual

or

Automatic
```

Automatic remediation should be carefully tested before production use.

---

# Centralized Logging Review

## 27. Log Archive Account

A mature AWS environment may use a dedicated Log Archive account.

Example:

```text
AWS Organization
│
├── Production
├── Development
├── Shared Services
│
└── Security OU
    ├── Security / Monitoring Account
    └── Log Archive Account
```

The Log Archive account stores protected long-term audit logs.

---

## 28. Log Archive vs Monitoring

These functions can be separated.

### Log Archive

Purpose:

```text
Long-Term Storage

Audit

Forensics

Retention
```

### Monitoring

Purpose:

```text
Search

Detection

Analysis

Alerting
```

Conceptually:

```text
Log Archive
→ Preserve Evidence

Monitoring
→ Use Evidence
```

---

## 29. Multi-Account Logging

Multiple accounts may generate logs:

```text
Production

Development

Security

Shared Services
```

Centralized architecture:

```text
Account A ────┐
Account B ────┼──> Central Logging
Account C ────┘
```

This reduces fragmented visibility.

---

## 30. Multi-Region Logging

Attackers or administrators may operate in Regions not normally used by an organization.

Example:

```text
Tokyo
Singapore
Virginia
```

Logging should consider all Regions required by the organization's architecture and security policy.

A visibility gap can exist if:

```text
Region A
→ Logged

Region B
→ Not Logged
```

---

# Log Correlation

## 31. Why Correlate Logs?

One log source rarely tells the complete story.

Example:

```text
CloudTrail
→ Who changed Security Group?

AWS Config
→ What changed?

VPC Flow Logs
→ Did network traffic occur?

OS Logs
→ Was login successful?

Application Logs
→ What did the user do?
```

Combining these creates a more complete incident timeline.

---

## 32. Security Investigation Scenario

Scenario:

A production EC2 instance suddenly has:

```text
TCP 22
Source: 0.0.0.0/0
```

The goal is to determine:

```text
Who changed it?

When?

Was the instance accessed?

Was the access successful?

What happened afterward?
```

---

## 33. Step 1 — AWS Config

Use AWS Config to determine:

```text
Previous Security Group Configuration

Current Security Group Configuration

Configuration Change Time
```

Example:

```text
10:00
TCP 22
10.0.0.0/8

10:35
TCP 22
0.0.0.0/0
```

AWS Config helps identify:

```text
WHAT changed.
```

---

## 34. Step 2 — CloudTrail

Search around:

```text
10:35
```

for:

```text
AuthorizeSecurityGroupIngress
```

Review:

```text
userIdentity

eventTime

sourceIPAddress

requestParameters
```

CloudTrail helps identify:

```text
WHO changed it.
```

---

## 35. Step 3 — VPC Flow Logs

Review network traffic after exposure.

Questions:

```text
Were external connections attempted?

Which source IPs contacted the instance?

Which destination port was used?

Was traffic ACCEPT or REJECT?
```

Example:

```text
External IP
    |
    v
TCP 22
    |
    v
EC2
```

Flow Logs help identify network communication.

---

## 36. Step 4 — Operating System Logs

If network traffic reached the instance, review host logs.

For Linux:

```text
SSH Authentication

Successful Login

Failed Login

sudo Activity
```

Questions:

```text
Was authentication successful?

Which local account was used?

What commands were executed?
```

---

## 37. Step 5 — CloudWatch

Review:

```text
CPU

Network Traffic

Application Errors

System Logs
```

Unexpected behavior after the network exposure may provide additional evidence.

---

## 38. Step 6 — Build Timeline

Example:

```text
10:35
Security Group modified

10:37
External TCP 22 connection

10:38
SSH authentication success

10:40
Unexpected process executed

10:42
Outbound network connection

10:45
Security alert triggered
```

A timeline helps investigators understand event sequence.

---

## 39. Step 7 — Determine Scope

Ask:

```text
Was only one instance affected?

Were credentials stolen?

Were IAM permissions used?

Was S3 data accessed?

Were other AWS resources modified?

Was persistence created?

Was data transferred externally?
```

Incident scope may extend beyond the originally affected resource.

---

# Detection Use Cases

## 40. Root User Activity

Detection:

```text
Root User Activity
       |
       v
CloudTrail
       |
       v
Detection Rule
       |
       v
Alert
```

Routine administrative tasks should generally use appropriately authorized identities rather than the root user.

Unexpected root activity should be investigated.

---

## 41. IAM Permission Change

Relevant events may include:

```text
AttachRolePolicy

PutRolePolicy

CreatePolicyVersion

SetDefaultPolicyVersion
```

Detection flow:

```text
IAM Change
    |
    v
CloudTrail
    |
    v
CloudWatch / Detection
    |
    v
Alert
```

Questions:

```text
Was the change authorized?

Did privileges increase?

Which role was affected?
```

---

## 42. Security Group Change

Relevant APIs may include:

```text
AuthorizeSecurityGroupIngress

AuthorizeSecurityGroupEgress

RevokeSecurityGroupIngress

ModifySecurityGroupRules
```

Changes should be reviewed based on:

```text
Source

Port

Protocol

Affected Resource
```

Particularly risky examples include:

```text
TCP 22
0.0.0.0/0

TCP 3389
0.0.0.0/0

Database Ports
0.0.0.0/0
```

---

## 43. Logging Disabled

Potentially important changes include:

```text
StopLogging

DeleteTrail

DeleteLogGroup

StopConfigurationRecorder
```

Conceptually:

```text
Security Logging
      |
      v
Disabled
      |
      v
Reduced Visibility
```

Unexpected logging configuration changes should be investigated quickly.

---

## 44. KMS Key Change

Examples:

```text
DisableKey

ScheduleKeyDeletion

PutKeyPolicy
```

Potential impact:

```text
Encrypted Resources

Backups

Application Availability

Recovery
```

KMS-related changes may affect both security and availability.

---

## 45. S3 Policy Change

Relevant configuration changes may affect:

```text
Bucket Policy

Block Public Access

Object Access

Cross-Account Access
```

Investigation can combine:

```text
CloudTrail
+
AWS Config
+
Access Analyzer
```

---

# Security Monitoring Architecture

## 46. Basic Architecture

```text
                  AWS Workloads
                       |
      +----------------+----------------+
      |                |                |
      v                v                v
  CloudTrail       CloudWatch       AWS Config
      |                |                |
      +----------------+----------------+
                       |
                       v
               Centralized Logs
                       |
              +--------+--------+
              |                 |
              v                 v
         Log Archive        Monitoring
              |                 |
              v                 v
         Amazon S3       Detection / Alerts
                                |
                                v
                         Security Analyst
```

---

## 47. Prevent, Detect, Respond

Security controls can be viewed in three categories.

### Prevent

Examples:

```text
IAM

SCP

Security Groups

Block Public Access

Encryption
```

### Detect

Examples:

```text
CloudTrail

CloudWatch

AWS Config

VPC Flow Logs

Detection Rules
```

### Respond

Examples:

```text
Systems Manager Automation

IAM Credential Revocation

Security Group Changes

Instance Isolation

Incident Response Process
```

A mature security architecture requires all three.

---

## 48. Detection Without Response

Poor model:

```text
Alert
 ↓
Nothing Happens
```

Better:

```text
Alert
 ↓
Triage
 ↓
Investigation
 ↓
Containment
 ↓
Remediation
 ↓
Recovery
```

Detection systems require operational processes.

---

## 49. Too Many Alerts

Excessive alerts can create:

```text
Alert Fatigue
```

Example:

```text
1,000 Alerts Per Day
       |
       v
Analysts Ignore Alerts
```

Detection rules should balance:

```text
Coverage

Accuracy

Context

Priority
```

Not every log event should generate an alert.

---

## 50. False Positives

A false positive occurs when normal activity triggers a security alert.

Example:

```text
Administrator
→ Authorized Security Group Change
→ Alert
```

The alert was technically correct but the activity was legitimate.

Detection tuning may consider:

```text
Approved Identities

Approved Change Windows

Known Automation

Expected Resources
```

However, exclusions should not create security blind spots.

---

## 51. False Negatives

A false negative occurs when malicious activity is not detected.

Example:

```text
Attacker
→ Malicious API Activity
→ No Alert
```

Possible reasons include:

```text
Missing Logs

Incorrect Detection Rule

Region Not Monitored

Data Event Not Enabled

Logging Disabled
```

Monitoring coverage should be periodically tested.

---

## 52. Logging Failure Is a Security Event

Suppose:

```text
Expected Logs
     |
     X
No Logs Arrive
```

Possible causes:

```text
Logging Disabled

Permission Error

KMS Error

Service Configuration Error

Pipeline Failure
```

Logging health should itself be monitored.

---

# Troubleshooting

## 53. CloudTrail Event Missing

Check:

```text
Correct Region?

Correct Time Range?

Management or Data Event?

Was Data Event logging configured?

Was the API supported?

Was the Trail recording the required event?
```

Remember that different event types have different logging requirements.

---

## 54. CloudWatch Log Missing

Check:

```text
Does the Log Group exist?

Is the source configured?

Does the source have permissions?

Is the correct Region selected?

Is the agent running?

Is the retention policy deleting older events?
```

---

## 55. Config Resource Missing

Check:

```text
Is AWS Config enabled?

Is Configuration Recorder running?

Is the resource type recorded?

Is the correct Region selected?

Is the resource type supported?
```

---

## 56. Alert Missing

Check:

```text
Did the log event arrive?

Did the metric filter match?

Did the metric receive data?

Did the alarm threshold trigger?

Did the alarm state change?

Is notification configured?

Is the SNS subscription confirmed?
```

Troubleshoot from the beginning of the pipeline.

---

## 57. Monitoring Troubleshooting Flow

```text
Source
  ↓
Log Generated?
  ↓
Log Collected?
  ↓
Log Centralized?
  ↓
Detection Matched?
  ↓
Metric Created?
  ↓
Alarm Triggered?
  ↓
Notification Sent?
  ↓
Analyst Received?
```

This approach helps identify the broken stage.

---

# Hands-on Practice

## 58. Practice — CloudTrail

Open:

```text
CloudTrail
→ Event History
```

Select one recent management event.

Record:

```text
Event Name:

Event Source:

Event Time:

Identity Type:

AWS Region:

Source:
```

Do not publish real sensitive details to GitHub.

---

## 59. Practice — CloudWatch

Open:

```text
CloudWatch
→ Metrics
```

Select one metric.

Identify:

```text
Namespace

Metric Name

Dimensions

Period

Statistic
```

Then review one Log Group if available.

---

## 60. Practice — AWS Config

Open:

```text
AWS Config
→ Resources
```

If recorded resources exist, review one resource timeline.

Identify:

```text
Current Configuration

Previous Configuration

Relationships

Compliance
```

---

## 61. Practice — Build an Incident Timeline

Use an imaginary scenario.

Scenario:

```text
Production Security Group
was opened to the Internet.
```

Create:

```text
09:00
Normal Configuration

10:20
Security Group Changed

10:22
External Connection

10:25
Successful Login

10:30
Unexpected API Activity

10:35
Alert
```

For each event, identify the most useful data source.

Example:

| Event | Data Source |
|---|---|
| Security Group Changed | AWS Config |
| Identity Responsible | CloudTrail |
| External Connection | VPC Flow Logs |
| Login | OS Logs |
| CPU Spike | CloudWatch |
| Alert | CloudWatch / Detection System |

---

## 62. Practice — Design Central Logging

Design a conceptual environment:

```text
Production Account

Development Account

Shared Services Account

Security Account

Log Archive Account
```

Define where the following go:

```text
CloudTrail

CloudWatch Logs

VPC Flow Logs

Config Data

Application Logs
```

Consider:

```text
Retention

Encryption

Access Control

Immutability

Region

Monitoring
```

---

## 63. Optional Security Investigation Exercise

Scenario:

An unknown IAM role performs:

```text
GetObject
```

against a sensitive S3 bucket.

Investigation plan:

### Step 1

CloudTrail Data Events:

```text
Who performed GetObject?
```

### Step 2

IAM:

```text
What permissions does the role have?
```

### Step 3

CloudTrail:

```text
What other API actions did the role perform?
```

### Step 4

Source:

```text
Which IP or AWS service was involved?
```

### Step 5

AWS Config:

```text
Was the bucket policy recently modified?
```

### Step 6

Scope:

```text
Which other objects were accessed?
```

Build a timeline before deciding whether the activity is malicious.

---

# Security Checklist

## 64. Logging Coverage

```text
[ ] Required CloudTrail events are recorded

[ ] Required Data Events are enabled

[ ] Required Regions are included

[ ] Required AWS accounts are included

[ ] Application logs are collected

[ ] OS logs are collected where required

[ ] Network logs are collected where required

[ ] Database logs are collected where required
```

---

## 65. Log Protection

```text
[ ] Central logs are stored securely

[ ] S3 Block Public Access is enabled

[ ] Log storage is encrypted

[ ] Delete permissions are restricted

[ ] Versioning is considered

[ ] Object Lock is considered

[ ] Logging administration is separated

[ ] Retention is defined
```

---

## 66. Detection

```text
[ ] Root activity is monitored

[ ] IAM changes are monitored

[ ] Network security changes are monitored

[ ] Logging configuration changes are monitored

[ ] Important KMS changes are monitored

[ ] Public exposure changes are monitored

[ ] Detection rules are regularly reviewed
```

---

## 67. Alerting

```text
[ ] Important detections generate alerts

[ ] Alert recipients are defined

[ ] SNS or other notification paths are tested

[ ] Alerts contain useful context

[ ] Alert severity is defined

[ ] Alert fatigue is monitored
```

---

## 68. Investigation

```text
[ ] CloudTrail events can be searched

[ ] CloudWatch logs can be queried

[ ] AWS Config history is available

[ ] Network logs are available

[ ] Log timestamps can be correlated

[ ] Investigation procedures are documented

[ ] Analysts have appropriate read access
```

---

## 69. Response

```text
[ ] Incident response roles are defined

[ ] Containment procedures exist

[ ] Compromised credentials can be revoked

[ ] Resources can be isolated

[ ] Remediation procedures are tested

[ ] Evidence is preserved

[ ] Lessons learned are documented
```

---

## Key Takeaways

- Logging and monitoring are essential parts of cloud security.
- CloudTrail records supported AWS API and account activity.
- CloudWatch provides metrics, logs, alarms, and analysis capabilities.
- AWS Config records resource configuration state and evaluates compliance.
- Centralized logging improves visibility across AWS accounts and Regions.
- Security logs should be protected as forensic evidence.
- A log event does not automatically represent a security incident.
- Effective monitoring requires detection, alerting, investigation, and response.
- AWS Config and CloudTrail complement each other by showing what changed and who performed the change.
- VPC Flow Logs can provide network context during investigations.
- Operating system and application logs provide visibility that AWS control-plane logs cannot.
- Security investigations should build timelines using multiple data sources.
- Logging failures should themselves be monitored.
- Detection rules should be tuned to reduce false positives while avoiding security blind spots.
- Logging, monitoring, and response processes should be tested regularly.
- Security monitoring should follow a continuous improvement cycle.

---

## Reflection

During this phase, I learned that AWS logging and monitoring involve much more than simply storing log files.

CloudTrail, CloudWatch, AWS Config, VPC Flow Logs, and application logs each provide different types of security visibility.

The most important lesson is that no single log source provides the complete picture of a security incident.

AWS Config can show what configuration changed, CloudTrail can show which identity performed the AWS API action, VPC Flow Logs can show network communication, and operating system or application logs can show what happened inside the workload.

I also learned that centralized logging improves security investigations by allowing events from different accounts and systems to be correlated.

From a security engineering perspective, the complete process should be viewed as a lifecycle:

Collect, centralize, protect, detect, alert, investigate, respond, and continuously improve.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Alert | A notification generated when a defined condition is detected |
| Alert Fatigue | Reduced analyst effectiveness caused by excessive alerts |
| Detection | Identifying activity that may require security investigation |
| False Negative | Malicious or unwanted activity that is not detected |
| False Positive | A legitimate event incorrectly treated as suspicious |
| Forensic Evidence | Information preserved for investigation of an incident |
| Log Correlation | Combining events from multiple sources to understand related activity |
| Security Monitoring | Continuous observation of systems for security-relevant activity |
| Telemetry | Metrics, logs, traces, and other data describing system behavior |
| Timeline | A chronological sequence of events used during an investigation |
