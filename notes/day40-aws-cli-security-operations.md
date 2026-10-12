# Day 40 — AWS CLI for Security Operations

## Topic

AWS CLI for Security Investigation, IAM Auditing, CloudTrail Analysis, Network Exposure, Data Security, and Security Findings

---

## Objectives

- Build a repeatable CLI-based security investigation workflow
- Verify account, role, profile, and Region before investigation
- Review IAM users, roles, and policies
- Generate and review IAM credential reports
- Investigate recent API activity with CloudTrail
- Identify potentially exposed Security Groups
- Review EC2 network exposure
- Review S3 public access controls
- Review S3 encryption configuration
- Review KMS keys and key states
- Review GuardDuty findings
- Review Amazon Inspector findings
- Review Security Hub findings
- Understand Security Hub GetFindings and GetFindingsV2
- Use JMESPath to summarize security information
- Understand pagination and multi-Region investigation
- Build a read-only-first security operations workflow

---

# Security Operations Workflow

## 1. Start With Context

Before investigating anything, verify:

```text
Who am I?

Which account?

Which role?

Which Region?

Which profile?
```

Run:

```bash
aws sts get-caller-identity
```

Then:

```bash
aws configure get region
```

If needed:

```bash
aws configure list
```

---

## 2. Why Context Comes First

In a multi-account environment:

```text
Security

Production

Development

Network
```

may all use different profiles.

Running a correct security command in the wrong account can still produce an incorrect investigation.

Therefore:

```text
Identity
   ↓
Account
   ↓
Region
   ↓
Investigation
```

---

# Investigation Preparation

## 3. Set a Profile

Example:

```bash
export AWS_PROFILE=security
```

Then verify:

```bash
aws sts get-caller-identity
```

Never assume the currently selected profile is correct.

---

## 4. Explicit Region

During investigation, explicitly specifying a Region can make commands easier to audit.

Example:

```bash
aws ec2 describe-instances \
  --region ap-northeast-1
```

For Regional security services, always consider whether the same investigation must be repeated in other Regions.

---

# IAM Security Review

## 5. List IAM Users

```bash
aws iam list-users
```

Readable view:

```bash
aws iam list-users \
  --query 'Users[].{
    User:UserName,
    Created:CreateDate
  }' \
  --output table
```

Questions:

```text
Are IAM users still required?

Are old users present?

Should workforce access use federation instead?
```

---

## 6. List IAM Roles

```bash
aws iam list-roles
```

Readable output:

```bash
aws iam list-roles \
  --query 'Roles[].{
    Role:RoleName,
    Created:CreateDate
  }' \
  --output table
```

Roles are especially important because modern AWS environments rely heavily on:

```text
EC2 Roles

Lambda Roles

Cross-Account Roles

Service Roles

Federated Roles
```

---

## 7. Review a Role

Example:

```bash
aws iam get-role \
  --role-name <role-name>
```

Review:

```text
AssumeRolePolicyDocument

Role ARN

MaxSessionDuration

Tags
```

The trust policy answers:

```text
Who can assume this role?
```

---

## 8. Review Attached Policies

For an IAM role:

```bash
aws iam list-attached-role-policies \
  --role-name <role-name>
```

Inline policies:

```bash
aws iam list-role-policies \
  --role-name <role-name>
```

For an IAM user:

```bash
aws iam list-attached-user-policies \
  --user-name <user-name>
```

---

# Credential Report

## 9. IAM Credential Report

AWS IAM can generate an account-wide credential report.

Generate:

```bash
aws iam generate-credential-report
```

Then retrieve:

```bash
aws iam get-credential-report
```

The report contains information about IAM credentials in the account.

---

## 10. Credential Report Use Cases

It can help identify:

```text
Password Enabled?

MFA Active?

Access Key Active?

Access Key Age?

Password Last Used?

Access Key Last Used?
```

This is useful for reviewing:

```text
Unused Credentials

Old Access Keys

Users Without MFA

Unexpected IAM Users
```

AWS stores a single credential report for the account, and generating a new report replaces the previous one. :chatgpt-content-reference{index="0"}

