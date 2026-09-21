# Day 18 — Amazon RDS Security

## Topic

Amazon RDS Security, Database Access Control, Encryption, Backup, and Monitoring

---

## Objectives

- Understand Amazon RDS and the Shared Responsibility Model.
- Understand the difference between EC2-hosted databases and RDS.
- Learn how to secure RDS network connectivity.
- Understand database authentication and authorization.
- Compare password authentication and IAM database authentication.
- Understand RDS encryption with AWS KMS.
- Learn how backups, snapshots, and Multi-AZ deployments work.
- Understand database logging and monitoring.
- Identify common RDS security misconfigurations.
- Practice reviewing RDS security configurations.

---

## 1. What Is Amazon RDS?

Amazon Relational Database Service (RDS) is a managed relational database service provided by AWS.

RDS simplifies database operations by managing many infrastructure-related tasks.

Examples include:

- Database provisioning
- Infrastructure maintenance
- Automated backups
- Storage management
- Database engine patching
- High availability through supported deployment options

Supported database engines include:

- PostgreSQL
- MySQL
- MariaDB
- Oracle
- Microsoft SQL Server
- Db2

Amazon Aurora is a related AWS-managed relational database service that is compatible with MySQL and PostgreSQL.

### Basic Architecture

```text
Application
     |
     v
Amazon RDS
     |
     +-- Database Engine
     +-- Managed Infrastructure
     +-- Database Storage
     +-- Backup and Recovery
     +-- Monitoring
```

Amazon RDS reduces infrastructure management responsibilities, but it does not eliminate customer security responsibilities.

---

## 2. RDS and the Shared Responsibility Model

The Shared Responsibility Model defines the security responsibilities of AWS and its customers.

### AWS Responsibilities

AWS manages the underlying infrastructure and managed-service components.

Examples include:

- Physical data center security
- Underlying hardware and networking
- Host operating system management
- Managed database infrastructure
- Supported infrastructure maintenance and patching

### Customer Responsibilities

Customers remain responsible for securing their database workloads.

Examples include:

- IAM permissions
- Database users and privileges
- Security Group configuration
- Public accessibility settings
- Database authentication
- Encryption configuration
- KMS key access
- Database parameter configuration
- Backup retention requirements
- Database logging and monitoring
- Application security

Conceptually:

```text
AWS
 |
 +-- Physical Infrastructure
 +-- Host OS
 +-- Managed Database Infrastructure

Customer
 |
 +-- IAM
 +-- Network Configuration
 +-- Database Users
 +-- Data Protection
 +-- Logging and Monitoring
 +-- Application Security
```

The exact responsibilities vary depending on the database engine and deployment configuration.

---

## 3. EC2-Hosted Database vs Amazon RDS

A database can run directly on EC2 or through Amazon RDS.

### Database on EC2

```text
EC2
 |
 +-- Guest Operating System
 +-- PostgreSQL / MySQL
 +-- Database Files
 +-- Backup Configuration
```

The customer manages:

- Operating system patching
- Database installation
- Database engine updates
- Backup implementation
- Availability architecture
- Operating system security
- Database security

### Amazon RDS

```text
Amazon RDS
 |
 +-- AWS-Managed Infrastructure
 +-- Managed Database Engine
 +-- Automated Backup Options
 +-- High Availability Options
```

AWS manages more infrastructure-related operations.

However, the customer still manages database access, workload configuration, and data protection requirements.

### Security Perspective

```text
EC2 Database
→ More infrastructure management responsibility

Amazon RDS
→ More infrastructure management handled by AWS
→ Customer still controls database security configuration
```

---

## 4. RDS Network Architecture

RDS databases normally operate inside an Amazon VPC.

A database should generally avoid direct Internet exposure unless there is a specific requirement.

Example:

