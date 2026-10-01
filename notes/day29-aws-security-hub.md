# Day 29 — AWS Security Hub

## Topic

AWS Security Hub CSPM Fundamentals, ASFF Findings, Security Standards, Controls, Aggregation, and Automation

---

## Objectives

- Understand the purpose of AWS Security Hub CSPM
- Understand the difference between threat detection and security posture management
- Understand AWS Security Finding Format
- Learn how Security Hub ingests findings from other services
- Understand security standards and controls
- Understand security scores
- Learn finding workflow status
- Understand automation rules
- Understand EventBridge-based response
- Learn cross-Region aggregation
- Understand delegated administrator and central configuration
- Understand finding suppression
- Practice reviewing and triaging Security Hub findings
- Identify common Security Hub operational mistakes

---

# Security Hub Fundamentals

## 1. What Is AWS Security Hub?

AWS Security Hub CSPM is a cloud security posture management and finding aggregation service.

It can collect and normalize security findings from:

```text
Security Hub Controls

Amazon GuardDuty

Amazon Inspector

Amazon Macie

Other AWS Services

Third-Party Products

Custom Integrations
```

Conceptually:

```text
GuardDuty ───────┐
Inspector ───────┤
Macie ───────────┤
Security Controls├──> Security Hub CSPM
Third-Party ─────┤
Custom Findings ─┘
                         |
                         v
                Normalized Findings
                         |
                         v
                  Central Security View
```

---

## 2. Why Security Hub Matters

Without a centralized security finding service:

```text
GuardDuty Console

Inspector Console

Macie Console

Config Console

Third-Party Console
```

Security teams must review multiple systems separately.

With Security Hub:

```text
Multiple Security Sources
          |
          v
     Security Hub
          |
          v
 Unified Finding View
```

This helps with:

```text
Prioritization

Triage

Compliance

Security Posture

Automation

Investigation
```

---

## 3. GuardDuty vs Security Hub

This distinction is important.

### GuardDuty

```text
Threat Detection
```

Question:

```text
Is suspicious or malicious activity happening?
```

Examples:

```text
Compromised Credential

Malicious Network Activity

Suspicious API Behavior
```

### Security Hub

```text
Security Posture
+
Finding Aggregation
```

Question:

```text
What security issues exist across the environment?
```

Conceptually:

```text
GuardDuty
→ Detect Threat

Security Hub
→ Aggregate, Normalize, Prioritize, Manage
```

Security Hub does not replace GuardDuty.

---

# AWS Security Finding Format

## 4. What Is ASFF?

AWS Security Finding Format, or ASFF, is a standardized format for security findings.

Different security products generate different data.

Security Hub normalizes them into:

```text
ASFF
```

Conceptually:

```text
GuardDuty Finding
       |
       v

Inspector Finding
       |
       v

Macie Finding
       |
       v

ASFF
       |
       v
Security Hub
```

This makes findings easier to process consistently.

---

## 5. Why Normalize Findings?

Without normalization:

```text
GuardDuty
→ Format A

Inspector
→ Format B

Macie
→ Format C
```

Automation becomes complicated.

With ASFF:

```text
Multiple Products
       |
       v
Common Finding Schema
       |
       v
Unified Automation
```

This helps:

```text
Filtering

Automation

Integration

Reporting

Triage
```

---

## 6. Important ASFF Fields

Common finding information includes:

```text
Id

ProductArn

GeneratorId

AwsAccountId

Types

FirstObservedAt

LastObservedAt

CreatedAt

UpdatedAt

Severity

Resources

Compliance

Workflow

RecordState
```

Not every finding uses every field in the same way.

---

## 7. Severity

Findings can contain severity information.

Conceptually:

```text
Finding
   |
   v
Severity
   |
   v
Triage Priority
```

Security teams should not use severity alone.

Also consider:

```text
Resource Criticality

Internet Exposure

Data Sensitivity

Threat Context

Business Impact
```

---

# Security Standards

## 8. What Is a Security Standard?

A security standard is a collection of security requirements.

Security Hub maps standards to security controls.

