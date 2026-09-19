# Day 17 — EBS Encryption

## Topic

Amazon EBS Encryption, AWS KMS Integration, and Secure Volume Management

---

## Objectives

- Understand Amazon EBS encryption.
- Understand encryption at rest and in transit.
- Learn how AWS KMS protects EBS encryption keys.
- Compare AWS managed and customer managed KMS keys.
- Understand EBS Encryption by Default.
- Learn how encrypted volumes and snapshots work.
- Understand how to encrypt existing unencrypted resources.
- Understand cross-account snapshot sharing.
- Identify common EBS encryption misconfigurations.
- Practice reviewing EBS encryption configurations.

---

## 1. What Is Amazon EBS?

Amazon Elastic Block Store (EBS) provides block storage volumes for Amazon EC2 instances.

EBS volumes can be used for:

- Operating system storage
- Application data
- Database files
- Log files
- Persistent workload storage

Conceptually:

```text
Amazon EC2
    |
    +-- Root EBS Volume
    |
    +-- Data EBS Volume
    |
    +-- Additional EBS Volumes
```

An EBS volume provides persistent block storage independently of the lifecycle of the attached instance, subject to the volume's deletion settings.

Because EBS volumes may contain sensitive information, encryption and access control are important security considerations.

---

## 2. What Is EBS Encryption?

Amazon EBS encryption protects data stored on EBS volumes and snapshots.

EBS encryption uses AWS Key Management Service (AWS KMS) to manage cryptographic keys.

When an encrypted EBS volume is attached to a supported EC2 instance, encryption protects:

- Data stored on the volume
- Data transferred between the instance and the EBS storage
- Snapshots created from the encrypted volume
- Volumes restored from encrypted snapshots

Conceptually:

```text
EC2 Instance
     |
     | Encrypted I/O
     |
Encrypted EBS Volume
     |
     +-- Encrypted Snapshot
             |
             +-- Encrypted Restored Volume
```

EBS encryption and decryption are transparent to the instance and applications.

An application does not need to implement its own EBS encryption logic.

---

## 3. Encryption at Rest vs Encryption in Transit

### Encryption at Rest

Encryption at rest protects data stored on persistent storage.

Example:

```text
Application Data
      |
      v
Encryption
      |
      v
Encrypted EBS Volume
```

Even if encrypted storage is accessed outside its normal authorized usage path, its contents remain protected by cryptographic controls.

### Encryption in Transit

Encryption in transit protects data while it is being transferred.

For EBS, encryption protects data transferred between the EC2 instance and its attached encrypted EBS volume.

```text
EC2 Host
    |
    | Encrypted Storage I/O
    |
EBS Storage
```

Important:

EBS encryption does not automatically encrypt application traffic between EC2 instances or between an EC2 instance and an external client.

Application-level network communication may require TLS or other transport encryption.

---

## 4. How EBS Encryption Works

Amazon EBS uses envelope encryption with AWS KMS.

The simplified encryption process is:

```text
AWS KMS Key
     |
     | Protects
     v
Encrypted Data Key
     |
     | Decrypted for authorized use
     v
Plaintext Data Key
     |
     | Encrypts and decrypts
     v
EBS Volume Data
```

The KMS key protects the data key used to encrypt the EBS volume.

The data key performs the actual volume data encryption.

This separation is called envelope encryption.

### Simplified Workflow

1. An encrypted EBS volume is created.
2. AWS KMS generates a data key protected by the selected KMS key.
3. Amazon EBS stores the encrypted data key with the volume.
4. When the volume is attached, authorized AWS services obtain the data key through AWS KMS.
5. The data key is used to encrypt and decrypt volume I/O.

The application continues using the volume normally.

---

## 5. AWS KMS Integration

AWS KMS manages cryptographic keys used by supported AWS services.

For Amazon EBS, KMS is responsible for protecting the encryption keys used by EBS volumes.

Conceptually:

```text
AWS KMS
   |
   +-- KMS Key
          |
          +-- Protects EBS Data Key
                    |
                    +-- Encrypts EBS Volume
```

A KMS key is not the same as the plaintext data key that encrypts the volume.

The KMS key is used to protect the volume's data key.

This distinction is important when troubleshooting encryption and key access.

---

## 6. AWS Managed Key vs Customer Managed Key

Amazon EBS supports AWS managed KMS keys and customer managed KMS keys.

### AWS Managed Key

The default AWS managed KMS key for EBS uses the alias:

```text
alias/aws/ebs
```

AWS creates and manages this key for EBS encryption in the relevant account and Region.

Characteristics:

- Managed by AWS
- Simplifies encryption configuration
- Suitable for many standard EBS encryption use cases
- Does not provide the same key policy control as customer managed keys