```text
VPC 10.0.0.0/16
 |
 +-- Public Subnets
 |     |
 |     +-- Application Load Balancer
 |
 +-- Private Application Subnets
 |     |
 |     +-- Application EC2
 |
 +-- Private Database Subnets
       |
       +-- Amazon RDS
```

Traffic flow:

```text
Internet
    |
    v
Application Load Balancer
    |
    v
Private Application
    |
    v
Private RDS Database
```

The database does not need to accept direct connections from the Internet.

---

## 5. DB Subnet Group

An RDS DB subnet group is a collection of subnets designated for database placement.

A typical DB subnet group contains subnets in at least two Availability Zones.

Example:

```text
VPC
 |
 +-- Availability Zone A
 |     |
 |     +-- Private DB Subnet A
 |
 +-- Availability Zone B
       |
       +-- Private DB Subnet B
```

The DB subnet group determines which subnets RDS can use.

A secure design should select subnets based on:

- Network exposure requirements
- Availability requirements
- Routing configuration
- Database connectivity requirements

Important:

A DB subnet group is not a firewall.

Security Groups and other network controls are still required.

---

## 6. Public Accessibility

RDS provides a Publicly Accessible configuration.

When public accessibility is enabled, the DB instance can have a publicly reachable endpoint, subject to network configuration and access controls.

### Less Secure Design

```text
Internet
    |
    v
Publicly Accessible RDS
    |
    v
Broad Security Group Rules
```

This unnecessarily increases the database attack surface.

### Preferred Private Architecture

```text
Application EC2
    |
    v
Private RDS Endpoint
    |
    v
Database
```

For databases that only serve internal applications:

```text
Publicly Accessible
→ No
```

is generally the appropriate configuration.

Private connectivity can also be provided through supported VPN or hybrid network architectures when necessary.

---

## 7. RDS Security Groups

Security Groups control network traffic to supported RDS resources.

They are stateful and use Allow rules.

Example:

```text
Application EC2
APP-SG
    |
    | TCP 5432
    v
Amazon RDS PostgreSQL
DB-SG
```

### Example PostgreSQL Rule

```text
Security Group:
DB-SG

Inbound:
TCP 5432

Source:
APP-SG
```

### Example MySQL Rule

```text
Security Group:
DB-SG

Inbound:
TCP 3306

Source:
APP-SG
```

Using Security Group references can restrict database access to the required application resources.

Avoid unnecessarily broad rules such as:

```text
TCP 5432
Source: 0.0.0.0/0
```

or:

```text
TCP 3306
Source: 0.0.0.0/0
```

---

## 8. RDS Authentication vs Authorization

Authentication verifies the identity of a database user.

Authorization determines which database operations that user may perform.

Example:

```text
Application
    |
    v
Database Authentication
    |
    v
Database Authorization
    |
    v
SELECT / INSERT / UPDATE
```

A user may authenticate successfully but still lack permission to access a particular table.

### Authentication

```text
Who are you?
```

### Authorization

```text
What are you allowed to do?
```

Database-level authorization must be configured using the permissions and roles supported by the selected database engine.

---

## 9. AWS IAM vs Database Permissions

AWS IAM permissions and database permissions are separate concepts.

### AWS IAM

Controls AWS API operations.

Examples:

```text
rds:DescribeDBInstances

rds:ModifyDBInstance

rds:DeleteDBInstance
```

These permissions control management actions on RDS resources.

### Database Permissions

Control operations inside the database.

Examples:

```sql
SELECT
INSERT
UPDATE
DELETE
```

An IAM identity with permission to describe an RDS instance does not automatically have permission to read database tables.

Conceptually:

```text
AWS IAM
→ RDS Resource Management

Database Authorization
→ Database Object Access
```

IAM database authentication can connect AWS identity-based authentication to supported database engines, but database privileges must still be configured separately.

---

## 10. Password Authentication

Traditional database authentication uses database usernames and passwords.

Example:

```text
Application
    |
    +-- Database Username
    +-- Database Password
    |
    v
Amazon RDS
```

