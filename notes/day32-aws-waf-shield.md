# Day 32 — AWS WAF & Shield

## Topic

AWS WAF, Web ACLs, Managed Rules, Bot Protection, Rate Limiting, and AWS Shield DDoS Protection

---

## Objectives

- Understand the purpose of AWS WAF
- Understand Web ACL architecture
- Learn how WAF rules are evaluated
- Understand rule priorities and default actions
- Learn common rule statement types
- Understand AWS Managed Rules
- Learn rate-based rules
- Understand Count, CAPTCHA, and Challenge actions
- Understand Bot Control
- Understand WAF logging and monitoring
- Understand AWS Shield Standard
- Understand AWS Shield Advanced
- Understand Layer 3, Layer 4, and Layer 7 DDoS protection
- Learn how WAF and Shield work together
- Understand multi-account WAF management with Firewall Manager
- Practice designing a secure web application protection architecture

---

# AWS WAF Fundamentals

## 1. What Is AWS WAF?

AWS WAF is a web application firewall.

It inspects HTTP and HTTPS requests sent to supported AWS web application resources.

Conceptually:

```text
Client
  |
  v
AWS WAF
  |
  v
Protected AWS Resource
  |
  v
Application
```

AWS WAF can inspect request attributes such as:

```text
IP Address

HTTP Headers

URI Path

Query String

HTTP Method

Request Body

Cookies
```

Based on configured rules, AWS WAF can decide how to handle the request.

---

## 2. AWS WAF Use Cases

Common use cases include:

```text
SQL Injection Protection

Cross-Site Scripting Protection

Bot Management

Rate Limiting

IP Blocking

Geo Restriction

Credential Stuffing Mitigation

Application Layer DDoS Mitigation

Custom Application Rules
```

AWS WAF primarily protects:

```text
Layer 7
```

web traffic.

---

## 3. Supported Resource Architecture

A common architecture:

```text
Internet
   |
   v
CloudFront
   |
   v
AWS WAF
   |
   v
Application Load Balancer
   |
   v
EC2 / ECS / Application
```

Other supported integrations can include:

```text
API Gateway

AppSync

Cognito

App Runner

Other Supported AWS Web Resources
```

---

# Web ACL

## 4. What Is a Web ACL?

A Web Access Control List, or Web ACL, contains rules that inspect web requests.

Conceptually:

```text
Web ACL
│
├── Rule 1
├── Rule 2
├── Rule 3
└── Default Action
```

The Web ACL is associated with one or more supported AWS resources.

---

## 5. Protection Pack

In the AWS WAF console, Web ACLs may also be presented as:

```text
Protection Packs
```

Conceptually:

```text
Protection Pack
=
Web ACL
+
Simplified Console Experience
```

The underlying AWS WAF Web ACL functionality remains the same.

---

## 6. Web ACL Evaluation

A web request flows through rules according to rule priority.

Example:

```text
Incoming Request
      |
      v
Rule Priority 0
      |
      v
Rule Priority 10
      |
      v
Rule Priority 20
      |
      v
Default Action
```

Lower priority numbers are evaluated first.

---

## 7. Default Action

If no rule terminates evaluation, the Web ACL applies its default action.

Typical default actions are:

```text
Allow

or

Block
```

Common design:

```text
Default:
Allow

Rules:
Block Known Bad Traffic
```

Another model:

```text
Default:
Block

Rules:
Allow Explicit Traffic
```

The correct approach depends on application requirements.

---

# Rule Actions

## 8. Allow

```text
Allow
```

permits the matching request.

Conceptually:

```text
Request Matches Rule
      |
      v
Allow
      |
      v
Application
```

---

## 9. Block

```text
Block
```

stops the matching request.

Conceptually:

```text
Request Matches Rule
      |
      v
Block
      |
      X
Application
```

A custom response can also be configured for supported use cases.

---

## 10. Count

```text
Count
```

records that the request matched the rule without blocking it.

Conceptually:

```text
Request
   |
   v
Rule Match
   |
   v
Count
   |
   v
Continue Evaluation
```

Count is useful when testing a rule before enforcing it.

---

## 11. Why Count Is Important

Poor rollout:

```text
New WAF Rule
   |
   v
Immediately Block
   |
   v
Legitimate Users Blocked
```

Better:

