# Day 23 — Centralized Logging

## Topic

Centralized Logging Architecture, Log Archive Accounts, Multi-Account Collection, and Security Monitoring

---

## Objectives

- Understand why centralized logging is important
- Understand the purpose of a dedicated Log Archive account
- Learn how logs can be centralized across AWS accounts
- Understand organization-wide CloudTrail logging
- Understand centralized CloudWatch Logs
- Review VPC Flow Logs and application logs
- Understand centralized log storage using Amazon S3
- Learn how to protect centralized logs
- Understand separation of duties
- Learn the difference between log storage and log analysis
- Understand multi-account and multi-Region considerations
- Design a basic centralized logging architecture

---

## 1. What Is Centralized Logging?

Centralized logging means collecting logs from multiple systems, AWS accounts, and Regions into a central location.

Without centralized logging:

```text
Account A
├── CloudTrail
├── CloudWatch Logs
└── VPC Flow Logs

Account B
├── CloudTrail
├── CloudWatch Logs
└── VPC Flow Logs

Account C
├── CloudTrail
├── CloudWatch Logs
└── VPC Flow Logs
```

A security engineer must inspect each account separately.

With centralized logging:

```text
Account A ──┐
Account B ──┼──> Central Logging Account
Account C ──┘
```

This provides a centralized location for:

```text
Security Monitoring

Incident Investigation

Audit

Compliance

Long-Term Retention
```

---

## 2. Why Centralize Logs?

In a multi-account AWS environment, logs may be distributed across many resources.

Examples include:

```text
AWS CloudTrail

Amazon CloudWatch Logs

VPC Flow Logs

AWS Config

Elastic Load Balancer Logs

AWS WAF Logs

Route 53 DNS Logs

Application Logs

Database Logs
```

Without centralization:

```text
Security Incident
      |
      v
Search Account A
      |
      v
Search Account B
      |
      v
Search Account C
```

This increases investigation complexity.

Centralization changes the model:

```text
Security Incident
      |
      v
Central Log Repository
      |
      v
Search and Correlate Events
```

---

## 3. Dedicated Log Archive Account

A common AWS security architecture uses a dedicated account for centralized log storage.

Conceptually:

```text
AWS Organization
│
├── Management Account
│
├── Security OU
│   │
│   ├── Security Tooling Account
│   │
│   └── Log Archive Account
│
├── Production Account
│
├── Development Account
│
└── Shared Services Account
```

The Log Archive account is dedicated to storing logs.

It should not normally host application workloads.

---

## 4. Why Use a Separate Account?

Suppose production administrators have access to both workloads and their audit logs.

If credentials are compromised:

```text
Compromised Administrator
        |
        +-- Modify Production
        |
        +-- Delete Audit Logs
```

This is dangerous because an attacker may attempt to remove evidence.

A separate Log Archive account creates stronger separation:

```text
Production Administrator
        |
        v
Production Account

Security / Logging Administrator
        |
        v
Log Archive Account
```

This supports:

```text
Separation of Duties

Reduced Blast Radius

Independent Audit Logs

Stronger Access Control
```

---

## 5. Separation of Duties

Separation of duties means different responsibilities are assigned to different roles or teams.

Example:

```text
Application Team
→ Manage workloads

Security Team
→ Monitor security

Log Archive Administrators
→ Manage log storage

Auditors
→ Read logs
```

A workload administrator should not automatically have permission to:

```text
Delete Logs

Disable Logging

Modify Log Retention

Change Logging Bucket Policies
```

This reduces the risk of accidental or malicious log destruction.

---

## 6. Centralized Logging Architecture

A simplified architecture may look like:

```text
AWS Organization
       |
       +---------------------+
       |                     |
       v                     v
Production Account      Development Account
       |                     |
       +-----------+---------+
                   |
                   v
             Log Archive Account
                   |
            +------+------+
            |             |
            v             v
       Amazon S3      CloudWatch Logs
            |             |
            v             v
       Long-Term       Monitoring
        Archive         Analysis
```

Security teams can use centralized logs for investigations and monitoring.

---

## 7. Common Log Sources