### Customer Managed Key

A customer managed KMS key is created and managed by the AWS customer.

Characteristics:

- Customer-controlled key policies
- More granular access management
- Customer-controlled key rotation configuration
- Key disabling and deletion management
- Cross-account sharing capabilities
- Additional key management responsibility and potential costs

### Comparison

| AWS Managed Key | Customer Managed Key |
|---|---|
| Managed by AWS | Managed by the customer |
| Default EBS key available | Customer creates the key |
| Limited customer control over key policy | Customer controls key policy |
| Cannot be shared across accounts for EBS snapshot use | Can support cross-account access |
| Simplified key management | More flexible key management |

The choice depends on organizational security, compliance, and operational requirements.

---

## 7. EBS Encryption by Default

Amazon EBS provides an Encryption by Default setting.

When enabled, new EBS volumes and snapshot copies created in the account and Region are encrypted automatically.

Conceptually:

```text
Create New EBS Volume
          |
          v
Encryption by Default
          |
          v
Encrypted EBS Volume
```

### Important Characteristics

- Configured separately for each AWS Region.
- Applies to newly created EBS volumes.
- Applies to snapshot copies created from unencrypted snapshots.
- Does not automatically encrypt existing volumes.
- Does not automatically encrypt existing snapshots.
- Uses the configured default EBS KMS key unless another key is selected.

Example:

```text
Existing Unencrypted Volume
          |
          | Enable Encryption by Default
          |
          v
Existing Volume Remains Unencrypted
```

However:

```text
New EBS Volume
          |
          v
Automatically Encrypted
```

Encryption by Default helps reduce the risk of accidentally creating new unencrypted storage.

---

## 8. EBS Encryption and AWS Regions

EBS encryption settings and KMS keys are Region-specific.

Example:

```text
AWS Account
│
├── ap-northeast-1
│   ├── EBS Encryption by Default
│   └── Regional KMS Key
│
└── ap-northeast-2
    ├── EBS Encryption by Default
    └── Regional KMS Key
```

Enabling encryption by default in one Region does not automatically enable it in every other Region.

A multi-Region security review should verify the configuration of every Region in use.

---

## 9. Encrypted Volumes and Snapshots

An EBS snapshot is a point-in-time backup of an EBS volume.

When a snapshot is created from an encrypted volume, the snapshot is also encrypted.

Example:

```text
Encrypted EBS Volume
        |
        v
Encrypted Snapshot
        |
        v
Encrypted Restored Volume
```

An encrypted snapshot cannot be copied as an unencrypted snapshot.

Likewise, a volume restored from an encrypted snapshot remains encrypted.

This helps preserve encryption throughout the backup and recovery process.

---

## 10. Encrypting an Existing Unencrypted Volume

Encryption by Default does not directly convert existing unencrypted EBS volumes.

To encrypt an existing unencrypted volume, a migration process is required.

### Example Migration Workflow

```text
Existing Unencrypted Volume
           |
           v
Create Snapshot
           |
           v
Create Encrypted Snapshot Copy
           |
           v
Create Encrypted Volume
           |
           v
Attach and Validate New Volume
```

### Step 1 — Prepare

Identify the volume and its attached EC2 instance.

Review:

- Volume ID
- Availability Zone
- Volume type
- Application dependencies
- Backup requirements
- Encryption requirements

For application-consistent recovery, coordinate the snapshot with the application and its write activity.

### Step 2 — Create a Snapshot

Create a snapshot of the unencrypted volume.

```text
Unencrypted Volume
        |
        v
Unencrypted Snapshot
```

### Step 3 — Create an Encrypted Copy

Copy the snapshot and enable encryption.

```text
Unencrypted Snapshot
        |
        v
Encrypted Snapshot Copy
```

Select the appropriate KMS key.

### Step 4 — Create a New Encrypted Volume

Create a new volume from the encrypted snapshot.

```text
Encrypted Snapshot
        |
        v
Encrypted EBS Volume
```

### Step 5 — Attach and Validate

Attach the new volume to the appropriate instance.

Validate:

- Data integrity
- File system
- Application functionality
- Encryption status
- Required KMS permissions

For root volumes and production workloads, plan the replacement procedure, maintenance window, recovery process, and rollback carefully.

Do not delete the original volume until the migration has been verified.

---

## 11. Changing the KMS Key

An existing encrypted EBS volume cannot have its associated KMS key directly replaced.

To use another KMS key, create a new encrypted volume using the desired key.

A common approach is:

```text
Encrypted Volume
       |
       v
Snapshot
       |
       v
Create Volume with New KMS Key
       |
       v
New Encrypted Volume
```