---

## 11. Decode Credential Report

The `Content` field is Base64-encoded.

A Linux example:

```bash
aws iam get-credential-report \
  --query Content \
  --output text |
base64 --decode
```

Save locally only if appropriate:

```bash
aws iam get-credential-report \
  --query Content \
  --output text |
base64 --decode > credential-report.csv
```

Do not upload a real credential report to GitHub.

---

## 12. Credential Report Review

Look for:

```text
MFA Active = false

Access Key Active = true

Old Access Key

Credential Not Used

Unexpected IAM User
```

Remember:

```text
Finding Something Unusual
≠
Confirmed Compromise
```

It requires investigation.

---

# IAM Security Questions

## 13. IAM Review Checklist

For each identity ask:

```text
Why does this identity exist?

Who owns it?

Does it need console access?

Does it need access keys?

Does it have MFA?

Does it have AdministratorAccess?

Can it AssumeRole into other accounts?

When was it last used?
```

---

# CloudTrail Investigation

## 14. CloudTrail Lookup Events

CloudTrail can search recent management events.

Example:

```bash
aws cloudtrail lookup-events \
  --max-items 10
```

CloudTrail `lookup-events` can retrieve management events from the last 90 days in the Region where the event occurred. :chatgpt-content-reference{index="1"}

---

## 15. Search by Event Name

Example:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=ConsoleLogin
```

Another example:

```bash
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=EventName,AttributeValue=AuthorizeSecurityGroupIngress
```

---

## 16. Search by User

```bash
aws cloudtrail lookup-events \
  --lookup-attributes \
    AttributeKey=Username,AttributeValue=<user-name>
```

This helps answer:

```text
What actions did this identity perform?
```

---

## 17. Recent Security Changes

Useful API names to search can include:

```text
CreateUser

CreateAccessKey

AttachUserPolicy

AttachRolePolicy

PutRolePolicy

AssumeRole

AuthorizeSecurityGroupIngress

PutBucketPolicy

DeleteTrail

StopLogging
```

Exact relevance depends on the incident.

---

## 18. CloudTrail Output

Readable example:

```bash
aws cloudtrail lookup-events \
  --max-items 20 \
  --query 'Events[].{
    Time:EventTime,
    User:Username,
    Event:EventName,
    Source:EventSource
  }' \
  --output table
```

---

## 19. Region Matters

CloudTrail lookup:

```text
Region A
```

does not automatically mean:

```text
Search Every Region
```

for ordinary regional event lookup.

If investigating organization-wide activity, consider all relevant Regions.

---

# Security Group Investigation

## 20. Review All Security Groups

```bash
aws ec2 describe-security-groups
```

Readable format:

```bash
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].{
    Group:GroupName,
    ID:GroupId,
    VPC:VpcId
  }' \
  --output table
```

---

## 21. Find IPv4 Internet Exposure

Potentially broad inbound access uses:

```text
0.0.0.0/0
```

Example:

```bash
aws ec2 describe-security-groups \
  --filters \
    Name=ip-permission.cidr,Values='0.0.0.0/0'
```

---

## 22. Find Public SSH Rules

Example:

```bash
aws ec2 describe-security-groups \
  --filters \
    Name=ip-permission.from-port,Values=22 \
    Name=ip-permission.to-port,Values=22 \
    Name=ip-permission.cidr,Values='0.0.0.0/0'
```

AWS CLI supports Security Group filters such as `ip-permission.cidr`, `ip-permission.from-port`, and `ip-permission.to-port`. :chatgpt-content-reference{index="2"}

---

## 23. Important Filter Caveat

Be careful.

When multiple Security Group filters are used:

```text
Port 22

and

0.0.0.0/0
```

the Security Group can match because **different rules inside the same Security Group** satisfy different filter conditions.

It does not necessarily mean one single rule is:

```text
TCP 22
0.0.0.0/0
```

AWS explicitly documents this behavior. :chatgpt-content-reference{index="3"}

Therefore:

```text
Server-Side Filter
      ↓
