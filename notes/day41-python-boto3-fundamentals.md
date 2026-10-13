# Day 41 — Python & boto3 Fundamentals

## Topic

Python Fundamentals for AWS Security Automation, boto3 Sessions, AWS Clients, API Responses, Exceptions, and Pagination

---

## Objectives

- Understand why Python is useful for AWS security automation
- Review Python variables and basic data types
- Understand lists and dictionaries
- Learn loops and conditional statements
- Understand functions
- Learn exception handling
- Understand JSON and Python dictionaries
- Install and import boto3
- Understand boto3 Sessions
- Understand boto3 clients
- Learn how boto3 obtains AWS credentials
- Verify identity using STS
- Call EC2, S3, and IAM APIs
- Understand AWS API responses
- Learn boto3 pagination
- Understand multi-account and multi-Region considerations
- Prepare for security automation with boto3

---

# Python for Cloud Security

## 1. Why Python?

Python is widely used for:

```text
Cloud Automation

Security Automation

API Integration

Data Processing

Incident Response

Infrastructure Management
```

AWS provides:

```text
boto3
```

as the AWS SDK for Python.

Conceptually:

```text
Python
   |
   v
boto3
   |
   v
AWS API
   |
   v
AWS Services
```

---

## 2. CLI vs boto3

Day 40:

```bash
aws ec2 describe-instances
```

Python equivalent concept:

```python
ec2.describe_instances()
```

Both ultimately interact with AWS APIs.

The difference is that Python makes it easier to add:

```text
Loops

Conditions

Functions

Error Handling

Reports

Automation Logic
```

---

# Python Variables

## 3. Variables

A variable stores a value.

Example:

```python
region = "ap-northeast-1"
```

Another:

```python
severity = "CRITICAL"
```

Variables can make automation reusable.

---

## 4. Strings

Strings store text.

```python
service = "GuardDuty"
```

```python
region = "ap-northeast-1"
```

Strings use:

```text
""

or

''
```

---

## 5. Integers

Integers store whole numbers.

```python
finding_count = 10
```

```python
port = 22
```

---

## 6. Booleans

Boolean values are:

```python
True
```

and:

```python
False
```

Example:

```python
is_public = True
```

Useful for security decisions.

---

## 7. None

Python uses:

```python
None
```

to represent no value.

Example:

```python
public_ip = None
```

This may mean:

```text
EC2 instance does not have a public IPv4 address
```

---

# Lists

## 8. Python List

A list stores multiple values.

Example:

```python
regions = [
    "ap-northeast-1",
    "ap-northeast-3"
]
```

Access the first item:

```python
print(regions[0])
```

---

## 9. Security Example

```python
approved_ports = [80, 443]
```

Then:

```python
if 22 not in approved_ports:
    print("SSH is not approved")
```

Lists are useful for:

```text
Regions

Accounts

Ports

Finding IDs

Resource IDs
```

---

# Dictionaries

## 10. Python Dictionary

A dictionary stores:

```text
Key → Value
```

Example:

```python
instance = {
    "InstanceId": "i-example",
    "State": "running",
    "Public": False
}
```

---

## 11. Access Dictionary Values

```python
print(instance["InstanceId"])
```

Result:

```text
i-example
```

---

## 12. Why Dictionaries Matter for AWS?

AWS API responses are mostly represented in Python as:

```text
Dictionaries

Lists

Strings

Numbers

Booleans
```

Example conceptual response:

```python
{
    "Account": "111122223333",
    "Arn": "arn:aws:sts::...",
    "UserId": "..."
}
```

Therefore:

```python
response["Account"]
```

can extract the account.

---

# Nested Data

## 13. Nested Dictionaries

AWS responses often contain nested structures.

Example:

```python
instance = {
    "State": {
        "Name": "running"
    }
}
```

To access:

```python
instance["State"]["Name"]
```

---

## 14. Lists Inside Dictionaries

Example:

```python
response = {
    "Instances": [
        {
            "InstanceId": "i-example1"
        },
        {
            "InstanceId": "i-example2"
        }
    ]
}
```

To access first instance:

```python
response["Instances"][0]["InstanceId"]
```

---

# Conditional Statements

## 15. if Statement

Example:

```python
severity = "CRITICAL"

if severity == "CRITICAL":
    print("Immediate investigation required")
```

