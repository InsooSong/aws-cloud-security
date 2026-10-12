# Day 39 — AWS CLI Fundamentals

## Topic

AWS CLI Fundamentals, Authentication, Profiles, Regions, Output Formats, Queries, and Secure Command-Line Usage

---

## Objectives

- Understand the purpose of the AWS CLI
- Understand the structure of AWS CLI commands
- Learn how AWS CLI authentication works
- Understand profiles and configuration files
- Learn how Regions are selected
- Understand configuration precedence
- Learn common output formats
- Understand JMESPath queries
- Learn the difference between server-side and client-side filtering
- Understand AWS STS get-caller-identity
- Learn basic CLI discovery and help commands
- Understand pagination
- Learn safe credential-handling practices
- Prepare for AWS security operations automation

---

# AWS CLI Fundamentals

## 1. What Is the AWS CLI?

The AWS Command Line Interface is a command-line tool used to interact with AWS services.

Instead of:

```text
AWS Management Console
       |
       v
Click Buttons
```

we can use:

```text
Terminal
   |
   v
AWS CLI
   |
   v
AWS APIs
```

Examples:

```bash
aws ec2 describe-instances
```

```bash
aws s3api list-buckets
```

```bash
aws iam list-users
```

The CLI is useful for:

```text
Administration

Troubleshooting

Security Investigation

Automation

Scripting

CI/CD
```

---

# Command Structure

## 2. AWS CLI Command Syntax

The basic command structure is:

```text
aws <service> <operation> [options]
```

Example:

```bash
aws ec2 describe-instances
```

Breakdown:

```text
aws
→ CLI executable

ec2
→ AWS service

describe-instances
→ API operation
```

---

## 3. Additional Options

Commands can include options.

Example:

```bash
aws ec2 describe-instances \
  --region ap-northeast-1 \
  --output json
```

Options modify:

```text
Region

Profile

Output

Filters

Queries

Pagination

Request Parameters
```

---

# CLI Version

## 4. Check AWS CLI Version

Run:

```bash
aws --version
```

Example format:

```text
aws-cli/2.x.x Python/... Linux/...
```

For this repository:

```text
AWS CLI Version 2
```

should be used.

---

# Help

## 5. CLI Help

AWS CLI includes built-in help.

Examples:

```bash
aws help
```

```bash
aws ec2 help
```

```bash
aws ec2 describe-instances help
```

Think of it as:

```text
AWS CLI
   |
   v
Service
   |
   v
Operation
   |
   v
Options
```

---

## 6. Discovering Commands

Example:

```bash
aws iam help
```

can show available IAM operations.

This is useful when you know:

```text
Service
```

but not:

```text
Exact CLI Command
```

---

# Authentication

## 7. AWS CLI Authentication

The AWS CLI must identify:

```text
Who is making the request?
```

Conceptually:

```text
AWS CLI
   |
   v
Credentials
   |
   v
Signed API Request
   |
   v
AWS
```

AWS requests are cryptographically signed by the CLI.

---

## 8. Prefer Temporary Credentials

For human users, prefer:

```text
IAM Identity Center

Federation

Console-Based Short-Term Credentials

AssumeRole
```

instead of:

```text
Permanent IAM User Access Keys
```

Temporary credentials reduce long-term credential exposure.

---

# IAM Identity Center

## 9. IAM Identity Center Authentication

A common multi-account workflow uses IAM Identity Center.

Configure:

```bash
aws configure sso
```

Then authenticate:

```bash
aws sso login --profile security
```

Use the profile:

```bash
aws sts get-caller-identity \
  --profile security
```

Conceptually:

```text
User
  |
  v
IAM Identity Center
  |
  v
Temporary AWS Credentials
  |
  v
AWS CLI
```

---

## 10. SSO Session Expiration

IAM Identity Center credentials are temporary.

When the SSO session expires:

```bash
aws sso login --profile security
```

must be run again.

To sign out:

```bash
aws sso logout
```

---

# AWS Profiles

## 11. What Is a Profile?

A profile is a named AWS CLI configuration.

Example:

```text
default

development

production

security
```

