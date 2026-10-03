# Day 30 — Amazon Inspector

## Topic

Amazon Inspector Fundamentals, Vulnerability Management, CVEs, Risk Prioritization, and Remediation

---

## Objectives

- Understand the purpose of Amazon Inspector
- Understand continuous vulnerability scanning
- Learn which AWS resources Inspector supports
- Understand EC2 vulnerability scanning
- Understand ECR container image scanning
- Understand Lambda vulnerability scanning
- Learn the meaning of CVE and CVSS
- Understand EPSS and exploit intelligence
- Learn how Inspector prioritizes findings
- Understand Inspector risk scores
- Learn package vulnerability findings
- Understand code vulnerability findings
- Understand network reachability findings where applicable
- Learn how Inspector integrates with Security Hub
- Practice reviewing and prioritizing vulnerabilities
- Identify common vulnerability management mistakes

---

# Inspector Fundamentals

## 1. What Is Amazon Inspector?

Amazon Inspector is a managed vulnerability management service.

It continuously scans supported AWS workloads for software vulnerabilities and exposure-related risks.

Conceptually:

```text
AWS Workloads
     |
     +-- EC2
     |
     +-- ECR Images
     |
     +-- Lambda
     |
     v
Amazon Inspector
     |
     v
Vulnerability Findings
     |
     v
Risk Prioritization
     |
     v
Remediation
```

Inspector helps identify weaknesses before they are exploited.

---

## 2. Inspector vs GuardDuty

This distinction is important.

### Amazon GuardDuty

```text
Threat Detection
```

Question:

```text
Is suspicious activity happening now?
```

### Amazon Inspector

```text
Vulnerability Management
```

Question:

```text
What known weaknesses exist in my workloads?
```

Conceptually:

```text
Inspector
→ Potential Weakness

GuardDuty
→ Suspicious Activity

Security Hub
→ Aggregate Both
```

---

## 3. Why Vulnerability Management Matters

A vulnerability does not automatically mean compromise.

Example:

```text
Vulnerable Package
      |
      v
CVE Exists
```

This means:

```text
Potential Security Weakness
```

not:

```text
Attack Confirmed
```

However, if the vulnerable resource is:

```text
Internet-Facing

Exploitable

Production

Contains Sensitive Data
```

the risk can become much higher.

---

# Continuous Scanning

## 4. Continuous Assessment

Amazon Inspector continuously monitors supported resources.

Conceptually:

```text
Resource Created
      |
      v
Inspector Discovers Resource
      |
      v
Scan
      |
      v
New Vulnerability Data Available
      |
      v
Re-Evaluate Resource
```

This means vulnerability assessment is not just a one-time scan.

---

## 5. Why Continuous Scanning Matters

A system that is secure today may become vulnerable tomorrow.

Example:

```text
Day 1
Package Version
→ No Known CVE

Day 20
New CVE Published

Same Package
→ Now Vulnerable
```

Continuous assessment allows Inspector to generate new findings when new vulnerability intelligence becomes available.

---

# Supported Resources

## 6. Main Inspector Resource Types

Amazon Inspector supports scanning of:

```text
Amazon EC2

Amazon ECR Container Images

AWS Lambda
```

Different resource types have different scan mechanisms and finding types.

---

# EC2 Scanning

## 7. EC2 Vulnerability Scanning

Inspector can assess supported EC2 instances for software package vulnerabilities.

Conceptually:

```text
EC2 Instance
      |
      v
Installed Packages
      |
      v
Inspector
      |
      v
Known Vulnerabilities
```

Potential examples:

```text
OpenSSL Vulnerability

Linux Kernel Vulnerability

Apache Vulnerability

Python Package Vulnerability
```

---

## 8. EC2 Scanning Methods

Inspector can use Systems Manager-based scanning or agentless mechanisms depending on supported configuration.

Conceptually:

```text
EC2
 |
 +-- SSM-Based Scan
 |
 +-- Agentless Scan
```

The exact scan method depends on account configuration and supported operating systems.

---

## 9. Systems Manager Dependency