---

## 16. if / else

```python
public_ip = None

if public_ip:
    print("Public IP detected")
else:
    print("No public IP")
```

---

## 17. Multiple Conditions

```python
severity = "CRITICAL"
is_public = True

if severity == "CRITICAL" and is_public:
    print("High-priority remediation")
```

Security automation often combines multiple conditions.

---

# Loops

## 18. for Loop

A loop processes multiple items.

Example:

```python
regions = [
    "ap-northeast-1",
    "ap-northeast-3"
]

for region in regions:
    print(region)
```

---

## 19. Security Use Case

```python
ports = [22, 80, 443]

for port in ports:
    if port == 22:
        print("Review SSH exposure")
```

---

## 20. Loop Through AWS Resources

Conceptually:

```python
for instance in instances:
    print(instance["InstanceId"])
```

This is the foundation of AWS security scanning scripts.

---

# Functions

## 21. Why Functions?

Functions make code reusable.

Instead of:

```text
Repeat Same Logic
```

create:

```text
Reusable Function
```

---

## 22. Basic Function

```python
def check_severity(severity):
    if severity == "CRITICAL":
        print("Critical finding")
```

Call:

```python
check_severity("CRITICAL")
```

---

## 23. Return Values

```python
def is_critical(severity):
    return severity == "CRITICAL"
```

Usage:

```python
result = is_critical("CRITICAL")

print(result)
```

Output:

```text
True
```

---

## 24. Security Function Example

```python
def is_public_cidr(cidr):
    return cidr in ["0.0.0.0/0", "::/0"]
```

Usage:

```python
if is_public_cidr("0.0.0.0/0"):
    print("Public exposure detected")
```

---

# Exception Handling

## 25. Why Exceptions Matter

AWS API calls can fail because of:

```text
AccessDenied

Wrong Region

Expired Credentials

Network Failure

Resource Not Found

Invalid Parameters
```

Automation should handle errors.

---

## 26. try / except

```python
try:
    result = 10 / 0
except Exception as error:
    print(error)
```

Without error handling:

```text
One Error
→ Entire Script Stops
```

---

# botocore Exceptions

## 27. ClientError

Boto3 commonly uses:

```python
from botocore.exceptions import ClientError
```

Example:

```python
try:
    response = client.some_operation()
except ClientError as error:
    print(error)
```

---

## 28. Inspect AWS Error

Conceptually:

```python
try:
    response = client.some_operation()
except ClientError as error:
    error_code = error.response["Error"]["Code"]
    print(error_code)
```

Possible values:

```text
AccessDenied

AccessDeniedException

NoSuchBucket

ExpiredToken
```

---

## 29. Do Not Hide Errors

Poor:

```python
try:
    ...
except:
    pass
```

This hides important security information.

Better:

```python
except ClientError as error:
    print(f"AWS API error: {error}")
```

In production automation, use proper logging.

---

# JSON

## 30. AWS APIs and JSON

AWS CLI often displays responses as:

```json
{
  "Account": "111122223333",
  "Arn": "arn:aws:..."
}
```

In Python, boto3 converts these API responses into Python data structures such as:

```text
dict

list
```

---

## 31. Python json Module

Import:

```python
import json
```

Convert dictionary to JSON string:

```python
print(json.dumps(data, indent=2))
```

This is useful when:

```text
Debugging

Creating Reports

Saving Results
```

---

## 32. Security Consideration

Do not dump sensitive API responses blindly.

Responses can include:

```text
Account IDs

ARNs

Internal IP Addresses

Policies

Resource Names

Security Findings
```

Review output before sharing or committing it.

---

# Installing boto3

## 33. Install boto3

Typical command:

```bash
python3 -m pip install boto3
```

Verify:

```bash
python3 -c "import boto3; print(boto3.__version__)"
```

For project isolation, using a virtual environment is recommended.

---

# Python Virtual Environment

## 34. Create Virtual Environment

Example:

```bash
python3 -m venv .venv
```

Activate on Linux/macOS:

```bash
source .venv/bin/activate
```

Install boto3:

```bash
python -m pip install boto3
```

---

## 35. Why Use a Virtual Environment?

It isolates project dependencies.

Conceptually:

```text
System Python

Project A
→ boto3 version A

Project B
→ boto3 version B
```

This avoids dependency conflicts.

---

