# Day 12 — VPC Security Review

## Topic

Amazon VPC Security Architecture, Traffic Flow, and Troubleshooting Review

---

## Objectives

- Review the core Amazon VPC components
- Understand how VPC networking components work together
- Review public, private, and isolated subnet design
- Understand end-to-end traffic flow
- Review Security Groups and Network ACLs
- Apply defense-in-depth to VPC architecture
- Identify common VPC security misconfigurations
- Practice systematic network troubleshooting
- Understand the role of VPC Flow Logs
- Understand the purpose of Reachability Analyzer

---

## 1. VPC Security Architecture Review

Amazon VPC provides the network foundation for many AWS workloads.

A secure VPC architecture combines multiple components:

```text
VPC
│
├── CIDR
├── Subnets
├── Route Tables
├── Internet Gateway
├── NAT Gateway
├── Security Groups
├── Network ACLs
└── Logging / Monitoring
```

No single component provides complete network security.

Security comes from combining multiple layers correctly.

---

## 2. Core VPC Components

### VPC

Defines the logical network boundary.

```text
VPC
10.0.0.0/16
```

### Subnet

Divides the VPC into smaller network segments.

```text
Public Subnet

Private Application Subnet

Private Database Subnet
```

### Route Table

Determines where network traffic is sent.

```text
Destination
→ Target
```

### Internet Gateway

Provides connectivity between a VPC and the Internet.

### NAT Gateway

Provides outbound IPv4 connectivity for private workloads.

### Security Group

Provides stateful resource-level traffic filtering.

### Network ACL

Provides stateless subnet-level traffic filtering.

---

## 3. Public, Private, and Isolated Subnets

### Public Subnet

A public subnet has a route to an Internet Gateway.

```text
0.0.0.0/0
→ Internet Gateway
```

Typical resources:

```text
Application Load Balancer

NAT Gateway

Internet-facing services
```

---

### Private Subnet

A private subnet does not have a direct route to an Internet Gateway.

It may use:

```text
0.0.0.0/0
→ NAT Gateway
```

for outbound IPv4 connectivity.

Typical resources:

```text
Application Servers

Backend Services

Internal APIs
```

---

### Isolated Subnet

An isolated subnet has no direct Internet route.

Example:

```text
10.0.0.0/16
→ local
```

Typical resources:

```text
Databases

Sensitive Internal Systems
```

---

## 4. Three-Tier Architecture

A common secure architecture separates workloads by function.

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
Public Subnet
   │
Application Load Balancer
   │
   ↓
Private Application Subnet
   │
Application Servers
   │
   ↓
Private Database Subnet
   │
Database
```

This separates:

```text
Internet-facing Layer

Application Layer

Data Layer
```

---

## 5. Multi-AZ Architecture

Production workloads should generally avoid depending on a single Availability Zone.

Example:

```text
VPC 10.0.0.0/16

AZ-A
├── Public Subnet
├── Private App Subnet
└── Private DB Subnet

AZ-B
├── Public Subnet
├── Private App Subnet
└── Private DB Subnet
```

Benefits include:

- High availability
- Fault tolerance
- Reduced single points of failure
- Improved resilience

---

## 6. Example Address Plan

```text
VPC
10.0.0.0/16

Public Subnet A
10.0.1.0/24

Public Subnet B
10.0.2.0/24

Private App Subnet A
10.0.11.0/24

Private App Subnet B
10.0.12.0/24

Private DB Subnet A
10.0.21.0/24

Private DB Subnet B
10.0.22.0/24
```

A clear address plan makes the architecture easier to understand and maintain.

---

## 7. Traffic Flow — Internet to Application

Consider:

```text
Internet User
      ↓
HTTPS 443
      ↓
Application Load Balancer
      ↓
Application Server
```

Traffic path:

```text
Internet
   ↓
Internet Gateway
   ↓
Public Route Table
   ↓
Public Subnet NACL
   ↓
ALB Security Group
   ↓
Load Balancer
   ↓
Application Security Group
   ↓
Private Application Server
```

Each layer must allow the intended communication.

---

## 8. Traffic Flow — Application to Database

Example:

```text
Application
   ↓
TCP 5432
   ↓
PostgreSQL
```

Security design:

```text
APP-SG
   ↓
TCP 5432
   ↓
DB-SG
```

Database access should normally be limited to the required application tier.

---

## 9. Traffic Flow — Private Workload to Internet

Private workloads may need outbound Internet access.

Example:

```text
Private EC2
   ↓
Private Route Table
   ↓
NAT Gateway
   ↓
Public Route Table
   ↓
Internet Gateway
   ↓
