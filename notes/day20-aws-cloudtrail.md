# Day 20 — AWS CloudTrail

## Topic

AWS CloudTrail Fundamentals, API Activity Logging, and Security Auditing

---

## Objectives

- Understand the purpose of AWS CloudTrail.
- Understand how AWS API activities are recorded.
- Learn the differences between CloudTrail event types.
- Understand Event History, Trails, and CloudTrail Lake.
- Learn how to interpret CloudTrail event records.
- Understand CloudTrail integration with S3 and CloudWatch Logs.
- Learn how to protect CloudTrail log files.
- Understand CloudTrail Insights and log file validation.
- Practice investigating security-related AWS API activity.

---

## 1. What Is AWS CloudTrail?

AWS CloudTrail is a service that records supported AWS account activity and API operations.

CloudTrail helps administrators and security engineers answer:

```text
Who performed the action?

What action was performed?

When did the action occur?

Where did the request originate?

Which AWS resource was affected?

Was the request successful?
```

CloudTrail records supported activity performed through:

- AWS Management Console
- AWS CLI
- AWS SDKs
- AWS APIs
- AWS services

### Basic Architecture

```text
User / IAM Role / AWS Service
             |
             v
         AWS API
             |
             v
        CloudTrail
             |
             v
        Event Record
             |
             +-- Identity
             +-- Action
             +-- Timestamp
             +-- Source IP
             +-- Resource
             +-- Result
```

CloudTrail provides an important audit trail for AWS security investigations.

---

## 2. Why Is CloudTrail Important?

CloudTrail provides visibility into security-relevant actions performed within AWS.

Examples include:

```text
IAM Policy Modified

Security Group Rule Added

EC2 Instance Terminated

S3 Bucket Policy Changed

KMS Key Disabled

RDS Instance Deleted
```

These activities may represent:

- Normal administrative operations
- Configuration changes
- Human error
- Unauthorized access
- Potential malicious activity

CloudTrail helps security teams investigate these activities and identify the responsible identities.

However, an API event alone does not necessarily indicate a security incident.

The event must be analyzed in context.

---

## 3. CloudTrail and the Shared Responsibility Model

AWS operates the underlying CloudTrail service.

Customers are responsible for configuring logging according to their security and retention requirements.

Customer responsibilities may include:

- Creating Trails or Event Data Stores.
- Selecting required event types.
- Configuring multi-Region logging.
- Protecting log storage.
- Configuring log retention.
- Restricting access to logs.
- Monitoring logging configuration.
- Investigating security events.

Conceptually:

```text
AWS
 |
 +-- Operates CloudTrail Infrastructure

Customer
 |
 +-- Configures Logging
 +-- Protects Audit Logs
 +-- Defines Retention
 +-- Configures Alerts
 +-- Investigates Events
```

---

## 4. CloudTrail Event Types

CloudTrail supports several event categories.

```text
CloudTrail
 |
 +-- Management Events
 |
 +-- Data Events
 |
 +-- Insights Events
 |
 +-- Network Activity Events
```

Each category provides different security information.

---

## 5. Management Events

Management events record supported operations performed on AWS resources and configurations.

They are also known as control plane operations.

Examples:

```text
CreateUser

AttachRolePolicy

RunInstances

AuthorizeSecurityGroupIngress

ModifyDBInstance

DeleteTrail
```

### Example

An administrator creates a new IAM user.

```text
Administrator
     |
     v
IAM CreateUser API
     |
     v
CloudTrail Management Event
```

The event can help identify:

- Who created the user.
- When the user was created.
- Which account was affected.
- Where the request originated.

Management events are particularly important for auditing infrastructure and permission changes.

---

## 6. Read and Write Management Events

Management events can be classified as read or write operations.

### Read Events

Read operations retrieve information without modifying resources.

Examples:

```text
DescribeInstances

ListBuckets

DescribeDBInstances
```

### Write Events

Write operations create, modify, or delete resources.

Examples:

```text
RunInstances

CreateUser

DeleteBucket

ModifyDBInstance
```

Write events are especially useful when investigating unexpected configuration changes.

However, read events can also be relevant during an investigation.

For example, unusual enumeration of AWS resources may indicate reconnaissance activity.

---

## 7. Data Events

Data events record supported operations performed on or within AWS resources.

They are also called data plane operations.

Examples include:

```text
S3 GetObject

S3 PutObject

S3 DeleteObject

Lambda Invoke
```

### Example — S3 Object Access