## 36. .gitignore

Do not commit the virtual environment.

Add:

```text
.venv/
```

to:

```text
.gitignore
```

---

# Import boto3

## 37. Basic Import

```python
import boto3
```

Then create a client:

```python
sts = boto3.client("sts")
```

---

# boto3 Sessions

## 38. What Is a Session?

A boto3 Session stores configuration context such as:

```text
Credentials

Profile

Region
```

Conceptually:

```text
Session
  |
  +-- Credentials
  +-- Region
  +-- Profile
  |
  v
AWS Clients
```

---

## 39. Default Session

```python
import boto3

session = boto3.Session()
```

This uses the available credential and configuration chain.

---

## 40. Named Profile

Example:

```python
session = boto3.Session(
    profile_name="security"
)
```

This corresponds conceptually to:

```bash
aws ... --profile security
```

---

## 41. Profile and Region

Example:

```python
session = boto3.Session(
    profile_name="development",
    region_name="ap-northeast-1"
)
```

---

# boto3 Credential Chain

## 42. Credential Discovery

Boto3 searches multiple locations for credentials.

Examples include:

```text
Explicit Session / Client Credentials

Environment Variables

AssumeRole

Web Identity

IAM Identity Center

Shared Credentials File

AWS Config

Container Credentials

EC2 Instance Role
```

Use credential providers rather than hard-coding secrets.

---

## 43. Never Hard-Code Credentials

Poor:

```python
client = boto3.client(
    "s3",
    aws_access_key_id="REAL_KEY",
    aws_secret_access_key="REAL_SECRET"
)
```

Do not store real credentials in source code.

Better:

```python
session = boto3.Session(
    profile_name="security"
)
```

or allow the environment/workload role to provide credentials.

---

# boto3 Clients

## 44. Client

A boto3 client provides low-level access to AWS service APIs.

Example:

```python
ec2 = session.client("ec2")
```

Conceptually:

```text
EC2 Client
    |
    v
EC2 APIs
```

---

## 45. Multiple Clients

Example:

```python
sts = session.client("sts")
ec2 = session.client("ec2")
s3 = session.client("s3")
iam = session.client("iam")
```

One Session can create clients for multiple AWS services.

---

# STS Identity

## 46. get_caller_identity

Python equivalent of:

```bash
aws sts get-caller-identity
```

is:

```python
import boto3

sts = boto3.client("sts")

response = sts.get_caller_identity()

print(response)
```

---

## 47. Extract Fields

```python
account = response["Account"]
arn = response["Arn"]

print(account)
print(arn)
```

`get_caller_identity()` returns the account, ARN, and user identifier for the credentials used by the request.

---

## 48. Safe Automation Pattern

Before running automation:

```python
identity = sts.get_caller_identity()

print(f"Account: {identity['Account']}")
print(f"Principal: {identity['Arn']}")
```

Always know which identity the script is using.

---

# EC2 with boto3

## 49. Create EC2 Client

```python
ec2 = session.client(
    "ec2",
    region_name="ap-northeast-1"
)
```

---

## 50. Describe Instances

Equivalent CLI:

```bash
aws ec2 describe-instances
```

Python:

```python
response = ec2.describe_instances()
```

---

## 51. EC2 Response Structure

Conceptually:

```text
response

└── Reservations
    └── Instances
        ├── InstanceId
        ├── State
        ├── PublicIpAddress
        └── SecurityGroups
```

---

## 52. Loop Through Instances

```python
response = ec2.describe_instances()

for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        print(instance["InstanceId"])
```

---

## 53. Instance State

```python
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:
        instance_id = instance["InstanceId"]
        state = instance["State"]["Name"]

        print(instance_id, state)
```

---

## 54. Optional Fields

Not every EC2 instance has:

```text
PublicIpAddress
```

Poor:

```python
public_ip = instance["PublicIpAddress"]
```

This can raise:

```text
KeyError
```

Better:

```python
public_ip = instance.get("PublicIpAddress")
```

---

## 55. Security Example

```python
for reservation in response["Reservations"]:
    for instance in reservation["Instances"]:

        instance_id = instance["InstanceId"]
        public_ip = instance.get("PublicIpAddress")

        if public_ip:
            print(f"{instance_id} has public IP: {public_ip}")
```

---

# S3 with boto3

## 56. Create S3 Client