Internet
```

The private EC2 does not need a public IPv4 address.

---

## 10. Route Table Review

Routing answers:

```text
Where can traffic go?
```

Example public route table:

```text
10.0.0.0/16 → local

0.0.0.0/0 → Internet Gateway
```

Example private route table:

```text
10.0.0.0/16 → local

0.0.0.0/0 → NAT Gateway
```

Example isolated route table:

```text
10.0.0.0/16 → local
```

---

## 11. Longest Prefix Match Review

When multiple routes match a destination, AWS chooses the most specific matching route.

Example:

```text
10.0.0.0/16   → local

10.0.10.0/24  → VPC Peering

0.0.0.0/0     → NAT Gateway
```

Destination:

```text
10.0.10.50
```

Selected:

```text
10.0.10.0/24
→ VPC Peering
```

because `/24` is more specific than `/16` or `/0`.

---

## 12. Security Group Review

Security Groups provide:

```text
Resource-Level Control

Stateful Filtering

Allow Rules Only
```

Example:

```text
ALB-SG

Inbound:
TCP 443
Source: 0.0.0.0/0
```

Application:

```text
APP-SG

Inbound:
TCP 8080
Source: ALB-SG
```

Database:

```text
DB-SG

Inbound:
TCP 5432
Source: APP-SG
```

---

## 13. Network ACL Review

Network ACLs provide:

```text
Subnet-Level Control

Stateless Filtering

Allow and Deny Rules
```

Important characteristics:

```text
Lower Rule Number
→ Evaluated First

First Match
→ Applied

Return Traffic
→ Must Also Be Allowed
```

NACLs are useful as additional subnet-level guardrails.

---

## 14. Security Group vs Network ACL

| Security Group | Network ACL |
|---|---|
| Resource level | Subnet level |
| Stateful | Stateless |
| Allow only | Allow and Deny |
| No rule priority | Rule number priority |
| Return traffic automatically allowed | Return traffic must be allowed |
| Supports SG references | Primarily network-based rules |

A useful model is:

```text
Security Group
→ Primary Workload Firewall

Network ACL
→ Additional Subnet Guardrail
```

---

## 15. Defense in Depth

A secure VPC should use multiple layers.

```text
Internet
   ↓
Routing
   ↓
Network ACL
   ↓
Security Group
   ↓
Operating System Firewall
   ↓
Application Security
```

Other controls include:

```text
IAM

Encryption

Logging

Monitoring

Threat Detection
```

This approach is called:

```text
Defense in Depth
```

---

## 16. Least-Privilege Networking

Least privilege also applies to network access.

Instead of:

```text
Allow All Traffic
from
0.0.0.0/0
```

define:

```text
Required Source

Required Protocol

Required Port

Required Destination
```

Example:

```text
Internet
→ HTTPS 443
→ ALB

ALB-SG
→ TCP 8080
→ APP-SG

APP-SG
→ TCP 5432
→ DB-SG
```

---

## 17. Common Misconfiguration — Public Database

Risky architecture:

```text
Internet
   ↓
Public Database
```

Combined with:

```text
Public IP

0.0.0.0/0

Database Port
```

this creates unnecessary exposure.

A better design is:

```text
Application
   ↓
Private Database
```

---

## 18. Common Misconfiguration — SSH Open to Everyone

Risky:

```text
TCP 22
Source: 0.0.0.0/0
```

Better:

```text
TCP 22
Source: Trusted Administrator Network
```

or use an alternative management solution such as AWS Systems Manager where appropriate.

---

## 19. Common Misconfiguration — Wrong Route Table

Example:

```text
Private Subnet
```

accidentally uses:

```text
0.0.0.0/0
→ Internet Gateway
```

instead of:

```text
0.0.0.0/0
→ NAT Gateway
```

This changes the intended network design.

Always verify:

```text
Subnet
→ Route Table Association
```

---

## 20. Common Misconfiguration — Missing NAT Route

Private EC2 cannot reach the Internet.

Check:

```text
Private Route Table

0.0.0.0/0
→ NAT Gateway
```

If the route does not exist, Internet-bound traffic has no valid path.

---

## 21. Common Misconfiguration — NACL Return Traffic

Request:

```text
Client
→ TCP 443
→ Server
```

Inbound NACL allows TCP 443.

But outbound ephemeral ports are blocked.

Result:

```text
Request reaches server

Response blocked

Connection fails
```

Because NACLs are stateless, both directions must be configured.

---

## 22. Common Misconfiguration — Overly Broad Security Group

Example:

```text
All Traffic
All Ports
0.0.0.0/0
```

This creates excessive exposure.

Review:

```text
Protocol

Port

Source