```text
Application
     |
     v
S3 GetObject
     |
     v
CloudTrail Data Event
```

A data event can help identify which identity accessed an object and when the operation occurred.

### Important

Data events are not included in the default 90-day Event History.

To record required data events, configure a Trail or CloudTrail Lake Event Data Store.

Data events may generate large volumes of logs and additional charges.

Select the required resources and event types based on security requirements.

---

## 8. Management Events vs Data Events

| Management Events | Data Events |
|---|---|
| Record supported control plane activity | Record supported data plane activity |
| IAM policy changes | S3 object reads |
| EC2 instance creation | S3 object uploads |
| RDS configuration changes | Lambda invocations |
| Available in Event History | Require additional logging configuration |
| Useful for configuration auditing | Useful for resource-level access auditing |

A useful mental model:

```text
Management Event
→ Who changed the resource configuration?

Data Event
→ Who performed an operation on resource data?
```

---

## 9. CloudTrail Insights

CloudTrail Insights helps identify unusual patterns in supported AWS API activity.

Examples include unusual changes in:

- API call rates
- API error rates

Conceptually:

```text
Normal API Activity
        |
        v
CloudTrail Insights
        |
        v
Unusual Activity Pattern
        |
        v
Insights Event
```

CloudTrail Insights can help identify unexpected operational or security-related behavior.

However:

```text
Unusual Activity
≠
Confirmed Security Incident
```

Anomalies require further investigation.

Insights must be enabled and configured for the relevant logging environment.

---

## 10. Network Activity Events

CloudTrail can also record supported network activity events associated with AWS API calls through VPC endpoints.

These events can help investigate API access attempts involving supported endpoint configurations.

Conceptually:

```text
Workload
    |
    v
VPC Endpoint
    |
    v
AWS Service API
    |
    v
CloudTrail Network Activity Event
```

Network activity events are different from VPC Flow Logs.

CloudTrail network activity events focus on supported API activity through VPC endpoints.

VPC Flow Logs provide network traffic metadata for VPCs, subnets, and network interfaces.

---

## 11. CloudTrail Event History

CloudTrail Event History is available automatically in an AWS account.

It provides access to recorded management events from the past 90 days.

Important characteristics:

- Available without creating a Trail.
- Displays management events.
- Limited to the past 90 days.
- Event searches are scoped to an AWS account and Region.
- Does not display Data Events.
- Does not replace long-term audit logging.

Conceptually:

```text
AWS Account
     |
     v
CloudTrail Event History
     |
     v
Recent Management Events
```

Event History is useful for reviewing recent AWS configuration and management activity.

---

## 12. What Is a CloudTrail Trail?

A Trail is a CloudTrail configuration that delivers selected event records to an Amazon S3 bucket.

Conceptually:

```text
AWS Account Activity
        |
        v
CloudTrail Trail
        |
        v
Amazon S3
        |
        v
Stored Audit Logs
```

A Trail can be configured to record:

- Management events
- Selected data events
- Insights events

A Trail can also deliver supported events to CloudWatch Logs for further monitoring.

Trails are useful when an organization requires ongoing audit records beyond the default Event History.

---

## 13. Single-Region vs Multi-Region Trail

### Single-Region Trail

Records selected activity within its configured Region.

Conceptually:

```text
Region A
    |
    v
CloudTrail
    |
    v
S3
```

### Multi-Region Trail

Records supported activity across enabled AWS Regions.

Conceptually:

```text
Region A ----+
             |
Region B ----+----> CloudTrail Trail
             |             |
Region C ----+             v
                         Amazon S3
```

Multi-Region Trails improve audit coverage when resources may be created or modified in different AWS Regions.

For security auditing, a multi-Region Trail is generally preferable when comprehensive regional coverage is required.

---

## 14. Organization Trail

AWS Organizations supports organization-level CloudTrail logging.

An organization Trail can collect selected events from the management account and member accounts.

Conceptually:

```text
AWS Organization
       |
       +-- Management Account
       |
       +-- Production Account
       |
       +-- Development Account
       |
       +-- Security Account
                  |
                  v
          Organization Trail
                  |
                  v
          Centralized S3 Bucket
```

Organization Trails can help security teams maintain centralized audit records across multiple AWS accounts.

Access to the centralized logs should be restricted to authorized identities.

---

## 15. CloudTrail Lake

CloudTrail Lake is a managed service for storing and querying supported event data.

It uses Event Data Stores to retain events for analysis.

Conceptually:

```text
AWS Events
     |
     v
CloudTrail Lake
     |
     v
Event Data Store
     |
     v
SQL Query
     |
     v
Investigation Results
```

CloudTrail Lake can support:

- Event searches
- Security investigations
- Audit analysis
- Queries across multiple attributes
- Long-term event retention

The selected event types, retention configuration, and query usage may affect cost.

---

## 16. Event History vs Trail vs CloudTrail Lake

| Feature | Main Purpose |
|---|---|
| Event History | Review recent management events |
| Trail | Deliver selected events to S3 for ongoing logging |
| CloudTrail Lake | Store and query supported events in managed Event Data Stores |

Example:

```text
Recent IAM Change
→ Event History

Long-Term Audit Records
→ Trail + S3

Advanced Event Investigation
→ CloudTrail Lake
```

These features can be used together depending on operational requirements.

---

## 17. CloudTrail Event Record

A CloudTrail event contains information about a recorded AWS operation.

Important fields include:

```text
eventTime

eventSource

eventName

awsRegion

sourceIPAddress

userIdentity

requestParameters

responseElements

errorCode

resources
```

Not every event contains every field.

The exact structure depends on the AWS service, event type, and API operation.

---

## 18. Example CloudTrail Event

The following is a simplified illustrative event.

```json
{
  "eventVersion": "1.11",
  "eventTime": "2026-09-01T10:00:00Z",
  "eventSource": "ec2.amazonaws.com",
  "eventName": "AuthorizeSecurityGroupIngress",
  "awsRegion": "ap-northeast-1",
  "sourceIPAddress": "203.0.113.10",
  "userIdentity": {
    "type": "AssumedRole",
    "arn": "arn:aws:sts::111122223333:assumed-role/SecurityAdmin/example-session"
  },
  "requestParameters": {
    "groupId": "sg-example"
  },
  "responseElements": {
    "return": true
  }
}
```

This example illustrates a Security Group ingress modification event.

It is not an actual event collected from an AWS account.

---

## 19. Important Event Fields

### eventTime

```text
When did the action occur?
```

CloudTrail event timestamps use UTC.

### eventSource

```text
Which AWS service received the request?
```

Examples:

```text
iam.amazonaws.com

ec2.amazonaws.com

s3.amazonaws.com
```

### eventName

```text
Which API operation was requested?
```

Examples:

```text
CreateUser

RunInstances

AuthorizeSecurityGroupIngress
```

### userIdentity

```text
Which identity made the request?
```

Examples:

```text
IAMUser

AssumedRole

Root

AWSService
```

### sourceIPAddress

```text
Where did the request originate?
```

The recorded value depends on the request context.

For example, some AWS service-originated requests may not contain a conventional client IP address.

### errorCode

```text
Did the request encounter an error?
```

An error field may help identify failed or unauthorized API operations.

A missing errorCode does not automatically prove that every intended downstream operation completed successfully.

---

## 20. Security Investigation Example — IAM Policy Change

Scenario:

An IAM role unexpectedly receives additional permissions.

Investigation:

```text
Unexpected IAM Permission
          |
          v
CloudTrail
          |
          v
Search Relevant IAM Events
          |
          v
Identify Principal
          |
          v
Review Timestamp and Source
          |
          v
Determine Whether Change Was Authorized
```

Relevant API operations may include:

```text
AttachRolePolicy

PutRolePolicy

CreatePolicyVersion

SetDefaultPolicyVersion
```

Questions:

```text
Who modified the permissions?

When did the change occur?

Which role or policy was affected?

Was the change part of an approved operation?

Were other IAM resources modified?
```

---

## 21. Security Investigation Example — Public Security Group

Scenario:

An EC2 Security Group unexpectedly allows SSH access from the Internet.

Configuration:

```text
TCP 22
Source: 0.0.0.0/0
```

Investigation:

```text
Public SSH Rule Detected
          |
          v
CloudTrail
          |
          v
AuthorizeSecurityGroupIngress
          |
          v
Review userIdentity
          |
          v
Review sourceIPAddress
          |
          v
Review requestParameters
```

The event may help identify the identity responsible for the change.

The security engineer should also determine whether the configuration was authorized and whether the affected instance was exposed.

---

## 22. Security Investigation Example — S3 Object Access

Scenario:

A sensitive S3 object may have been accessed unexpectedly.

Investigation:

```text
Sensitive S3 Object
        |
        v
CloudTrail Data Events
        |
        v
GetObject
        |
        v
Review Principal and Time
```