Profiles let one workstation interact with multiple AWS accounts or roles.

---

## 12. Use a Profile

Example:

```bash
aws ec2 describe-instances \
  --profile development
```

Another example:

```bash
aws sts get-caller-identity \
  --profile security
```

---

## 13. List Profiles

Run:

```bash
aws configure list-profiles
```

Example:

```text
default
development
production
security
```

---

## 14. Why Named Profiles Matter

Poor:

```text
One credential
→ Used for every account
```

Better:

```text
Development Profile

Production Profile

Security Profile
```

This makes account context more explicit.

---

# Configuration Files

## 15. AWS CLI Files

On Linux and macOS, common files are:

```text
~/.aws/config

~/.aws/credentials
```

---

## 16. Config File

Example:

```ini
[default]
region = ap-northeast-1
output = json

[profile development]
region = ap-northeast-1
output = json
```

The config file commonly stores:

```text
Region

Output Format

Role Configuration

SSO Configuration
```

---

## 17. Credentials File

Traditional access-key profiles can be stored in:

```text
~/.aws/credentials
```

Conceptually:

```ini
[example]
aws_access_key_id = EXAMPLE
aws_secret_access_key = EXAMPLE
```

Never put real credential values in:

```text
GitHub

README

Shell Scripts

Screenshots

Documentation
```

---

# Credential Security

## 18. Never Commit Credentials

Never commit:

```text
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_SESSION_TOKEN
```

to Git.

Poor:

```bash
AWS_ACCESS_KEY_ID=AKIA...
```

inside a script committed to GitHub.

---

## 19. Long-Term Keys

Avoid long-term IAM user keys where temporary credential mechanisms can be used.

Better:

```text
Human
→ IAM Identity Center

Workload
→ IAM Role

Cross Account
→ AssumeRole

CI/CD
→ Workload Identity / Temporary Credentials
```

---

# Environment Variables

## 20. AWS Environment Variables

AWS CLI settings can also come from environment variables.

Examples:

```bash
export AWS_PROFILE=development
```

```bash
export AWS_REGION=ap-northeast-1
```

Temporary AWS credentials can include:

```text
AWS_ACCESS_KEY_ID

AWS_SECRET_ACCESS_KEY

AWS_SESSION_TOKEN
```

---

## 21. AWS_PROFILE

Instead of:

```bash
aws ec2 describe-instances \
  --profile development
```

for every command:

```bash
export AWS_PROFILE=development
```

Then:

```bash
aws ec2 describe-instances
```

uses that profile unless overridden.

---

# Configuration Precedence

## 22. Why Precedence Matters

AWS settings may exist in multiple places.

Example:

```text
Profile:
ap-northeast-1

Environment:
us-east-1

CLI option:
eu-west-1
```

Which Region is used?

Configuration precedence determines the answer.

---

## 23. Basic Precedence Model

A useful simplified model:

```text
Command-Line Option
        ↓
Environment Variable
        ↓
Profile / Configuration
```

Higher-precedence settings override lower-precedence settings.

Example:

```bash
export AWS_REGION=us-east-1
```

Then:

```bash
aws ec2 describe-instances \
  --region ap-northeast-1
```

uses:

```text
ap-northeast-1
```

because the command-line option has higher precedence.

---

# Configuration Inspection

## 24. Review Current Configuration

Run:

```bash
aws configure list
```

This helps identify:

```text
Profile

Access Key Source

Region

Configuration Source
```

---

## 25. Review Specific Profile

Example:

```bash
aws configure list \
  --profile development
```

Use this when troubleshooting unexpected AWS CLI behavior.

---

# Region

## 26. AWS Region

Many AWS CLI commands operate in a specific Region.

Example:

```bash
aws ec2 describe-instances \
  --region ap-northeast-1
```

Remember:

```text
EC2 Tokyo
≠
EC2 Singapore
```

---

## 27. Region Selection

Region can come from:

```text
Profile

Environment Variable

Command-Line Option
```

For security investigation, always confirm:

```text
Which Account?

Which Region?
```

---

## 28. Regional vs Global Services

Some services are heavily Regional:

```text
EC2

RDS

Lambda

GuardDuty

Inspector
```

Some services have global characteristics:

```text
IAM

Route 53

CloudFront
```

Do not assume every command behaves identically by Region.

---

# STS GetCallerIdentity

## 29. Verify Current Identity

One of the most useful AWS CLI commands is:

```bash
aws sts get-caller-identity
```

Example response:

```json
{
  "UserId": "EXAMPLE",
  "Account": "111122223333",
  "Arn": "arn:aws:sts::111122223333:assumed-role/example/example"
}
```

This answers:

```text
Who am I?

Which account am I using?

Which role / identity am I using?
```

---

## 30. Why Run It First?

Before modifying resources:

```text
aws sts get-caller-identity
```

helps prevent:

```text
Running a command in the wrong account
```

Especially in:

```text
Production

Security

Multi-Account Environments
```

---

## 31. Recommended Workflow

Before security operations:

```bash
aws sts get-caller-identity
```

Then verify Region:

```bash
aws configure get region
```

Conceptually:

```text
Identity
   ↓
Account
   ↓
Region
   ↓
Command
```

---

# Output Formats

## 32. Output Options

AWS CLI supports output formats including:

```text
json

yaml

yaml-stream

text

table
```

---

## 33. JSON

Example:

```bash
aws ec2 describe-instances \
  --output json
```

JSON is especially useful for:

```text
Automation

Scripts

JMESPath Queries

APIs

boto3 Learning
```

For this repo, JSON should be the primary format.

---

## 34. Table

Example:

```bash
aws ec2 describe-instances \
  --output table
```

Useful for:

```text
Human Readability

Quick Terminal Review
```

Less useful for automated processing.

---

## 35. Text

Example:

```bash
aws sts get-caller-identity \
  --output text
```

Text output can be useful with:

```text
grep

awk

sed

Shell Scripts
```

But care is needed when combining text output with pagination and queries.

---

## 36. YAML

Example:

```bash
aws ec2 describe-instances \
  --output yaml
```

Useful when YAML is easier to read than JSON.

---

# JMESPath Queries

## 37. What Is --query?

AWS CLI supports client-side filtering using:

```text
--query
```

It uses:

```text
JMESPath
```

syntax.

Example:

```bash
aws sts get-caller-identity \
  --query Account \
  --output text
```

Result conceptually:

```text
111122223333
```

---

## 38. Extract Multiple Fields

Example:

```bash
aws sts get-caller-identity \
  --query '{Account:Account,Arn:Arn}'
```

Output:

```json
{
  "Account": "111122223333",
  "Arn": "arn:aws:..."
}
```

---

## 39. EC2 Query Example

Example:

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].InstanceId'
```

This extracts instance IDs.

---

## 40. Custom Table Query

Example:

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].{
    ID:InstanceId,
    Type:InstanceType,
    State:State.Name
  }' \
  --output table
```

Useful for quick investigation.

---

# Filtering

## 41. Server-Side Filtering

Some AWS APIs support server-side filters.

Example:

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running"
```

Conceptually:

```text
AWS Service
   |
   v
Filter
   |
   v
Smaller Response
```

---

## 42. Client-Side Filtering

`--query` filters data after the AWS response is received by the CLI.

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].InstanceId'
```

Conceptually:

```text
AWS Response
     |
     v
AWS CLI
     |
     v
JMESPath Query
```

---

## 43. Server vs Client Filtering

```text
--filters
→ Usually service/API-side filtering

--query
→ CLI-side output filtering
```

Whenever possible for large datasets:

```text
Server-Side Filter
        +
JMESPath Query
```

can be efficient and readable.

---

# Pagination

## 44. Why Pagination Exists

Some APIs return many results.

Example:

```text
10,000 AWS Resources
```

The service may return results in multiple pages.

Conceptually:

```text
Page 1
   ↓
Page 2
   ↓
Page 3
```

AWS CLI normally handles pagination automatically for paginated operations.

---

## 45. Disable Automatic Pagination

Option:

```bash
--no-paginate
```

This causes the CLI to make only the first page request for supported paginated commands.

Use carefully.