For SSM-based package scanning, the instance generally requires appropriate Systems Manager support.

Conceptually:

```text
EC2
 |
 v
SSM Agent
 |
 v
Systems Manager
 |
 v
Inspector
```

If an EC2 instance is not eligible for scanning, investigate:

```text
SSM Agent

IAM Role

Network Connectivity

Supported OS

Inspector Coverage
```

---

# ECR Scanning

## 10. Container Image Scanning

Amazon Inspector integrates with Amazon ECR to scan container images.

Conceptually:

```text
Container Image
      |
      v
Amazon ECR
      |
      v
Inspector
      |
      v
Package Vulnerabilities
```

This helps identify vulnerabilities before images are deployed.

---

## 11. Image Scan Timing

Container image scanning can occur when:

```text
Image Pushed

Image Updated

New CVE Intelligence Available
```

Conceptually:

```text
ECR Image
   |
   v
Scan
   |
   v
Clean Today
   |
   v
New CVE Tomorrow
   |
   v
Re-Evaluated
```

---

## 12. Image Tags Are Not Security Boundaries

Example:

```text
prod-latest
```

is only a tag.

A tag does not guarantee that the image is secure.

Security decisions should use:

```text
Image Digest

Vulnerability Findings

Build Provenance

Deployment Policy
```

where appropriate.

---

# Lambda Scanning

## 13. Lambda Standard Scanning

Inspector can scan supported Lambda function dependencies for package vulnerabilities.

Conceptually:

```text
Lambda Function
      |
      v
Dependencies
      |
      v
Inspector
      |
      v
Package Findings
```

Examples may include vulnerable:

```text
Python Libraries

Node.js Packages

Java Dependencies
```

---

## 14. Lambda Code Scanning

Inspector can also perform code scanning for supported Lambda functions.

Conceptually:

```text
Lambda Source Code
      |
      v
Static Analysis
      |
      v
Code Vulnerability Finding
```

Potential examples can include:

```text
Hard-Coded Credentials

Injection Risks

Insecure Cryptographic Usage

Unsafe Code Patterns
```

The exact detection depends on supported languages and analyzers.

---

# CVE

## 15. What Is a CVE?

CVE stands for:

```text
Common Vulnerabilities and Exposures
```

A CVE identifier looks like:

```text
CVE-2026-XXXX
```

It provides a standardized identifier for a publicly disclosed vulnerability.

---

## 16. CVE Example

Conceptually:

```text
CVE-2026-12345
```

may describe:

```text
Software:
Example Library

Affected Versions:
1.0 – 1.4

Fixed Version:
1.5
```

If an EC2 instance contains version:

```text
1.3
```

Inspector may create a finding.

---

# CVSS

## 17. What Is CVSS?

CVSS stands for:

```text
Common Vulnerability Scoring System
```

It provides a numeric severity score.

Typical range:

```text
0.0 – 10.0
```

General categories include:

```text
Low

Medium

High

Critical
```

---

## 18. CVSS Is Not the Entire Risk

Suppose:

```text
CVE A
CVSS 9.8
```

but:

```text
Not Reachable

No Known Exploit

Unused Package
```

Compare with:

```text
CVE B
CVSS 8.0

Internet-Facing

Known Exploit

Actively Exploited
```

The second may deserve more urgent attention.

Therefore:

```text
CVSS
≠
Complete Risk Priority
```

---

# EPSS

## 19. What Is EPSS?

EPSS stands for:

```text
Exploit Prediction Scoring System
```

It estimates the probability that a vulnerability will be exploited in the wild.

Conceptually:

```text
CVE
 |
 +-- CVSS
 |   → How severe?
 |
 +-- EPSS
     → How likely to be exploited?
```

This helps security teams prioritize vulnerabilities.

---

## 20. Why EPSS Matters

Example:

```text
CVE A

CVSS:
9.8

EPSS:
Very Low
```

versus:

```text
CVE B

CVSS:
8.1

EPSS:
High
```

The second vulnerability may deserve faster remediation depending on exposure and business context.