A centralized logging architecture can include many AWS log sources.

### AWS CloudTrail

Records supported AWS API activity.

```text
Who changed AWS resources?
```

### AWS Config

Records resource configuration history.

```text
What changed?
```

### CloudWatch Logs

Stores system, application, and service logs.

```text
What happened inside the system?
```

### VPC Flow Logs

Record network traffic metadata.

```text
Which network communication occurred?
```

### Application Logs

Record application behavior.

```text
Did authentication fail?

Did an application error occur?
```

---

## 8. Organization CloudTrail

AWS Organizations can use an organization trail.

Conceptually:

```text
AWS Organization
│
├── Account A
├── Account B
├── Account C
└── Account D
        |
        v
Organization Trail
        |
        v
Central S3 Bucket
```

An organization trail can record supported events from accounts in the organization.

This helps create consistent audit coverage.

---

## 9. Organization Trail Benefits

Without an organization trail:

```text
Account A
→ Trail A

Account B
→ Trail B

Account C
→ Trail C
```

Configuration may become inconsistent.

With an organization trail:

```text
Organization
      |
      v
Organization Trail
      |
      v
Central Logging
```

Benefits include:

```text
Consistent Logging

Central Administration

Multi-Account Visibility

Reduced Configuration Drift
```

---

## 10. Multi-Region CloudTrail Logging

Security-relevant resources may exist in different AWS Regions.

Example:

```text
Tokyo
Singapore
Virginia
Frankfurt
```

If logging only covers one Region:

```text
Tokyo
→ Logged

Singapore
→ Not Included
```

This creates a visibility gap.

A security-focused organization trail should consider the required Region coverage.

Conceptually:

```text
Region A ──┐
Region B ──┼──> Organization Trail
Region C ──┘
               |
               v
          Central S3
```

---

## 11. Central S3 Log Storage

Amazon S3 is commonly used as a centralized archive for AWS logs.

Conceptually:

```text
CloudTrail ──────┐
VPC Flow Logs ───┤
AWS Config ──────┼──> Central S3 Bucket
WAF Logs ────────┤
Other Logs ──────┘
```

Amazon S3 is suitable for:

```text
Long-Term Storage

Audit

Compliance

Forensics

Lifecycle Management
```

---

## 12. Protecting the Logging Bucket

A centralized logging bucket contains security-sensitive information.

Important protections include:

```text
Block Public Access

Least-Privilege Bucket Policy

Encryption

Versioning

Object Lock where required

Lifecycle Policies

Restricted Delete Permissions
```

Conceptually:

```text
Central Logging Bucket
        |
        +-- No Public Access
        |
        +-- Encryption
        |
        +-- Restricted Administrators
        |
        +-- Retention Controls
```

Logs should be treated as sensitive security evidence.

---

## 13. Encryption

Centralized logs may contain:

```text
Usernames

Source IP Addresses

Resource Names

API Parameters

Application Events
```

Therefore, encryption should be considered.

Conceptually:

```text
Logs
 ↓
Amazon S3
 ↓
Encryption
 ↓
Protected Log Objects
```

Depending on requirements, organizations may use:

```text
SSE-S3

or

SSE-KMS
```

When using SSE-KMS, appropriate KMS key policies and IAM permissions are required.

---

## 14. S3 Versioning

S3 Versioning can help protect logs against accidental modification or deletion.

Conceptually:

```text
Log Object
│
├── Version 1
├── Version 2
└── Delete Marker
```

Versioning can improve recovery options.

However:

```text
Versioning
≠
Complete Immutability
```

Additional retention controls may be required.

---

## 15. S3 Object Lock

S3 Object Lock can provide write-once-read-many style protection for supported use cases.

Conceptually:

```text
Log Object
     |
     v
Object Lock
     |
     v
Modification / Deletion Restricted
```

This can help organizations meet requirements for immutable audit logs.

Possible use cases include:

```text
Regulatory Compliance

Audit Evidence

Forensic Logs
```

Object Lock configuration should be carefully designed according to retention requirements.

---

## 16. Lifecycle Policies

Not all logs need to remain in high-cost storage indefinitely.