Security considerations include:

- Strong credentials
- Secure credential storage
- Credential rotation
- Least-privilege database accounts
- Encrypted network connections
- Avoiding application use of the database administrator account

Database passwords should not be hard-coded in source code or stored in public repositories.

---

## 11. AWS Secrets Manager

AWS Secrets Manager can securely store database credentials.

Conceptually:

```text
Application
    |
    v
IAM Role
    |
    v
AWS Secrets Manager
    |
    v
Database Credentials
    |
    v
Amazon RDS
```

Benefits include:

- Centralized credential storage
- IAM-based secret access
- Reduced hard-coded credentials
- Support for credential rotation
- Integration with supported RDS configurations

The application should receive only the permissions required to retrieve its own secret.

Secrets Manager does not automatically grant database privileges.

---

## 12. IAM Database Authentication

IAM database authentication allows supported RDS database engines to authenticate connections using an authentication token instead of a traditional database password.

Supported engines include compatible versions of:

- MariaDB
- MySQL
- PostgreSQL

Support depends on the engine, version, and AWS Region.

### Conceptual Flow

```text
Application
    |
    v
IAM Role
    |
    v
Generate Authentication Token
    |
    v
TLS Database Connection
    |
    v
Amazon RDS
    |
    v
Database User
```

The application needs appropriate IAM permissions, and the database user must be configured for IAM authentication.

Example IAM permission:

```text
rds-db:connect
```

IAM authentication tokens are short-lived.

They reduce the need to store permanent database passwords in supported authentication scenarios.

Important:

IAM database authentication does not replace database-level authorization.

The authenticated database user still needs the appropriate database privileges.

---

## 13. Database Least Privilege

Applications should use database accounts with only the permissions they require.

### Risky Example

```text
Application
    |
    v
Database Administrator Account
    |
    v
Full Database Privileges
```

If the application is compromised, excessive database permissions may increase the impact.

### Better Design

```text
Application
    |
    v
Dedicated Database User
    |
    v
Required Tables and Operations Only
```

For example, a reporting application may only need:

```sql
SELECT
```

on specific tables.

It should not automatically receive:

```sql
DROP TABLE
ALTER TABLE
CREATE USER
```

or unrestricted database administration permissions.

---

## 14. RDS Encryption at Rest

Amazon RDS supports encryption at rest using AWS KMS.

Encryption can protect:

- Database storage
- Automated backups
- Read replicas, subject to supported configurations
- Database snapshots

Conceptually:

```text
Application
    |
    v
Amazon RDS
    |
    v
Encrypted Database Storage
    |
    v
AWS KMS
```

RDS encryption protects stored data.

However, encryption does not replace database authentication, authorization, or network security.

---

## 15. Encryption of Existing Databases

For standard RDS DB instances, encryption is selected when the database instance is created.

An existing unencrypted DB instance cannot simply be modified to enable encryption in place.

A migration approach is:

```text
Unencrypted RDS
      |
      v
Create Snapshot
      |
      v
Create Encrypted Snapshot Copy
      |
      v
Restore New Encrypted RDS
      |
      v
Validate and Migrate
```

Before migration, consider:

- Application downtime
- Data consistency
- Connection endpoint changes
- Backup and recovery
- KMS key permissions
- Rollback procedures

Encryption migration should be planned and tested before production use.

---

## 16. Encryption in Transit

Database connections may carry sensitive application data and authentication information.

Use TLS to protect network communication.

Conceptually:

```text
Application
    |
    | TLS
    v
Amazon RDS
```

TLS provides protection against unauthorized interception of database traffic.

For supported engines and configurations, database parameters or engine-specific settings can be used to require encrypted connections.

Example security requirement:

```text
Application
→ Database Connection
→ TLS Required
```

The application should also validate the database server certificate according to its database client configuration.

---

## 17. RDS Backups

Amazon RDS supports automated backups and manual DB snapshots.