---

# Exploit Intelligence

## 21. Known Exploit Information

Inspector can use exploit intelligence to indicate whether public exploit information is associated with a vulnerability.

Conceptually:

```text
CVE
 |
 +-- Exploit Available?
 |
 +-- Known Exploit Activity?
```

This helps improve remediation priority.

---

## 22. Exploitability and Context

A useful prioritization model is:

```text
Vulnerability Severity
        +
Exploit Availability
        +
EPSS
        +
Network Exposure
        +
Resource Criticality
        =
Remediation Priority
```

---

# Inspector Risk Score

## 23. Inspector Score

Amazon Inspector can assign an Inspector score to supported vulnerability findings.

Conceptually:

```text
Base CVSS
   |
   v
AWS Context
   |
   v
Inspector Risk Adjustment
   |
   v
Inspector Score
```

Inspector can adjust risk based on contextual factors.

---

## 24. Why Context Matters

Example:

```text
Vulnerability
CVSS 9.8
```

but resource:

```text
Private

Not Internet Reachable
```

Inspector may adjust prioritization differently than a resource that is:

```text
Publicly Reachable

Production

Internet-Facing
```

Context improves practical prioritization.

---

# Finding Types

## 25. Package Vulnerability Finding

Generated when Inspector identifies a vulnerable software package.

Example:

```text
EC2
   |
   v
openssl 3.x
   |
   v
Known CVE
   |
   v
Inspector Finding
```

Finding details may include:

```text
Package Name

Installed Version

Fixed Version

CVE

Severity

CVSS

Exploit Information

EPSS
```

---

## 26. Code Vulnerability Finding

Generated for supported Lambda code scanning.

Example:

```text
Lambda Code
    |
    v
Insecure Pattern
    |
    v
Inspector Finding
```

Possible categories may include:

```text
Injection

Credential Exposure

Cryptographic Weakness

Unsafe API Usage
```

---

# Network Reachability

## 27. Reachability Context

Inspector can incorporate network exposure context into vulnerability prioritization for supported resources.

Conceptually:

```text
EC2 Vulnerability
      |
      +-- Internet Reachable?
      |
      +-- Network Path?
```

This helps distinguish:

```text
Critical but isolated

from

Critical and exposed
```

---

## 28. Exposure Matters

Compare:

```text
Instance A

CVE:
High

Private Subnet

Restricted SG
```

with:

```text
Instance B

Same CVE

Public IP

0.0.0.0/0
```

Instance B may represent greater practical risk.

---

# Remediation

## 29. Remediation Information

Inspector findings can provide remediation guidance.

Example:

```text
Installed Version:
1.2.3

Fixed Version:
1.2.8
```

Possible remediation:

```text
Upgrade Package
```

or:

```text
Rebuild Image
```

---

## 30. Patch vs Rebuild

For EC2:

```text
Patch Existing Instance
```

may be appropriate.

For immutable infrastructure:

```text
Build New AMI

Patch Image

Redeploy

Terminate Old Instance
```

may be preferable.

---

## 31. Container Remediation

Poor:

```text
Patch Running Container Manually
```

Better:

```text
Update Base Image
      |
      v
Rebuild Container Image
      |
      v
Push to ECR
      |
      v
Rescan
      |
      v
Redeploy
```

This preserves reproducibility.

---

## 32. Lambda Remediation

Example:

```text
Vulnerable Dependency
      |
      v
Update package version
      |
      v
Rebuild deployment
      |
      v
Deploy Lambda
      |
      v
Inspector Re-Evaluates
```

---

# Finding Status

## 33. Finding Lifecycle

Inspector findings can change over time.

Conceptually:

```text
Vulnerability Detected
      |
      v
ACTIVE
      |
      v
Remediation
      |
      v
CLOSED
```

The exact lifecycle depends on resource and finding type.

---

## 34. Findings Can Reappear

A vulnerability can return if:

```text
Old Image Redeployed

Vulnerable Package Reinstalled

New Resource Created

New CVE Published
```

Therefore:

```text
Closed Finding
≠
Permanent Security
```

---

# Suppression

## 35. Suppression Rules

Inspector supports suppression rules for findings matching selected criteria.

Conceptually:

```text
Finding
   |
   v
Suppression Rule
   |
   v
Suppressed
```

Use cases might include:

```text
Accepted Risk

Non-Production Test Resource

Compensating Control
```

---

## 36. Suppression Risks

Poor rule:

```text
Suppress All Medium Findings
```

This may hide meaningful vulnerabilities.

Better:

```text
Specific CVE

Specific Resource

Specific Environment

Documented Exception
```

Suppression should be reviewed periodically.

---

# Security Hub Integration

## 37. Inspector and Security Hub

Inspector findings can be sent to Security Hub.

Conceptually:

```text
Inspector
    |
    v
Vulnerability Finding
    |
    v
Security Hub
    |
    v
ASFF
    |
    v
Central Triage
```

This connects Day 30 directly to Day 29.

---

## 38. Combined Security View

Example:

```text
Inspector
→ Critical Vulnerability

GuardDuty
→ Suspicious EC2 Activity

Security Hub
→ Both Findings on Same Resource
```

This combination is more concerning than either finding alone.

---

# Vulnerability Prioritization

## 39. Poor Prioritization

Poor strategy:

```text
Sort by CVSS

Patch from 10.0 downward
```

This ignores:

```text
Exposure

Exploit Activity

Business Criticality

Compensating Controls
```

---

## 40. Better Prioritization

A stronger model:

```text
Severity
   +
Exploitability
   +
EPSS
   +
Internet Exposure
   +
Asset Criticality
   +
Data Sensitivity
   =
Priority
```

---

## 41. Example Priority

### Finding A

```text
CVSS:
9.8

Internet:
No

EPSS:
Low

Resource:
Development
```

### Finding B

```text
CVSS:
8.4

Internet:
Yes

EPSS:
High

Exploit:
Available

Resource:
Production
```

Finding B may deserve more urgent remediation depending on context.

---

# Common Misconfigurations

## 42. Inspector Not Enabled Everywhere

Example:

```text
Tokyo
→ Enabled

Singapore
→ Disabled
```

A vulnerable workload in Singapore may not receive expected coverage.

Review:

```text
Accounts

Regions

Resource Types
```

---

## 43. Unsupported / Unmanaged EC2

An EC2 instance may not be scanned correctly because of:

```text
Unsupported OS

SSM Problems

Missing Permissions

Network Problems
```

Coverage should be monitored.

---

## 44. ECR Images Never Remediated

Poor process:

```text
Finding
→ Ignore
→ Deploy Vulnerable Image
```

Better:

```text
Finding
→ Fix Dependency
→ Rebuild
→ Rescan
→ Deploy
```

---

## 45. Patch Without Testing

Poor:

```text
Critical CVE
→ Patch Production Immediately
→ Application Breaks
```

Better:

```text
Assess

Test

Deploy

Validate
```

Urgency should be balanced with service stability.

---

## 46. Suppress Everything Noisy

Noise should not be handled by blindly suppressing large categories.

Better:

```text
Tune Scope

Fix Root Causes

Document Exceptions

Review Suppression
```

---

## 47. Scanner Without Ownership

If no team owns remediation:

```text
Inspector Finding
      |
      v
Nobody Acts
```

Vulnerability scanning alone provides limited security value.

Define:

```text
Owner

SLA

Priority

Remediation Process
```

---

# Vulnerability Management Workflow

## 48. End-to-End Process

```text
Discover Resource
       |
       v
Scan
       |
       v
Find Vulnerability
       |
       v
Assess Risk
       |
       v
Prioritize
       |
       v
Assign Owner
       |
       v
Remediate
       |
       v
Rescan
       |
       v
Close
```

---

## 49. Remediation SLA

Organizations may define SLA by severity and context.

Example concept:

```text
Critical + Internet-Facing
→ Immediate / Very Short SLA

High
→ Short SLA

Medium
→ Normal Patch Cycle

Low
→ Planned Remediation
```