```python
s3 = session.client("s3")
```

---

## 57. List Buckets

```python
response = s3.list_buckets()
```

Then:

```python
for bucket in response["Buckets"]:
    print(bucket["Name"])
```

---

## 58. Security Warning

Bucket names can expose:

```text
Application Names

Customer Names

Environment Names

Internal Projects
```

Do not publish real bucket inventory.

---

# IAM with boto3

## 59. Create IAM Client

```python
iam = session.client("iam")
```

---

## 60. List IAM Roles

```python
response = iam.list_roles()

for role in response["Roles"]:
    print(role["RoleName"])
```

---

## 61. Security Review Example

```python
for role in response["Roles"]:

    role_name = role["RoleName"]

    if "Admin" in role_name:
        print(f"Review role: {role_name}")
```

Important:

```text
Role Name
≠
Actual Permission
```

This only identifies candidates for deeper inspection.

---

# Pagination

## 62. Why Pagination Matters

AWS APIs often return results in pages.

Conceptually:

```text
API
 |
 +-- Page 1
 +-- Page 2
 +-- Page 3
```

Calling:

```python
ec2.describe_instances()
```

once might not be sufficient for large environments.

---

## 63. boto3 Paginator

Create paginator:

```python
paginator = ec2.get_paginator(
    "describe_instances"
)
```

Then:

```python
for page in paginator.paginate():
    print(page)
```

---

## 64. EC2 Pagination

```python
paginator = ec2.get_paginator(
    "describe_instances"
)

for page in paginator.paginate():

    for reservation in page["Reservations"]:

        for instance in reservation["Instances"]:

            print(instance["InstanceId"])
```

This provides complete enumeration.

---

## 65. Why Security Engineers Need Pagination

Suppose:

```text
Page 1
→ 50 resources

Entire Environment
→ 500 resources
```

If the script checks only page 1:

```text
450 resources
→ Never Evaluated
```

This creates a security coverage gap.

---

# Reusable Functions

## 66. Build an Identity Function

```python
def get_identity(session):

    sts = session.client("sts")

    return sts.get_caller_identity()
```

Usage:

```python
identity = get_identity(session)

print(identity["Account"])
```

---

## 67. EC2 Function

```python
def list_instances(session, region):

    ec2 = session.client(
        "ec2",
        region_name=region
    )

    paginator = ec2.get_paginator(
        "describe_instances"
    )

    for page in paginator.paginate():

        for reservation in page["Reservations"]:

            for instance in reservation["Instances"]:

                yield instance
```

---

## 68. Why yield?

`yield` allows the function to return resources one at a time.

Conceptually:

```text
Instance 1
   ↓
Process

Instance 2
   ↓
Process
```

instead of loading everything into one large list.

For beginner automation, regular lists are also fine.

---

# Building a Basic Inventory Script

## 69. Example

```python
import boto3

session = boto3.Session(
    profile_name="development",
    region_name="ap-northeast-1"
)

sts = session.client("sts")

identity = sts.get_caller_identity()

print("AWS Account:", identity["Account"])

ec2 = session.client("ec2")

paginator = ec2.get_paginator(
    "describe_instances"
)

for page in paginator.paginate():

    for reservation in page["Reservations"]:

        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            public_ip = instance.get("PublicIpAddress")

            print(
                instance_id,
                state,
                public_ip
            )
```

---

# Improving Output

## 70. f-Strings

Instead of:

```python
print(instance_id, state)
```

use:

```python
print(
    f"Instance: {instance_id} | "
    f"State: {state}"
)
```

This improves readability.

---

## 71. Security Output

Example:

```python
if public_ip:

    print(
        f"[REVIEW] "
        f"{instance_id} "
        f"has public IP {public_ip}"
    )
```

This begins turning inventory into security logic.

---

# Multi-Region Automation

## 72. Region List

Example:

```python
regions = [
    "ap-northeast-1",
    "ap-northeast-3"
]
```

Then:

```python
for region in regions:

    ec2 = session.client(
        "ec2",
        region_name=region
    )

    print(f"Checking {region}")
```

---

## 73. Why Multi-Region Matters

Remember:

```text
Tokyo Safe
≠
AWS Account Safe
```

if resources exist in:

```text
Singapore

Virginia

Frankfurt
```

Security automation must understand Region scope.