Conceptually:

```text
Security Standard
       |
       v
Security Controls
       |
       v
Security Checks
       |
       v
Findings
```

Standards can be based on:

```text
AWS Best Practices

Industry Frameworks

Regulatory Requirements
```

---

## 9. AWS Foundational Security Best Practices

One important standard is:

```text
AWS Foundational Security Best Practices
```

It evaluates AWS resources against AWS security recommendations.

Examples of controls may check:

```text
S3 Public Access

EBS Encryption

RDS Encryption

IAM Security

CloudTrail Configuration

Security Group Exposure
```

---

## 10. Other Standards

Security Hub supports multiple standards.

Examples may include:

```text
AWS Foundational Security Best Practices

CIS AWS Foundations Benchmark

NIST Standards

PCI DSS

AI Security Best Practices
```

The exact standards available can evolve over time.

Enable standards that match:

```text
Security Requirements

Compliance Requirements

Organizational Policies
```

---

# Security Controls

## 11. What Is a Security Control?

A security control represents a specific security requirement.

Example:

```text
EBS volumes should be encrypted.
```

Conceptually:

```text
Control
   |
   v
Security Check
   |
   v
Resource
   |
   +-- Passed
   |
   +-- Failed
```

---

## 12. Control Findings

When a control checks a resource, Security Hub can generate a control finding.

Example:

```text
Control:

EBS Encryption Required

Resource:

vol-example

Result:

FAILED
```

The finding is represented using ASFF.

---

## 13. Consolidated Controls

A single security concept may appear in multiple standards.

Example:

```text
EBS Encryption
```

could be relevant to:

```text
AWS Best Practices

CIS

NIST
```

Consolidated controls help Security Hub treat the same underlying security control consistently across standards.

---

## 14. Compliance Status

Control findings can include compliance information.

Conceptually:

```text
Security Check
      |
      +-- PASSED
      |
      +-- FAILED
      |
      +-- WARNING
      |
      +-- NOT_AVAILABLE
```

The exact result depends on the control.

A failed control means:

```text
Configuration Requirement Not Met
```

It does not automatically mean:

```text
Active Security Compromise
```

---

# Security Score

## 15. What Is the Security Score?

Security Hub calculates a security score based on enabled controls with available data.

Conceptually:

```text
Passed Controls
      /
Enabled Evaluated Controls
      |
      v
Security Score
```

Displayed as:

```text
0–100%
```

---

## 16. Security Score Interpretation

Example:

```text
80%
```

does not mean:

```text
Environment Is 80% Secure
```

It means the score reflects the proportion of evaluated enabled controls that passed according to Security Hub's scoring model.

Therefore:

```text
Security Score
≠
Absolute Security Measurement
```

It is a posture indicator.

---

## 17. Security Score Limitations

A high score does not guarantee:

```text
No Malware

No Compromised Credentials

No Application Vulnerabilities

No Insider Threat
```

Similarly, a low score may include:

```text
Low-Risk Development Resources

Non-Relevant Controls

Accepted Exceptions
```

Security teams should use the score as one input.

---

# Findings

## 18. Finding Sources

Security Hub findings may come from:

```text
Security Hub Controls

Amazon GuardDuty

Amazon Inspector

Amazon Macie

Third-Party Products

Custom Integrations
```

Conceptually:

```text
Source
   |
   v
ASFF Finding
   |
   v
Security Hub
```

---

## 19. Finding Triage

When reviewing a finding, ask:

```text
Which service generated it?

What resource is affected?

What is the severity?

Is the resource production?

Is it Internet-facing?

Does it contain sensitive data?

Is the activity ongoing?

Is remediation required?
```

---

# Workflow Status

## 20. Workflow Status

Security Hub tracks investigation progress using workflow status.

Important states include:

```text
NEW

NOTIFIED

SUPPRESSED

RESOLVED
```

---

## 21. NEW

```text
NEW
```

means the finding has not yet been fully reviewed.

Conceptually:

```text
Finding Created
     |
     v
NEW
```

Security teams should triage new findings.

