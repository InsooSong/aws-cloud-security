# Day 31 — Amazon Macie

## Topic

Amazon Macie Fundamentals, Sensitive Data Discovery, Managed Data Identifiers, Custom Data Identifiers, and S3 Data Protection

---

## Objectives

- Understand the purpose of Amazon Macie
- Understand how Macie discovers sensitive data in Amazon S3
- Learn the difference between sensitive data findings and policy findings
- Understand managed data identifiers
- Understand custom data identifiers
- Learn how allow lists work
- Understand automated sensitive data discovery
- Understand sensitive data discovery jobs
- Learn how Macie prioritizes findings
- Understand how Macie analyzes S3 bucket security posture
- Learn how Macie integrates with Security Hub
- Understand multi-account Macie administration
- Practice reviewing sensitive data findings
- Identify common Macie configuration mistakes

---

# Macie Fundamentals

## 1. What Is Amazon Macie?

Amazon Macie is a managed data security and privacy service.

It helps identify and protect sensitive data stored in Amazon S3.

Conceptually:

```text
Amazon S3
    |
    v
Amazon Macie
    |
    v
Sensitive Data Discovery
    |
    v
Findings
```

Macie can identify data such as:

```text
Credentials

Financial Information

Personally Identifiable Information

Personal Health Information

Custom Organizational Data
```

---

## 2. Why Macie Matters

Organizations often store large amounts of data in S3.

Example:

```text
S3 Buckets
│
├── Logs
├── Backups
├── Customer Data
├── Documents
├── Application Data
└── Archives
```

Without data classification:

```text
Where is sensitive data?

Who owns it?

Is it encrypted?

Is it public?

Is it shared externally?
```

may be difficult to answer.

Macie helps provide this visibility.

---

## 3. Macie vs Inspector vs GuardDuty

These services have different roles.

### Amazon Macie

```text
Sensitive Data Discovery
```

Question:

```text
Where is sensitive data stored?
```

### Amazon Inspector

```text
Vulnerability Management
```

Question:

```text
What known weaknesses exist?
```

### Amazon GuardDuty

```text
Threat Detection
```

Question:

```text
Is suspicious activity occurring?
```

### Security Hub

```text
Centralized Findings
```

Question:

```text
Where can all these security findings be managed?
```

---

# S3 Security Visibility

## 4. S3 Inventory Context

Macie maintains information about S3 buckets.

It can help review properties such as:

```text
Bucket Name

Public Access

Encryption

Shared Access

Object Count

Storage Size

Sensitive Data Discovery Status
```

Conceptually:

```text
S3 Bucket
    |
    v
Macie Inventory
    |
    v
Security and Data Context
```

---

## 5. Data Security Questions

For each S3 bucket, a security engineer should ask:

```text
Does this bucket contain sensitive data?

Is the bucket public?

Is encryption enabled?

Is the bucket shared?

Which account owns it?

When was sensitive data last analyzed?
```

This combines:

```text
Data Classification

+

Security Posture
```

---

# Sensitive Data Discovery

## 6. What Is Sensitive Data Discovery?

Sensitive data discovery analyzes S3 objects for information that matches defined sensitive-data patterns.

Conceptually:

```text
S3 Object
   |
   v
Macie Analysis
   |
   +-- No Sensitive Data Detected
   |
   +-- Sensitive Data Detected
```

When sensitive data is detected, Macie can generate a finding.

---

## 7. Discovery Methods

Macie provides two main approaches:

```text
Automated Sensitive Data Discovery

Sensitive Data Discovery Jobs
```

Both analyze S3 objects but serve different operational needs.

---

# Automated Sensitive Data Discovery

## 8. Automated Sensitive Data Discovery

Automated sensitive data discovery continuously evaluates representative objects across S3 buckets.

Conceptually:

```text
S3 Buckets
    |
    v
Macie
    |
    v
Select Objects
    |
    v
Analyze
    |
    v
Sensitive Data Profile
```

This helps continuously identify where sensitive data may exist without creating a separate manual job for every bucket.

---

## 9. Default Automated Discovery

By default, automated discovery analyzes general purpose S3 buckets in the account.

For an organization administrator, this can also include member-account buckets.

