# Day 21 — Amazon CloudWatch

## Topic

Amazon CloudWatch Fundamentals, Metrics, Logs, Alarms, and Security Monitoring

---

## Objectives

- Understand the purpose of Amazon CloudWatch.
- Understand CloudWatch Metrics and namespaces.
- Learn how CloudWatch collects resource metrics.
- Understand basic and detailed monitoring.
- Learn how CloudWatch Logs organizes log data.
- Understand Log Groups and Log Streams.
- Learn how CloudWatch Alarms work.
- Understand CloudWatch Logs Insights.
- Learn how Metric Filters convert logs into metrics.
- Understand CloudTrail and CloudWatch integration.
- Practice basic monitoring and security log analysis.

---

## 1. What Is Amazon CloudWatch?

Amazon CloudWatch is a monitoring and observability service for AWS resources and applications.

CloudWatch helps administrators and security engineers monitor:

- Resource performance
- Application availability
- System health
- Operational logs
- Security-related events
- Abnormal resource behavior

Conceptually:

```text
AWS Resources / Applications
             |
             v
       Amazon CloudWatch
             |
      +------+------+
      |             |
      v             v
    Metrics        Logs
      |             |
      v             v
    Alarms      Logs Insights
      |
      v
 Notifications / Actions
```

CloudWatch provides information that can help identify operational problems and support security investigations.

However, CloudWatch does not automatically detect every security incident.

The effectiveness of monitoring depends on the selected metrics, collected logs, configured alarms, and investigation processes.

---

## 2. CloudWatch and CloudTrail

CloudWatch and CloudTrail serve different purposes.

### AWS CloudTrail

CloudTrail records supported AWS API activity.

Examples:

```text
CreateUser

AttachRolePolicy

AuthorizeSecurityGroupIngress

TerminateInstances
```

CloudTrail helps answer:

```text
Who performed an AWS API action?
```

### Amazon CloudWatch

CloudWatch collects and analyzes metrics and logs.

Examples:

```text
CPU Utilization

Memory Usage

Application Errors

Database Connections
```

CloudWatch helps answer:

```text
What is happening to the resource or application?
```

### Integration

```text
AWS API Activity
       |
       v
AWS CloudTrail
       |
       v
CloudWatch Logs
       |
       v
Metric Filter / Log Analysis
       |
       v
CloudWatch Alarm
       |
       v
Notification
```

CloudTrail event logging and CloudWatch monitoring can work together to support security operations.

---

## 3. CloudWatch Metrics

A metric is a time-ordered set of numerical data points.

Examples include:

```text
CPUUtilization

NetworkIn

NetworkOut

DatabaseConnections

HTTPCode_Target_5XX_Count
```

Each metric represents a measurable characteristic of a resource or application.

Conceptually:

```text
EC2 Instance
     |
     v
CPUUtilization
     |
     v
CloudWatch Metric
     |
     v
Graph / Alarm
```

Metrics help identify:

- Resource exhaustion
- Performance degradation
- Unexpected activity
- Availability problems
- Changes in workload behavior

---

## 4. Namespaces and Dimensions

CloudWatch organizes metrics using namespaces.

A namespace is a container for related metrics.

Examples:

```text
AWS/EC2

AWS/RDS

AWS/S3

AWS/ApplicationELB

CWAgent
```

### Dimensions

Dimensions identify the resource or characteristics associated with a metric.

Example:

```text
Namespace:
AWS/EC2

Metric:
CPUUtilization

Dimension:
InstanceId = i-example
```

Conceptually:

```text
Namespace
    |
    v
Metric Name
    |
    v
Dimensions
    |
    v
Metric Data
```

Dimensions allow CloudWatch to distinguish metrics belonging to different resources.

---

## 5. Common EC2 Metrics

CloudWatch collects several standard EC2 metrics.

Examples include:

| Metric | Purpose |
|---|---|
| CPUUtilization | Measures instance CPU utilization |
| NetworkIn | Measures incoming network traffic |
| NetworkOut | Measures outgoing network traffic |
| DiskReadBytes | Measures bytes read through supported instance storage metrics |
| DiskWriteBytes | Measures bytes written through supported instance storage metrics |
| StatusCheckFailed | Indicates EC2 status check failures |