Candidate Security Groups
      ↓
Inspect Actual Rules
```

is safer.

---

## 24. Inspect Inbound Rules

Example:

```bash
aws ec2 describe-security-groups \
  --group-ids <security-group-id> \
  --query 'SecurityGroups[].IpPermissions'
```

Review:

```text
Protocol

FromPort

ToPort

CIDR

Referenced Security Group
```

---

## 25. IPv6 Exposure

Do not forget:

```text
::/0
```

Example filter:

```bash
aws ec2 describe-security-groups \
  --filters \
    Name=ip-permission.ipv6-cidr,Values='::/0'
```

A review that only checks `0.0.0.0/0` can miss IPv6 exposure.

---

# EC2 Exposure

## 26. Review Instances

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].{
    ID:InstanceId,
    State:State.Name,
    PublicIP:PublicIpAddress,
    PrivateIP:PrivateIpAddress,
    VPC:VpcId,
    Subnet:SubnetId
  }' \
  --output table
```

Questions:

```text
Does it have a public IP?

Which Security Groups?

Which subnet?

Which IAM role?

Is it production?
```

---

## 27. Security Context

A public IP alone does not necessarily mean:

```text
Exploitable
```

Risk depends on:

```text
Route Table

Internet Gateway

Security Group

NACL

Host Firewall

Running Service
```

Use CLI output as investigation context, not automatic proof of exposure.

---

# S3 Security Review

## 28. List Buckets

```bash
aws s3api list-buckets
```

Readable:

```bash
aws s3api list-buckets \
  --query 'Buckets[].Name' \
  --output table
```

Do not publish real bucket names.

---

## 29. Bucket Public Access Block

Check bucket-level Public Access Block:

```bash
aws s3api get-public-access-block \
  --bucket <bucket-name>
```

This returns the bucket-level configuration.

However, effective S3 Block Public Access also depends on account-level configuration, and organization-level policies can influence account settings. S3 uses the most restrictive combination of applicable settings. :chatgpt-content-reference{index="4"}

---

## 30. Account-Level Public Access Block

First get your account:

```bash
ACCOUNT_ID=$(aws sts get-caller-identity \
  --query Account \
  --output text)
```

Then:

```bash
aws s3control get-public-access-block \
  --account-id "$ACCOUNT_ID"
```

This helps compare:

```text
Bucket Level

Account Level

Organization-Level Governance
```

---

## 31. S3 Encryption

Check:

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name>
```

Modern Amazon S3 general-purpose buckets use default server-side encryption with SSE-S3 unless another supported default encryption configuration is selected. The command shows the bucket's default encryption configuration. :chatgpt-content-reference{index="5"}

Therefore:

```text
get-bucket-encryption succeeds
```

does not automatically mean:

```text
SSE-KMS
```

Check the algorithm.

---

## 32. SSE-S3 vs SSE-KMS

Possible values include:

```text
AES256
→ SSE-S3

aws:kms
→ SSE-KMS
```

Example query:

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name> \
  --query 'ServerSideEncryptionConfiguration.Rules[].ApplyServerSideEncryptionByDefault'
```

---

## 33. Bucket Policy

Review:

```bash
aws s3api get-bucket-policy \
  --bucket <bucket-name>
```

Security questions:

```text
Is Principal too broad?

Is cross-account access expected?

Is TLS required?

Are explicit Deny conditions present?
```

---

# KMS Security Review

## 34. List KMS Keys

```bash
aws kms list-keys
```

KMS is Regional, so check the correct Region.

---

## 35. Describe a Key

```bash
aws kms describe-key \
  --key-id <key-id>
```

Useful information includes:

```text
Key ARN

Key State

Key Manager

Key Spec

Key Usage

Creation Date

Multi-Region Status
```

`DescribeKey` returns metadata such as the key state, origin, key specification, usage, and supported algorithms. :chatgpt-content-reference{index="6"}

---

## 36. List Aliases

```bash
aws kms list-aliases
```

Aliases help humans understand key purpose.

Example:

```text
alias/prod-rds

alias/security-logs
```