---

# Discover Available Regions

## 74. EC2 Regions

You can use EC2:

```python
ec2 = session.client(
    "ec2",
    region_name="ap-northeast-1"
)

response = ec2.describe_regions()
```

Then:

```python
regions = [
    region["RegionName"]
    for region in response["Regions"]
]
```

---

## 75. Approved Regions vs All Regions

For security operations:

```text
All AWS Regions
```

may not always be the best scan scope.

Often better:

```text
Organization Approved Regions
```

because this aligns with:

```text
SCP

Compliance

Security Coverage
```

---

# Multi-Account Automation

## 76. Multi-Account Challenge

One account:

```text
Simple
```

Organization:

```text
Security

Production

Development

Network

Shared Services
```

requires account-aware automation.

---

## 77. Cross-Account Pattern

Conceptually:

```text
Security Account
      |
      v
STS AssumeRole
      |
      v
Member Account
      |
      v
Temporary Credentials
      |
      v
boto3 Session
```

This will be studied more deeply in Day 42.

---

# Logging

## 78. Avoid print for Larger Automation

For simple study:

```python
print()
```

is fine.

For real automation use:

```python
import logging
```

Example:

```python
import logging

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(__name__)

logger.info("Security scan started")
```

---

## 79. Security Logging

Avoid logging:

```text
Secrets

Access Keys

Session Tokens

Sensitive Data
```

Automation logs can become another data exposure point.

---

# Environment Variables

## 80. Configuration Values

Instead of hard-coding:

```python
region = "ap-northeast-1"
```

you may use:

```python
import os

region = os.getenv(
    "AWS_REGION",
    "ap-northeast-1"
)
```

This allows configuration without changing code.

---

## 81. Secrets Are Different

Environment variables can be appropriate for some runtime configuration, but do not treat them as a universal secret management solution.

For actual application secrets, prefer services such as:

```text
AWS Secrets Manager
```

where appropriate.

---

# Error Handling with boto3

## 82. Example

```python
import boto3
from botocore.exceptions import ClientError

session = boto3.Session()

s3 = session.client("s3")

try:

    response = s3.get_bucket_encryption(
        Bucket="example-bucket"
    )

    print(response)

except ClientError as error:

    print(
        error.response["Error"]["Code"]
    )
```

---

## 83. Specific Errors

Better than handling every error the same way:

```python
except ClientError as error:

    code = error.response["Error"]["Code"]

    if code == "AccessDenied":
        print("Permission denied")

    else:
        print(f"AWS error: {code}")
```

---

# Boto3 Client vs Resource

## 84. Client

Example:

```python
s3 = session.client("s3")
```

Clients map closely to AWS service APIs.

This makes clients particularly useful for:

```text
Security Automation

Complete API Coverage

Consistent AWS Documentation
```

---

## 85. Resource

Some boto3 services also provide higher-level resource abstractions.

Example:

```python
s3 = session.resource("s3")
```

Resources can make some operations easier to read.

However, not every service or operation has resource support.

For this security study:

```text
Prefer Client
```

because it maps closely to AWS APIs and CLI operations.

---

# CLI to boto3 Mapping

## 86. STS

CLI:

```bash
aws sts get-caller-identity
```

boto3:

```python
sts.get_caller_identity()
```

---

## 87. EC2

CLI:

```bash
aws ec2 describe-instances
```

boto3:

```python
ec2.describe_instances()
```

---

## 88. S3

CLI:

```bash
aws s3api list-buckets
```

boto3:

```python
s3.list_buckets()
```

---

## 89. IAM

CLI:

```bash
aws iam list-roles
```

boto3:

```python
iam.list_roles()
```

---

# Security Scanner Foundation

## 90. Basic Workflow

A future security scanner can follow:

```text
Create Session
      ↓
Verify Identity
      ↓
Enumerate Regions
      ↓
Enumerate Resources
      ↓
Evaluate Security Rules
      ↓
Collect Findings
      ↓
Generate Report
```

---

## 91. Example Finding Object

Instead of printing immediately:

```python
finding = {
    "resource": "i-example",
    "region": "ap-northeast-1",
    "issue": "Public IP detected",
    "severity": "REVIEW"
}
```

Append:

```python
findings.append(finding)
```

Later:

```python
for finding in findings:
    print(finding)
```

---