These metrics help administrators monitor EC2 performance and availability.

### Example

```text
EC2 Instance
     |
     v
CPUUtilization
     |
     v
Unexpected Increase
     |
     v
Investigation
```

An unexpected increase in CPU utilization may result from:

- Normal application workload
- Batch processing
- Application malfunction
- Unexpected processes
- Potentially malicious activity

A high CPU value alone does not confirm a security incident.

---

## 6. Basic vs Detailed Monitoring

Amazon EC2 supports basic and detailed monitoring.

### Basic Monitoring

Standard EC2 metrics are generally available at five-minute intervals.

### Detailed Monitoring

Detailed monitoring provides supported EC2 metrics at one-minute intervals.

Conceptually:

```text
Basic Monitoring
→ 5-minute metric granularity

Detailed Monitoring
→ 1-minute metric granularity
```

Detailed monitoring can help detect changes more quickly.

However, detailed monitoring may incur additional charges.

The appropriate monitoring level depends on:

- Workload criticality
- Availability requirements
- Monitoring requirements
- Cost considerations

---

## 7. CloudWatch Agent

Default EC2 metrics do not provide every operating system metric.

For example, standard EC2 metrics generally do not include guest operating system memory utilization or file system usage.

The CloudWatch Agent can collect additional metrics and logs.

Examples include:

```text
Memory Usage

Disk Usage

System Logs

Application Logs
```

Conceptually:

```text
EC2 Operating System
          |
          v
     CloudWatch Agent
          |
          v
     CloudWatch Metrics
     CloudWatch Logs
```

The agent requires appropriate configuration and permissions.

---

## 8. Custom Metrics

CloudWatch supports custom metrics published by applications or monitoring agents.

Example:

```text
Application
     |
     v
FailedLoginCount
     |
     v
CloudWatch Custom Metric
```

Other examples include:

```text
ActiveUsers

QueueLength

ApplicationErrorCount

TransactionFailures
```

Custom metrics allow organizations to monitor application-specific conditions that are not available through default AWS metrics.

Custom metric usage may incur additional charges.

---

## 9. CloudWatch Logs

CloudWatch Logs collects, stores, and provides access to log data.

Log sources can include:

- EC2 operating systems
- Applications
- AWS Lambda
- AWS CloudTrail
- Amazon RDS
- VPC Flow Logs
- Other supported AWS services

Conceptually:

```text
Application / AWS Service
           |
           v
      CloudWatch Logs
           |
           v
        Log Group
           |
           v
        Log Stream
           |
           v
        Log Events
```

CloudWatch Logs helps with troubleshooting, operational monitoring, and security investigations.

---

## 10. Log Groups

A Log Group organizes related log streams.

Examples:

```text
/aws/lambda/example-function

/application/security

/ec2/system

/cloudtrail/management
```

A Log Group can have settings such as:

- Retention period
- Access permissions
- Encryption configuration
- Log class

Example:

```text
Log Group:
application-security
```

This Log Group may contain logs from several application instances.

---

## 11. Log Streams

A Log Stream is a sequence of log events associated with a particular source.

Example:

```text
Log Group:
application-security
       |
       +-- instance-a
       |
       +-- instance-b
       |
       +-- instance-c
```

Each stream contains timestamped log events.

Conceptually:

```text
Log Group
    |
    v
Log Stream
    |
    v
Timestamped Events
```

Log Streams help organize logs from different instances, applications, or processes.

---

## 12. Log Events

A log event contains a timestamp and a message.

Example:

```text
2026-09-01T10:00:00Z
INFO Application started

2026-09-01T10:01:00Z
WARN Authentication failed

2026-09-01T10:02:00Z
ERROR Database connection failed
```

Security engineers can examine log events to understand system behavior.

Important information may include:

```text
Timestamp

Source

Event Type

User

IP Address

Error Message
```

The available fields depend on the logging source.

---

## 13. Log Retention

CloudWatch Logs allows retention periods to be configured for Log Groups.

A retention policy determines how long log events are stored.

Conceptually:

```text
Log Events
     |
     v
Retention Period
     |
     v
Automatic Expiration
```