---

## 37. Review Key Policy

```bash
aws kms get-key-policy \
  --key-id <key-id> \
  --policy-name default
```

Questions:

```text
Who administers the key?

Who can encrypt?

Who can decrypt?

Is cross-account access allowed?

Are permissions broader than necessary?
```

---

## 38. Check Key Rotation

For applicable symmetric customer-managed keys:

```bash
aws kms get-key-rotation-status \
  --key-id <key-id>
```

Do not assume rotation is appropriate or supported for every key type.

---

# GuardDuty Operations

## 39. Find Detector

GuardDuty commands need a detector ID.

```bash
aws guardduty list-detectors
```

Example shell variable:

```bash
DETECTOR_ID=$(aws guardduty list-detectors \
  --query 'DetectorIds[0]' \
  --output text)
```

---

## 40. List GuardDuty Findings

```bash
aws guardduty list-findings \
  --detector-id "$DETECTOR_ID"
```

The command returns finding IDs and is paginated. :chatgpt-content-reference{index="7"}

---

## 41. Sort Findings by Severity

```bash
aws guardduty list-findings \
  --detector-id "$DETECTOR_ID" \
  --sort-criteria '{
    "AttributeName":"severity",
    "OrderBy":"DESC"
  }'
```

This is useful for triage.

---

## 42. Get Finding Details

First select finding IDs.

Then:

```bash
aws guardduty get-findings \
  --detector-id "$DETECTOR_ID" \
  --finding-ids <finding-id>
```

`get-findings` can retrieve detailed GuardDuty finding information for specified IDs. :chatgpt-content-reference{index="8"}

---

## 43. Useful GuardDuty Fields

Review:

```text
Type

Severity

AccountId

Region

Resource

Service

CreatedAt

UpdatedAt
```

Security questions:

```text
Which resource?

Which principal?

Which IP?

Which API?

Is the finding current?

Are there related findings?
```

---

# Inspector Operations

## 44. List Inspector Findings

Amazon Inspector uses the `inspector2` CLI namespace.

```bash
aws inspector2 list-findings
```

This is a paginated operation. :chatgpt-content-reference{index="9"}

---

## 45. Filter Critical Inspector Findings

Example:

```bash
aws inspector2 list-findings \
  --filter-criteria '{
    "severity": [
      {
        "comparison": "EQUALS",
        "value": "CRITICAL"
      }
    ]
  }'
```

---

## 46. Readable Inspector Output

Example:

```bash
aws inspector2 list-findings \
  --query 'findings[].{
    Severity:severity,
    Type:type,
    Title:title,
    Resource:resources[0].id,
    Status:status
  }' \
  --output table
```

Exact fields depend on finding type.

---

## 47. Inspector Investigation Questions

For each finding:

```text
What resource?

Which CVE?

Which package?

What version?

Is a fix available?

What is the severity?

Is exploit information available?

Is the resource publicly exposed?

Is the resource production?
```

---

# Security Hub Operations

## 48. Security Hub Findings

Traditional Security Hub CSPM finding retrieval:

```bash
aws securityhub get-findings
```

`get-findings` supports filtering, sorting, pagination, and cross-Region aggregation when called in the configured aggregation/home Region. :chatgpt-content-reference{index="10"}

---

## 49. Critical Findings

Example:

```bash
aws securityhub get-findings \
  --filters '{
    "SeverityLabel": [
      {
        "Value": "CRITICAL",
        "Comparison": "EQUALS"
      }
    ]
  }'
```

---

## 50. Active Findings

Example concept:

```bash
aws securityhub get-findings \
  --filters '{
    "RecordState": [
      {
        "Value": "ACTIVE",
        "Comparison": "EQUALS"
      }
    ]
  }'
```

Combine with severity where appropriate.

---

## 51. Readable Security Hub Output

Example:

```bash
aws securityhub get-findings \
  --query 'Findings[].{
    Severity:Severity.Label,
    Title:Title,
    Account:AwsAccountId,
    Region:Region,
    Workflow:Workflow.Status,
    State:RecordState
  }' \
  --output table
```