---

## 22. NOTIFIED

```text
NOTIFIED
```

can indicate that the responsible resource owner has been informed.

Example:

```text
Security Team
     |
     v
Finds Issue
     |
     v
Application Owner Notified
```

---

## 23. SUPPRESSED

```text
SUPPRESSED
```

means the finding was reviewed and no further action is currently considered necessary.

Examples:

```text
Accepted Risk

Known Test Resource

Expected Behavior
```

Suppression should be documented.

---

## 24. RESOLVED

```text
RESOLVED
```

indicates the issue has been reviewed and remediated.

Conceptually:

```text
Finding
   |
   v
Investigation
   |
   v
Remediation
   |
   v
RESOLVED
```

---

## 25. Workflow Status Is Not a Prevention Mechanism

Important:

```text
SUPPRESSED
```

or:

```text
RESOLVED
```

does not necessarily prevent Security Hub from generating a new finding if the issue occurs again.

Workflow status tracks investigation state.

---

# Record State

## 26. Record State

ASFF findings also contain:

```text
RecordState
```

Important values include:

```text
ACTIVE

ARCHIVED
```

This is different from:

```text
Workflow Status
```

Conceptually:

```text
Workflow
→ Investigation Progress

RecordState
→ Finding Record Activity
```

---

# Automation Rules

## 27. What Are Automation Rules?

Security Hub automation rules can automatically modify findings based on matching criteria.

Conceptually:

```text
Finding
   |
   v
Matching Criteria
   |
   v
Automation Rule
   |
   v
Update Finding
```

Possible actions include updating:

```text
Severity

Workflow Status

Other Supported ASFF Fields
```

---

## 28. Automation Rule Example

Suppose:

```text
Account:
Development

Finding:
Low Severity
```

An automation rule might:

```text
Set Workflow Status
→ SUPPRESSED
```

if the condition matches an approved use case.

---

## 29. Priority of Automation Rules

Multiple automation rules can exist.

Security teams should:

```text
Define Specific Conditions

Review Rule Priority

Avoid Overlapping Rules

Test Expected Results
```

Broad automation can hide important findings.

---

## 30. Automation vs Remediation

Automation rules modify findings.

They do not necessarily change the affected AWS resource.

Example:

```text
Finding
→ Workflow = SUPPRESSED
```

does not fix:

```text
Public S3 Bucket
```

For resource remediation, other automation is needed.

---

# EventBridge Automation

## 31. Security Hub and EventBridge

Security Hub findings can be sent through Amazon EventBridge.

Conceptually:

```text
Security Hub Finding
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

---

## 32. Automated Notification

Example:

```text
Critical Finding
      |
      v
Security Hub
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

---

## 33. Automated Remediation

Example:

```text
Failed Security Control
      |
      v
Security Hub
      |
      v
EventBridge
      |
      v
Lambda / SSM Automation
      |
      v
Remediation
```

Automatic remediation must be tested carefully.

---

## 34. Automation Order

Conceptually:

```text
Finding
   |
   v
Security Hub Automation Rule
   |
   v
Finding Updated
   |
   v
EventBridge
   |
   v
External Action
```

Automation rules modify the finding before EventBridge processes the updated finding.

---

# Multi-Account Security Hub

## 35. Delegated Administrator

AWS Organizations can designate a Security Hub delegated administrator.

Conceptually:

```text
AWS Organizations
       |
       v
Delegated Security Administrator
       |
       +-- Production
       |
       +-- Development
       |
       +-- Shared Services
```

This allows centralized management.

---

## 36. Why Use a Security Account?

A dedicated security account can manage:

```text
Security Hub

GuardDuty

Security Findings

Security Monitoring
```

This supports:

```text
Separation of Duties

Centralized Visibility

Reduced Administrative Fragmentation
```

---

# Central Configuration

## 37. Central Configuration

Security Hub central configuration allows a delegated administrator to centrally configure Security Hub across AWS Organizations.

Conceptually:

```text
Security Account
     |
     v
Configuration Policy
     |
     +-- Account A
     |
     +-- Account B
     |
     +-- OU A
```