Backups are important for:

- Recovery from accidental deletion
- Recovery from application errors
- Disaster recovery
- Restoring corrupted data
- Operational continuity

### Automated Backups

Automated backups support recovery within the configured backup retention period.

They can provide point-in-time recovery for supported RDS configurations.

### Manual Snapshots

Manual snapshots are created explicitly.

They can be retained independently of the automated backup retention schedule.

Conceptually:

```text
Amazon RDS
    |
    +-- Automated Backups
    |
    +-- Manual Snapshots
```

Backup retention should reflect business and recovery requirements.

---

## 18. Backup Security

Backups may contain the same sensitive data as the production database.

Therefore, backups require appropriate protection.

Review:

- Snapshot encryption
- Snapshot sharing permissions
- KMS key permissions
- Backup retention
- Cross-account access
- Cross-Region recovery requirements

Example:

```text
Production Database
       |
       v
Encrypted Snapshot
       |
       v
Restricted Backup Access
```

Avoid unnecessary external sharing of database snapshots.

A backup should not be considered secure merely because the production database is private.

---

## 19. Multi-AZ Deployment

Amazon RDS supports Multi-AZ deployment options for high availability.

A typical Multi-AZ DB instance deployment maintains a standby instance in another Availability Zone.

Conceptually:

```text
Availability Zone A
       |
       v
Primary Database
       |
       | Replication
       v
Availability Zone B
       |
       v
Standby Database
```

If a supported failure occurs, RDS can perform an automatic failover.

Multi-AZ deployment can improve:

- Availability
- Fault tolerance
- Infrastructure resilience

However:

```text
Multi-AZ
≠
Backup
```

Replicated changes may include unwanted modifications or deletions.

Backups are still necessary for data recovery.

---

## 20. Read Replicas vs Multi-AZ

Read replicas and Multi-AZ deployments serve different primary purposes.

| Multi-AZ | Read Replica |
|---|---|
| High availability | Read scalability |
| Supports failover | Supports read workloads |
| Maintains additional database capacity | Provides an additional readable database |
| Does not replace backups | Does not replace backups |

Actual behavior depends on the selected engine and deployment type.

Read replicas also need appropriate network access controls, encryption, and monitoring.

---

## 21. Deletion Protection

RDS provides a deletion protection setting for supported database resources.

Conceptually:

```text
Delete DB Instance
        |
        v
Deletion Protection Enabled
        |
        v
Deletion Blocked
```

Deletion protection helps reduce accidental database deletion.

However, authorized administrators may be able to disable deletion protection.

It should be combined with:

- Least-privilege IAM
- Backup and recovery
- Change management
- Monitoring
- Appropriate administrative access controls

---

## 22. RDS Logging and Monitoring

Database security requires visibility into both AWS management activity and database activity.

Important services and features include:

```text
AWS CloudTrail

Amazon CloudWatch

RDS Database Logs

RDS Events

Enhanced Monitoring

Performance Insights / Database Performance Monitoring
```

The available monitoring features depend on the engine and deployment configuration.

---

## 23. CloudTrail vs Database Logs

AWS CloudTrail records supported AWS API activity.

Example questions:

```text
Who modified the DB instance?

Who changed the backup configuration?

Who deleted a DB snapshot?

Who changed an RDS security setting?
```

Database logs provide different information.

Example questions:

```text
Which database user connected?

Which SQL statement failed?

Was an authentication attempt rejected?

Were unexpected database operations performed?
```

CloudTrail does not automatically record every SQL query executed inside an RDS database.

Database audit logging must be configured separately where required and supported.

---

## 24. CloudWatch Monitoring

CloudWatch can monitor RDS operational metrics.

Examples include:

```text
CPUUtilization

DatabaseConnections

FreeStorageSpace

ReadLatency

WriteLatency
```

These metrics can help identify:

- Unusual connection activity
- Resource exhaustion
- Storage capacity problems
- Performance degradation
- Availability issues