Example lifecycle:

```text
0–30 Days
→ S3 Standard

30–90 Days
→ Lower-Cost Storage

90+ Days
→ Archive Storage

Retention End
→ Expiration
```

The exact lifecycle depends on:

```text
Incident Response Requirements

Compliance

Legal Requirements

Storage Costs
```

Logs should not be deleted before required investigation or retention periods expire.

---

## 17. Centralizing CloudWatch Logs

CloudWatch Logs can also be centralized across accounts.

Conceptually:

```text
Account A CloudWatch Logs ──┐
Account B CloudWatch Logs ──┼──> Central Monitoring Account
Account C CloudWatch Logs ──┘
```

Modern AWS Organizations environments can define centralized logging rules that replicate selected CloudWatch Logs data from source accounts and Regions into a destination account.

This provides centralized:

```text
Monitoring

Log Search

Metric Filters

Security Analysis
```

---

## 18. CloudWatch Logs Centralization

A centralized log rule defines:

```text
Source Accounts

Source Regions

Selected Log Groups

Destination Account

Destination Region
```

Conceptually:

```text
Source Account
      |
      v
CloudWatch Log Group
      |
      v
Centralization Rule
      |
      v
Destination Account
      |
      v
Centralized Log Group
```

This can simplify centralized monitoring across an AWS Organization.

---

## 19. Source and Destination Accounts

### Source Account

The account where logs originate.

Example:

```text
Production Account
```

### Destination Account

The account that stores centralized copies.

Example:

```text
Monitoring Account
```

Conceptually:

```text
Production
    |
    v
CloudWatch Logs
    |
    v
Monitoring Account
```

Both accounts must meet the required organization and permission requirements for centralized log collection.

---

## 20. Cross-Region Centralization

Logs may also originate from different Regions.

Example:

```text
Tokyo
Singapore
Virginia
```

CloudWatch Logs centralization can copy supported new log data into a central Region.

Conceptually:

```text
Tokyo Logs ───────┐
Singapore Logs ───┼──> Central Region
Virginia Logs ────┘
```

A backup destination Region may also be configured for additional resilience.

---

## 21. Historical Log Limitation

An important point with CloudWatch Logs centralization:

```text
Centralization Rule Created
            |
            v
New Log Events
            |
            v
Central Destination
```

Logs that existed before the rule was created are not automatically centralized by this feature.

Therefore:

```text
Centralization
→ Forward-Looking Collection
```

should be planned early.

---

## 22. Subscription Filters

CloudWatch Logs subscription filters provide another mechanism for streaming log events.

Conceptually:

```text
CloudWatch Log Group
        |
        v
Subscription Filter
        |
        v
Destination
```

Possible destinations can include supported streaming and processing services.

This enables near-real-time log processing.

Example:

```text
Application Logs
       |
       v
Subscription Filter
       |
       v
Central Security Pipeline
```

---

## 23. Log Streaming vs Archiving

These are different requirements.

### Archiving

```text
Logs
 ↓
Amazon S3
 ↓
Long-Term Storage
```

Purpose:

```text
Audit

Compliance

Forensics
```

### Streaming

```text
Logs
 ↓
CloudWatch / Subscription
 ↓
Analysis Pipeline
```

Purpose:

```text
Real-Time Monitoring

Detection

Alerting
```

A mature security architecture may need both.

---

## 24. VPC Flow Logs

VPC Flow Logs provide network traffic metadata.

They can be enabled for supported:

```text
VPCs

Subnets

Network Interfaces
```

Example:

```text
Source IP

Destination IP

Source Port

Destination Port

Protocol

ACCEPT / REJECT
```

Centralized VPC Flow Logs help security teams investigate network behavior across multiple workloads.

---

## 25. Network Investigation Example

Scenario:

An EC2 instance communicates with an unexpected external IP.

Conceptually:

```text
EC2
 |
 v
Unexpected External Connection
 |
 v
VPC Flow Logs
 |
 v
Central Log Repository
 |
 v
Security Investigation
```

Questions:

```text
Which instance generated traffic?

Which destination IP was contacted?

Which port was used?

Was traffic accepted or rejected?

Did other accounts show similar behavior?
```

Centralized logs make cross-account analysis easier.

---

## 26. Application Logs

Cloud security monitoring is not limited to AWS service logs.

Applications may produce:

```text
Authentication Logs

Authorization Failures

Application Errors

Transaction Logs

Security Events
```

Example:

```text
Application
     |
     v
CloudWatch Agent
     |
     v
CloudWatch Logs
     |
     v
Central Monitoring
```

These logs can provide context that CloudTrail does not contain.

---

## 27. Database Logs

Database services may produce logs such as:

```text
Authentication Logs

Error Logs

Slow Query Logs

Audit Logs
```

Centralizing important database logs can help investigate:

```text
Unexpected Login Attempts

Privilege Abuse

Application Problems

Suspicious Queries
```

Database logging requirements depend on the database engine and workload.

---

## 28. Log Archive vs Monitoring Account

A mature architecture may separate log storage and log analysis.

Example:

```text
Security OU
│
├── Log Archive Account
│      |
│      +-- Long-Term Logs
│      +-- Protected S3 Storage
│
└── Security / Monitoring Account
       |
       +-- CloudWatch
       +-- Security Tools
       +-- Detection
       +-- Investigation
```

This supports separation of duties.

---

## 29. Why Separate Storage and Monitoring?

Suppose security analysts need to search logs but should not modify long-term archives.

Conceptually:

```text
Security Analyst
      |
      v
Monitoring Account
      |
      v
Read / Analyze Logs
```

while:

```text
Log Archive Account
      |
      v
Restricted Immutable Storage
```

This reduces the number of users with direct access to archived evidence.

---

## 30. Logging Account Access Control

Access to centralized logs should follow least privilege.

Example roles:

```text
LogWriter
→ Services write logs

SecurityAnalyst
→ Read and query logs

LogAdministrator
→ Manage storage configuration

Auditor
→ Read-only access
```

Avoid:

```text
Everyone
→ Full S3 Access
```

Central logs often contain sensitive information.

---

## 31. Protect Against Log Deletion

Attackers may attempt to remove evidence after compromising an environment.

Potential attack:

```text
Compromise
   |
   v
Malicious Activity
   |
   v
Delete Logs
```

Security controls should make this difficult.

Possible controls include:

```text
Separate Log Account

Restricted Delete Permissions

S3 Versioning

Object Lock

SCPs

Monitoring Log Configuration Changes
```

This supports forensic readiness.

---

## 32. Monitor Logging Configuration

Logging infrastructure itself should be monitored.

Important changes may include:

```text
CloudTrail Disabled

Trail Deleted

Logging Stopped

S3 Logging Policy Modified

Log Bucket Deleted

Config Recorder Stopped
```

Conceptually:

```text
Logging Control Changed
       |
       v
CloudTrail Event
       |
       v
Detection
       |
       v
Security Alert
```

Logging controls should not silently disappear.

---

## 33. Logging Pipeline Failure

A centralized logging system may fail because of:

```text
Permission Errors

KMS Key Problems

Incorrect Bucket Policy

Centralization Rule Errors

Service Quotas

Network / Service Configuration
```

Security teams should monitor whether logs are actually arriving.

Conceptually:

```text
Expected Logs
      |
      v
Central Repository
      |
      X
No Logs Arriving
      |
      v
Alert / Investigation
```

Logging availability is itself a security requirement.

---

## 34. Data Residency

Centralizing logs across Regions can create data residency considerations.

Example:

```text
Region A Logs
      |
      v
Central Region B
```

Logs may contain:

```text
IP Addresses

User Identifiers

Resource Names

Application Data
```

Organizations should consider:

```text
Regulatory Requirements

Privacy Requirements

Regional Data Policies
```

before transferring logs between Regions.

---

## 35. Cost Considerations

Centralized logging can create costs through:

```text
Log Ingestion

Log Storage

Cross-Region Transfer

CloudWatch Queries

KMS Requests

S3 Storage

Archive Retrieval
```

Security logging should not simply collect everything forever.

Instead:

```text
Identify Important Logs

Define Retention

Archive Older Logs

Filter Noise

Monitor Cost
```

Security and cost requirements should be balanced.

---

## 36. Centralized Logging Security Model

A useful architecture is:

```text
Workload Accounts
       |
       +-- CloudTrail
       +-- CloudWatch Logs
       +-- VPC Flow Logs
       +-- Application Logs
       +-- Database Logs
       |
       v
Centralized Logging
       |
       +----------------------+
       |                      |
       v                      v
Log Archive Account      Monitoring Account
       |                      |
       v                      v
Amazon S3              CloudWatch / Analysis
       |
       v
Long-Term Retention
```

---

## 37. Detection Pipeline Example

Example monitoring pipeline:

```text
IAM Policy Changed
        |
        v
CloudTrail
        |
        v
Centralized Logs
        |
        v
Detection Rule
        |
        v
Alert
        |
        v
Security Analyst
        |
        v
Investigation
```

This creates the basic security operations cycle:

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
```

---

## 38. Incident Investigation Example

Scenario:

An administrator discovers that:

```text
TCP 22
0.0.0.0/0
```

was added to a production Security Group.

### CloudTrail

Determine:

```text
Who changed it?

Which API was used?

When was it changed?

Where did the request originate?
```

### AWS Config

Determine:

```text
What was the previous configuration?

When did the configuration change?

Is the resource noncompliant?
```

### VPC Flow Logs

Determine:

```text
Did external systems connect to the affected instance?
```

### Application / OS Logs

Determine:

```text
Was a login successful?

Was suspicious activity performed?
```

Centralization allows these logs to be correlated more easily.

---

## 39. Example Multi-Account Architecture

```text
                         AWS Organization
                                |
         +----------------------+----------------------+
         |                      |                      |
         v                      v                      v
   Production Account     Development Account    Shared Account
         |                      |                      |
         | CloudTrail           | CloudTrail           | CloudTrail
         | CloudWatch           | CloudWatch           | CloudWatch
         | Flow Logs            | Flow Logs            | Flow Logs
         |                      |                      |
         +----------------------+----------------------+
                                |
                                v
                        Security OU
                                |
                    +-----------+-----------+
                    |                       |
                    v                       v
             Log Archive Account     Monitoring Account
                    |                       |
                    v                       v
               Amazon S3            Centralized Logs
                    |                       |
                    v                       v
             Long-Term Archive      Analysis / Alerting
```

---

## 40. Security Review Questions

When designing centralized logging, ask:

```text
Which logs must be collected?

Which accounts must be included?

Which Regions must be included?

Where will logs be stored?

How long must logs be retained?

Who can read the logs?

Who can delete the logs?

Can workload administrators alter archived logs?

Are logs encrypted?

Are logs protected from public access?

Are critical logs immutable?

How are logs queried?

How are alerts generated?

How do we know if logging stops?

Are cross-Region data transfers allowed?
```

---

## 41. Hands-on Practice

### Practice A — Identify Log Sources

Review your AWS environment and identify available log sources.

Example:

```text
CloudTrail

CloudWatch Logs

VPC Flow Logs

AWS Config

RDS Logs
```

Create a simple table:

```text
Log Source:
Purpose:
Current Destination:
Retention:
Security Value:
```

---

## 42. Practice — CloudTrail Destination

Review:

```text
CloudTrail
    |
    v
Trails
```

Identify:

```text
Trail Name

Organization Trail?

Multi-Region?

S3 Destination

Log File Validation

CloudWatch Logs Integration
```

Ask:

```text
Would this architecture still preserve logs if a workload account were compromised?
```

---

## 43. Practice — CloudWatch Logs

Review:

```text
CloudWatch
   |
   v
Log Groups
```

For one log group, identify:

```text
Source

Retention

Encryption

Log Streams
```

Then consider:

```text
Should this log be centralized?

How long should it be retained?

Who should be allowed to read it?
```

---

## 44. Practice — Design a Log Archive

Create a conceptual architecture without deploying resources.

Requirements:

```text
Three AWS Accounts

Two AWS Regions