A configuration policy can define:

```text
Security Hub Enabled?

Which Standards Enabled?

Which Controls Enabled?
```

---

## 38. Home Region

Central configuration uses a:

```text
Home Region
```

The delegated administrator manages configuration policies from this Region.

Conceptually:

```text
Home Region
     |
     +-- Configuration
     |
     +-- Aggregation
```

The home Region can also act as the aggregation Region.

---

## 39. Linked Regions

Other Regions can be configured as:

```text
Linked Regions
```

Conceptually:

```text
Region A ──┐
Region B ──┼──> Home / Aggregation Region
Region C ──┘
```

This provides centralized visibility across Regions.

---

# Cross-Region Aggregation

## 40. Finding Aggregation

Security Hub can aggregate findings from multiple Regions.

Conceptually:

```text
Tokyo Findings ─────┐
Singapore Findings ─┼──> Aggregation Region
Virginia Findings ──┘
```

This helps security teams avoid reviewing each Region separately.

---

## 41. Why Aggregation Matters

Without aggregation:

```text
Check Tokyo

Check Singapore

Check Virginia
```

With aggregation:

```text
Central Region
→ Unified Findings
```

This reduces operational complexity.

---

# Finding Suppression

## 42. When to Suppress

Possible legitimate reasons include:

```text
Approved Exception

Test Environment

Compensating Control

Known Expected Activity
```

Before suppression:

```text
Document Reason

Define Scope

Set Review Date

Verify Risk Acceptance
```

---

## 43. Poor Suppression

Poor rule:

```text
Suppress All Low Findings
```

This may hide useful signals.

Better:

```text
Specific Finding

Specific Resource

Specific Account

Known Reason
```

---

# Security Standards Strategy

## 44. Do Not Enable Everything Blindly

More controls do not automatically mean better security.

Possible problems:

```text
Large Number of Findings

Irrelevant Controls

Alert Fatigue

Operational Cost
```

Select standards based on:

```text
Environment

Compliance

Threat Model

Business Requirements
```

---

## 45. Disable vs Suppress

Important distinction:

### Disable Control

Use when:

```text
The control is not relevant.
```

Then Security Hub does not continue checking that control.

### Suppress Finding

Use when:

```text
The control is relevant,
but a specific finding requires no action.
```

Conceptually:

```text
Control Not Relevant
→ Disable

Specific Exception
→ Suppress
```

---

# Integration with GuardDuty

## 46. GuardDuty Finding Flow

From Day 28:

```text
Suspicious Activity
      |
      v
GuardDuty
      |
      v
GuardDuty Finding
      |
      v
Security Hub
      |
      v
ASFF
```

Security Hub can then:

```text
Aggregate

Prioritize

Change Workflow

Automate Response
```

---

## 47. Investigation Example

Security Hub receives:

```text
GuardDuty
Potential Credential Compromise
```

Security analyst:

```text
1. Review Finding

2. Identify Resource

3. Review GuardDuty Evidence

4. Check CloudTrail

5. Check AWS Config

6. Determine Scope

7. Contain Credentials

8. Update Workflow Status
```

---

# Integration with AWS Config

## 48. Security Controls and AWS Config

Many Security Hub controls rely on AWS Config to evaluate resource configurations.

Conceptually:

```text
AWS Resource
      |
      v
AWS Config
      |
      v
Security Hub Control
      |
      v
Compliance Result
```

Therefore, AWS Config recording is important for many posture checks.

---

## 49. Example Control

Requirement:

```text
EBS Volume Must Be Encrypted
```

Flow:

```text
EBS Volume
     |
     v
AWS Config
     |
     v
Security Hub Control
     |
     +-- PASSED
     |
     +-- FAILED
```

---

# Security Score Review

## 50. Improving the Score

Poor strategy:

```text
Goal:
Make Security Score 100%
```

Better strategy:

```text
Understand Failed Controls
       |
       v
Assess Risk
       |
       v
Prioritize Critical Resources
       |
       v
Remediate
```

The goal is:

```text
Better Security
```

not merely:

```text
Better Number
```

---

# Troubleshooting

## 51. Missing Finding

Check:

```text
Is Security Hub enabled?

Is the integration enabled?

Is the correct Region selected?

Is cross-Region aggregation configured?

Was the finding archived?

Was it suppressed?

Does the integration send findings to Security Hub?
```

---

## 52. Missing Control Results

Check:

```text
Is the Security Standard enabled?

Is the Control enabled?

Is AWS Config enabled?

Is the required resource being recorded?

Is the correct Region selected?
```

---

## 53. Score Not Appearing

Check:

```text
Are standards enabled?

Are controls generating data?

Is AWS Config recording required resources?

Has enough time passed for score calculation?
```

---

## 54. Too Many Findings

Possible causes:

```text
Too Many Standards

Irrelevant Controls

Test Resources

Duplicated Security Signals

Poor Automation Rules
```

Approaches:

```text
Disable Irrelevant Controls

Use Specific Automation

Use Specific Suppression

Prioritize by Context
```

---

# Hands-on Practice

## 55. Practice — Open Security Hub

Navigate:

```text
AWS Console
   |
   v
Security Hub
```

Review:

```text
Summary

Findings

Controls

Security Standards

Integrations
```

---

## 56. Practice — Review Findings

Choose one available or sample finding.

Record:

```text
Finding Source:

Severity:

Resource:

Account:

Region:

Workflow Status:

Record State:

Compliance Status:
```

Then answer:

```text
Why is this finding important?

What additional evidence is required?

What would I investigate next?
```

---

## 57. Practice — Review Controls

Navigate:

```text
Security Hub
   |
   v
Controls
```

Choose one control.

Review:

```text
Control ID

Title

Severity

Enabled Standards

Failed Resources

Passed Resources
```

---

## 58. Practice — Review Standards

Navigate:

```text
Security Hub
   |
   v
Security Standards
```

Review enabled standards.

Examples:

```text
AWS Foundational Security Best Practices

CIS Benchmark

Other Available Standards
```

Ask:

```text
Why is this standard enabled?

Does it match the environment?
```

---

## 59. Practice — Review Security Score

Review:

```text
Overall Security Score

Standard Score
```

Identify:

```text
Failed Controls

High-Severity Controls

Critical Resources
```

Do not focus only on the numeric score.

---

## 60. Practice — Finding Workflow

For a sample finding, decide conceptually whether it should be:

```text
NEW

NOTIFIED

SUPPRESSED

RESOLVED
```

Explain why.

---

## 61. Optional CLI Practice

Check Security Hub status:

```bash
aws securityhub describe-hub
```

Get enabled standards:

```bash
aws securityhub get-enabled-standards
```

Get findings:

```bash
aws securityhub get-findings \
  --max-results 10
```

Get enabled controls for a standard:

```bash
aws securityhub describe-standards-controls \
  --standards-subscription-arn <subscription-arn>
```

Do not publish real finding or account information to a public repository.

---

# Architecture Exercise

## 62. Multi-Account Security Architecture

Design:

```text
AWS Organization
        |
        +-- Production
        |
        +-- Development
        |
        +-- Shared Services
        |
        +-- Security Account
                |
                v
          Security Hub
                |
        +-------+-------+
        |       |       |
        v       v       v
   GuardDuty Inspector Macie
```

Security Hub aggregates findings into the security account.

---

## 63. Automated Response Architecture

```text
GuardDuty
Inspector
Macie
Controls
   |
   v
Security Hub
   |
   v
Automation Rules
   |
   v
Updated ASFF Finding
   |
   v
EventBridge
   |
   +-- SNS
   |
   +-- Lambda
   |
   +-- Systems Manager
   |
   v
Security Response
```

---

# Incident Scenario

## 64. Scenario

Security Hub receives:

```text
High Severity GuardDuty Finding

Resource:
Production EC2
```

At the same time:

```text
Security Hub Control

Security Group
FAILED

TCP 22
0.0.0.0/0
```

Possible investigation:

```text
GuardDuty
→ Suspicious Activity

Security Hub
→ Aggregate Context

AWS Config
→ Security Group Changed

CloudTrail
→ Who Changed It?

VPC Flow Logs
→ Was the Instance Accessed?

OS Logs
→ Was Login Successful?
```

---

## 65. Finding Triage Workflow

```text
Security Hub Finding
       |
       v
Check Source
       |
       v
Check Severity
       |
       v
Identify Resource
       |
       v
Assess Business Context
       |
       v
Correlate Other Findings
       |
       v
Investigate
       |
       v
Remediate
       |
       v
Update Workflow
```

---

# Security Checklist

```text
[ ] Security Hub is enabled in required accounts

[ ] Required Regions are covered

[ ] A delegated administrator is configured where appropriate

[ ] Central configuration is used where appropriate

[ ] Appropriate security standards are enabled

[ ] Irrelevant controls are disabled deliberately

[ ] AWS Config records required resource types

[ ] GuardDuty integration is enabled

[ ] Inspector integration is planned or enabled

[ ] Macie integration is planned where required

[ ] Findings use centralized aggregation

[ ] Finding severity is reviewed with business context

[ ] Critical and High findings have response procedures

[ ] Workflow statuses are used consistently

[ ] Suppression is narrowly scoped

[ ] Suppression decisions are documented

[ ] Automation rules are tested

[ ] EventBridge response workflows are tested

[ ] Security score is used as a posture indicator, not an absolute security measurement

[ ] Findings are correlated with CloudTrail and AWS Config

[ ] Central security configuration is periodically reviewed
```

---

## Key Takeaways

- Security Hub CSPM centralizes security posture and security findings.
- Findings from multiple services are normalized using ASFF.
- GuardDuty detects threats, while Security Hub aggregates and manages findings.
- Security standards contain multiple security controls.
- Security controls evaluate AWS resource configurations and generate findings.
- Security Hub can calculate security scores based on enabled evaluated controls.
- Security score is a posture indicator, not an absolute measurement of security.
- Workflow statuses include NEW, NOTIFIED, SUPPRESSED, and RESOLVED.
- Workflow status tracks investigation progress.
- Automation rules can automatically update findings.
- EventBridge can trigger actions outside Security Hub.
- Multi-account environments can use a delegated administrator.
- Central configuration can manage standards and controls across AWS Organizations.
- Cross-Region aggregation provides centralized regional visibility.
- AWS Config is important for many Security Hub control evaluations.
- Suppression should be specific and documented.
- Disabling a non-relevant control is different from suppressing a specific finding.
- Security Hub should support investigation and remediation rather than simply maximizing a score.

---

## Reflection

Today I learned that AWS Security Hub provides a centralized security posture and finding management layer across AWS environments.

Unlike GuardDuty, which focuses on threat detection, Security Hub aggregates findings from multiple AWS and third-party security products and normalizes them using the AWS Security Finding Format.

I also learned that Security Hub evaluates security posture using standards and controls, while the security score provides a high-level indication of control compliance.

The most important lesson is that security findings still require context. A high-severity finding should be evaluated together with resource criticality, Internet exposure, business impact, and evidence from services such as CloudTrail and AWS Config.

From a security operations perspective, Security Hub can serve as a central point for finding triage, workflow management, automation, and multi-account security visibility.

---

## Vocabulary

| Word | Meaning |
|---|---|
| ASFF | Standardized AWS format used to represent security findings |
| Automation Rule | Rule that automatically updates Security Hub findings |
| Cross-Region Aggregation | Collecting Security Hub findings from linked Regions into a central Region |
| Delegated Administrator | AWS Organizations account centrally managing Security Hub |
| Record State | ASFF field indicating whether a finding record is active or archived |
| Security Control | A specific security requirement evaluated against AWS resources |
| Security Hub CSPM | AWS service for centralized security posture and finding management |
| Security Score | Percentage-based indicator of passed enabled evaluated controls |
| Security Standard | A collection of security requirements and controls |
| Workflow Status | State representing the investigation progress of a finding |