```text
New Rule
   |
   v
Count
   |
   v
Observe Traffic
   |
   v
Tune Rule
   |
   v
Block
```

This reduces false positives.

---

# Rule Statements

## 12. IP Set Rules

An IP set contains IP addresses or CIDR ranges.

Example:

```text
203.0.113.0/24
```

Conceptually:

```text
Source IP
    |
    v
IP Set
    |
 +--+--+
 |     |
Match  No Match
```

Possible uses:

```text
Block Known Malicious IPs

Allow Corporate IP Ranges

Restrict Administrative Endpoints
```

---

## 13. Geo Match

Geo match rules inspect the country associated with source IP addresses.

Example:

```text
Country
→ JP
→ US
→ KR
```

Possible uses:

```text
Regional Access Control

Fraud Reduction

Business Restrictions
```

Geo blocking alone should not be treated as strong authentication.

---

## 14. String Match

A rule can inspect request content for specific values.

Examples:

```text
URI Path

Header

Query Parameter

Cookie
```

Example:

```text
URI:
/admin
```

can receive additional protection.

---

## 15. Regex Pattern Set

Regular expression pattern sets allow more flexible request matching.

Example:

```text
/admin/.*
```

Potential uses include:

```text
Path Protection

Known Malicious Patterns

Application-Specific Filtering
```

Regex rules should be carefully tested.

---

## 16. SQL Injection Match

AWS WAF can inspect requests for SQL injection patterns.

Conceptually:

```text
Request
   |
   v
SQL Injection Inspection
   |
   +-- Suspicious
   |
   +-- Normal
```

Example attack concept:

```text
' OR 1=1 --
```

WAF can provide a protective layer against common SQL injection attempts.

However:

```text
WAF
≠
Replacement for Parameterized Queries
```

Application code must still be secure.

---

## 17. XSS Match

AWS WAF can detect patterns associated with cross-site scripting.

Example concept:

```text
<script>
```

WAF provides additional defense but does not replace:

```text
Output Encoding

Input Validation

Content Security Policy

Secure Application Development
```

---

# AWS Managed Rules

## 18. What Are AWS Managed Rules?

AWS Managed Rules are predefined rule groups maintained by AWS.

Conceptually:

```text
AWS
  |
  v
Managed Rule Group
  |
  v
Web ACL
```

These help protect against common web application threats without requiring every detection rule to be built manually.

---

## 19. Common Managed Rule Groups

Examples include groups designed for:

```text
Common Web Threats

Known Bad Inputs

SQL Injection

Linux / Unix Threats

WordPress

PHP

Windows

Amazon IP Reputation

Anonymous IP Lists
```

The exact available rule groups can evolve.

---

## 20. Managed Rule Group Versioning

Managed rule groups can have versions.

Conceptually:

```text
Rule Group v1
     |
     v
Updated Threat Detection
     |
     v
Rule Group v2
```

When appropriate:

```text
Review New Version

Test with Count

Monitor

Deploy
```

Avoid blindly applying changes to production.

---

## 21. Rule Action Override

A managed rule group's individual rule actions can be overridden.

Example:

```text
Managed Rule Default:
Block
```

Temporary testing:

```text
Override:
Count
```

This helps evaluate impact before enforcement.

---

# Labels

## 22. WAF Labels

AWS WAF rules can add labels to requests.

Conceptually:

```text
Request
   |
   v
Managed Rule
   |
   v
Label
   |
   v
Custom Rule
```

Labels allow later rules to make decisions based on earlier inspection results.

---

## 23. Label-Based Architecture

Example:

```text
Bot Control
     |
     v
Labels Request as Bot
     |
     v
Custom Rule
     |
     +-- Allow Verified Bot
     |
     +-- Challenge Unknown Bot
     |
     +-- Block Malicious Bot
```

This enables more granular policies.

---

# Rate-Based Rules

## 24. What Is a Rate-Based Rule?

A rate-based rule counts requests that match aggregation criteria and applies rate limiting when the configured request rate is exceeded.

Conceptually:

```text
Client
  |
  v
Requests
  |
  v
Rate-Based Rule
  |
  +-- Below Limit
  |
  +-- Above Limit
          |
          v
       Action
```

---

## 25. Rate Limit Use Cases

Examples include:

```text
Login Endpoint

Password Reset

API Endpoint

Search Endpoint

Expensive Application Operation
```