Important:

S3 object-level data events must have been configured before the activity occurred.

Enabling data-event logging after an incident does not retroactively create historical records of earlier object access.

---

## 23. CloudTrail and CloudWatch

CloudTrail and CloudWatch serve different purposes.

### CloudTrail

Records supported AWS API activity and account events.

Example:

```text
Who modified the Security Group?
```

### CloudWatch

Collects and monitors metrics and logs, and supports alarms and operational monitoring.

Example:

```text
Did CPU utilization exceed a threshold?
```

### Integration

```text
AWS API Activity
       |
       v
CloudTrail
       |
       v
CloudWatch Logs
       |
       v
Analysis / Monitoring
```

CloudTrail records can be delivered to CloudWatch Logs when the integration is configured.

---

## 24. EventBridge and Security Alerts

CloudTrail-related API activity can also be used with Amazon EventBridge to build security notifications and automated responses.

Example:

```text
IAM Configuration Change
          |
          v
EventBridge Rule
          |
          v
Notification / Security Workflow
```

Potential monitoring use cases include:

```text
Root User Activity

Unauthorized API Calls

Security Group Changes

CloudTrail Configuration Changes

KMS Key Changes
```

Important:

CloudTrail logging by itself does not guarantee immediate detection or alerting.

Appropriate event rules, log processing, permissions, and notification mechanisms must be configured.

---

## 25. Protecting CloudTrail Logs

CloudTrail log files contain security-relevant information.

A secure logging architecture should protect them against unauthorized access, modification, and deletion.

Recommended controls include:

- Restrict access to the logging bucket.
- Enable S3 Block Public Access.
- Apply least-privilege bucket policies.
- Use appropriate encryption.
- Define log retention requirements.
- Consider S3 Object Lock for immutable retention where required.
- Separate log administration from workload administration where practical.
- Monitor changes to logging configurations.

Conceptually:

```text
CloudTrail
     |
     v
Protected S3 Bucket
     |
     +-- Restricted Access
     +-- Encryption
     +-- Retention
     +-- Integrity Validation
```

Logs are evidence and should receive appropriate protection.

---

## 26. CloudTrail Log File Validation

CloudTrail supports log file integrity validation for Trails.

This feature can help determine whether delivered CloudTrail log files have been modified or deleted after delivery.

Conceptually:

```text
CloudTrail Log Files
        |
        v
Digest Files
        |
        v
Integrity Validation
        |
        v
Verification Result
```

Log file integrity validation provides a way to verify log authenticity and integrity.

It does not prevent an authorized or unauthorized actor from deleting log files.

Therefore, integrity validation should be combined with access controls and retention protections.

---

## 27. Common CloudTrail Misconfigurations

### No Long-Term Logging

```text
Event History Only
```

Problem:

Management events are only available in Event History for 90 days.

Mitigation:

Configure an appropriate Trail or Event Data Store for longer retention.

### Missing Data Events

```text
S3 Object Access
      |
      v
Data Events Not Configured
```

Problem:

Required object-level activity may not be available for investigation.

Mitigation:

Enable selected data events for sensitive resources.

### Incomplete Region Coverage

```text
Region A
→ Logged

Region B
→ Not Logged
```

Problem:

Activities in unmonitored Regions may not be captured by the intended Trail.

Mitigation:

Review multi-Region logging requirements.

### Excessive Log Access

```text
Logging Bucket
      |
      v
Broad Write / Delete Permissions
```

Problem:

An attacker with excessive permissions may attempt to modify or delete audit evidence.

Mitigation:

Apply least privilege and additional retention protections.

### Logging Without Monitoring

```text
CloudTrail Logs
      |
      v
No Alerts or Review
```

Problem:

Suspicious activity may remain unnoticed.

Mitigation:

Integrate logging with appropriate monitoring and incident response processes.

---

## 28. Hands-on Practice

### Practice A — Review Event History

Open the AWS Management Console.

Navigate to:

```text
CloudTrail
    |
    v
Event History
```

Review recent management events.

Identify:

```text
Event Name

Event Time

Event Source

AWS Region

Username / Identity

Source IP Address
```

Select an event and open its detailed JSON record.

### Practice B — Investigate an IAM Event

Use the Event History search function.

Search by Event Name:

```text
CreateUser
```

or:

```text
AttachRolePolicy
```

If no matching event exists, select another management event available in your account.

Review:

```text
Who performed the operation?

When was it performed?

Which resource was affected?

Was the operation successful?
```