Retention should reflect:

- Security investigation requirements
- Compliance requirements
- Operational requirements
- Storage costs

Important:

CloudWatch Logs does not automatically provide the same retention configuration for every Log Group.

Retention settings should be reviewed individually or managed through an organizational baseline.

---

## 14. CloudWatch Alarms

CloudWatch Alarms monitor metrics or supported metric expressions against configured conditions.

Conceptually:

```text
CloudWatch Metric
       |
       v
Alarm Evaluation
       |
       v
Threshold Breached
       |
       v
ALARM State
       |
       v
Notification / Action
```

Examples include:

```text
CPU Utilization > 80%

Available Storage < Defined Threshold

Application Error Count > Defined Threshold
```

A CloudWatch Alarm can perform supported actions when its state changes.

---

## 15. CloudWatch Alarm States

CloudWatch metric alarms have three main states.

### OK

The monitored metric is within the configured acceptable range according to the alarm evaluation.

### ALARM

The metric has breached the configured threshold according to the alarm evaluation.

### INSUFFICIENT_DATA

The alarm does not have sufficient data to determine whether the condition is met.

Conceptually:

```text
OK
→ Normal according to configured threshold

ALARM
→ Threshold condition met

INSUFFICIENT_DATA
→ Insufficient data for evaluation
```

An ALARM state does not automatically mean that a security incident has occurred.

The metric and operational context must be investigated.

---

## 16. Alarm Evaluation

An alarm can be configured using:

```text
Metric

Statistic

Period

Evaluation Periods

Datapoints to Alarm

Threshold
```

### Example

```text
Metric:
CPUUtilization

Statistic:
Average

Period:
5 minutes

Evaluation Periods:
3

Datapoints to Alarm:
3

Threshold:
80%
```

This configuration requires three breaching data points within the three evaluation periods.

Conceptually:

```text
Period 1: 85% → Breaching

Period 2: 88% → Breaching

Period 3: 90% → Breaching

Result:
ALARM
```

A configuration can also use an M-out-of-N evaluation.

For example:

```text
Datapoints to Alarm:
2

Evaluation Periods:
3
```

This requires at least two breaching data points within the three evaluated periods.

---

## 17. Missing Data Treatment

Metrics may occasionally stop reporting data.

Possible reasons include:

- Instance shutdown
- Monitoring configuration failure
- Network connectivity problems
- Intermittently reported metrics

CloudWatch allows alarms to define how missing data should be treated.

Common options include:

```text
Breaching

Not Breaching

Ignore

Missing
```

Example:

```text
Expected Metric:
Application Heartbeat

No Data Received
       |
       v
Missing Data Treatment
       |
       v
Alarm Evaluation
```

The correct configuration depends on the metric.

For a heartbeat metric, missing data may indicate a problem.

For an error-count metric that only publishes data when errors occur, missing data may be normal.

---

## 18. Amazon SNS Integration

Amazon Simple Notification Service (SNS) can deliver notifications triggered by CloudWatch Alarms.

Conceptually:

```text
CloudWatch Metric
       |
       v
CloudWatch Alarm
       |
       v
Amazon SNS Topic
       |
       v
Email / Other Supported Subscribers
```

Example:

```text
EC2 CPUUtilization > 80%
          |
          v
CloudWatch Alarm
          |
          v
SNS Notification
          |
          v
Administrator
```

A configured notification helps administrators respond to monitored conditions.

CloudWatch does not automatically send an email merely because an alarm exists.

The SNS topic, subscription, permissions, and alarm actions must be configured appropriately.

---

## 19. CloudWatch Logs Insights

CloudWatch Logs Insights is a tool for searching and analyzing log data.

It supports querying selected CloudWatch Log Groups.

Conceptually:

```text
CloudWatch Logs
       |
       v
Logs Insights Query
       |
       v
Filtered Results
       |
       v
Investigation
```

Logs Insights can help answer:

```text
How many authentication failures occurred?

Which source IP generated the most errors?

When did the application start failing?

Which API operations were denied?
```

Logs Insights provides different query languages. The following examples use CloudWatch Logs Insights QL.

---

## 20. Basic Logs Insights Query

Example:

```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```