Rate limiting can reduce:

```text
Brute Force

Credential Stuffing

Scraping

Application-Layer DDoS

API Abuse
```

---

## 26. Login Example

Example:

```text
/login
```

Possible design:

```text
Same Client
   |
   v
Too Many Requests
   |
   v
Rate-Based Rule
   |
   v
Block / Challenge
```

This can increase the cost of automated login abuse.

---

## 27. Scope-Down Statements

A rate-based rule can be limited to selected requests.

Example:

```text
Only Count Requests Where:

URI = /login
```

Conceptually:

```text
All Traffic
    |
    v
Scope Down
    |
    v
/login Requests
    |
    v
Rate Limit
```

This avoids rate-limiting unrelated application traffic.

---

# CAPTCHA and Challenge

## 28. CAPTCHA Action

CAPTCHA asks a client to complete a puzzle to demonstrate human interaction.

Conceptually:

```text
Suspicious Request
      |
      v
CAPTCHA
      |
   +--+--+
   |     |
Pass    Fail
```

Useful scenarios can include:

```text
Credential Stuffing

Scraping

Spam

Suspicious Login Activity
```

---

## 29. Challenge Action

Challenge runs a silent browser challenge.

Conceptually:

```text
Client
  |
  v
Silent Challenge
  |
  v
Valid Browser Session?
```

Unlike CAPTCHA, the user normally does not need to solve a visible puzzle.

---

## 30. CAPTCHA vs Challenge

```text
CAPTCHA
→ User Interaction

Challenge
→ Silent Browser Verification
```

Challenge can often provide a better user experience where a visible CAPTCHA would be too disruptive.

---

## 31. Tokens

AWS WAF can issue tokens after successful CAPTCHA or Challenge validation.

Conceptually:

```text
Client
  |
  v
CAPTCHA / Challenge
  |
  v
Valid Token
  |
  v
Future Requests
```

Tokens help WAF track validated browser sessions.

---

# Bot Control

## 32. AWS WAF Bot Control

Bot Control is an AWS Managed Rules capability for identifying and managing bot traffic.

Possible bot categories include:

```text
Search Engines

Scrapers

Scanners

Automated Browsers

Monitoring Bots

Malicious Automation
```

Conceptually:

```text
Web Request
     |
     v
Bot Control
     |
     v
Bot Classification
     |
     v
Label / Action
```

---

## 33. Common Protection Level

Bot Control provides a Common protection level.

This primarily detects many self-identifying bots using techniques such as:

```text
Static Request Analysis

Known Bot Signatures
```

This can identify verified and unverified automated clients.

---

## 34. Targeted Protection Level

Targeted Bot Control adds advanced detection for sophisticated bots.

Detection can include:

```text
Browser Interrogation

Fingerprinting

Behavior Analysis

Rate Analysis

Machine Learning
```

Conceptually:

```text
Sophisticated Bot
       |
       v
Targeted Bot Control
       |
       v
Challenge / CAPTCHA / Block
```

---

## 35. Verified Bots

Not all bots are malicious.

Examples:

```text
Search Engine Crawlers

Monitoring Services
```

Bot Control can classify and label verified bots.

This allows policies such as:

```text
Verified Search Bot
→ Allow

Unknown Scraper
→ Rate Limit

Malicious Automation
→ Block
```

---

# Fraud Control

## 36. Account Takeover Protection

AWS WAF provides managed protection for account takeover scenarios.

Conceptually:

```text
Login Endpoint
     |
     v
Credential Abuse
     |
     v
WAF Fraud Control
```

This can help mitigate:

```text
Credential Stuffing

Automated Login Attacks
```

---

## 37. Account Creation Fraud Prevention

Another managed protection targets account creation abuse.

Examples:

```text
Fake Account Creation

Automated Sign-Up

Promotional Abuse

Bulk Registration
```

This is useful for applications where account creation itself is an attack target.

---

# Logging and Monitoring

## 38. WAF Visibility

AWS WAF provides visibility through:

```text
CloudWatch Metrics

Sampled Requests

WAF Logs
```

These help determine:

```text
Which Rules Match?

Which Requests Are Blocked?

Which IPs Generate Traffic?

Are False Positives Occurring?
```

---

## 39. WAF Logs

WAF logs can include information such as:

```text
Timestamp

Web ACL

Rule

Action

Client IP

HTTP Method

URI

Headers

Labels
```

Logs are useful for:

```text
Security Investigation

Rule Tuning

Threat Hunting

Troubleshooting
```

---

## 40. Sensitive Logging Considerations

HTTP requests may contain sensitive information.

Examples:

```text
Authorization Header

Cookies

Query Parameters

Tokens
```

Logging configurations should avoid unnecessary secret exposure.

Where appropriate:

```text
Redact Sensitive Fields
```

from WAF logs.

---

## 41. WAF Investigation Example

Scenario:

```text
AWS WAF
→ Blocks SQL Injection Pattern
```

Investigation:

```text
Source IP

URI

Request Method

Matching Rule

Frequency

Other Requests From Same Source
```

Then correlate with:

```text
Application Logs

CloudFront Logs

ALB Logs

GuardDuty

CloudTrail
```

---

# DDoS Fundamentals

## 42. What Is a DDoS Attack?

DDoS stands for:

```text
Distributed Denial of Service
```

Conceptually:

```text
Compromised Client A ──┐
Compromised Client B ──┼──> Target
Compromised Client C ──┤
Compromised Client D ──┘
```

The attacker attempts to overwhelm a service with traffic or requests.

---

## 43. DDoS Layers

DDoS attacks can target multiple layers.

### Layer 3

```text
Network Layer
```

Examples:

```text
Volumetric Network Attacks
```

### Layer 4

```text
Transport Layer
```

Examples:

```text
TCP SYN Flood
```

### Layer 7

```text
Application Layer
```

Examples:

```text
HTTP Request Flood

Expensive API Request Flood
```

---

# AWS Shield Standard

## 44. Shield Standard

AWS Shield Standard provides automatic DDoS protection for AWS customers at no additional Shield subscription charge.

It helps protect against common network and transport-layer attacks.

Conceptually:

```text
Internet
   |
   v
AWS Edge / Network
   |
   v
Shield Standard
   |
   v
AWS Resource
```

---

## 45. Shield Standard Examples

Protection can help mitigate common attacks such as:

```text
UDP Reflection

TCP SYN Floods

Other Common Infrastructure-Layer DDoS Attacks
```

Shield Standard works automatically and does not require a separate subscription.

---

# AWS Shield Advanced

## 46. Shield Advanced

Shield Advanced provides enhanced DDoS protection for selected AWS resources.

Conceptually:

```text
Critical Internet-Facing Resource
          |
          v
Shield Advanced
          |
          v
Advanced DDoS Protection
```

Unlike Shield Standard:

```text
Shield Advanced
→ Paid Subscription
```

---

## 47. Protected Resources

Shield Advanced can protect supported resources such as:

```text
CloudFront

Route 53 Hosted Zones

Global Accelerator

Elastic IP Addresses

EC2 through Elastic IP

Application Load Balancers

Classic Load Balancers

Supported Network Load Balancer Architectures
```

Protection must be explicitly configured for the resource.

---

## 48. Shield Advanced Benefits

Shield Advanced adds capabilities such as:

```text
Advanced DDoS Detection

Advanced Event Visibility

Application-Layer Protection

Automatic Application-Layer Mitigation

DDoS Cost Protection Features

Shield Response Team Support
```

Exact eligibility and configuration requirements apply.

---

# Shield Response Team

## 49. Shield Response Team

The Shield Response Team, or SRT, consists of AWS specialists focused on DDoS response.

Conceptually:

```text
DDoS Event
    |
    v
Shield Advanced
    |
    v
SRT
    |
    v
Response Assistance
```

Organizations can configure appropriate access so the SRT can assist during DDoS events.

---

## 50. Proactive Engagement

For supported Shield Advanced configurations:

```text
DDoS Event
+
Unhealthy Protected Resource
        |
        v
SRT Proactive Engagement
```

This can reduce response time during major attacks.

Required setup should be completed before an incident occurs.

---

# WAF and Shield Together

## 51. Layer 3 / 4 vs Layer 7

A useful model:

```text
Shield
→ Infrastructure DDoS Protection

WAF
→ HTTP / HTTPS Request Filtering
```

Together:

```text
Internet
   |
   v
Shield
   |
   v
AWS WAF
   |
   v
Application
```

---

## 52. Shield Advanced and WAF