Conceptually:

```text
AWS Account / Organization
        |
        v
S3 Buckets
        |
        v
Automated Discovery
```

Bucket exclusions and discovery settings can be customized.

---

## 10. Automated Discovery Configuration

Automated discovery can be configured to control:

```text
Included / Excluded Buckets

Managed Data Identifiers

Custom Data Identifiers

Allow Lists
```

This helps align analysis with organizational requirements.

---

## 11. Representative Sampling

Automated sensitive data discovery does not necessarily inspect every object continuously.

Instead:

```text
Macie
   |
   v
Select Representative Objects
   |
   v
Analyze Samples
   |
   v
Build Sensitive Data Profile
```

The goal is to provide continuous data classification efficiently.

For exhaustive analysis of a defined scope, use a sensitive data discovery job.

---

# Sensitive Data Discovery Jobs

## 12. Discovery Jobs

A sensitive data discovery job analyzes S3 objects according to a defined scope.

Conceptually:

```text
Selected Buckets
      |
      v
Discovery Job
      |
      v
Analyze Objects
      |
      v
Results / Findings
```

Jobs provide greater control over:

```text
Buckets

Object Selection

Schedule

Data Identifiers

Allow Lists
```

---

## 13. One-Time vs Scheduled Jobs

Jobs can be configured as:

```text
One-Time

or

Scheduled
```

Example:

```text
One-Time
→ Investigate a specific bucket

Scheduled
→ Recurring compliance scan
```

---

## 14. When to Use a Job

Use discovery jobs when you need:

```text
Specific Bucket Scope

Defined Schedule

Audit Evidence

Detailed Scan Coverage

Custom Detection Criteria
```

---

# Managed Data Identifiers

## 15. What Are Managed Data Identifiers?

Managed data identifiers are built-in detection criteria maintained by AWS.

They combine techniques such as:

```text
Pattern Matching

Keywords

Validation Logic

Machine Learning
```

to identify sensitive data.

---

## 16. Sensitive Data Categories

Managed data identifiers can detect categories such as:

```text
Credentials

Financial Information

Personal Information
```

Examples include:

```text
AWS Secret Access Keys

Credit Card Numbers

Bank Account Numbers

Passport Numbers

Driver License Numbers

Health Information
```

---

## 17. Credentials Detection

Managed identifiers can detect credential-related data such as:

```text
AWS Secret Access Keys

Private Keys

JSON Web Tokens

API Keys

Authorization Headers
```

Example:

```text
S3 Object
   |
   v
Contains AWS Secret Access Key
   |
   v
Macie Finding
```

---

## 18. Financial Data

Examples include:

```text
Credit Card Numbers

Bank Account Numbers

Financial Identifiers
```

Depending on the identifier, Macie may use:

```text
Pattern

Keyword Proximity

Validation
```

to reduce false positives.

---

## 19. PII and PHI

Macie can detect multiple forms of:

```text
Personally Identifiable Information

Personal Health Information
```

Examples can include:

```text
Passport Numbers

Driver License Numbers

National Identification Numbers

Medical Identification Numbers
```

Support varies by country and identifier type.

---

# Custom Data Identifiers

## 20. What Is a Custom Data Identifier?

A custom data identifier lets an organization define its own sensitive-data pattern.

Examples:

```text
Employee ID

Customer Account Number

Internal Project Code

Custom Classification Label
```

Conceptually:

```text
Organization-Specific Pattern
       |
       v
Custom Data Identifier
       |
       v
Macie Detection
```

---

## 21. Custom Identifier Components

A custom data identifier can use:

```text
Regular Expression

Keywords

Ignore Words

Proximity Rules
```

Conceptually:

```text
Regex
 +
Keyword Context
 +
Exclusions
      |
      v
Detection Logic
```

---

## 22. Regex Example

Suppose internal employee IDs use:

```text
EMP-123456
```

A conceptual regex could be:

```text
EMP-[0-9]{6}
```

But a regex alone may generate false positives.

Adding nearby keywords such as:

```text
Employee ID

Employee Number
```

can improve accuracy.

---

## 23. Keyword Proximity

Conceptually:

```text
Employee ID: EMP-123456
```