Exact timelines should depend on organizational policy.

---

# Investigation Scenario

## 50. Scenario

Inspector reports:

```text
Critical CVE

Resource:
Production EC2

Internet Reachable:
Yes

Exploit Available:
Yes
```

Investigation should include:

```text
Is the service exposed?

Is the vulnerable package running?

Is the vulnerable feature used?

Is there evidence of exploitation?

Are GuardDuty findings present?

What does CloudTrail show?

What do OS logs show?
```

---

## 51. Correlating with GuardDuty

If Inspector says:

```text
Critical Vulnerability
```

and GuardDuty says:

```text
Suspicious Network Activity
```

on the same EC2 instance:

```text
Risk Priority
↑
```

because there may be evidence that the vulnerability is being targeted or exploited.

---

## 52. Correlating with AWS Config

AWS Config can help answer:

```text
When did the Security Group become public?

Was this instance recently exposed?

Did the network configuration change?
```

This can help explain why the vulnerable resource became reachable.

---

## 53. Correlating with CloudTrail

CloudTrail can answer:

```text
Who changed the Security Group?

Who launched the instance?

Who modified the IAM Role?

Who changed Inspector configuration?
```

---

# Multi-Account Inspector

## 54. Delegated Administrator

AWS Organizations can use a delegated administrator for Inspector.

Conceptually:

```text
AWS Organizations
       |
       v
Security Account
       |
       v
Inspector Delegated Administrator
       |
       +-- Production
       |
       +-- Development
       |
       +-- Shared Services
```

This supports centralized vulnerability management.

---

## 55. Auto-Enable

Organizations can configure automatic enablement for supported Inspector scan types.

This helps prevent gaps when:

```text
New Account Created

New Workload Added
```

Security baselines should define required coverage.

---

# Hands-on Practice

## 56. Practice — Open Amazon Inspector

Navigate:

```text
AWS Console
   |
   v
Amazon Inspector
```

Review:

```text
Dashboard

Coverage

Findings

Account Management
```

---

## 57. Practice — Coverage

Open:

```text
Inspector
→ Coverage
```

Review resources by type:

```text
EC2

ECR

Lambda
```

Identify:

```text
Covered

Not Covered

Reason
```

Coverage problems are security problems because unscanned resources create visibility gaps.

---

## 58. Practice — Review a Finding

Select one finding.

Record:

```text
Finding Type:

Severity:

CVE:

Resource:

Package:

Installed Version:

Fixed Version:

CVSS:

EPSS:

Exploit Available:

Network Exposure:
```

Not every field will be present for every finding.

---

## 59. Practice — Prioritize Findings

Choose three findings and rank them based on:

```text
Severity

Exploit Availability

EPSS

Internet Reachability

Production vs Development

Resource Criticality
```

Do not rank by CVSS alone.

---

## 60. Practice — Review ECR

If ECR is available:

```text
ECR
→ Repository
→ Image
→ Scan Results
```

Review:

```text
Image Digest

Image Tag

Critical Findings

High Findings

Package Details
```

Do not deploy a vulnerable image solely for practice.

---

## 61. Practice — Review Lambda

If Lambda scanning is enabled:

```text
Inspector
→ Lambda Findings
```

Review:

```text
Package Vulnerability

Code Vulnerability

Function Name

Runtime

Dependency
```

---

## 62. Optional CLI Practice

List findings:

```bash
aws inspector2 list-findings
```

Filter by severity:

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

Check account status:

```bash
aws inspector2 batch-get-account-status
```

List coverage:

```bash
aws inspector2 list-coverage
```

Do not publish real account IDs, resource ARNs, private image names, or vulnerability details tied to customer systems in a public repository.

---

# Architecture Exercise

## 63. Secure Vulnerability Management Architecture

```text
AWS Organization
       |
       v
Security Account
       |
       v
Amazon Inspector
       |
       +----------------------+
       |          |           |
       v          v           v
      EC2        ECR        Lambda
       |          |           |
       +----------+-----------+
                  |
                  v
               Findings
                  |
                  v
            Security Hub
                  |
                  v
          Security Operations
```