This query:

1. Selects the timestamp and log message.
2. Sorts events by timestamp in descending order.
3. Returns up to 20 matching results.

Conceptually:

```text
Select Fields
      |
      v
Sort Results
      |
      v
Limit Output
```

---

## 21. Filter Log Messages

Example:

```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

This query searches for log messages containing:

```text
ERROR
```

It can help identify application failures.

For example:

```text
Database connection failed

Authentication service error

Application exception
```

The exact results depend on the log format and selected Log Groups.

---

## 22. Count Authentication Failures

Suppose an application generates log messages containing:

```text
Authentication failed
```

A simple query is:

```sql
fields @timestamp, @message
| filter @message like /Authentication failed/
| stats count(*) as FailedLogins by bin(5m)
| sort bin(5m) desc
```

This query groups matching log events into five-minute intervals.

It can help identify periods with unusually high authentication failure counts.

However, the meaning of authentication failures depends on the application and logging format.

A high count may result from:

- User mistakes
- Expired credentials
- Application configuration problems
- Automated login attempts
- Potential brute-force activity

Additional investigation is required before determining the cause.

---

## 23. CloudTrail Log Analysis

If CloudTrail events are delivered to CloudWatch Logs, Logs Insights can analyze the recorded API activity.

Example:

```sql
fields @timestamp, eventName, eventSource, sourceIPAddress
| filter eventName = "AuthorizeSecurityGroupIngress"
| sort @timestamp desc
| limit 20
```

This searches for Security Group ingress modification events.

Potential investigation questions:

```text
Who modified the Security Group?

When was the change made?

Where did the request originate?

Which Security Group was affected?
```

The available fields depend on the collected event structure.

---

## 24. Search for AccessDenied Events

CloudTrail logs may contain authorization failures.

Example:

```sql
fields @timestamp, eventName, eventSource, errorCode
| filter errorCode like /AccessDenied|UnauthorizedOperation/
| sort @timestamp desc
| limit 50
```

This can help identify API operations that failed because of authorization restrictions.

Possible causes include:

- Incorrect IAM permissions
- Expired or invalid session conditions
- Restrictive SCPs
- Permissions boundaries
- Unauthorized access attempts

An AccessDenied event does not automatically indicate an attack.

It should be investigated using the principal, action, resource, and surrounding activity.

---

## 25. Metric Filters

CloudWatch Logs Metric Filters can convert matching log events into numerical metrics.

Example:

```text
Application Log
       |
       v
Authentication Failed
       |
       v
Metric Filter
       |
       v
FailedLoginCount
```

A metric filter can count matching events.

That metric can then be used to create a CloudWatch Alarm.

Conceptually:

```text
Log Event
    |
    v
Metric Filter
    |
    v
CloudWatch Metric
    |
    v
CloudWatch Alarm
    |
    v
SNS Notification
```

Metric filters only process new matching log events after the filter is created.

They do not retroactively generate historical metric data from previously ingested logs.

---

## 26. Example — IAM Security Monitoring

Suppose an organization wants to monitor IAM policy changes.

Relevant CloudTrail API operations include:

```text
AttachRolePolicy

PutRolePolicy

CreatePolicyVersion

SetDefaultPolicyVersion
```

A simplified monitoring architecture is:

```text
IAM Policy Change
       |
       v
CloudTrail
       |
       v
CloudWatch Logs
       |
       v
Metric Filter
       |
       v
CloudWatch Alarm
       |
       v
Security Team Notification
```

The monitoring system can notify the security team when matching activity occurs.

The security team should determine whether the modification was expected and authorized.

---

## 27. Example — Root User Activity

The AWS root user has highly privileged access.

Root user activity should be monitored because routine administration should normally use appropriately authorized identities instead.

Conceptually:

```text
Root User API Activity
        |
        v
CloudTrail Event
        |
        v
CloudWatch Logs
        |
        v
Detection Rule
        |
        v
Security Alert
```

An alert should provide relevant investigation details, such as:

```text
Event Time

Event Name

Source IP

Account