---

# Security Hub GetFindingsV2

## 52. Modern Security Hub API

Current AWS CLI also provides:

```bash
aws securityhub get-findings-v2
```

This is important for the newer Security Hub data model.

`GetFindingsV2` can use `Scopes` to define an AWS Organizations-wide or OU-specific data boundary when used from the delegated administrator account, and then apply finding filters inside that scope. :chatgpt-content-reference{index="11"}

---

## 53. Why V2 Matters

Conceptually:

```text
Security Hub CSPM
→ Traditional ASFF-style finding workflows

Security Hub V2
→ Newer unified security finding capabilities
```

Do not assume older Security Hub examples represent every newer Security Hub capability.

---

## 54. Exposure Findings

For example, newer Security Hub exposure analysis can be retrieved using `get-findings-v2` filters.

Conceptually:

```bash
aws securityhub get-findings-v2 \
  --max-results 10
```

AWS documents the V2 API for exposure findings and newer Security Hub features. :chatgpt-content-reference{index="12"}

---

# Finding Correlation

## 55. Inspector + GuardDuty

Example:

```text
Inspector
→ Critical CVE

GuardDuty
→ Suspicious Network Activity

Same EC2
```

Priority:

```text
Higher
```

because:

```text
Known Weakness
+
Threat Activity
```

exist together.

---

## 56. Macie + GuardDuty

Conceptually:

```text
Macie
→ Sensitive Data in S3

GuardDuty
→ Suspicious S3 Access
```

Potential conclusion:

```text
Sensitive Data Exposure
```

---

## 57. Security Hub

Security Hub can provide the broader view:

```text
GuardDuty

Inspector

Macie

CSPM
   |
   v
Security Hub
```

The CLI enables these findings to become input for future automation.

---

# Security Investigation Sequence

## 58. Example Incident

Suppose you receive:

```text
Suspicious EC2 Activity
```

First:

```bash
aws sts get-caller-identity
```

Then verify Region:

```bash
aws configure get region
```

---

## 59. Step 1 — GuardDuty

```text
Find Finding
    ↓
Identify EC2
    ↓
Identify IP / Activity
```

---

## 60. Step 2 — Inspector

Search for vulnerabilities affecting the same EC2 resource.

Question:

```text
Is the instance vulnerable?
```

---

## 61. Step 3 — EC2 / Security Group

Review:

```text
Public IP?

Security Group?

Port Exposure?
```

---

## 62. Step 4 — CloudTrail

Review:

```text
Who launched it?

Who changed the Security Group?

Who changed the IAM role?
```

---

## 63. Step 5 — IAM

Review:

```text
Instance Profile

Role Permissions

Trust Policy

Recent Credential Changes
```

---

## 64. Step 6 — Security Hub

Check whether related security signals exist.

Conceptually:

```text
GuardDuty
+
Inspector
+
CSPM
      |
      v
Correlated Context
```

---

# Public Exposure Hunt

## 65. Example Workflow

```text
Security Groups
      ↓
0.0.0.0/0 / ::/0
      ↓
Identify Instances
      ↓
Check Public IP
      ↓
Check Inspector
      ↓
Check GuardDuty
      ↓
Review CloudTrail Changes
```

This is more useful than viewing a Security Group in isolation.

---

# S3 Investigation Workflow

## 66. S3 Security Check

For each important bucket:

```text
Bucket
  ↓
Public Access Block
  ↓
Bucket Policy
  ↓
Encryption
  ↓
CloudTrail Activity
  ↓
Macie / GuardDuty Context
```

---

## 67. Do Not Assume Public Access From One Setting

For S3:

```text
Bucket-Level Block Public Access
```

is only one piece.

Also consider:

```text
Account-Level BPA

Organization-Level Controls

Bucket Policy

Access Points

ACL-related controls
```

AWS applies the most restrictive applicable Public Access Block configuration. :chatgpt-content-reference{index="13"}

---

# Read-Only First

## 68. Investigation Principle

During initial triage prefer:

```text
List

Describe

Get

Lookup
```

before:

```text
Delete

Terminate

Disable

Detach

Revoke
```

Why?

Because premature remediation can:

```text
Destroy Evidence

Break Production

Alert an Attacker

Make Root Cause Analysis Harder
```

---

## 69. Read-Only Does Not Mean Risk-Free

Even read APIs can expose:

```text
Resource Names

Policies

Account IDs

Security Architecture

Metadata
```

Do not post investigation output publicly.

---

# Multi-Region Operations

## 70. Security Services Are Often Regional

Examples:

```text
GuardDuty

Inspector

EC2

Security Hub

KMS
```

Therefore:

```text
Tokyo clean
```

does not imply:

```text
Every Region clean
```

---

## 71. Enumerate Regions

Example:

```bash
aws ec2 describe-regions \
  --query 'Regions[].RegionName' \
  --output text
```

Then security scripts can iterate only through:

```text
Approved Regions
```

rather than blindly scanning every possible Region.

---

# Multi-Account Operations

## 72. Cross-Account Investigation

Conceptually:

```text
Security Account
     |
     v
AssumeRole
     |
     v
Production Account
```

Then run:

```bash
aws sts get-caller-identity
```

again.

Never assume role switching succeeded without verifying identity.

---

## 73. Recommended Process

```text
Security Profile
      ↓
Assume Production Investigation Role
      ↓
Verify Caller Identity
      ↓
Run Read-Only Commands
      ↓
Record Evidence
```

---

# Query Examples

## 74. IAM Roles

```bash
aws iam list-roles \
  --query 'Roles[].RoleName' \
  --output text
```

---

## 75. Running EC2 Instances

```bash
aws ec2 describe-instances \
  --filters \
    Name=instance-state-name,Values=running \
  --query 'Reservations[].Instances[].InstanceId' \
  --output text
```

---

## 76. Security Group Overview

```bash
aws ec2 describe-security-groups \
  --query 'SecurityGroups[].{
    ID:GroupId,
    Name:GroupName,
    VPC:VpcId
  }' \
  --output table
```

---

## 77. KMS Key IDs

```bash
aws kms list-keys \
  --query 'Keys[].KeyId' \
  --output text
```

---

## 78. Inspector Critical Findings

```bash
aws inspector2 list-findings \
  --filter-criteria '{
    "severity": [
      {
        "comparison":"EQUALS",
        "value":"CRITICAL"
      }
    ]
  }' \
  --query 'findings[].{
    Title:title,
    Resource:resources[0].id,
    Severity:severity
  }' \
  --output table
```

---

# Pagination

## 79. Security Enumeration Must Be Complete

Commands such as:

```text
describe-security-groups

GuardDuty list-findings

Inspector list-findings

Security Hub get-findings
```

can be paginated. :chatgpt-content-reference{index="14"}

Avoid:

```text
First Page
=
Entire Environment
```

assumption.

---

# Evidence Handling

## 80. Save Read-Only Output

During authorized investigations you might store relevant output locally:

```bash
aws cloudtrail lookup-events \
  --max-items 50 \
  --output json > cloudtrail-events.json
```

or:

```bash
aws inspector2 list-findings \
  --output json > inspector-findings.json
```

Treat these files as security-sensitive.

---

## 81. Never Commit Real Evidence

Do not commit:

```text
Account IDs

Internal IP Addresses

Real ARNs

Security Group Rules

Bucket Names

IAM Role Names

Finding Details

Customer Information
```

to a public GitHub repo.

For GitHub notes use placeholders such as:

```text
<account-id>

<role-name>

<bucket-name>

<finding-id>
```

---

# Troubleshooting

## 82. AccessDenied

If:

```text
AccessDenied
```

check:

```text
IAM Policy

Permissions Boundary

SCP

Session Policy

Resource Policy

KMS Key Policy

RCP
```

Day 35 concepts apply directly here.

---

## 83. Empty Results

Empty output can mean:

```text
No Resources

Wrong Account

Wrong Region

Wrong Filter

No Permission to Relevant Context

Service Not Enabled
```