CloudTrail

CloudWatch Logs

VPC Flow Logs

Central S3 Archive
```

Example:

```text
Account A ──┐
Account B ──┼──> Log Archive Account
Account C ──┘
                  |
                  v
              Amazon S3
```

Define:

```text
Encryption

Retention

Access Control

Versioning

Object Lock

Lifecycle
```

---

## 45. Optional Architecture Exercise

Design security roles for the centralized environment.

### Application Administrator

```text
Can:
Manage Application Resources

Cannot:
Delete Central Logs
```

### Security Analyst

```text
Can:
Read and Analyze Logs

Cannot:
Modify Workload Resources
```

### Log Administrator

```text
Can:
Manage Logging Infrastructure

Limited:
Direct Workload Access
```

### Auditor

```text
Can:
Read Archived Logs

Cannot:
Modify Logs
```

This demonstrates separation of duties.

---

## 46. Centralized Logging Checklist

```text
[ ] Required AWS accounts are included

[ ] Required AWS Regions are included

[ ] CloudTrail is centralized

[ ] CloudWatch Logs are centralized where required

[ ] VPC Flow Logs are collected where required

[ ] Application logs are collected

[ ] Database logs are collected where required

[ ] Long-term logs are stored in a dedicated account

[ ] S3 Block Public Access is enabled

[ ] Logs are encrypted

[ ] Log access follows least privilege

[ ] Delete permissions are tightly restricted

[ ] Versioning is enabled where appropriate

[ ] Object Lock is considered for immutable logs

[ ] Lifecycle policies match retention requirements

[ ] Logging failures are monitored

[ ] Logging configuration changes generate alerts

[ ] Log storage and monitoring responsibilities are separated

[ ] Data residency requirements are considered

[ ] Logging costs are monitored
```

---

## Key Takeaways

- Centralized logging collects security and operational logs from multiple systems into a common location.
- A dedicated Log Archive account can protect logs independently from workload accounts.
- Separation of duties reduces the risk that workload administrators can modify or delete audit evidence.
- Organization Trails provide centralized CloudTrail logging across AWS Organizations.
- Multi-Region logging reduces regional visibility gaps.
- Amazon S3 is commonly used for long-term centralized log storage.
- Central logging buckets should use strong access controls, encryption, and retention policies.
- S3 Versioning and Object Lock can improve protection against log modification or deletion.
- CloudWatch Logs can be centralized across accounts and Regions.
- CloudWatch log centralization processes new log data after the centralization rule is created.
- Subscription filters can stream log data for near-real-time analysis.
- Log archiving and real-time monitoring are different requirements.
- Logging infrastructure itself must be monitored.
- Centralized logging improves security investigations by allowing multiple log sources to be correlated.
- A mature architecture may separate log archival from security monitoring and analysis.

---

## Reflection

Today I learned that centralized logging is an important part of cloud security architecture, especially in multi-account AWS environments.

Instead of keeping logs inside each workload account, organizations can send security-related logs to dedicated logging and monitoring accounts.

This improves visibility, supports separation of duties, and makes it harder for someone who compromises a workload account to destroy audit evidence.

I also learned that long-term log storage and real-time monitoring are different requirements. Amazon S3 is useful for durable archival, while CloudWatch Logs and other monitoring services can support analysis and detection.

The most important lesson is that logs should be treated as security evidence. They must be collected, protected, retained, monitored, and made available to authorized investigators.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Centralized Logging | Collecting logs from multiple systems into a central location |
| Data Residency | Requirements concerning where data is physically or logically stored |
| Forensic Readiness | Preparing systems and logs so security incidents can be effectively investigated |
| Immutability | Protection that prevents data from being changed or deleted |
| Log Archive | A dedicated location used for long-term log retention |
| Log Correlation | Combining events from multiple log sources to understand an incident |
| Log Retention | The period during which log data is preserved |
| Organization Trail | A CloudTrail trail that records supported activity across AWS Organization accounts |
| Separation of Duties | Dividing responsibilities among different roles or teams |
| Subscription Filter | A CloudWatch Logs mechanism for streaming matching log events |