Result
```

Root user activity is not automatically malicious.

However, unexpected root user activity should be investigated.

---

## 28. CloudWatch Dashboards

CloudWatch Dashboards allow multiple monitoring widgets to be displayed in one place.

Example:

```text
Security Dashboard
       |
       +-- EC2 CPU Utilization
       |
       +-- Application Errors
       |
       +-- RDS Connections
       |
       +-- Failed Login Metrics
       |
       +-- CloudWatch Alarm Status
```

Dashboards help security and operations teams review the health and behavior of workloads.

However, a dashboard is not a replacement for alerts.

A dashboard generally requires someone to view it, while properly configured alarms can trigger notifications or supported actions.

---

## 29. CloudWatch Security Considerations

CloudWatch logs may contain sensitive operational information.

Examples include:

```text
Usernames

Source IP Addresses

Application Errors

Internal Resource Names

Request Parameters
```

Applications should avoid logging:

- Passwords
- Access keys
- Authentication tokens
- Unnecessary personal information
- Other sensitive secrets

### Security Controls

```text
Least-Privilege IAM

Log Retention

Encryption

Access Monitoring

Sensitive Data Protection
```

Log access should be restricted to authorized users and applications.

Monitoring data itself should be treated as a security-sensitive resource.

---

## 30. Monitoring vs Threat Detection

Monitoring can identify unusual activity.

However:

```text
High CPU
≠
Confirmed Attack
```

Similarly:

```text
Multiple Failed Logins
≠
Confirmed Brute-Force Attack
```

Security investigation requires correlation with additional evidence.

Useful sources include:

```text
CloudWatch Logs

CloudTrail

VPC Flow Logs

Application Logs

Operating System Logs
```

CloudWatch helps collect and analyze relevant information, but final security conclusions require context.

---

## 31. CloudWatch Troubleshooting

If expected monitoring information is missing, check the following.

### Missing Metrics

```text
Is the resource running?

Is the correct Region selected?

Is the correct namespace selected?

Are the correct dimensions used?

Is the CloudWatch Agent configured where required?
```

### Missing Logs

```text
Is the logging source configured?

Does the Log Group exist?

Does the log producer have the required permissions?

Is the correct Region selected?

Is the log stream receiving events?
```

### Alarm Not Triggering

```text
Is the correct metric selected?

Is the threshold correct?

Are sufficient data points available?

Is the evaluation period appropriate?

How is missing data treated?

Is the alarm action configured?
```

### Notification Not Received

```text
Is the alarm in the expected state?

Is an SNS topic configured?

Is the subscription confirmed?

Are notification permissions correct?

Did the alarm transition into the relevant state?
```

---

## 32. Hands-on Practice

### Practice A — Explore CloudWatch Metrics

Open the AWS Management Console.

Navigate to:

```text
CloudWatch
    |
    v
Metrics
```

Select an available namespace, such as:

```text
AWS/EC2
```

Review an available metric:

```text
CPUUtilization
```

Identify:

```text
Namespace

Metric Name

Dimensions

Statistic

Period

Latest Data Points
```

If no EC2 instances exist, review another available AWS service metric.

### Practice B — Explore CloudWatch Logs

Navigate to:

```text
CloudWatch
    |
    v
Logs
    |
    v
Log Groups
```

Select an available Log Group.

Review:

```text
Log Group Name

Log Streams

Retention

Encryption Configuration

Recent Events
```

Do not publish real account IDs, sensitive log messages, or customer information in GitHub.

### Practice C — Review CloudWatch Alarms

Navigate to:

```text
CloudWatch
    |
    v
Alarms
```

Review an existing alarm or explore the alarm creation workflow.

Identify:

```text
Metric

Threshold

Period

Evaluation Periods

Datapoints to Alarm

Missing Data Treatment

Alarm Actions
```

Creating an alarm is optional.

### Practice D — Logs Insights

If a suitable Log Group is available, open Logs Insights.

Select a narrow time range and run:

```sql
fields @timestamp, @message
| sort @timestamp desc
| limit 20
```

Review the returned events.

If the Log Group contains application error messages, try:

```sql
fields @timestamp, @message
| filter @message like /ERROR/
| sort @timestamp desc
| limit 20
```

Record what the query returned without exposing sensitive log data.

---

## 33. Optional Monitoring Exercise

Design a monitoring workflow for an EC2 application.

Requirements:

```text
Monitor CPU Utilization