You may unintentionally miss resources.

---

## 46. Pagination Security Risk

During security investigation:

```text
First Page Only
```

may result in:

```text
Incomplete Investigation
```

Always confirm whether the operation is paginated.

---

# Common Read-Only Commands

## 47. Identity

```bash
aws sts get-caller-identity
```

---

## 48. Regions

```bash
aws ec2 describe-regions
```

---

## 49. EC2

```bash
aws ec2 describe-instances
```

---

## 50. S3

```bash
aws s3api list-buckets
```

---

## 51. IAM

```bash
aws iam list-users
```

```bash
aws iam list-roles
```

---

## 52. CloudTrail

```bash
aws cloudtrail describe-trails
```

---

## 53. GuardDuty

```bash
aws guardduty list-detectors
```

These commands are useful foundations for Day 40.

---

# High-Level S3 vs S3API

## 54. AWS S3 Commands

AWS CLI provides high-level commands such as:

```bash
aws s3 ls
```

```bash
aws s3 cp
```

```bash
aws s3 sync
```

These are convenient for file-oriented workflows.

---

## 55. S3API Commands

There are also API-oriented commands:

```bash
aws s3api list-buckets
```

```bash
aws s3api get-bucket-encryption \
  --bucket <bucket-name>
```

For:

```text
Security Inspection

Automation

Exact API Behavior
```

`s3api` is often more useful.

---

# Read vs Write Commands

## 56. Read-Only Commands

Examples:

```text
describe-*

list-*

get-*
```

often retrieve information.

Examples:

```bash
aws ec2 describe-instances
```

```bash
aws iam list-roles
```

---

## 57. Write Commands

Examples:

```text
create-*

delete-*

put-*

update-*

modify-*

terminate-*
```

These may change AWS resources.

Example:

```bash
aws ec2 terminate-instances
```

Use extra caution.

---

## 58. Naming Is Not a Security Guarantee

Do not assume every:

```text
get
describe
list
```

operation is always harmless or that every write action follows a predictable name.

Always check:

```bash
aws <service> <command> help
```

before unfamiliar operations.

---

# Safe CLI Workflow

## 59. Before Running a Command

Use:

```text
1. Verify Profile

2. Verify Identity

3. Verify Account

4. Verify Region

5. Review Command

6. Review Resource

7. Execute
```

---

## 60. Example

```bash
export AWS_PROFILE=development

aws sts get-caller-identity

aws configure get region

aws ec2 describe-instances
```

Only after verifying context should you perform write operations.

---

# Production Safety

## 61. Production Commands

Before production operations:

```text
Do I have the correct account?

Do I have the correct profile?

Do I have the correct Region?

Do I have the correct resource ID?

Is this command read-only or modifying?

Can the action be rolled back?
```

---

## 62. Avoid Copy-Paste Blindly

Poor:

```text
Copy Internet Command
       |
       v
Paste into Production
```

Better:

```text
Understand Command
      ↓
Check Help
      ↓
Test in NonProduction
      ↓
Run in Production
```

---

# Debugging

## 63. --debug

AWS CLI provides:

```bash
--debug
```

Example:

```bash
aws sts get-caller-identity \
  --debug
```

This produces detailed diagnostic output.

Use it for:

```text
Credential Problems

Endpoint Problems

Request Signing Problems

Network Troubleshooting
```

---

## 64. Debug Output Can Be Sensitive

Debug output may contain:

```text
Request Metadata

Headers

Resource Information

Environment Context
```

Do not publish debug output without reviewing it.

---

# SSL Verification

## 65. SSL Verification

AWS CLI verifies SSL certificates by default.

There is an option:

```text
--no-verify-ssl
```

but disabling verification weakens transport security.

Avoid using it unless there is a specific controlled troubleshooting reason.

---

# CLI History and Secrets

## 66. Shell History Risk

Commands typed into the terminal may be saved in shell history.

Poor:

```bash
aws some-service command \
  --password "SecretPassword"
```

This may leave the secret in:

```text
Shell History
```

Avoid putting sensitive values directly on the command line when safer mechanisms exist.

---

## 67. Terminal Output Risk