Macie can use:

```text
Keyword
+
Pattern
+
Proximity
```

to increase confidence.

This reduces accidental matches elsewhere in the document.

---

## 24. Ignore Words

Ignore words can exclude known false-positive patterns.

Example:

```text
TEST-ACCOUNT-123456
```

If test identifiers should not count as sensitive data, an ignore pattern can reduce noise.

---

# Allow Lists

## 25. What Is an Allow List?

An allow list defines values or patterns that should not be treated as sensitive data matches.

Example:

```text
Public Company Phone Number

Known Test Credential Pattern

Public Support Email
```

Conceptually:

```text
Potential Match
      |
      v
Allow List
      |
      +-- Allowed
      |
      +-- Sensitive
```

---

## 26. Why Allow Lists Matter

Without allow lists:

```text
Expected Public Value
      |
      v
Sensitive Data Finding
```

This can increase false positives.

Allow lists help reduce:

```text
Noise

Unnecessary Findings

Alert Fatigue
```

They should be carefully scoped.

---

# Sensitive Data Findings

## 27. What Is a Sensitive Data Finding?

A sensitive data finding is generated when Macie detects sensitive data in an S3 object.

It can include information such as:

```text
Sensitive Data Type

Occurrence Count

Bucket

Object

Encryption Status

Public Access Context

Severity
```

Importantly, the finding does not include the actual sensitive data value.

---

## 28. Why Findings Do Not Include Sensitive Values

Poor design:

```text
Sensitive Data Found
      |
      v
Copy Sensitive Value
into Finding
```

This would create another sensitive-data location.

Instead:

```text
Finding
→ Metadata About Detection
```

not:

```text
Finding
→ Original Sensitive Data
```

This reduces secondary exposure.

---

## 29. Finding Severity

Macie assigns severity based on finding type and context.

Example factors can include:

```text
Sensitive Data Type

Occurrence Count

Bucket Security

Exposure
```

Severity helps prioritization but should not be used alone.

---

## 30. Sensitive Data Finding Example

Scenario:

```text
S3 Object

customer-export.csv
```

contains:

```text
Credit Card Data

Customer IDs
```

and the bucket is:

```text
Publicly Accessible
```

This deserves significantly higher attention than the same data in a tightly restricted internal bucket.

---

# Policy Findings

## 31. Policy Findings

Macie can also generate policy-related findings for S3 bucket security issues.

These can highlight conditions such as:

```text
Public Access

External Sharing

Security Configuration Changes
```

Conceptually:

```text
S3 Security Posture
       |
       v
Macie
       |
       v
Policy Finding
```

---

## 32. Sensitive Data vs Policy Findings

A useful distinction:

```text
Sensitive Data Finding
→ What sensitive information exists?

Policy Finding
→ Is the S3 security posture risky?
```

Together:

```text
Sensitive Data
+
Public Exposure
=
High Priority
```

---

# Discovery Results

## 33. Sensitive Data Discovery Results

Macie creates an analysis record for each S3 object analyzed by a discovery job or automated discovery.

These records are called:

```text
Sensitive Data Discovery Results
```

They can include:

```text
Successful Analysis

No Sensitive Data Found

Sensitive Data Found

Analysis Error
```

---

## 34. Findings vs Discovery Results

This distinction is important.

### Finding

Created when a security-relevant issue is detected.

### Discovery Result

Analysis record for an object that Macie analyzed.

Therefore:

```text
Every Analyzed Object
→ Discovery Result

Sensitive Data Detected
→ May Also Produce Finding
```

---

## 35. Results Repository

Sensitive data discovery results can be stored in an S3 repository.

Conceptually:

```text
Macie Analysis
      |
      v
Discovery Result
      |
      v
S3 Results Repository
```

The repository should be protected because it contains detailed analysis metadata.

---

## 36. KMS Protection for Results

A sensitive data discovery results repository can use a KMS key.

Conceptually:

```text
Macie Results
    |
    v
S3
    |
    v
KMS Encryption
```

This connects Macie back to:

```text
Day 25–26
→ AWS KMS
```

---

# Investigation

## 37. Finding Investigation Questions

For a Macie finding, ask:

```text
What sensitive data was detected?

How many occurrences?

Which bucket?

Which object?

Is the bucket public?

Is it externally shared?

Is encryption enabled?

Who owns the bucket?

Does the data need to exist there?

Who accessed the data?
```

---

## 38. Correlating with CloudTrail

Macie identifies:

```text
Sensitive Data Exists
```

CloudTrail can help investigate:

```text
Who accessed it?

Who changed the bucket policy?

Who disabled Block Public Access?
```

Conceptually:

```text
Macie
→ What sensitive data exists?

CloudTrail
→ Who interacted with it?
```

---

## 39. Correlating with AWS Config

AWS Config can help determine:

```text
When did the bucket become public?

Was encryption changed?

Was the bucket policy modified?
```

This adds configuration history to the investigation.

---

## 40. Correlating with GuardDuty

Example:

```text
Macie
→ Sensitive Data in S3

GuardDuty
→ Suspicious S3 Object Access
```

Together:

```text
Potential Data Exfiltration
```

This deserves higher priority.

---

## 41. Correlating with Security Hub

Macie findings can be sent to Security Hub.

Conceptually:

```text
Macie
   |
   v
Finding
   |
   v
Security Hub
   |
   v
ASFF
```

This supports centralized triage.

---

# Automated Sensitive Data Discovery

## 42. Sensitive Data Profiles

Automated discovery builds data profiles for S3 buckets.

Conceptually:

```text
Bucket
   |
   v
Macie Samples Objects
   |
   v
Sensitive Data Classification
   |
   v
Bucket Profile
```

This helps prioritize buckets containing higher concentrations of sensitive information.

---

## 43. Why Automated Discovery Is Useful

Large environments may contain:

```text
100

1,000

10,000+
```

S3 buckets.

Running manual discovery jobs everywhere is difficult.

Automated discovery provides ongoing visibility with lower operational overhead.

---

## 44. Customize Automated Discovery

You can customize:

```text
Buckets to Include

Buckets to Exclude

Managed Data Identifiers

Custom Data Identifiers

Allow Lists
```

This reduces irrelevant scans and improves signal quality.

---

# Multi-Account Macie

## 45. Macie Administrator

AWS Organizations can designate a Macie administrator account.

Conceptually:

```text
AWS Organizations
       |
       v
Security Account
       |
       v
Macie Administrator
       |
       +-- Production
       |
       +-- Development
       |
       +-- Shared Services
```

This supports centralized S3 data security management.

---

## 46. Member Accounts

The Macie administrator can review supported information for organization member accounts.

This improves visibility across:

```text
Accounts

Buckets

Sensitive Data Findings

Policy Findings
```

---

## 47. Why Centralize Macie?

Without centralization:

```text
Account A
→ Macie

Account B
→ Macie

Account C
→ Macie
```

Security teams must review separately.

With organization administration:

```text
Organization
     |
     v
Central Macie Administrator
```

This supports consistent governance.

---

# Remediation

## 48. Sensitive Data Remediation

When sensitive data is found, remediation depends on context.

Possible actions:

```text
Remove Public Access

Restrict Bucket Policy

Enable Encryption

Move Data

Delete Unnecessary Data

Tokenize Data

Mask Data

Apply Retention Policy
```

Macie identifies the problem.

It does not decide the business requirement for the data.

---

## 49. Data Minimization

One of the strongest security controls is:

```text
Do Not Store Data
That Is Not Needed
```

Example:

```text
Old Customer Export

No Business Need

Contains PII
```

Possible remediation:

```text
Securely Delete
```

rather than simply adding more access controls.

---

## 50. Public Bucket Scenario

Scenario:

```text
S3 Bucket
    |
    +-- Public
    |
    +-- Contains PII
```

Priority:

```text
Very High
```

Potential response:

```text
Restrict Public Access

Preserve Evidence

Identify Access History

Review Bucket Policy

Determine Exposure Window

Notify Required Stakeholders
```

---

## 51. Credential Leak Scenario

Macie detects:

```text
AWS Secret Access Key
```

inside an S3 object.

Possible response:

```text
Identify Credential

Disable / Rotate Credential

Review CloudTrail

Remove Credential from Object

Review Application Design

Search for Additional Copies
```