## 92. Why Collect Findings?

This prepares for:

```text
JSON Reports

CSV Reports

Security Hub Integration

Slack Notifications

Ticket Creation

Dashboards
```

Day 42 will build on this.

---

# Hands-on Practice

## 93. Practice — Python Version

Check:

```bash
python3 --version
```

---

## 94. Practice — Virtual Environment

```bash
python3 -m venv .venv
```

Activate:

```bash
source .venv/bin/activate
```

Install:

```bash
python -m pip install boto3
```

---

## 95. Practice — Verify boto3

```bash
python -c \
  "import boto3; print(boto3.__version__)"
```

---

## 96. Practice — Verify Identity

Create:

```text
scripts/check_identity.py
```

Content:

```python
import boto3

session = boto3.Session()

sts = session.client("sts")

identity = sts.get_caller_identity()

print("Account:", identity["Account"])
print("Principal:", identity["Arn"])
```

Run:

```bash
python scripts/check_identity.py
```

Do not publish the real output.

---

## 97. Practice — Use Named Profile

Modify:

```python
session = boto3.Session(
    profile_name="development"
)
```

Verify that it matches:

```bash
aws sts get-caller-identity \
  --profile development
```

---

## 98. Practice — EC2 Inventory

Create:

```text
scripts/list_ec2.py
```

Example:

```python
import boto3

session = boto3.Session(
    profile_name="development",
    region_name="ap-northeast-1"
)

ec2 = session.client("ec2")

paginator = ec2.get_paginator(
    "describe_instances"
)

for page in paginator.paginate():

    for reservation in page["Reservations"]:

        for instance in reservation["Instances"]:

            instance_id = instance["InstanceId"]
            state = instance["State"]["Name"]
            public_ip = instance.get("PublicIpAddress")

            print(
                f"{instance_id} | "
                f"{state} | "
                f"{public_ip}"
            )
```

---

## 99. Practice — S3 Inventory

Create:

```text
scripts/list_s3.py
```

Example:

```python
import boto3

session = boto3.Session(
    profile_name="development"
)

s3 = session.client("s3")

paginator = s3.get_paginator(
    "list_buckets"
)

for page in paginator.paginate():

    for bucket in page["Buckets"]:

        print(bucket["Name"])
```

Do not commit real bucket names.

---

## 100. Practice — IAM Roles

Create:

```text
scripts/list_roles.py
```

Example:

```python
import boto3

session = boto3.Session(
    profile_name="development"
)

iam = session.client("iam")

paginator = iam.get_paginator(
    "list_roles"
)

for page in paginator.paginate():

    for role in page["Roles"]:

        print(role["RoleName"])
```

---

# Repository Structure

## 101. Suggested Structure

You can begin adding a small scripts directory:

```text
aws-cloud-security/
├── README.md
├── notes/
│   └── day41-python-boto3-fundamentals.md
└── scripts/
    ├── check_identity.py
    ├── list_ec2.py
    ├── list_s3.py
    └── list_roles.py
```

Keep scripts:

```text
Read-Only

Simple

Well-Commented

Credential-Free
```

at this stage.

---

# .gitignore

## 102. Recommended Entries

```gitignore
.venv/
__pycache__/
*.pyc

.env

credential-report.csv
*.log
```

Do not blindly ignore every JSON or CSV file if future sanitized reports are intentionally part of the portfolio.

---

# Common Mistakes

## 103. Hard-Coded Credentials

Never:

```python
aws_access_key_id="..."
aws_secret_access_key="..."
```

inside GitHub code.

---

## 104. No Identity Check

Poor:

```text
Run Script
→ Modify Production
```

without verifying:

```text
Account

Role

Region
```

---

## 105. Ignoring Pagination

Poor:

```python
response = iam.list_roles()
```

then assuming:

```text
All Roles Checked
```

Better:

```python
paginator = iam.get_paginator(
    "list_roles"
)
```

---

## 106. Assuming Every Field Exists

Poor:

```python
instance["PublicIpAddress"]
```

Better:

```python
instance.get("PublicIpAddress")
```

AWS responses can vary by resource configuration.

---

## 107. Catching Every Error Silently

Poor:

```python
except:
    pass
```

This can hide:

```text
AccessDenied

Expired Credentials

Configuration Errors
```

---

## 108. Scanning One Region Only