Commands can also expose:

```text
Secrets

Account IDs

Resource ARNs

Internal Infrastructure Information
```

Do not blindly:

```text
Screenshot

Paste to GitHub

Share Logs
```

---

# Useful Environment Inspection

## 68. Current Profile

Linux/macOS:

```bash
echo $AWS_PROFILE
```

---

## 69. Current Region

```bash
aws configure get region
```

---

## 70. Current Identity

```bash
aws sts get-caller-identity
```

Together:

```text
Profile
   ↓
Region
   ↓
Identity
```

should be checked before sensitive operations.

---

# Hands-on Practice

## 71. Practice — Check CLI Version

Run:

```bash
aws --version
```

Record:

```text
AWS CLI Version:
```

Do not include unnecessary environment-specific information in public GitHub notes.

---

## 72. Practice — List Profiles

```bash
aws configure list-profiles
```

Identify which profiles are safe to use for practice.

---

## 73. Practice — Review Configuration

```bash
aws configure list
```

Then:

```bash
aws configure get region
```

Confirm which Region will be used.

---

## 74. Practice — Verify Identity

Run:

```bash
aws sts get-caller-identity
```

Identify:

```text
Account

ARN

Identity Type
```

Do not commit your real Account ID or ARN.

---

## 75. Practice — Output Formats

Try:

```bash
aws sts get-caller-identity \
  --output json
```

```bash
aws sts get-caller-identity \
  --output table
```

```bash
aws sts get-caller-identity \
  --output text
```

Compare readability.

---

## 76. Practice — Query

Run:

```bash
aws sts get-caller-identity \
  --query Account \
  --output text
```

Then:

```bash
aws sts get-caller-identity \
  --query Arn \
  --output text
```

Do not save real values in public GitHub documentation.

---

## 77. Practice — EC2 Query

If authorized:

```bash
aws ec2 describe-instances \
  --query 'Reservations[].Instances[].{
    InstanceId:InstanceId,
    Type:InstanceType,
    State:State.Name
  }' \
  --output table
```

This provides a readable EC2 inventory.

---

## 78. Practice — Server-Side Filter

Example:

```bash
aws ec2 describe-instances \
  --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId'
```

Observe the combination of:

```text
Server-Side Filtering

+

Client-Side Query
```

---

## 79. Practice — S3 Inventory

If authorized:

```bash
aws s3api list-buckets \
  --query 'Buckets[].Name'
```

Do not publish real bucket names.

---

## 80. Practice — CLI Help

Explore:

```bash
aws guardduty help
```

Then:

```bash
aws guardduty list-detectors help
```

Practice finding:

```text
Required Parameters

Optional Parameters

Output Structure

Global Options
```

---

# Troubleshooting

## 81. Unable to Locate Credentials

Error concept:

```text
Unable to locate credentials
```

Check:

```text
Are you logged in?

Is the correct profile selected?

Has the SSO session expired?

Are environment variables configured?

Is the profile name correct?
```

---

## 82. Expired Token

Possible error:

```text
ExpiredToken
```

For IAM Identity Center:

```bash
aws sso login \
  --profile <profile>
```

may be required.

---

## 83. Wrong Region

Scenario:

```bash
aws ec2 describe-instances
```

returns no instances.

Possible reason:

```text
Wrong Region
```

Check:

```bash
aws configure get region
```

and try the intended Region.

---

## 84. Wrong Account

Scenario:

```text
Expected Production Resources

But Nothing Appears
```

Check:

```bash
aws sts get-caller-identity
```

You may be authenticated to another account.

---

## 85. AccessDenied

Example:

```text
AccessDeniedException
```

Possible sources include:

```text
IAM Policy

Permissions Boundary

SCP

Resource Policy

Session Policy

KMS Policy

RCP
```

CLI authentication success does not mean every API is authorized.

---

# Security Investigation Workflow

## 86. Safe Investigation Pattern

Start with:

```bash
aws sts get-caller-identity
```

Then:

```text
Confirm Account
Confirm Region
Confirm Role
```

Then run:

```text
Read-Only Security Commands
```

Examples:

```text
Describe

List

Get
```

before considering remediation actions.

---

# CLI and Automation

## 87. Why CLI Is Important for Automation

Manual console process:

```text
Open Console
      ↓
Select Region
      ↓
Open Service
      ↓
Click Resources
```

CLI:

```text
Command
   ↓
Structured Response
   ↓
Query
   ↓
Script
```

This is the bridge to automation.

---

## 88. CLI to Shell Script

Example conceptual flow:

```text
AWS CLI
   |
   v
JSON
   |
   v
JMESPath
   |
   v
Shell Variable
   |
   v
Security Decision
```

---

## 89. CLI to boto3

AWS CLI:

```bash
aws ec2 describe-instances
```

Python boto3 concept:

```text
ec2.describe_instances()
```

Both ultimately interact with AWS service APIs.

Understanding the CLI makes boto3 easier to learn.

---

# Security Checklist

```text
[ ] AWS CLI v2 is used

[ ] Long-term access keys are avoided where possible

[ ] Human users use temporary credentials

[ ] IAM Identity Center is used where appropriate

[ ] Named profiles are used for different environments

[ ] Production and development profiles are clearly distinguishable

[ ] Current identity is verified before sensitive operations

[ ] Current Region is verified before sensitive operations

[ ] Credentials are never committed to Git

[ ] Secrets are not passed directly on command lines when avoidable

[ ] Shell history exposure is considered

[ ] JSON is used for automation-friendly output

[ ] JMESPath queries are used for structured filtering

[ ] Server-side filtering is used for large datasets where supported

[ ] Pagination is considered during investigations

[ ] --no-verify-ssl is avoided

[ ] Debug output is reviewed before sharing

[ ] Production commands are tested in non-production where possible

[ ] Read-only inspection precedes remediation

[ ] CLI output containing internal resource information is not published
```

---

## Key Takeaways

- AWS CLI provides programmatic command-line access to AWS service APIs.
- AWS CLI commands follow the service-operation-options structure.
- Authentication context is critical before running any command.
- Temporary credentials are preferable to long-lived IAM access keys.
- IAM Identity Center provides scalable CLI authentication for human users.
- Named profiles help separate accounts and environments.
- Command-line options override lower-precedence Region and output settings.
- `aws sts get-caller-identity` is one of the most important commands for verifying the active AWS identity.
- Region and account should be verified before performing security-sensitive operations.
- JSON is the preferred output format for automation.
- `--query` uses JMESPath for client-side response filtering.
- Service-specific filters can reduce data before it reaches the CLI.
- Pagination must be considered when enumerating security resources.
- CLI output and debug logs can contain sensitive infrastructure information.
- AWS CLI skills provide the foundation for shell automation and boto3.

---

## Reflection

Today I learned the fundamentals of using the AWS CLI securely.

The most important lesson is that I should always understand my authentication context before running AWS commands. In a multi-account environment, verifying the active profile, AWS account, role, and Region can prevent commands from being executed against the wrong environment.

I also learned how profiles, environment variables, command-line options, output formats, JMESPath queries, and server-side filters affect AWS CLI behavior.

From a cloud security perspective, AWS CLI is more than an administrative tool. It provides a repeatable interface to AWS APIs and forms the foundation for security investigation, scripting, Python automation, and Infrastructure as Code workflows.

---

## Vocabulary

| Word | Meaning |
|---|---|
| AWS CLI | Command-line interface used to interact with AWS service APIs |
| Client-Side Filtering | Filtering performed by the AWS CLI after receiving the service response |
| Configuration Precedence | Rules that determine which AWS CLI setting is used when multiple sources define it |
| get-caller-identity | STS operation used to identify the current AWS account and principal |
| JMESPath | Query language used by AWS CLI `--query` to filter responses |
| Pagination | Splitting large API result sets into multiple response pages |
| Profile | Named AWS CLI configuration for credentials and settings |
| Server-Side Filtering | Filtering performed by the AWS service before data is returned |
| STS | AWS Security Token Service used to issue temporary credentials |
| Temporary Credentials | Time-limited AWS credentials typically issued through STS or federation |