Treat exposed credentials as compromised until proven otherwise.

---

# Common Misconfigurations

## 52. Macie Enabled but Discovery Not Used

Poor:

```text
Macie Enabled
→ No Jobs
→ Automated Discovery Disabled
```

Result:

```text
Limited Sensitive Data Visibility
```

Enabling the service alone does not guarantee that all required data is analyzed.

---

## 53. Scan Everything Without Scope

Poor strategy:

```text
Analyze Every Object Forever
```

Potential issues:

```text
High Cost

Noise

Unnecessary Processing
```

Better:

```text
Classify Critical Buckets

Use Automated Discovery

Create Targeted Jobs
```

---

## 54. No Custom Identifiers

Managed identifiers may not understand organizational data such as:

```text
Employee Number

Internal Customer ID

Project Classification
```

Custom identifiers can fill this gap.

---

## 55. Poor Regex Design

Broad regex:

```text
[0-9]{6}
```

could match many harmless numbers.

Better:

```text
Regex
+
Keywords
+
Proximity
+
Ignore Rules
```

---

## 56. Public Data Added to Allow List Too Broadly

Poor:

```text
Allow Any Value Matching Broad Pattern
```

This may hide real sensitive data.

Allow lists should be specific and reviewed.

---

## 57. Findings Without Owners

Poor:

```text
Macie Finding
     |
     v
Nobody Reviews
```

A useful data security process requires:

```text
Owner

Priority

Response Procedure

Remediation SLA
```

---

# Cost Considerations

## 58. Discovery Cost

Sensitive data analysis has cost implications.

Factors can include:

```text
Amount of Data Analyzed

Number of Objects

Discovery Jobs

Automated Discovery
```

Therefore:

```text
More Scanning
≠
Automatically Better
```

Analysis should align with risk and data classification needs.

---

# Hands-on Practice

## 59. Practice — Open Macie

Navigate:

```text
AWS Console
   |
   v
Amazon Macie
```

Review:

```text
Summary

S3 Buckets

Findings

Sensitive Data Discovery

Settings
```

---

## 60. Practice — Review S3 Buckets

Open:

```text
Macie
→ S3 Buckets
```

For one bucket, review:

```text
Public Access

Encryption

Object Count

Storage Size

Shared Access

Sensitive Data Status
```

Do not expose customer bucket names or sensitive metadata in GitHub.

---

## 61. Practice — Review Managed Data Identifiers

Navigate to the managed data identifier list.

Choose examples from:

```text
Credentials

Financial

PII
```

For each one, identify:

```text
Identifier Name

Data Type

Country / Region Support

Keyword Requirement
```

---

## 62. Practice — Design a Custom Identifier

Do not use real sensitive data.

Example requirement:

```text
Employee ID:
EMP-123456
```

Conceptually define:

```text
Regex:
EMP-[0-9]{6}

Keyword:
Employee ID
```

Then consider:

```text
What false positives might occur?

What ignore words are required?
```

---

## 63. Practice — Review a Finding

Choose a sample or existing Macie finding.

Record:

```text
Finding Type:

Severity:

Bucket:

Object:

Sensitive Data Category:

Sensitive Data Type:

Occurrences:

Public Access:

Encryption:
```

Do not copy real sensitive values.

---

## 64. Practice — Investigation Plan

For a finding involving PII:

```text
1. Confirm bucket owner

2. Confirm data classification

3. Review public / shared access

4. Review encryption

5. Check CloudTrail access history

6. Determine whether storage is required

7. Remediate exposure

8. Document outcome
```

---

## 65. Optional CLI Practice

Check Macie status:

```bash
aws macie2 get-macie-session
```

List findings:

```bash
aws macie2 list-findings
```

Get finding details:

```bash
aws macie2 get-findings \
  --finding-ids <finding-id>
```

List managed identifiers:

```bash
aws macie2 list-managed-data-identifiers
```

List discovery jobs:

```bash
aws macie2 list-classification-jobs
```

Do not publish real account IDs, bucket names, object keys, or findings tied to customer data.

---

# Architecture Exercise

## 66. Sensitive Data Security Architecture