Purpose
```

and remove unnecessary access.

---

## 23. Common Misconfiguration — Broad Outbound Access

Outbound access is often overlooked.

Example:

```text
All Traffic
→ 0.0.0.0/0
```

may be broader than required.

Depending on workload requirements, outbound restrictions can help reduce:

- Command-and-control communication
- Data exfiltration
- Unnecessary external access

---

## 24. VPC Flow Logs

VPC Flow Logs can capture metadata about IP traffic.

Flow Logs can be created for:

```text
VPC

Subnet

Network Interface
```

They can help with:

- Connectivity troubleshooting
- Security monitoring
- Identifying rejected traffic
- Investigating unexpected communication

Conceptually:

```text
Network Traffic
      ↓
VPC Flow Logs
      ↓
CloudWatch Logs / S3
      ↓
Analysis
```

---

## 25. Flow Log Security Use Case

Suppose suspicious outbound communication is detected.

A security engineer can review Flow Logs to investigate:

```text
Source IP

Destination IP

Source Port

Destination Port

Protocol

ACCEPT / REJECT
```

This can help identify unexpected network behavior.

---

## 26. Reachability Analyzer

Reachability Analyzer can analyze network reachability between AWS resources.

Conceptually:

```text
Source
   ↓
AWS Network Configuration
   ↓
Destination
```

It analyzes components such as:

```text
Route Tables

Security Groups

Network ACLs

Gateways

Network Interfaces
```

If a path is not reachable, it can identify the component blocking the path.

---

## 27. Reachability Analyzer Example

Problem:

```text
Application Server
cannot connect to
Database Server
```

Instead of manually checking every component first:

```text
Source:
Application

Destination:
Database

Protocol:
TCP

Port:
5432
```

Reachability Analyzer can evaluate the configured path.

Possible result:

```text
Not Reachable

Blocking Component:
Security Group
```

or:

```text
Network ACL

Route Table
```

---

## 28. Reachability Analyzer Is Not Packet Capture

Reachability Analyzer performs configuration analysis.

Conceptually:

```text
Network Configuration
→ Analyzed
```

It does not need to send test packets through the network.

It answers:

```text
Should this path be reachable
based on the current configuration?
```

---

## 29. Troubleshooting Method

When a network connection fails, avoid randomly changing rules.

Use a systematic approach.

### Step 1 — Identify Source

```text
Where does the connection start?
```

### Step 2 — Identify Destination

```text
Where should the connection go?
```

### Step 3 — Identify Protocol and Port

Example:

```text
TCP 443

TCP 5432
```

### Step 4 — Check Routing

```text
Is there a valid network path?
```

### Step 5 — Check NACL

```text
Forward allowed?

Return allowed?
```

### Step 6 — Check Security Group

```text
Does the destination allow the required traffic?
```

### Step 7 — Check OS / Application

```text
Is the service actually listening?
```

---

## 30. Troubleshooting Flow

```text
Connection Failed
       ↓
Identify Source
       ↓
Identify Destination
       ↓
Protocol / Port
       ↓
Route Table
       ↓
Network ACL
       ↓
Security Group
       ↓
Operating System Firewall
       ↓
Application
```

This process is more reliable than immediately opening additional firewall rules.

---

## 31. Scenario 1 — Internet Cannot Reach Web Application

Architecture:

```text
Internet
   ↓
ALB
```

Expected:

```text
HTTPS 443
```

Check:

```text
Internet Gateway

Public Route Table

ALB Subnet

NACL

ALB Security Group

Listener Configuration
```

Possible causes:

```text
Missing IGW route

Security Group missing TCP 443

NACL blocking traffic

Incorrect listener
```

---

## 32. Scenario 2 — Application Cannot Reach Database

Expected:

```text
Application
→ TCP 5432
→ PostgreSQL
```

Check:

```text
Route

APP-SG

DB-SG

Application Subnet NACL

Database Subnet NACL

Database Listener
```

Preferred Security Group design:

```text
DB-SG

TCP 5432
Source: APP-SG
```

---

## 33. Scenario 3 — Private EC2 Cannot Access Internet

Expected path:

```text
Private EC2
   ↓
Private Route Table
   ↓
NAT Gateway
   ↓
Internet Gateway
   ↓
Internet
```

Check:

```text
Private route:
0.0.0.0/0 → NAT Gateway

NAT Gateway status

NAT subnet route:
0.0.0.0/0 → Internet Gateway

Internet Gateway attached

Security Group outbound rules

Network ACLs
```

---

## 34. Scenario 4 — Unexpected Internet Exposure

Suppose an application server should be private.

Check:

```text
Does the instance have a public IP?

Does its subnet route to an Internet Gateway?

Does the Security Group allow public inbound access?