Collect Application Logs

Detect Repeated Application Errors

Notify the Administrator
```

Example architecture:

```text
EC2
 |
 +-- CPUUtilization
 |       |
 |       v
 |   CloudWatch Metric
 |       |
 |       v
 |   CloudWatch Alarm
 |
 +-- Application Logs
         |
         v
    CloudWatch Agent
         |
         v
    CloudWatch Logs
         |
         v
    Metric Filter
         |
         v
    ErrorCount Metric
         |
         v
    CloudWatch Alarm
         |
         v
      SNS Topic
         |
         v
    Administrator
```

Questions:

```text
Which metrics should be monitored?

What threshold is appropriate?

How should missing data be treated?

What log patterns should be detected?

Who should receive notifications?

What should happen after an alert?
```

Do not create unnecessary monitoring resources without considering AWS costs.

---

## 34. Security Checklist

When reviewing CloudWatch monitoring, ask:

```text
[ ] Are important AWS resources monitored?

[ ] Are critical application metrics collected?

[ ] Are operating system metrics collected where required?

[ ] Are security-relevant logs available?

[ ] Are Log Groups protected by least-privilege IAM?

[ ] Are log retention periods appropriate?

[ ] Are sensitive credentials excluded from logs?

[ ] Are important metrics configured with alarms?

[ ] Are alarm thresholds and evaluation periods appropriate?

[ ] Is missing data handled correctly?

[ ] Are alarm notifications configured?

[ ] Are SNS subscriptions confirmed?

[ ] Are CloudTrail events monitored where required?

[ ] Are Metric Filters configured for relevant security events?

[ ] Are Logs Insights queries available for investigations?

[ ] Are monitoring and notification configurations periodically reviewed?
```

---

## Key Takeaways

- Amazon CloudWatch provides monitoring and observability for AWS resources and applications.
- Metrics represent numerical measurements over time.
- Namespaces organize related metrics.
- Dimensions distinguish metrics associated with different resources.
- Default EC2 metrics do not include every operating system metric.
- CloudWatch Agent can collect additional metrics and logs.
- CloudWatch Logs organizes log data into Log Groups, Log Streams, and Log Events.
- CloudWatch Alarms evaluate metrics against configured conditions.
- Alarm states include OK, ALARM, and INSUFFICIENT_DATA.
- Alarm evaluation depends on thresholds, periods, and data point requirements.
- Missing data treatment should match the monitored workload.
- SNS can deliver notifications when configured alarm actions are triggered.
- Logs Insights provides log search and analysis capabilities.
- Metric Filters convert matching log events into CloudWatch metrics.
- CloudTrail and CloudWatch can be integrated to monitor security-related AWS API activity.
- Monitoring results require investigation and context before determining whether a security incident occurred.

---

## Reflection

Today I learned that Amazon CloudWatch provides visibility into the performance, availability, and behavior of AWS resources and applications.

The most important distinction is that CloudWatch Metrics provide numerical measurements, while CloudWatch Logs provide detailed event information.

I also learned that CloudWatch Alarms can help identify abnormal conditions by evaluating metrics against defined thresholds.

CloudWatch Logs Insights allows security engineers to investigate logs, while Metric Filters can convert selected log patterns into metrics for automated monitoring.

From a security engineering perspective, collecting metrics and logs is only the beginning. Effective monitoring also requires appropriate thresholds, log retention, access controls, notifications, and investigation procedures.

CloudWatch and CloudTrail complement each other by providing operational visibility and AWS API activity records.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Alarm | A monitoring resource that evaluates a metric against defined conditions |
| Dimension | An attribute used to identify a specific metric |
| Log Group | A container for related log streams |
| Logs Insights | A CloudWatch feature for searching and analyzing log data |
| Log Stream | A sequence of log events from a particular source |
| Metric | A numerical measurement collected over time |
| Metric Filter | A mechanism that converts matching log events into numerical metrics |
| Namespace | A container used to organize related CloudWatch metrics |
| Observability | The ability to understand a system's state through its outputs |
| Threshold | A value used to determine whether an alarm condition is met |