However, operational metrics alone are not sufficient to detect every database security event.

Database audit logs and appropriate security monitoring should be used when required.

---

## 25. Enhanced Monitoring

RDS Enhanced Monitoring provides additional operating system-level metrics for supported RDS database instances.

It can help administrators investigate:

- CPU usage
- Memory usage
- Process activity
- Resource utilization

Enhanced Monitoring does not provide unrestricted access to the underlying operating system.

The underlying infrastructure remains managed by AWS.

---

## 26. Common RDS Security Misconfigurations

### Public Database Exposure

Risk:

```text
Publicly Accessible: Yes

Security Group:
0.0.0.0/0 → TCP 5432
```

Mitigation:

Use private database connectivity and restrict Security Group sources.

### Excessive Database Privileges

Risk:

```text
Application
→ Database Administrator Account
```

Mitigation:

Use dedicated application accounts with only required privileges.

### Hard-Coded Credentials

Risk:

```text
Database Password
→ Application Source Code
→ GitHub
```

Mitigation:

Use appropriate secret management and temporary authentication where supported.

### Unencrypted Database Storage

Risk:

```text
Sensitive Database
→ Unencrypted Storage
```

Mitigation:

Configure encryption at database creation or plan migration of existing unencrypted databases.

### Inadequate Backup Retention

Risk:

```text
Database Failure
→ Required Recovery Point Unavailable
```

Mitigation:

Define retention and recovery requirements, and test restoration.

### Missing Database Audit Logs

Risk:

```text
Unexpected SQL Activity
→ Insufficient Investigation Evidence
```

Mitigation:

Enable supported database audit logging according to security requirements.

### Missing Deletion Protection

Risk:

```text
Accidental Administrative Action
→ Database Deleted
```

Mitigation:

Enable deletion protection where appropriate and maintain recoverable backups.

---

## 27. Example — Secure RDS Architecture

```text
                    Internet
                        |
                        v
               Application Load Balancer
                        |
                        | HTTPS 443
                        v
                  Private EC2
                        |
                        | Database Port
                        v
                 Private Amazon RDS
                        |
          +-------------+-------------+
          |             |             |
          v             v             v
        KMS          Backups       Monitoring
          |             |             |
          v             v             v
      Encryption     Recovery     CloudWatch
```

### Network Controls

```text
ALB-SG:
Allow HTTPS from required clients

APP-SG:
Allow application traffic from ALB-SG

DB-SG:
Allow database traffic from APP-SG
```

### Identity Controls

```text
Application EC2
       |
       v
IAM Role
       |
       v
Secrets Manager / Supported IAM DB Authentication
       |
       v
Least-Privilege Database User
```

### Data Protection

```text
Encrypted RDS Storage

Encrypted Backups

TLS Connections

Restricted Snapshot Sharing
```

### Monitoring

```text
CloudTrail

CloudWatch

Database Logs

Security Alerts
```

This architecture combines identity, network, data protection, availability, and monitoring controls.

---

## 28. Hands-on Practice

For today's practice, review the Amazon RDS console.

Creating a database is not required.

### Practice A — Database Configuration

Navigate to:

```text
AWS Management Console
    |
    v
Amazon RDS
    |
    v
Databases
```

Review an existing test database or the database creation workflow.

Identify:

- Database engine
- Engine version
- DB instance class
- VPC
- DB subnet group
- Public accessibility
- Security Groups
- Encryption status
- KMS key
- Backup retention
- Multi-AZ configuration
- Deletion protection

### Practice B — Network Security

Review the database connectivity configuration.

Answer:

```text
Is the database publicly accessible?

Which subnet group is configured?

Which Security Groups are attached?

Which application resources can connect?

Are unnecessary database ports exposed?
```

### Practice C — Data Protection

Review:

```text
Encryption Status

KMS Key

Automated Backups

Manual Snapshots

Deletion Protection
```