Does the NACL allow broad Internet traffic?
```

Security review should identify unintended exposure before it becomes an incident.

---

## 35. VPC Security Review Checklist

When reviewing a VPC, ask:

```text
Is the VPC CIDR properly planned?

Are subnet purposes clearly separated?

Are multiple Availability Zones used?

Which subnets are public?

Which subnets are private?

Which subnets are isolated?

Does every route table have an intended purpose?

Where does 0.0.0.0/0 point?

Where does ::/0 point?

Are public IP addresses necessary?

Are databases directly exposed?

Are Security Groups least-privilege?

Are administrative ports publicly accessible?

Are NACL rules ordered correctly?

Are ephemeral ports handled correctly?

Are NAT Gateways deployed appropriately?

Can VPC endpoints reduce Internet dependency?

Are VPC Flow Logs enabled where required?

Can network reachability be verified?

Are unnecessary network paths present?
```

---

## 36. Security Review Mental Model

A useful review order is:

```text
Architecture
    ↓
Addressing
    ↓
Subnet Placement
    ↓
Routing
    ↓
Network ACLs
    ↓
Security Groups
    ↓
Public Exposure
    ↓
Logging
    ↓
Monitoring
```

This helps keep reviews systematic.

---

## 37. Hands-on Practice

For today's practice, review one VPC in the AWS console.

Document:

```text
VPC CIDR

Availability Zones

Subnets

Route Tables

Internet Gateway

NAT Gateway

Security Groups

Network ACLs
```

Classify each subnet as:

```text
Public

Private

Isolated
```

Then select one communication path and trace it.

Example:

```text
Internet
→ Load Balancer
→ Application
→ Database
```

For each hop, identify:

```text
Route

NACL

Security Group

Protocol

Port
```

---

## 38. Optional Reachability Analyzer Practice

If suitable resources exist, use Reachability Analyzer to analyze one network path.

Example:

```text
Source:
Application EC2

Destination:
Database ENI

Protocol:
TCP

Destination Port:
5432
```

Review whether the path is:

```text
Reachable

or

Not Reachable
```

If not reachable, identify the blocking component.

---

## 39. Security Architecture Example

```text
                         Internet
                             │
                             ↓
                     Internet Gateway
                             │
              ┌──────────────┴──────────────┐
              │                             │
             AZ-A                          AZ-B
              │                             │
        Public Subnet                 Public Subnet
              │                             │
         ALB / NAT GW                  ALB / NAT GW
              │                             │
        Private App                  Private App
              │                             │
              └───────────┬─────────────────┘
                          │
                          ↓
                  Private Database
```

Security controls:

```text
ALB-SG
→ HTTPS from Internet

APP-SG
→ Application port from ALB-SG

DB-SG
→ Database port from APP-SG

NACL
→ Subnet-level guardrails

Route Tables
→ Intended paths only

Flow Logs
→ Network visibility
```

---

## Key Takeaways

- VPC security depends on multiple network controls working together.
- Subnet classification is primarily determined by routing.
- Public workloads should be limited to resources that require Internet-facing access.
- Private workloads can use NAT Gateway for outbound IPv4 connectivity.
- Security Groups provide stateful resource-level filtering.
- Network ACLs provide stateless subnet-level filtering.
- Routing determines whether a network path exists.
- Security controls determine whether traffic is permitted.
- Least privilege applies to both IAM and network access.
- Multi-AZ design improves resilience.
- VPC Flow Logs improve network visibility.
- Reachability Analyzer can help validate and troubleshoot configured network paths.
- Network troubleshooting should be systematic rather than based on opening broader permissions.

---

## Reflection

Today I reviewed how Amazon VPC networking and security components work together.

The most important lesson is that connectivity and security cannot be evaluated by looking at only one component.

A successful connection may depend on the route table, Network ACL, Security Group, operating system firewall, and application configuration.

I also learned that secure VPC design should minimize unnecessary public exposure and separate Internet-facing, application, and database workloads.

Security Groups provide the main workload-level traffic control, while Network ACLs can provide additional subnet-level guardrails.

Finally, VPC Flow Logs and Reachability Analyzer can improve visibility and troubleshooting by helping identify unexpected traffic or configuration problems.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Attack Surface | The set of possible points where a system can be attacked |
| Defense in Depth | Using multiple layers of security controls |
| Network Path | The route traffic follows between a source and destination |
| Network Visibility | The ability to observe and analyze network activity |
| Reachability | Whether a valid network path exists between two resources |
| Reachability Analyzer | An AWS tool that analyzes configured network paths |
| Segmentation | Separating workloads into different network zones |
| VPC Flow Logs | Logs containing metadata about IP traffic in a VPC |