Do not immediately conclude:

```text
No Security Issue
```

---

## 84. GuardDuty No Detector

If:

```bash
aws guardduty list-detectors
```

returns no detector:

Possible explanation:

```text
GuardDuty not enabled in this Region
```

Check organization and Region coverage.

---

## 85. Inspector Empty Findings

Possible explanations:

```text
No Current Findings

No Supported Resources

Coverage Gap

Wrong Region

Inspector Not Enabled
```

Again:

```text
No Finding
≠
No Risk
```

---

# Hands-on Practice

## 86. Practice — Verify Context

Run:

```bash
aws sts get-caller-identity
```

```bash
aws configure get region
```

Record only:

```text
Profile Type

Region
```

Do not record real account IDs publicly.

---

## 87. Practice — IAM Inventory

Run:

```bash
aws iam list-users
```

```bash
aws iam list-roles
```

Answer:

```text
Are IAM users present?

Are most identities roles?

Are any unexpected roles visible?
```

---

## 88. Practice — Credential Report

If authorized:

```bash
aws iam generate-credential-report
```

then:

```bash
aws iam get-credential-report
```

Review locally:

```text
MFA

Access Keys

Last Used
```

Do not commit the CSV.

---

## 89. Practice — CloudTrail

```bash
aws cloudtrail lookup-events \
  --max-items 10 \
  --query 'Events[].{
    Time:EventTime,
    Event:EventName,
    User:Username
  }' \
  --output table
```

Identify:

```text
Most Recent API Activity
```

---

## 90. Practice — Security Groups

Run:

```bash
aws ec2 describe-security-groups \
  --filters \
    Name=ip-permission.cidr,Values='0.0.0.0/0'
```

For each candidate:

```text
Inspect actual inbound rules
```

Do not modify them for practice.

---

## 91. Practice — S3 Security

For a test bucket:

```bash
aws s3api get-public-access-block \
  --bucket <bucket-name>
```

Then:

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name>
```

Identify:

```text
Public Access Block

Encryption Algorithm
```

---

## 92. Practice — KMS

```bash
aws kms list-keys
```

For one test key:

```bash
aws kms describe-key \
  --key-id <key-id>
```

Review:

```text
Key Manager

State

Usage

Multi-Region
```

---

## 93. Practice — GuardDuty

```bash
aws guardduty list-detectors
```

If enabled:

```bash
aws guardduty list-findings \
  --detector-id <detector-id>
```

Do not generate malicious activity solely for practice.

---

## 94. Practice — Inspector

If enabled:

```bash
aws inspector2 list-findings
```

Filter:

```text
Critical / High
```

and identify:

```text
Resource

Finding Type

Status
```

---

## 95. Practice — Security Hub

If enabled:

```bash
aws securityhub get-findings \
  --max-items 10
```

Review:

```text
Source

Severity

Resource

Workflow

Record State
```

If the newer Security Hub capabilities are available in your environment, also inspect:

```bash
aws securityhub get-findings-v2 \
  --max-results 10
```

---

# Security Operations Scenario

## 96. Scenario

Alert:

```text
Suspicious Network Activity
on Production EC2
```

Investigation workflow:

```text
1. Verify account / Region

2. Review GuardDuty finding

3. Identify EC2 instance

4. Review public IP

5. Review Security Groups

6. Review Inspector findings

7. Review IAM role

8. Review CloudTrail

9. Review related Security Hub findings

10. Determine scope

11. Preserve evidence

12. Decide containment
```

---

# Investigation Mental Model

## 97. Identity

```text
Who?
```

Use:

```text
IAM

STS

CloudTrail
```

---

## 98. Resource

```text
What was affected?
```

Use:

```text
EC2

S3

KMS

Inspector
```

---

## 99. Exposure

```text
Could the attacker reach it?
```

Use:

```text
Security Groups

Public IP

S3 Access

Network Configuration
```

---

## 100. Activity

```text
What happened?
```

Use:

```text
CloudTrail

GuardDuty