---

## 64. DevSecOps Flow

A mature container workflow can look like:

```text
Developer
   |
   v
Build Image
   |
   v
Push to ECR
   |
   v
Inspector Scan
   |
   +-- Acceptable
   |      |
   |      v
   |   Deploy
   |
   +-- High Risk
          |
          v
       Rebuild
```

This shifts vulnerability detection earlier in the deployment lifecycle.

---

# Security Checklist

```text
[ ] Inspector is enabled in required accounts

[ ] Required Regions are covered

[ ] EC2 scanning is enabled

[ ] ECR scanning is enabled

[ ] Lambda scanning is enabled where required

[ ] Lambda code scanning is enabled where appropriate

[ ] Inspector coverage is monitored

[ ] Unsupported or unscanned resources are investigated

[ ] Critical and High findings have remediation owners

[ ] Findings are prioritized using context, not CVSS alone

[ ] EPSS is considered where available

[ ] Exploit intelligence is reviewed

[ ] Internet exposure is considered

[ ] Production resources receive higher priority where appropriate

[ ] ECR images are rebuilt after vulnerable dependencies are fixed

[ ] Lambda dependencies are updated and redeployed

[ ] Findings are integrated with Security Hub

[ ] Suppression rules are narrowly scoped

[ ] Exceptions are documented

[ ] Remediation SLAs are defined

[ ] Rescanning confirms remediation
```

---

## Key Takeaways

- Amazon Inspector is a managed vulnerability management service.
- Inspector continuously assesses supported EC2, ECR, and Lambda resources.
- Continuous scanning allows new findings to appear when new CVEs are published.
- EC2 scanning identifies vulnerable software packages on supported instances.
- ECR scanning identifies vulnerabilities in container image packages.
- Lambda scanning can identify package and supported code vulnerabilities.
- CVE provides a standardized vulnerability identifier.
- CVSS measures technical vulnerability severity.
- EPSS estimates the likelihood of exploitation in the wild.
- Exploit intelligence can help determine whether a vulnerability has known exploit activity.
- Inspector uses AWS context to improve vulnerability prioritization.
- CVSS alone should not determine remediation priority.
- Internet exposure, exploitability, resource criticality, and business context should also be considered.
- Vulnerability scanning must be connected to ownership and remediation processes.
- Inspector findings can be centralized in Security Hub.
- Suppression should be narrowly scoped and documented.
- A vulnerability finding does not automatically mean the resource has been compromised.

---

## Reflection

Today I learned that Amazon Inspector provides continuous vulnerability management for AWS workloads.

The most important lesson is that vulnerability severity and real-world risk are not the same thing.

A CVSS score describes the technical severity of a vulnerability, while factors such as exploit availability, EPSS, network exposure, and resource criticality help determine how urgently the vulnerability should be remediated.

I also learned that vulnerability management is a lifecycle rather than a scan. Security teams must discover resources, assess vulnerabilities, prioritize findings, assign remediation owners, fix the issue, rescan the resource, and verify that the vulnerability is resolved.

From a cloud security perspective, Amazon Inspector becomes even more useful when its findings are correlated with GuardDuty, Security Hub, AWS Config, and CloudTrail.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Code Vulnerability | A potentially insecure pattern detected in application source code |
| CVE | Standard identifier for a publicly disclosed vulnerability |
| CVSS | Scoring system used to measure technical vulnerability severity |
| EPSS | Probability estimate for whether a vulnerability is likely to be exploited |
| Exploit Intelligence | Information about known or available exploitation of a vulnerability |
| Inspector Score | AWS Inspector-adjusted score that considers AWS environmental context |
| Package Vulnerability | A vulnerability found in an installed software package or dependency |
| Remediation | Action taken to correct or reduce a vulnerability |
| Vulnerability | A weakness that could potentially be exploited |
| Vulnerability Management | Continuous process of finding, prioritizing, fixing, and verifying vulnerabilities |