Alternatively, an encrypted snapshot can be copied and re-encrypted using another KMS key.

The new volume or snapshot must be validated before replacing the original resource.

---

## 12. Cross-Account Snapshot Sharing

Organizations may need to share EBS snapshots between AWS accounts.

Examples include:

- Disaster recovery
- Account migration
- Centralized backup
- Development environment preparation

Conceptually:

```text
Source AWS Account
       |
       v
Encrypted Snapshot
       |
       v
Destination AWS Account
```

When an encrypted EBS snapshot is shared, access to the snapshot alone is not sufficient.

The destination account also needs appropriate access to the customer managed KMS key used to encrypt the snapshot.

### Cross-Account Requirements

- Share the encrypted snapshot with the destination account.
- Use a customer managed KMS key that supports the required cross-account permissions.
- Configure the required KMS key policy and IAM permissions.
- Allow the destination account to copy or restore the snapshot as appropriate.

An encrypted snapshot protected by the default AWS managed EBS key cannot be shared directly across accounts.

### Recommended Workflow

```text
Source Account
      |
      v
Encrypted Snapshot
      |
      v
Share Snapshot and KMS Key Access
      |
      v
Destination Account
      |
      v
Copy Snapshot
      |
      v
Encrypt Copy with Destination KMS Key
```

This allows the destination account to manage the copied snapshot using its own KMS key.

---

## 13. KMS Key Permissions

Using a customer managed KMS key requires appropriate authorization.

Relevant KMS operations can include:

```text
kms:DescribeKey

kms:Decrypt

kms:GenerateDataKey

kms:GenerateDataKeyWithoutPlaintext

kms:CreateGrant

kms:ReEncrypt*
```

The exact permissions depend on the EBS operation.

Access must be evaluated using applicable KMS key policies, IAM policies, and grants.

### Security Principle

```text
Required EBS Operation
         |
         v
Required KMS Permissions
         |
         v
Least-Privilege Access
```

Do not grant unrestricted KMS administration merely to enable volume encryption.

For example, permissions to create grants should be restricted to the required AWS service use cases.

---

## 14. KMS Key Availability

An encrypted EBS volume depends on its associated KMS key.

If the required KMS key becomes unavailable, operations that require that key may fail.

Potential causes include:

- Disabled KMS key
- Key scheduled for deletion
- Incorrect KMS key policy
- Missing IAM permissions
- Missing KMS grants

Conceptually:

```text
Encrypted EBS Volume
        |
        v
Required KMS Key
        |
        v
Key Unavailable
        |
        v
Encryption-Related Operation May Fail
```

Therefore, KMS key lifecycle management is an important part of storage availability and disaster recovery.

A customer managed key should not be disabled or deleted without reviewing its dependencies.

---

## 15. Encryption Does Not Replace Access Control

Encryption at rest does not prevent all forms of unauthorized data access.

For example, an attacker who compromises an authorized EC2 instance may be able to read data from an attached encrypted volume through the operating system.

Conceptually:

```text
Encrypted EBS
     +
Compromised EC2 Instance
     |
     v
Potential Access to Decrypted Data
```

Encryption must be combined with:

- Least-privilege IAM
- Secure EC2 configuration
- Operating system access control
- EBS snapshot permissions
- KMS key permissions
- Logging and monitoring

This is an example of defense in depth.

---

## 16. Common EBS Encryption Misconfigurations

### Unencrypted Volumes

Problem:

```text
Sensitive Data
     |
     v
Unencrypted EBS Volume
```

Security consideration:

Enable encryption for new volumes and plan migration of existing unencrypted volumes where required.

### Encryption by Default Enabled in Only One Region

Problem:

```text
Region A
Encryption Enabled

Region B
Encryption Disabled
```

Security consideration:

Review the encryption configuration in every Region used by the organization.

### Excessive KMS Permissions

Problem:

```text
Application Role
      |
      v
Unnecessary KMS Permissions
```

Security consideration:

Grant only the KMS permissions required by the workload.

### Incorrect Snapshot Sharing

Problem:

```text
Encrypted Snapshot
       |
       v
Shared with External Account
       |
       v
Unexpected Data Access
```

Security consideration:

Review snapshot sharing permissions and the associated KMS key policy.

### KMS Key Disabled Without Dependency Review

Problem:

```text
Production EBS Volume
        |
        v
Customer Managed KMS Key
        |
        v
Key Disabled
```

Security consideration:

Review all dependent volumes, snapshots, AMIs, and recovery procedures before changing key availability.

---

## 17. Hands-on Practice

### Practice A — Review Encryption by Default

Open the AWS Management Console.

Navigate to:

```text
EC2
  |
  v
Account Attributes / Settings
  |
  v
EBS Encryption
```

Depending on the console version, the configuration may appear under EC2 Settings.

Review:

- Selected AWS Region
- Encryption by Default status
- Default KMS key

Repeat the review for another Region if applicable.

Record your findings:

```text
Region:

Encryption by Default:

Default KMS Key:

Security Observation:
```

Do not change account-wide encryption settings without understanding their effect on existing workflows.

### Practice B — Review Existing Volumes

Navigate to:

```text
EC2
  |
  v
Elastic Block Store
  |
  v
Volumes
```

For a test volume, review:

- Volume ID
- Encryption status
- KMS key
- Volume type
- Attached instance
- Availability Zone

Record:

```text
Volume ID:

Encrypted:

KMS Key:

Attached Instance:

Security Observation:
```

Do not publish real account IDs, resource IDs, customer information, or sensitive configuration details in GitHub.

### Practice C — Review Snapshots

Navigate to:

```text
EC2
  |
  v
Elastic Block Store
  |
  v
Snapshots
```

Review:

- Snapshot encryption status
- KMS key
- Source volume
- Snapshot sharing permissions

Identify whether the snapshot is encrypted and whether any external access is configured.

### Optional Practice — Encryption Migration

In a disposable test environment:

1. Create a small unencrypted test volume, if permitted.
2. Create a snapshot.
3. Create an encrypted copy of the snapshot.
4. Create a new encrypted volume from the copy.
5. Verify that the new volume is encrypted.
6. Remove temporary resources after completing the exercise.

This exercise may incur AWS charges.

Do not perform encryption migration directly on production volumes.

---

## 18. Security Checklist

When reviewing EBS encryption, ask:

```text
[ ] Is EBS Encryption by Default enabled in required Regions?

[ ] Are all sensitive EBS volumes encrypted?

[ ] Are root and data volumes protected?

[ ] Are snapshots encrypted?

[ ] Are snapshot sharing permissions appropriate?

[ ] Is the correct KMS key configured?

[ ] Are customer managed KMS key permissions restricted?

[ ] Are required KMS keys enabled and available?

[ ] Are key deletion and rotation procedures documented?

[ ] Are existing unencrypted volumes identified?

[ ] Is there a migration plan for unencrypted resources?

[ ] Are backup and recovery procedures tested?

[ ] Are encryption settings reviewed across all required Regions?

[ ] Are encryption and access control managed together?
```

---

## Key Takeaways

- Amazon EBS provides persistent block storage for EC2.
- EBS encryption protects volume data at rest and in transit between EC2 and EBS storage.
- AWS KMS protects the data keys used by encrypted EBS volumes.
- AWS managed and customer managed KMS keys provide different levels of management control.
- EBS Encryption by Default applies to new resources in the configured Region.
- Existing unencrypted volumes are not automatically encrypted when Encryption by Default is enabled.
- Snapshots created from encrypted volumes are also encrypted.
- Volumes restored from encrypted snapshots remain encrypted.
- Existing volumes cannot have their encryption status or KMS key directly changed.
- Cross-account encrypted snapshot sharing requires appropriate snapshot and KMS permissions.
- KMS key availability is important for encrypted EBS operations.
- Encryption must be combined with access control, backup, monitoring, and secure instance configuration.

---

## Reflection

Today I learned that EBS encryption protects persistent block storage through integration with AWS KMS.

The most important concept is the distinction between the KMS key and the data key used to encrypt the EBS volume.

I also learned that Encryption by Default is a preventive control for newly created resources, not an automatic migration mechanism for existing unencrypted volumes.

Encrypted snapshots preserve encryption during backup and recovery, while cross-account sharing introduces additional KMS permission requirements.

From a security perspective, I should review not only whether a volume is encrypted, but also which KMS key protects it, who can access the volume and snapshots, and whether the required key will remain available during recovery.

EBS encryption is therefore part of a broader data protection strategy that includes access control, key management, backup, and operational resilience.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Cross-Account Access | Access to resources across different AWS accounts |
| Customer Managed Key | A KMS key created and managed by an AWS customer |
| Data Key | A cryptographic key used to encrypt and decrypt data |
| EBS Encryption | Encryption of Amazon EBS volumes and snapshots |
| Encryption at Rest | Protecting data while it is stored |
| Encryption by Default | Automatic encryption of newly created eligible EBS resources |
| Encryption in Transit | Protecting data while it is transferred |
| Envelope Encryption | Encrypting data with a data key that is protected by another key |
| KMS Key | A key managed by AWS KMS that can protect other cryptographic keys |
| Snapshot | A point-in-time backup of an EBS volume |
