# Day 42 — Security Automation with boto3

## Topic

AWS Security Automation with boto3 — Resource Enumeration, Security Checks, Findings, Severity, and JSON Reporting

---

## Objectives

- Build a simple AWS security scanner using boto3
- Verify AWS account and Region before scanning
- Reuse boto3 Sessions and clients
- Enumerate AWS resources with paginators
- Detect EC2 instances with public IP addresses
- Detect publicly exposed Security Group rules
- Review S3 Public Access Block configuration
- Review S3 default encryption configuration
- Retrieve GuardDuty findings
- Retrieve Amazon Inspector findings
- Create normalized security findings
- Assign simple finding severity levels
- Generate a JSON security report
- Handle AWS API errors safely
- Understand multi-Region security scanning
- Understand the limitations of automated security checks

---

# From Inventory to Security Automation

## 1. Day 41 vs Day 42

Day 41 focused on:

```text
AWS API
   ↓
Retrieve Resources
```

Day 42 adds:

```text
AWS API
   ↓
Retrieve Resources
   ↓
Evaluate Security Rules
   ↓
Create Findings
   ↓
Generate Report
```

Example:

```text
EC2 Instance
   ↓
Has Public IP?
   ↓
Yes
   ↓
Create Security Finding
```

---

# Security Automation Architecture

## 2. Scanner Architecture

```text
boto3 Session
      |
      v
Verify Identity
      |
      v
AWS Services
      |
      +-- EC2
      +-- S3
      +-- GuardDuty
      +-- Inspector
      |
      v
Security Checks
      |
      v
Normalized Findings
      |
      v
JSON Report
```

---

## 3. Read-Only First

The scanner should initially use read-only AWS APIs.

Examples:

```text
Describe

List

Get
```

Avoid automatic:

```text
Delete

Terminate

Revoke

Modify

Disable
```

during initial security assessment.

Detection and remediation should be separated.

---

# Finding Structure

## 4. Normalize Findings

Different AWS services return different response formats.

Create a common finding structure.

Example:

```python
finding = {
    "service": "EC2",
    "resource": "i-example",
    "region": "ap-northeast-1",
    "issue": "EC2 instance has a public IP address",
    "severity": "REVIEW"
}
```

---

## 5. Why Normalize Findings?

Without normalization:

```text
EC2 Response
S3 Response
GuardDuty Response
Inspector Response
```

all look different.

With normalization:

```text
Service

Resource

Region

Issue

Severity
```

can be processed consistently.

---

# Severity Model

## 6. Simple Severity Levels

For this study project:

```text
INFO

REVIEW

MEDIUM

HIGH

CRITICAL
```

The scanner should not pretend to provide perfect risk scoring.

Severity is context-dependent.

---

## 7. Context Matters

Example:

```text
Public IP
```

alone does not automatically mean:

```text
Critical Risk
```

A public web server may intentionally require a public IP.

Therefore:

```text
Public IP
→ REVIEW
```

can be more appropriate.

But:

```text
SSH
+
0.0.0.0/0
```

may deserve:

```text
HIGH
```

depending on organizational policy.

---

# Scanner Configuration

## 8. Configuration

Example:

```python
PROFILE_NAME = "development"

REGIONS = [
    "ap-northeast-1"
]
```

Later this can be replaced with:

```text
Command-Line Arguments

Configuration Files

Environment Variables

Organization Policy
```

---

# Verify Identity

## 9. Always Verify Identity

Before scanning:

```python
sts = session.client("sts")

identity = sts.get_caller_identity()
```

Print:

```text
Account

Principal

Regions
```

before continuing.

---

## 10. Why Identity Verification Matters

Security automation running against:

```text
Wrong AWS Account
```

can produce misleading results.

For remediation automation, it could be much more dangerous.

---

# Findings Collection

## 11. Findings List

Create:

```python
findings = []
```

Each security check appends findings.

Example:

```python
findings.append({
    "service": "EC2",
    "resource": instance_id,
    "region": region,
    "issue": "Public IP detected",
    "severity": "REVIEW"
})
```

---

# EC2 Public IP Check

## 12. Security Question

Ask:

```text
Which EC2 instances have public IPv4 addresses?
```

---

## 13. Enumeration

Use:

```python
ec2.get_paginator(
    "describe_instances"
)
```

Then inspect:

```python
instance.get(
    "PublicIpAddress"
)
```

---

## 14. Finding Logic

Conceptually:

```python
if public_ip:
    create_finding()
```

This identifies resources that require further review.

---

## 15. Public IP Is Not Automatically Vulnerable

Risk also depends on:

```text
Route Table

Internet Gateway

Security Group

NACL

Host Firewall

Running Service

Application Configuration
```

Therefore the scanner should describe:

```text
Potential Exposure

not

Confirmed Vulnerability
```

---

# Security Group Check

## 16. Security Question

Ask:

```text
Are sensitive ports reachable from the internet?
```

Public IPv4:

```text
0.0.0.0/0
```

Public IPv6:

```text
::/0
```

---

## 17. Sensitive Ports

For a simple learning scanner:

```python
SENSITIVE_PORTS = {
    22: "SSH",
    3389: "RDP",
    3306: "MySQL",
    5432: "PostgreSQL"
}
```

This is only an example security policy.

---

## 18. Security Group Rules

Inspect:

```text
IpProtocol

FromPort

ToPort

IpRanges

Ipv6Ranges
```

Do not rely only on broad EC2 server-side filters.

---

## 19. Why Inspect Each Rule?

AWS Security Group filtering can return a group where separate rules satisfy separate filter criteria.

Therefore:

```text
Filter candidate groups
       ↓
Inspect actual rules
```

is safer than assuming all filter conditions came from the same rule.

---

## 20. Port Range Logic

A rule may allow:

```text
FromPort = 0

ToPort = 65535
```

Therefore do not only check:

```python
from_port == 22
```

Instead:

```python
from_port <= 22 <= to_port
```

---

## 21. IPv4 and IPv6

Check both:

```text
0.0.0.0/0

::/0
```

Ignoring IPv6 can create a visibility gap.

---

# S3 Public Access Block

## 22. Security Question

Ask:

```text
Is bucket-level Public Access Block fully enabled?
```

Use:

```python
s3.get_public_access_block(
    Bucket=bucket_name
)
```

---

## 23. Public Access Block Settings

Review:

```text
BlockPublicAcls

IgnorePublicAcls

BlockPublicPolicy

RestrictPublicBuckets
```

A strict bucket-level configuration typically has all four set to:

```text
True
```

---

## 24. Important Limitation

Bucket-level Public Access Block is only part of the effective S3 access model.

Also consider:

```text
Account-Level Public Access Block

Organization Policies

Bucket Policies

Access Points

ACLs
```

Therefore a scanner should not claim:

```text
Bucket Is Public
```

solely because one bucket-level setting is disabled.

Use wording such as:

```text
Bucket-level Public Access Block is not fully enabled.
```

---

# S3 Encryption

## 25. Security Question

Ask:

```text
What default server-side encryption is configured?
```

Use:

```python
s3.get_bucket_encryption(
    Bucket=bucket_name
)
```

---

## 26. Encryption Algorithms

Common values:

```text
AES256
→ SSE-S3

aws:kms
→ SSE-KMS
```

The scanner can distinguish them.

---

## 27. Example Security Policy

For a learning project:

```text
SSE-S3
→ INFO / REVIEW

SSE-KMS
→ OK
```

if the organization's hypothetical policy requires KMS.

But:

```text
SSE-S3
≠
Unencrypted
```

Do not incorrectly report it as plaintext storage.

---

# GuardDuty Findings

## 28. GuardDuty Workflow

```text
Region
   ↓
List Detectors
   ↓
Detector ID
   ↓
List Findings
   ↓
Get Finding Details
```

---

## 29. Detector

Use:

```python
response = guardduty.list_detectors()
```

If no detector exists:

```text
GuardDuty may not be enabled in this Region.
```

This can itself be useful security coverage information.

---

## 30. Finding IDs

Use:

```python
guardduty.list_findings(
    DetectorId=detector_id
)
```

The API returns finding IDs.

Then retrieve details:

```python
guardduty.get_findings(
    DetectorId=detector_id,
    FindingIds=finding_ids
)
```

---

## 31. Severity

GuardDuty severity is numeric.

Conceptually:

```text
1.0 – 3.9
→ Low

4.0 – 6.9
→ Medium

7.0 – 8.9
→ High

9.0 – 10.0
→ Critical
```

The scanner can map numeric severity into readable categories.

---

# Inspector Findings

## 32. Amazon Inspector

Use the:

```text
inspector2
```

boto3 client.

Example:

```python
inspector = session.client(
    "inspector2",
    region_name=region
)
```

---

## 33. Paginator

Use:

```python
paginator = inspector.get_paginator(
    "list_findings"
)
```

This prevents missing findings in larger environments.

---

## 34. Inspector Finding Fields

Useful information includes:

```text
title

severity

type

resources

status

remediation
```

---

## 35. Inspector Severity

Inspector already provides finding severity.

Examples:

```text
INFORMATIONAL

LOW

MEDIUM

HIGH

CRITICAL
```