Poor:

```text
Tokyo checked
→ Entire account assumed secure
```

Security automation must understand AWS Region scope.

---

## 109. Printing Sensitive Responses

Poor:

```python
print(response)
```

for every API in production.

Responses may contain sensitive metadata.

Print only fields that are required.

---

# Troubleshooting

## 110. NoCredentialsError

Possible error:

```text
Unable to locate credentials
```

Potential reasons:

```text
No CLI Profile

SSO Session Expired

Wrong Profile Name

Environment Not Configured

No Workload Role
```

---

## 111. ProfileNotFound

Possible error:

```text
ProfileNotFound
```

Check:

```bash
aws configure list-profiles
```

and verify:

```python
profile_name="..."
```

---

## 112. AccessDenied

Authentication can work while authorization fails.

Check:

```text
IAM

Permissions Boundary

SCP

Resource Policy

Session Policy

KMS Key Policy

RCP
```

---

## 113. Wrong Region

If the script finds no EC2 instances:

```text
No Resources
```

may actually mean:

```text
Wrong Region
```

Verify:

```python
print(session.region_name)
```

---

# Security Checklist

```text
[ ] Python environment is isolated with a virtual environment

[ ] boto3 is installed inside the project environment

[ ] Real AWS credentials are never stored in source code

[ ] AWS credential providers are used

[ ] Named profiles are used when appropriate

[ ] STS identity is verified before security automation

[ ] Account context is understood

[ ] Region context is understood

[ ] boto3 clients are used for AWS security APIs

[ ] AWS responses are treated as nested Python dictionaries and lists

[ ] Optional response fields are accessed safely

[ ] Exceptions are handled explicitly

[ ] AccessDenied errors are not hidden

[ ] Pagination is used for resource enumeration

[ ] Multi-Region scope is considered

[ ] Multi-account scope is considered

[ ] Scripts begin with read-only operations

[ ] Sensitive API responses are not logged unnecessarily

[ ] Virtual environment files are excluded from Git

[ ] Real AWS resource inventory is not committed publicly
```

---

## Key Takeaways

- Python provides the programming foundation for AWS security automation.
- boto3 is the AWS SDK for Python.
- AWS CLI operations map closely to boto3 client methods.
- Python dictionaries and lists are especially important because AWS API responses use nested structures.
- Loops allow security checks to be applied across many resources.
- Functions make security logic reusable.
- Exception handling prevents one API error from crashing an entire automation workflow.
- boto3 Sessions provide profile, credential, and Region context.
- Credentials should be obtained through the AWS credential provider chain rather than hard-coded.
- `sts.get_caller_identity()` verifies the account and principal used by automation.
- boto3 clients provide direct access to AWS service APIs.
- Pagination is essential for complete resource enumeration.
- Multi-account and multi-Region context must be considered in security automation.
- Day 41 provides the foundation for building actual AWS security scanners on Day 42.

---

## Reflection

Today I learned how Python and boto3 can be used as the foundation for AWS security automation.

The most important lesson is that boto3 is closely related to the AWS CLI commands I learned previously. A CLI operation such as `aws ec2 describe-instances` maps naturally to the boto3 method `ec2.describe_instances()`.

I also learned that AWS API responses are primarily represented as Python dictionaries and lists, which makes understanding nested data structures essential for cloud security automation.

Pagination, exception handling, credential management, account verification, and Region awareness are also critical because a script that silently misses resources or runs against the wrong environment can create dangerous security blind spots.

From a cloud security perspective, Python allows repetitive security investigation steps to become repeatable, scalable, and eventually automated across multiple resources, Regions, and AWS accounts.

---

## Vocabulary

| Word | Meaning |
|---|---|
| boto3 | AWS SDK for Python |
| Client | Low-level boto3 interface for calling AWS service APIs |
| ClientError | botocore exception representing many AWS API errors |
| Credential Provider Chain | Ordered sources that boto3 checks when locating AWS credentials |
| Dictionary | Python key-value data structure commonly used for AWS API responses |
| Exception | Error condition that can be handled programmatically |
| List | Ordered Python collection used frequently in AWS API responses |
| Paginator | boto3 mechanism for processing all pages of a paginated AWS API |
| SDK | Software Development Kit used by applications to interact with a service |
| Session | boto3 object containing AWS credential, profile, and Region context |