Security Hub
```

---

## 101. Weakness

```text
Why could it happen?
```

Use:

```text
Inspector

Security Configuration

IAM
```

---

## 102. Impact

```text
What could be accessed?
```

Review:

```text
IAM Permissions

KMS

Secrets

S3

Databases

Cross-Account Roles
```

---

# Security Checklist

```text
[ ] Active identity is verified before investigation

[ ] Correct AWS account is confirmed

[ ] Correct Region is confirmed

[ ] Investigation starts with read-only APIs

[ ] IAM users and roles are inventoried

[ ] IAM credential reports are reviewed securely

[ ] Long-lived access keys are identified

[ ] MFA status is reviewed

[ ] CloudTrail is used to investigate API activity

[ ] CloudTrail Region scope is considered

[ ] Public IPv4 Security Group rules are reviewed

[ ] Public IPv6 Security Group rules are reviewed

[ ] Candidate Security Groups are manually validated

[ ] Public EC2 exposure is reviewed in context

[ ] S3 Public Access Block is reviewed

[ ] Account-level S3 Public Access Block is considered

[ ] S3 default encryption is reviewed

[ ] Bucket policies are reviewed where required

[ ] KMS key state and policy are reviewed

[ ] GuardDuty findings are reviewed

[ ] Inspector vulnerability findings are reviewed

[ ] Security Hub findings are reviewed centrally

[ ] Newer Security Hub V2 APIs are understood

[ ] Pagination is considered

[ ] Multi-Region coverage is considered

[ ] Multi-account coverage is considered

[ ] Investigation output is handled as sensitive data

[ ] Real security evidence is never committed to public GitHub
```

---

## Key Takeaways

- AWS CLI can provide a repeatable security investigation workflow.
- Security operations should always begin by verifying account, identity, role, profile, and Region.
- IAM credential reports help identify account-level credential risks.
- CloudTrail provides recent management API activity for investigation.
- Security Groups can be reviewed for broad IPv4 and IPv6 exposure.
- Security Group server-side filters identify candidates but must be validated against individual rules.
- S3 Public Access Block must be considered at bucket, account, and organization levels.
- Modern S3 buckets use default server-side encryption, but the encryption type still matters.
- KMS CLI commands help review key state, configuration, and key policies.
- GuardDuty provides threat-detection findings.
- Inspector provides vulnerability findings.
- Security Hub centralizes and prioritizes security findings.
- Security Hub V2 APIs provide newer organization-scoped and unified finding capabilities.
- Security investigations should begin read-only and preserve evidence before remediation.
- Pagination, account coverage, and Region coverage must be considered when interpreting CLI results.

---

## Reflection

Today I learned how to use the AWS CLI as a practical cloud security investigation tool.

The most important lesson is that individual commands become much more useful when they are connected into an investigation workflow.

For example, a GuardDuty finding can identify suspicious activity, EC2 and Security Group commands can reveal network exposure, Inspector can identify vulnerabilities, IAM can explain the permissions available to the resource, and CloudTrail can show who changed the environment.

I also learned that an empty CLI result does not always mean the environment is secure. I must consider whether I am using the correct account and Region, whether the service is enabled, whether the resource is covered, and whether pagination or filters could hide relevant data.

From a cloud security perspective, AWS CLI provides a repeatable foundation for investigation that can later be converted into Python and boto3 automation.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Blast Radius | Potential scope of impact caused by a security compromise |
| Credential Report | IAM report containing account-wide credential status information |
| Correlation | Combining signals from multiple security sources to understand an incident |
| Evidence Preservation | Protecting relevant data before remediation or system changes |
| Exposure | Condition that makes a resource reachable or accessible to potential attackers |
| Finding | Security-related observation produced by a service such as GuardDuty or Inspector |
| Finding Coverage | Scope of resources, accounts, and Regions monitored by a security service |
| Public Access Block | Amazon S3 control for restricting public access mechanisms |
| Read-Only Investigation | Security investigation using non-modifying APIs before containment or remediation |
| Security Triage | Initial process of reviewing and prioritizing a security signal |