Determine whether the configuration meets the intended recovery and security requirements.

### Practice D — Monitoring

Review:

```text
CloudWatch Metrics

Database Log Exports

Enhanced Monitoring

RDS Events
```

Identify which information is available for database security investigations.

### Optional Architecture Exercise

Design a secure PostgreSQL environment with:

```text
Private RDS

Private Application EC2

TCP 5432 restricted to APP-SG

Encryption at rest

TLS database connections

Least-privilege database user

Automated backups

Deletion protection

CloudWatch monitoring
```

Document the network path and explain the purpose of each security control.

Do not publish real database endpoints, credentials, account IDs, or sensitive infrastructure information in GitHub.

---

## Security Checklist

When reviewing Amazon RDS security, ask:

```text
[ ] Is the database placed in an appropriate VPC?

[ ] Are private database subnets used where appropriate?

[ ] Is public accessibility disabled unless required?

[ ] Are Security Groups restricted to necessary sources?

[ ] Are database users granted least-privilege permissions?

[ ] Are application accounts separate from administrator accounts?

[ ] Are database credentials stored securely?

[ ] Is IAM database authentication appropriate and supported?

[ ] Is encryption at rest enabled?

[ ] Are database connections protected by TLS?

[ ] Are KMS permissions appropriately restricted?

[ ] Are automated backups configured?

[ ] Is backup retention sufficient?

[ ] Are database snapshots encrypted and access-controlled?

[ ] Is Multi-AZ deployment required for availability?

[ ] Is deletion protection enabled where appropriate?

[ ] Are database logs collected and reviewed?

[ ] Are CloudWatch metrics and alarms configured?

[ ] Are database engine versions and patches managed appropriately?

[ ] Has the database recovery procedure been tested?
```

---

## Key Takeaways

- Amazon RDS is a managed relational database service.
- AWS manages the underlying infrastructure, but customers remain responsible for database security configuration.
- IAM permissions and database-level privileges are different.
- Database network access should be restricted using VPC architecture and Security Groups.
- Public database exposure should be avoided unless explicitly required.
- Applications should use dedicated, least-privilege database accounts.
- IAM database authentication is available for supported engines and configurations.
- AWS Secrets Manager can help protect and rotate database credentials.
- RDS encryption at rest uses AWS KMS.
- TLS protects database connections in transit.
- Automated backups and snapshots support recovery.
- Multi-AZ improves availability but does not replace backups.
- Deletion protection helps prevent accidental database deletion.
- CloudTrail records AWS management activity, while database logs provide database-level visibility.
- RDS security requires defense in depth.

---

## Reflection

Today I learned that Amazon RDS reduces infrastructure management responsibilities but does not eliminate the customer's responsibility for database security.

The most important distinction is that AWS IAM permissions control RDS management operations, while database privileges control access to tables and other database objects.

I also learned that database security requires multiple layers, including private network connectivity, least-privilege database accounts, secure authentication, encryption, backups, and monitoring.

Multi-AZ deployment improves availability, but it cannot replace a proper backup and recovery strategy.

From a security engineering perspective, I should evaluate RDS by considering the entire architecture rather than reviewing only the database instance configuration.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Automated Backup | A managed backup mechanism that supports database recovery |
| Database Audit Logging | Recording security-relevant database operations and events |
| Database Authentication | The process of verifying a database user's identity |
| Database Authorization | The process of determining a database user's privileges |
| DB Subnet Group | A collection of subnets used for RDS database placement |
| Deletion Protection | A control designed to prevent accidental database deletion |
| Encryption at Rest | Protecting data while it is stored |
| Failover | Switching to another database instance after a failure |
| IAM DB Authentication | Authentication to supported database engines using an IAM-generated token |
| Multi-AZ | A deployment architecture using multiple Availability Zones |
| Public Accessibility | A setting that controls whether an RDS instance can have public connectivity |
| RDS | Amazon's managed relational database service |