For application-layer DDoS protection:

```text
Shield Advanced
       +
AWS WAF
```

are commonly used together.

A Web ACL can include:

```text
Rate-Based Rules

Managed Rules

Custom Rules
```

to mitigate Layer 7 attacks.

---

## 53. Automatic Application-Layer DDoS Mitigation

Shield Advanced can support automatic application-layer DDoS mitigation for eligible resources.

Conceptually:

```text
Layer 7 DDoS
      |
      v
Shield Advanced Detection
      |
      v
AWS WAF Mitigation Rule
      |
      v
Attack Traffic Mitigated
```

This should be configured and validated before an actual event.

---

# Firewall Manager

## 54. AWS Firewall Manager

AWS Firewall Manager helps centrally manage security policies across accounts and resources.

Conceptually:

```text
AWS Organizations
       |
       v
Firewall Manager
       |
       +-- AWS WAF
       |
       +-- Shield Advanced
       |
       +-- Security Groups
       |
       +-- Network Firewall
```

---

## 55. Multi-Account WAF

Without central management:

```text
Account A
→ Configure WAF

Account B
→ Configure WAF

Account C
→ Configure WAF
```

With Firewall Manager:

```text
Security Account
      |
      v
Central WAF Policy
      |
      +-- Account A
      +-- Account B
      +-- Account C
```

This improves consistency.

---

# Common Misconfigurations

## 56. WAF Exists but Is Not Associated

Poor:

```text
Web ACL
   |
   X
Application
```

A Web ACL provides no protection if it is not associated with the intended resource.

Always verify resource association.

---

## 57. Immediate Blocking Without Testing

Poor:

```text
New Managed Rule
      |
      v
Block
      |
      v
Production Outage
```

Better:

```text
Count
  ↓
Analyze
  ↓
Tune
  ↓
Block
```

---

## 58. Excessively Broad Allow Rule

Example:

```text
Priority 0

Allow:
0.0.0.0/0
```

This can prevent later blocking logic from being reached depending on rule structure.

Rule priorities must be reviewed carefully.

---

## 59. Rate Limit Too Low

Example:

```text
Normal Traffic:
500 Requests

Rate Limit:
100
```

Result:

```text
Legitimate Users Blocked
```

Rate limits should be based on real application traffic.

---

## 60. Rate Limit Too High

Example:

```text
Attack:
5,000 Requests

Rate Limit:
1,000,000
```

Result:

```text
Rule Provides Little Protection
```

Tune thresholds using traffic data.

---

## 61. Relying Only on IP Blocking

Attackers can use:

```text
Botnets

Proxy Networks

Changing IP Addresses
```

Therefore:

```text
IP Blocking Alone
```

may be insufficient.

Combine:

```text
Managed Rules

Rate Limiting

Bot Detection

Challenge

Application Controls
```

---

## 62. WAF Replaces Secure Coding

Incorrect:

```text
WAF Enabled
→ SQL Injection Fixed
```

Correct:

```text
Secure Application Code
      +
AWS WAF
      =
Defense in Depth
```

WAF should provide an additional protective layer.

---

## 63. Shield Advanced Assumed Automatic Everywhere

Incorrect:

```text
Subscribe to Shield Advanced
→ Every AWS Resource Protected
```

Correct:

```text
Shield Advanced Subscription
      |
      v
Select / Configure Protected Resources
```

Protection requires proper configuration.

---

# Security Architecture

## 64. Public Web Application

Example:

```text
Internet
   |
   v
Route 53
   |
   v
CloudFront
   |
   +-- Shield
   |
   +-- AWS WAF
   |
   v
Application Load Balancer
   |
   v
Private Application Servers
   |
   v
Private RDS
```

Security layers:

```text
Shield
→ DDoS

WAF
→ Web Attacks

Security Groups
→ Network Access

IAM
→ AWS Authorization

KMS
→ Encryption

GuardDuty
→ Threat Detection
```

---

## 65. Defense in Depth

A web application should not rely on one service.

Conceptually:

```text
Shield
   ↓
WAF
   ↓
CloudFront / ALB
   ↓
Security Groups
   ↓
Application Security
   ↓
IAM
   ↓
Data Protection
   ↓
Monitoring
```

---

# Incident Scenario

## 66. Credential Stuffing

Scenario:

```text
Attacker
   |
   v
Thousands of Login Requests
   |
   v
/login
```

Possible controls:

```text
WAF Rate-Based Rule

Bot Control

Challenge

CAPTCHA

Fraud Control ATP

Application MFA
```

---

## 67. SQL Injection Attack

Scenario:

```text
Attacker
   |
   v
Malicious Query Parameter
   |
   v
AWS WAF
```

Possible response:

```text
Managed SQLi Rule
→ Block
```

Then investigate:

```text
WAF Logs

Application Logs

Source IP

Affected Endpoint
```

Also verify that the application uses parameterized SQL queries.

---

## 68. Layer 7 DDoS

Scenario:

```text
Large Botnet
     |
     v
Millions of HTTP Requests
     |
     v
Application
```

Possible protections:

```text
CloudFront

AWS WAF

Rate-Based Rules

Bot Control

Shield Advanced

Automatic Application-Layer Mitigation
```

---

# Monitoring

## 69. Metrics to Review

Potential WAF metrics include:

```text
AllowedRequests

BlockedRequests

CountedRequests

CaptchaRequests

ChallengeRequests
```

Review changes over time.

Example:

```text
BlockedRequests
      |
      v
Sudden Increase
      |
      v
Investigation
```

---

## 70. False Positive Investigation

Scenario:

```text
WAF BlockedRequests
Suddenly Increase
```

Questions:

```text
Which Rule?

Which URI?

Which Clients?

Was a New Rule Deployed?

Is Legitimate Traffic Affected?
```

Use logs before simply disabling the rule.

---

# Hands-on Practice

## 71. Practice — Open AWS WAF

Navigate:

```text
AWS Console
   |
   v
AWS WAF
```

Review:

```text
Protection Packs / Web ACLs

Rules

IP Sets

Regex Pattern Sets
```

---

## 72. Practice — Review a Web ACL

If one exists, inspect:

```text
Associated Resource

Default Action

Rules

Priorities

Actions

CloudWatch Metrics
```

Ask:

```text
Which rule executes first?

Which rules terminate evaluation?

What happens if nothing matches?
```

---

## 73. Practice — Review AWS Managed Rules

Browse available managed rule groups.

Choose examples for:

```text
Common Threats

SQL Injection

IP Reputation

Bot Control
```

Review:

```text
Rule Group Capacity

Default Actions

Available Overrides
```

Do not enable paid managed rule groups solely for practice.

---

## 74. Practice — Design a Rate-Based Rule

Scenario:

```text
/login endpoint
```

Design conceptually:

```text
Scope:
URI = /login

Aggregation:
Client IP

Limit:
Based on Normal Traffic

Action:
Count First
```

After observation:

```text
Count
→ Challenge / Block
```

---

## 75. Practice — Count Before Block

For a new managed rule:

```text
Rule Action Override
→ Count
```

Review:

```text
Matched Requests

False Positives

Affected URLs

Client Types
```

Then decide whether enforcement is safe.

---

## 76. Practice — Review Shield

Navigate:

```text
AWS WAF & Shield
   |
   v
Shield
```

Review:

```text
Shield Standard

Shield Advanced

Protected Resources

DDoS Events
```

Do not subscribe to Shield Advanced solely for practice because it incurs significant cost.

---

## 77. Optional CLI Practice

List Web ACLs:

```bash
aws wafv2 list-web-acls \
  --scope REGIONAL \
  --region ap-northeast-1
```

For CloudFront:

```bash
aws wafv2 list-web-acls \
  --scope CLOUDFRONT \
  --region us-east-1
```

List IP sets:

```bash
aws wafv2 list-ip-sets \
  --scope REGIONAL \
  --region ap-northeast-1
```

Get logging configuration:

```bash
aws wafv2 get-logging-configuration \
  --resource-arn <web-acl-arn>
```

Do not publish real production Web ACL ARNs or sensitive security rules in a public repository.

---

# Architecture Exercise

## 78. Secure Web Application Design

Requirements:

```text
Public Website

CloudFront

ALB

Private EC2

RDS

Login Page

Bot Traffic

DDoS Risk
```

Design:

```text
Internet
   |
   v
Route 53
   |
   v
CloudFront
   |
   +-- Shield
   |
   +-- AWS WAF
   |     |
   |     +-- Managed Rules
   |     +-- SQLi / XSS
   |     +-- Rate-Based Rule
   |     +-- Bot Control
   |     +-- Challenge
   |
   v
ALB
   |
   v
Private EC2
   |
   v
Private RDS
```

---

## 79. Security Decision Exercise

For each scenario, choose an appropriate first control.

### Known SQL Injection Pattern

```text
AWS Managed Rules / SQLi Rule
```

### Too Many Requests from a Client

```text
Rate-Based Rule
```

### Suspicious Automated Browser

```text
Challenge / Bot Control
```

### Human Verification Required

```text
CAPTCHA
```

### Large Infrastructure-Layer DDoS

```text
Shield
```

### Organization-Wide WAF Policy

```text
Firewall Manager
```

---

# Security Checklist

```text
[ ] Public web applications use appropriate WAF protection

[ ] Web ACLs are associated with intended resources

[ ] Default actions are reviewed

[ ] Rule priorities are documented

[ ] AWS Managed Rules are used where appropriate

[ ] New rules are tested with Count before enforcement

[ ] SQL injection protections are enabled where appropriate

[ ] XSS protections are enabled where appropriate

[ ] Rate limits are based on real traffic patterns

[ ] Sensitive endpoints have additional protection

[ ] Bot Control is considered for automated abuse

[ ] CAPTCHA and Challenge are used selectively

[ ] WAF logging is enabled where required

[ ] Sensitive request fields are protected in logs

[ ] CloudWatch metrics are monitored

[ ] Shield Standard protection is understood

[ ] Shield Advanced is considered for critical public workloads

[ ] Shield Advanced protected resources are explicitly configured

[ ] Application-layer DDoS mitigation is planned

[ ] Firewall Manager is considered for multi-account environments

[ ] WAF is treated as defense in depth, not as a replacement for secure coding
```

---

## Key Takeaways

- AWS WAF protects supported web applications by inspecting HTTP and HTTPS requests.
- Web ACLs contain ordered rules and a default action.
- Rule priority determines evaluation order.
- Count is useful for safely testing rules before blocking traffic.
- AWS Managed Rules provide maintained protections for common threats.
- Rate-based rules help mitigate request floods, credential attacks, and API abuse.
- CAPTCHA provides interactive human verification.
- Challenge provides silent browser verification.
- Bot Control classifies and manages automated traffic.
- WAF logs and CloudWatch metrics are important for rule tuning and investigation.
- AWS Shield Standard provides automatic baseline DDoS protection.
- Shield Advanced provides additional DDoS detection, mitigation, visibility, and response capabilities for explicitly protected resources.
- AWS WAF focuses primarily on application-layer request filtering.
- AWS Shield focuses on DDoS resilience across network, transport, and application layers.
- WAF and Shield should be used together for critical Internet-facing applications.
- AWS Firewall Manager can centrally manage protections across multiple accounts.
- WAF does not replace secure coding or application security controls.

---

## Reflection

Today I learned that AWS WAF and AWS Shield provide complementary protection for Internet-facing AWS applications.

AWS WAF inspects HTTP and HTTPS requests and allows security engineers to create rules for common application attacks, abusive clients, bots, and excessive request rates.

The most important operational lesson is to test new WAF rules using Count before changing them to Block, because an overly broad security rule can cause an application outage.

I also learned that AWS Shield Standard provides baseline DDoS protection automatically, while Shield Advanced provides additional protection and response capabilities for critical workloads.

From a cloud security perspective, WAF and Shield should be part of a defense-in-depth architecture together with secure application code, Security Groups, IAM, encryption, monitoring, and threat detection.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AWS WAF | AWS web application firewall for inspecting HTTP and HTTPS requests |
| Bot Control | AWS WAF managed protection for identifying and managing bot traffic |
| CAPTCHA | Interactive challenge used to distinguish humans from automated clients |
| Challenge | Silent browser challenge used to validate a client session |
| DDoS | Distributed Denial of Service attack |
| Managed Rule Group | Predefined and maintained collection of WAF rules |
| Rate-Based Rule | Rule that tracks request rates and limits excessive traffic |
| Shield Advanced | Paid AWS service providing enhanced DDoS protection and response capabilities |
| Shield Standard | Automatic baseline AWS DDoS protection |
| Web ACL | Ordered collection of WAF rules and a default action |