```text
AWS Organization
       |
       v
Security Account
       |
       v
Amazon Macie
       |
       v
S3 Buckets
       |
       +-- Production Data
       |
       +-- Backups
       |
       +-- Logs
       |
       +-- Customer Files
       |
       v
Sensitive Data Findings
       |
       v
Security Hub
       |
       v
Security Team
```

---

## 67. Full Security Correlation

Scenario:

```text
Macie
→ PII Detected

AWS Config
→ Bucket Became Public

CloudTrail
→ User Changed Bucket Policy

GuardDuty
→ Suspicious GetObject Activity

Security Hub
→ Aggregates Findings
```

This can indicate:

```text
Potential Sensitive Data Exposure
```

---

# Security Checklist

```text
[ ] Macie is enabled in required accounts

[ ] Required Regions are covered

[ ] S3 buckets are inventoried

[ ] Automated sensitive data discovery is enabled where appropriate

[ ] Sensitive buckets receive targeted discovery jobs where required

[ ] Managed data identifiers match organizational requirements

[ ] Custom data identifiers exist for organization-specific data

[ ] Regex patterns are tested for false positives

[ ] Allow lists are narrowly scoped

[ ] Public S3 access is reviewed

[ ] Bucket encryption is reviewed

[ ] Sensitive data findings have defined owners

[ ] High-risk findings have remediation procedures

[ ] Sensitive data findings are integrated with Security Hub

[ ] CloudTrail is available for access investigation

[ ] AWS Config is available for bucket configuration history

[ ] Exposed credentials are rotated immediately

[ ] Unnecessary sensitive data is removed

[ ] Discovery results repositories are protected

[ ] Macie costs and analysis scope are periodically reviewed
```

---

## Key Takeaways

- Amazon Macie helps discover and classify sensitive data stored in Amazon S3.
- Macie can identify credentials, financial information, PII, PHI, and other sensitive data.
- Managed data identifiers provide AWS-maintained detection criteria.
- Custom data identifiers allow organizations to detect organization-specific sensitive data.
- Custom identifiers can combine regex, keywords, ignore words, and proximity rules.
- Allow lists reduce known false positives.
- Automated sensitive data discovery provides continuous S3 data classification.
- Sensitive data discovery jobs provide targeted and scheduled analysis.
- Sensitive data findings describe detected sensitive information without exposing the actual sensitive value.
- Policy findings focus on S3 security posture and exposure.
- Discovery results record object-level analysis outcomes even when no finding is generated.
- Macie findings can be centralized through Security Hub.
- Macie should be correlated with CloudTrail, AWS Config, and GuardDuty during sensitive-data investigations.
- Data minimization can be more effective than simply adding more security controls.
- Sensitive data discovery should be connected to ownership and remediation processes.

---

## Reflection

Today I learned that Amazon Macie provides visibility into sensitive data stored in Amazon S3.

The most important lesson is that protecting data begins with understanding where sensitive information exists.

Macie uses managed data identifiers to detect common sensitive data types and custom data identifiers to detect organization-specific information.

I also learned that sensitive data discovery and S3 security posture should be evaluated together. Sensitive data stored in a private and encrypted bucket has a very different risk profile from the same data stored in a publicly accessible bucket.

From a cloud security perspective, Macie becomes most useful when its findings are correlated with CloudTrail, AWS Config, GuardDuty, and Security Hub to determine whether sensitive data was exposed or accessed unexpectedly.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Allow List | Values or patterns that Macie should exclude from sensitive-data matches |
| Automated Sensitive Data Discovery | Continuous Macie analysis of S3 data without manually defining individual jobs |
| Custom Data Identifier | Organization-defined logic for detecting custom sensitive data |
| Data Classification | Categorizing data according to sensitivity or business value |
| Data Minimization | Keeping only the data that is actually required |
| Discovery Job | User-defined Macie scan for selected S3 data |
| Discovery Result | Record describing Macie's analysis of an S3 object |
| Managed Data Identifier | AWS-maintained detection logic for a known sensitive data type |
| Sensitive Data | Information that requires protection because of privacy, security, or business requirements |
| Sensitive Data Discovery | Process of analyzing data to identify sensitive information |