Reuse the AWS severity where appropriate.

---

# Security Hub

## 36. Optional Security Hub Integration

Security Hub can be queried using:

```python
securityhub.get_findings()
```

and newer environments also support:

```python
securityhub.get_findings_v2()
```

For Day 42, Security Hub integration can remain optional because the project already gathers GuardDuty and Inspector findings directly.

---

## 37. Why Keep It Optional?

The goal today is:

```text
Build Security Automation Logic
```

not:

```text
Integrate Every AWS Security Service
```

Start small and keep the project understandable.

---

# Error Handling

## 38. One Failure Should Not Stop Everything

Suppose:

```text
S3 AccessDenied
```

occurs.

The scanner should ideally continue checking:

```text
EC2

GuardDuty

Inspector
```

rather than terminating the entire scan.

---

## 39. Handle ClientError

Example:

```python
try:
    ...
except ClientError as error:
    ...
```

Record errors separately if needed.

---

## 40. Expected Missing Configuration

Some API failures can represent expected configuration states.

Example:

```text
NoSuchPublicAccessBlockConfiguration
```

may mean a bucket-level Public Access Block configuration does not exist.

The scanner should distinguish:

```text
Configuration Missing

from

Scanner Failure
```

---

# Multi-Region Scanning

## 41. Scan Approved Regions

Example:

```python
REGIONS = [
    "ap-northeast-1",
    "ap-northeast-3"
]
```

Then:

```python
for region in REGIONS:
    run_region_checks()
```

---

## 42. Why Not Assume One Region?

Security services and resources such as:

```text
EC2

GuardDuty

Inspector

KMS
```

are Regional.

Therefore:

```text
One Region Scanned
≠
Entire Account Scanned
```

---

# Multi-Account Future Design

## 43. Current Project

Day 42 can scan:

```text
One Account
+
Multiple Regions
```

---

## 44. Future Design

An organization-level scanner could:

```text
Security Account
      |
      v
AssumeRole
      |
      +-- Prod
      +-- Dev
      +-- Network
      |
      v
Run Same Checks
```

This is a natural future portfolio extension.

---

# JSON Reporting

## 45. Why JSON?

JSON provides structured output that can later be consumed by:

```text
Python

SIEM

Lambda

Security Hub

Dashboards

CI/CD

Ticketing Systems
```

---

## 46. Example Report

```json
{
  "summary": {
    "finding_count": 2
  },
  "findings": [
    {
      "service": "EC2",
      "resource": "i-example",
      "region": "ap-northeast-1",
      "issue": "Public IP detected",
      "severity": "REVIEW"
    }
  ]
}
```

---

## 47. Do Not Commit Real Reports

Security reports can contain:

```text
Account IDs

Resource IDs

Internal Architecture

Vulnerabilities

Finding Details
```

Therefore add real generated reports to:

```text
.gitignore
```

---

# Security Scanner Design

## 48. Functions

Recommended structure:

```text
verify_identity()

check_public_ec2()

check_security_groups()

check_s3_security()

get_guardduty_findings()

get_inspector_findings()

write_report()
```

---

## 49. Main Workflow

```text
main()
  |
  +-- Create Session
  |
  +-- Verify Identity
  |
  +-- For Each Region
  |      |
  |      +-- EC2 Check
  |      +-- Security Group Check
  |      +-- GuardDuty
  |      +-- Inspector
  |
  +-- S3 Check
  |
  +-- Generate Report
```

---

# Security Automation Principle

## 50. Detection Before Remediation

For this project:

```text
Detect
→ Report
```

not:

```text
Detect
→ Automatically Delete / Modify
```

Automated remediation requires additional considerations:

```text
False Positives

Business Context

Rollback

Approval

Evidence Preservation

Production Impact
```

---

## 51. Human-in-the-Loop

A safe initial model:

```text
Automation
   ↓
Finding
   ↓
Human Review
   ↓
Decision
   ↓
Remediation
```

This is appropriate for the current learning stage.

---

# Common Mistakes

## 52. Treating Public IP as a Vulnerability

Incorrect:

```text
Public IP
=
Critical Vulnerability
```

Correct:

```text
Public IP
=
Requires Contextual Review
```

---

## 53. Treating SSE-S3 as No Encryption

Incorrect:

```text
AES256
=
Unencrypted
```

Correct:

```text
AES256
=
SSE-S3
```

---

## 54. Checking Only IPv4

Incorrect:

```text
0.0.0.0/0 only
```

Also check:

```text
::/0
```

---

## 55. Ignoring Port Ranges

Rule:

```text
0-65535
```

includes:

```text
22

3389

3306

5432
```