### Practice C — Review a Security Group Event

Search for:

```text
AuthorizeSecurityGroupIngress
```

If a matching event exists, inspect:

```text
userIdentity

sourceIPAddress

requestParameters

eventTime
```

Identify the principal that requested the Security Group modification.

### Practice D — Review Trail Configuration

Navigate to:

```text
CloudTrail
    |
    v
Trails
```

If a Trail exists, review:

```text
Trail Name

Multi-Region Configuration

Management Events

Data Events

S3 Destination

CloudWatch Logs Integration

Log File Validation
```

Do not create additional paid logging resources unless needed for your learning environment.

---

## 29. Optional AWS CLI Practice

If AWS CLI is configured with authorized credentials, review recent management events.

### Check the Current Identity

```bash
aws sts get-caller-identity
```

### View Recent Events

```bash
aws cloudtrail lookup-events \
  --region ap-northeast-1 \
  --max-results 10
```

### Search for a Specific API Event

```bash
aws cloudtrail lookup-events \
  --region ap-northeast-1 \
  --lookup-attributes AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress \
  --max-results 10
```

### Extract Selected Event Fields

```bash
aws cloudtrail lookup-events \
  --region ap-northeast-1 \
  --max-results 10 \
  --query 'Events[].{Time:EventTime,Name:EventName,User:Username}' \
  --output table
```

The lookup-events command searches recorded management events within the applicable Event History retention period.

It does not provide a complete substitute for configured data-event logging or long-term audit storage.

Do not publish real account IDs, source IP addresses, access keys, or sensitive CloudTrail event records in a public GitHub repository.

---

## 30. Security Checklist

When reviewing CloudTrail, ask:

```text
[ ] Is a Trail or Event Data Store configured for required long-term logging?

[ ] Are the required AWS Regions covered?

[ ] Are management events being recorded?

[ ] Are sensitive data events enabled where required?

[ ] Is organization-level logging required?

[ ] Is the log destination protected?

[ ] Is S3 Block Public Access enabled for the logging bucket?

[ ] Are log access permissions restricted?

[ ] Is encryption configured appropriately?

[ ] Is the required log retention period defined?

[ ] Is log file integrity validation enabled where required?

[ ] Are logging configuration changes monitored?

[ ] Are important security events generating alerts?

[ ] Can investigators identify the principal responsible for an API action?

[ ] Are log access and investigation procedures documented?
```

---

## Key Takeaways

- AWS CloudTrail records supported AWS account activity and API operations.
- Event History provides recent management events for the past 90 days.
- Management events record supported control plane activity.
- Data events record supported data plane activity.
- Data events require additional logging configuration.
- Trails deliver selected event records to Amazon S3.
- CloudTrail Lake supports event storage and SQL-based analysis.
- Multi-Region Trails improve audit coverage across AWS Regions.
- Organization Trails support centralized multi-account logging.
- CloudTrail event records help identify identities, actions, timestamps, and affected resources.
- CloudTrail Insights can identify unusual API activity patterns.
- CloudTrail logs should be protected against unauthorized access and deletion.
- Log file integrity validation helps detect modification of delivered logs.
- CloudTrail must be integrated with monitoring and response processes to support effective security operations.

---

## Reflection

Today I learned that AWS CloudTrail is an important service for auditing AWS account activity and investigating security-related events.

The most important distinction is the difference between management events and data events. Management events provide visibility into supported AWS resource configuration changes, while data events provide visibility into supported operations performed on resource data.

I also learned that Event History is useful for recent investigations, but long-term audit requirements require a Trail or CloudTrail Lake Event Data Store.

From a security engineering perspective, collecting logs is only the first step. Logs must also be protected, retained, reviewed, and integrated with monitoring and incident response processes.

When investigating AWS activity, I should identify the principal, API action, timestamp, source, affected resource, and result before determining whether the activity was authorized.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Audit Trail | A record of activities used for auditing and investigation |
| CloudTrail Insights | A feature for identifying unusual API activity patterns |
| Data Event | A recorded operation performed on or within a supported resource |
| Event Data Store | A managed event storage resource used by CloudTrail Lake |
| Event History | CloudTrail's recent management event history |
| Log Integrity | Assurance that log data has not been improperly modified |
| Log Retention | The period during which logs are preserved |
| Management Event | A recorded AWS control plane operation |
| Principal | An identity that performs an AWS action |
| Trail | A configuration that delivers selected CloudTrail events to S3 |