The scanner must evaluate ranges.

---

## 56. Ignoring Pagination

A successful script does not guarantee complete security coverage.

Use paginators where supported.

---

## 57. Logging Sensitive Data

Avoid putting:

```text
Credentials

Secrets

Customer Data

Complete IAM Policies
```

into generated logs or public reports.

---

# Hands-on Practice

## 58. Run Identity Check

```bash
python scripts/check_identity.py
```

Verify:

```text
Account

Principal

Region
```

---

## 59. Run Security Scanner

Example:

```bash
python scripts/security_scan.py
```

Expected conceptual output:

```text
AWS Security Scan

Checking ap-northeast-1...

[REVIEW] EC2 instance has public IP

[HIGH] Security Group exposes SSH to 0.0.0.0/0

Checking S3...

Security scan completed.

Findings: 2
```

---

## 60. Review JSON Report

Example:

```text
reports/security-report.json
```

Inspect:

```text
Service

Resource

Region

Issue

Severity
```

Do not commit a real report.

---

# Suggested Repository Structure

```text
aws-cloud-security/
├── README.md
├── .gitignore
│
├── notes/
│   └── day42-security-automation-boto3.md
│
├── scripts/
│   ├── check_identity.py
│   ├── list_ec2.py
│   ├── list_s3.py
│   ├── list_roles.py
│   └── security_scan.py
│
└── reports/
    └── .gitkeep
```

The `reports/` directory can exist while generated reports remain ignored.

---

# Security Checklist

```text
[ ] Scanner uses read-only AWS APIs

[ ] Current identity is verified before scanning

[ ] AWS profile is explicit

[ ] Scan Regions are explicit

[ ] EC2 enumeration uses pagination

[ ] Public IP findings are treated as review items, not confirmed vulnerabilities

[ ] Security Group rules check IPv4 and IPv6

[ ] Security Group port ranges are evaluated correctly

[ ] S3 Public Access Block is reviewed

[ ] Effective S3 public access limitations are understood

[ ] S3 encryption algorithm is identified correctly

[ ] SSE-S3 is not reported as unencrypted

[ ] GuardDuty coverage is checked per Region

[ ] GuardDuty findings are retrieved safely

[ ] Inspector findings use pagination

[ ] Findings use a normalized structure

[ ] Errors do not unnecessarily stop the entire scan

[ ] Security reports contain no credentials

[ ] Real reports are excluded from Git

[ ] Automatic remediation is not enabled without additional safeguards
```

---

## Key Takeaways

- boto3 can convert repetitive AWS security checks into reusable automation.
- Security automation should verify identity and Region before scanning.
- AWS resources should be enumerated with pagination where supported.
- Findings from different services should be normalized into a common format.
- Public exposure must be evaluated with context rather than automatically treated as a vulnerability.
- Security Group automation should inspect actual individual rules and include IPv6.
- S3 Public Access Block is only one part of effective S3 access.
- SSE-S3 is valid server-side encryption and should not be reported as unencrypted.
- GuardDuty provides threat findings while Inspector provides vulnerability findings.
- Multi-Region coverage must be explicitly designed.
- Detection and automated remediation should initially remain separate.
- JSON reports provide a foundation for future integrations with SIEM, dashboards, CI/CD, and security platforms.

---

## Reflection

Today I learned how to move from basic boto3 API usage to practical AWS security automation.

Instead of only listing AWS resources, I can now evaluate resource configurations, create normalized findings, assign simple severity levels, and generate structured security reports.

I also learned that security automation requires careful interpretation. A public IP is not automatically a vulnerability, an S3 bucket without a specific KMS configuration is not necessarily unencrypted, and a missing GuardDuty finding does not guarantee that a Region is fully monitored.

The most important lesson is that automation should improve security visibility without removing context. Detection, evidence collection, and reporting can be automated safely, while remediation should be introduced only after false positives, production impact, approvals, and rollback strategies are considered.

---

## Vocabulary

| Word | Meaning |
|---|---|
| False Positive | Finding reported as risky even though the configuration is legitimate |
| Finding | Structured security observation produced by a scanner or security service |
| Human-in-the-Loop | Model where automation detects issues but humans approve important actions |
| Normalization | Converting different data formats into a consistent structure |
| Remediation | Action taken to correct or reduce a security risk |
| Report | Structured output containing the results of a security assessment |
| Security Automation | Using code to perform repeatable security monitoring and operational tasks |
| Security Coverage | Scope of accounts, Regions, resources, and services being monitored |
| Security Scanner | Tool that evaluates resources against security rules and generates findings |
| Severity | Classification used to communicate the potential importance of a finding |
