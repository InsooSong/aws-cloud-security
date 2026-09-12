# Day 7 — Public & Private Subnets

## Topic

Public and Private Subnets, Route Table Associations, and Secure Subnet Architecture

---

## Objectives

- Understand the difference between public and private subnets
- Understand how route tables determine subnet behavior
- Understand the requirements for direct Internet access
- Learn how public IPv4 addresses relate to public subnets
- Understand how private subnets access external services
- Learn the basic role of NAT Gateway
- Understand multi-tier subnet architecture
- Design subnet layouts across multiple Availability Zones
- Analyze subnet architecture from a security perspective

---

## 1. What Makes a Subnet Public or Private?

A subnet is not public or private because of its name.

The subnet's routing configuration determines whether it is public or private.

Conceptually:

```text
Subnet
   ↓
Route Table
   ↓
Routing Decision
```

### Public Subnet

A subnet is considered public when its route table contains a route to an Internet Gateway.

Example:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          igw-xxxxxxxx
```

The important route is:

```text
0.0.0.0/0
→ Internet Gateway
```

---

### Private Subnet

A private subnet does not have a direct route to an Internet Gateway.

Example:

```text
Destination        Target

10.0.0.0/16        local
```

or:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          nat-xxxxxxxx
```

The second example can provide outbound Internet access through a NAT Gateway, but the subnet itself is still private.

---

## 2. Public Subnet Architecture

A basic public subnet architecture looks like:

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
VPC 10.0.0.0/16
   │
   └── Public Subnet
       10.0.1.0/24
            │
            └── EC2
```

Route table:

```text
10.0.0.0/16
→ local

0.0.0.0/0
→ Internet Gateway
```

This gives the subnet a routing path to the Internet.

However, this alone does not automatically make an EC2 instance publicly reachable.

---

## 3. Requirements for Direct IPv4 Internet Access

For an EC2 instance in a public subnet to communicate directly with the Internet using IPv4, several conditions are typically required.

```text
EC2 Instance
   │
   ├── Public IPv4 / Elastic IP
   │
   ├── Security Group permits traffic
   │
   └── Subnet Route Table
            │
            └── 0.0.0.0/0
                 ↓
          Internet Gateway
```

Important components include:

- Internet Gateway attached to the VPC
- Route to the Internet Gateway
- Public IPv4 address or Elastic IP
- Security Group rules
- Network ACL rules

Therefore:

```text
Public Subnet
≠
Every resource is publicly accessible
```

A public subnet only provides a possible network path.

Other security controls still determine whether communication is permitted.

---

## 4. Public IPv4 Address

An EC2 instance may have:

```text
Private IPv4 Address
+
Public IPv4 Address
```

Example:

```text
Private IP
10.0.1.10

Public IP
203.0.113.x
```

Inside the VPC, communication primarily uses the private address.

For Internet communication, AWS maps the public IPv4 address to the instance's private IPv4 address.

A public IPv4 address alone is not enough.

The subnet must also have the appropriate route to an Internet Gateway.

---

## 5. Public Subnet Example

Consider:

```text
VPC
10.0.0.0/16

Public Subnet
10.0.1.0/24
```

Route table:

```text
10.0.0.0/16      local
0.0.0.0/0        igw-123456
```

EC2:

```text
Private IP:
10.0.1.10

Public IP:
203.0.113.x
```

Traffic flow:

```text
EC2
 ↓
Route Table
 ↓
Internet Gateway
 ↓
Internet
```

Inbound Internet traffic must also pass applicable security controls.

---

## 6. Private Subnet Architecture

A private subnet does not have a direct route to an Internet Gateway.

Example:

```text
VPC 10.0.0.0/16
│
└── Private Subnet
    10.0.11.0/24
        │
        └── Application Server
```

Basic route table:

```text
10.0.0.0/16
→ local
```

There is no:

```text
0.0.0.0/0
→ Internet Gateway
```

Therefore, resources in the subnet do not have a direct Internet route.

---

## 7. Why Use Private Subnets?

Many workloads do not need to receive connections directly from the Internet.

Examples include:

- Application servers
- Database servers
- Internal APIs
- Backend services
- Internal monitoring systems

Instead of:

```text
Internet
   ↓
Application Server
   ↓
Database
```

a more secure architecture may be:

```text
Internet
   ↓
Load Balancer
   ↓
Application Server
   ↓
Database
```

Only the necessary entry point is exposed.

---

## 8. Network Exposure

A useful security principle is:

```text
Do not expose a resource
unless it needs to be exposed.
```

For example:

```text
Load Balancer
→ Public Subnet

Application Server
→ Private Subnet

Database
→ Private Subnet
```

The Internet does not need direct connectivity to the application server or database.

This reduces the attack surface.

---

## 9. Can a Private Subnet Access the Internet?

Yes.

A private subnet can access the Internet without having a direct route to an Internet Gateway.

One common solution for IPv4 is a NAT Gateway.

Architecture:

```text
Private Subnet
      │
      ↓
NAT Gateway
      │
      ↓
Internet Gateway
      │
      ↓
Internet
```

The NAT Gateway allows resources in the private subnet to initiate connections to external destinations.

External hosts cannot use the NAT Gateway to initiate unsolicited connections directly to those private instances.

---

## 10. NAT Gateway

NAT stands for:

```text
Network Address Translation
```

A public NAT Gateway is commonly deployed in a public subnet.

Example:

```text
VPC
│
├── Public Subnet
│      │
│      └── NAT Gateway
│             ↓
│      Internet Gateway
│
└── Private Subnet
       │
       └── Application Server
```

The private subnet route table contains:

```text
0.0.0.0/0
→ NAT Gateway
```

The NAT Gateway's public subnet then has:

```text
0.0.0.0/0
→ Internet Gateway
```

---

## 11. NAT Traffic Flow

Suppose an application server needs to download an operating system update.

Traffic flow:

```text
Private EC2
10.0.11.10
      │
      ↓
Private Route Table
      │
0.0.0.0/0 → NAT Gateway
      │
      ↓
Public NAT Gateway
      │
      ↓
Public Route Table
      │
0.0.0.0/0 → Internet Gateway
      │
      ↓
Internet
```

The connection originates from the private workload.

The Internet does not obtain direct inbound connectivity to that EC2 instance through the NAT Gateway.

---

## 12. Public vs Private Route Tables

### Public Subnet Route Table

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          Internet Gateway
```

### Private Subnet Route Table with NAT

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          NAT Gateway
```

The important difference is the target for:

```text
0.0.0.0/0
```

Public:

```text
0.0.0.0/0
→ Internet Gateway
```

Private with Internet egress:

```text
0.0.0.0/0
→ NAT Gateway
```

---

## 13. Isolated Subnet

A subnet can also be isolated from the Internet.

Example route table:

```text
10.0.0.0/16
→ local
```

There is no default route to:

```text
Internet Gateway

or

NAT Gateway
```

This architecture may be useful for highly sensitive resources.

Example:

```text
Database Subnet
```

Conceptually:

```text
Application
    ↓
Database

Internet
    ✕
Database
```

---

## 14. Public, Private, and Isolated Subnets

A simple comparison:

| Subnet Type | Direct Route to IGW | Outbound Internet via NAT | Typical Resources |
|---|---:|---:|---|
| Public | Yes | Not required | Load balancer, NAT Gateway |
| Private | No | Often Yes | Application servers |
| Isolated | No | No | Databases, sensitive internal systems |

The exact design depends on application requirements.

---

## 15. Route Table Association

Every subnet must be associated with a route table.

A subnet can use:

```text
Main Route Table
```

or:

```text
Custom Route Table
```

Example:

```text
VPC
│
├── Public Subnet
│      ↓
│   Public Route Table
│
├── Private App Subnet
│      ↓
│   Private Route Table
│
└── Database Subnet
       ↓
    Isolated Route Table
```

Using separate route tables makes routing intent easier to understand and manage.

---

## 16. Example Route Table Design

### Public Route Table

```text
10.0.0.0/16
→ local

0.0.0.0/0
→ Internet Gateway
```

### Private Application Route Table

```text
10.0.0.0/16
→ local

0.0.0.0/0
→ NAT Gateway
```

### Database Route Table

```text
10.0.0.0/16
→ local
```

This results in:

```text
Public
→ Direct Internet path

Private Application
→ Outbound Internet through NAT

Database
→ No Internet route
```

---

## 17. Multi-Tier Architecture

A common application architecture separates resources into tiers.

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
Public Subnet
   │
Load Balancer
   │
   ↓
Private Application Subnet
   │
Application Server
   │
   ↓
Private / Isolated Database Subnet
   │
Database
```

This provides network separation between:

```text
Web Entry Layer

Application Layer

Data Layer
```

---

## 18. Security Benefits of Subnet Separation

Subnet separation can help improve:

- Network segmentation
- Attack surface reduction
- Access control
- Routing control
- Incident containment
- Architecture visibility

Instead of placing everything into:

```text
Public Subnet
```

resources can be separated according to their purpose.

Example:

```text
Internet-facing
→ Public

Backend
→ Private

Database
→ Isolated / Private
```

---

## 19. Multi-AZ Subnet Design

Production architectures often use multiple Availability Zones.

Example:

```text
VPC 10.0.0.0/16
│
├── Availability Zone A
│   │
│   ├── Public Subnet A
│   │   10.0.1.0/24
│   │
│   ├── Private App Subnet A
│   │   10.0.11.0/24
│   │
│   └── Database Subnet A
│       10.0.21.0/24
│
└── Availability Zone B
    │
    ├── Public Subnet B
    │   10.0.2.0/24
    │
    ├── Private App Subnet B
    │   10.0.12.0/24
    │
    └── Database Subnet B
        10.0.22.0/24
```

This provides both:

```text
Network Segmentation
+
Availability Zone Redundancy
```

---

## 20. Example Production Architecture

```text
                      Internet
                          │
                          ↓
                  Internet Gateway
                          │
                          ↓
               ┌─────────────────────┐
               │   VPC 10.0.0.0/16  │
               │                     │
       ┌───────┴────────┐   ┌────────┴───────┐
       │      AZ-A      │   │      AZ-B      │
       │                │   │                │
       │ Public Subnet  │   │ Public Subnet  │
       │   10.0.1.0/24  │   │   10.0.2.0/24  │
       │       │        │   │       │        │
       │   Load Balancer│   │   Load Balancer│
       │       │        │   │       │        │
       │       ↓        │   │       ↓        │
       │ Private App    │   │ Private App    │
       │ 10.0.11.0/24   │   │ 10.0.12.0/24   │
       │       │        │   │       │        │
       │       ↓        │   │       ↓        │
       │ Database       │   │ Database       │
       │ 10.0.21.0/24   │   │ 10.0.22.0/24   │
       │                │   │                │
       └────────────────┘   └────────────────┘
```

This architecture minimizes direct exposure of internal workloads.

---

## 21. NAT Gateway High Availability

If an architecture spans multiple Availability Zones, NAT design should also consider availability.

Example:

```text
AZ-A

Private Subnet A
      ↓
NAT Gateway A
      ↓
Internet


AZ-B

Private Subnet B
      ↓
NAT Gateway B
      ↓
Internet
```

Using a NAT Gateway in each Availability Zone can reduce cross-AZ dependencies.

Conceptually:

```text
Private Subnet A
→ NAT A

Private Subnet B
→ NAT B
```

This can improve resilience.

---

## 22. Security Group Relationships

Subnet placement alone does not determine which resources may communicate.

Security Groups also control traffic.

Example:

```text
Internet
   ↓
Load Balancer SG
   ↓
Application SG
   ↓
Database SG
```

A common design is:

```text
Load Balancer SG
Allow:
HTTPS from Internet

Application SG
Allow:
Application port from Load Balancer SG

Database SG
Allow:
Database port from Application SG
```

This creates controlled communication between layers.

Security Groups will be studied in detail later.

---

## 23. Public Database Anti-Pattern

A risky architecture is:

```text
Internet
   ↓
Public Subnet
   ↓
Database
```

especially when combined with:

```text
Public IP
+
Open Security Group
```

A better design is usually:

```text
Internet
   ↓
Application
   ↓
Private Database
```

The database normally does not need direct Internet exposure.

---

## 24. Bastion Host Concept

Traditionally, administrators sometimes use a bastion host to reach instances inside private networks.

Architecture:

```text
Administrator
     ↓
Internet
     ↓
Bastion Host
Public Subnet
     ↓
Private EC2
```

The bastion host acts as a controlled entry point.

However, a bastion host itself becomes an Internet-facing system and must be carefully secured.

Modern AWS environments may also use AWS Systems Manager Session Manager to manage instances without requiring inbound SSH access.

---

## 25. Reducing Direct SSH Exposure

Less secure architecture:

```text
Internet
   ↓
TCP 22
   ↓
Every EC2 Instance
```

A better architecture may avoid exposing SSH directly.

For example:

```text
Administrator
      ↓
AWS Systems Manager
      ↓
Private EC2
```

This can reduce the need for:

```text
Public IP addresses

Inbound TCP 22

SSH key distribution
```

The exact management architecture depends on workload requirements.

---

## 26. VPC Endpoints

Private workloads do not always need a NAT Gateway to access AWS services.

For supported AWS services, VPC endpoints can provide private connectivity.

Example:

```text
Private EC2
    ↓
VPC Endpoint
    ↓
Amazon S3
```

instead of:

```text
Private EC2
    ↓
NAT Gateway
    ↓
Internet Gateway
    ↓
Amazon S3
```

Benefits can include:

- Reduced Internet dependency
- Private connectivity
- Reduced exposure
- Potential cost optimization

VPC endpoints will be studied in more detail later.

---

## 27. Routing Security Perspective

When reviewing a subnet, I should first inspect its route table.

Example questions:

```text
Does this subnet have a route to an Internet Gateway?

Does 0.0.0.0/0 point to a NAT Gateway?

Does this subnet need Internet access?

Does this resource need a public IP?

Are sensitive workloads isolated?

Are there unexpected routes?
```

The route table often reveals the intended network role of the subnet.

---

## 28. Public Does Not Mean Insecure

A public subnet is not automatically insecure.

Internet-facing services must exist somewhere.

Examples include:

```text
Application Load Balancer

Public API endpoint

NAT Gateway
```

The important question is:

```text
Does this resource actually require public connectivity?
```

If yes, public placement may be appropriate.

If no, a private subnet is usually preferable.

---

## 29. Private Does Not Mean Secure

Likewise:

```text
Private Subnet
≠
Automatically Secure
```

A private resource may still be vulnerable because of:

- Overly permissive Security Groups
- Compromised internal systems
- Excessive IAM permissions
- Vulnerable applications
- Poor patch management
- Incorrect routes
- Exposed credentials

Network placement is only one security layer.

---

## 30. Defense in Depth

AWS networking security should use multiple controls.

```text
Subnet Design
     +
Route Tables
     +
Security Groups
     +
Network ACLs
     +
IAM
     +
Logging
     +
Monitoring
```

This creates:

```text
Defense in Depth
```

No single security control should be considered sufficient by itself.

---

## 31. Example — Three-Tier Security Flow

Consider a web application.

### User Layer

```text
Internet User
      ↓
HTTPS 443
```

### Public Layer

```text
Application Load Balancer
Public Subnet
```

### Application Layer

```text
EC2 Application
Private Subnet
```

### Database Layer

```text
Amazon RDS
Private Database Subnet
```

Traffic flow:

```text
Internet
   ↓
HTTPS 443
   ↓
Load Balancer
   ↓
Application Port
   ↓
Application Server
   ↓
Database Port
   ↓
RDS
```

Each layer should accept traffic only from the required source.

---

## 32. Example Address Plan

For practice:

```text
VPC
10.0.0.0/16
```

### Public Layer

```text
Public Subnet A
10.0.1.0/24

Public Subnet B
10.0.2.0/24
```

### Application Layer

```text
Private App Subnet A
10.0.11.0/24

Private App Subnet B
10.0.12.0/24
```

### Database Layer

```text
Private DB Subnet A
10.0.21.0/24

Private DB Subnet B
10.0.22.0/24
```

This structure provides clear separation between application tiers.

---

## 33. Hands-on Practice

For today's practice, I reviewed subnet and route table relationships in the Amazon VPC console.

I checked:

- Existing subnets
- Availability Zones
- Associated route tables
- Local routes
- Internet Gateway routes
- Public IPv4 configuration

I classified each subnet by reviewing its routing configuration.

Example:

```text
Subnet A

Route:
0.0.0.0/0 → Internet Gateway

Classification:
Public Subnet
```

Example:

```text
Subnet B

Route:
0.0.0.0/0 → NAT Gateway

Classification:
Private Subnet
```

Example:

```text
Subnet C

No default Internet route

Classification:
Isolated Subnet
```

---

## 34. Optional Architecture Exercise

Design the following environment:

```text
VPC
10.0.0.0/16
```

Requirements:

```text
2 Availability Zones

2 Public Subnets

2 Private Application Subnets

2 Private Database Subnets
```

Architecture:

```text
VPC 10.0.0.0/16

AZ-A
├── Public:      10.0.1.0/24
├── Application: 10.0.11.0/24
└── Database:    10.0.21.0/24

AZ-B
├── Public:      10.0.2.0/24
├── Application: 10.0.12.0/24
└── Database:    10.0.22.0/24
```

Determine which route table each subnet should use.

---

## 35. Security Checklist

When reviewing subnet architecture, I should ask:

```text
Which subnets have direct Internet routes?

Which resources have public IP addresses?

Do those resources actually need public access?

Are application servers separated from Internet-facing resources?

Are databases placed in private or isolated subnets?

Do private workloads need outbound Internet access?

Can VPC endpoints replace some Internet-bound traffic?

Are route table associations correct?

Are multiple Availability Zones being used?

Does each layer allow only required network communication?

Is administrative access exposed directly to the Internet?

Can Systems Manager reduce SSH exposure?
```

---

## Key Takeaways

- A subnet becomes public through its routing configuration.
- A route to an Internet Gateway provides a direct Internet path.
- A public IPv4 address alone does not make a resource reachable from the Internet.
- Private subnets do not have a direct route to an Internet Gateway.
- Private workloads can use a NAT Gateway for outbound IPv4 Internet connectivity.
- NAT Gateway does not provide unsolicited inbound Internet connectivity to private instances.
- Isolated subnets can operate without Internet routes.
- Route tables should reflect the security role of each subnet.
- Public, application, and database workloads should be separated when appropriate.
- Multi-AZ subnet design improves availability and resilience.
- VPC endpoints can provide private access to supported AWS services.
- Public subnet does not automatically mean insecure.
- Private subnet does not automatically mean secure.
- Secure network architecture requires multiple layers of controls.

---

## Reflection

Today I learned that public and private subnets are primarily defined by routing rather than by their names.

A public subnet has a route to an Internet Gateway, while a private subnet does not have a direct route to the Internet Gateway.

I also learned that private resources can still initiate outbound Internet connections through a NAT Gateway without accepting unsolicited inbound Internet connections.

From a security perspective, subnet design should reflect the role and exposure requirements of each workload.

Internet-facing components can be placed in public subnets, while application servers and databases can remain in private or isolated subnets.

However, subnet placement alone is not enough to secure an AWS workload.

Routing, Security Groups, Network ACLs, IAM, logging, monitoring, and workload security must work together as part of a defense-in-depth strategy.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Bastion Host | A controlled host traditionally used to access systems in private networks |
| Defense in Depth | Using multiple layers of security controls |
| Egress | Network traffic leaving a system or network |
| Ingress | Network traffic entering a system or network |
| Internet Gateway | A VPC component that enables communication between a VPC and the Internet |
| Internet-Facing | Accessible or designed to communicate directly with the Internet |
| Isolated Subnet | A subnet without direct Internet ingress or egress routes |
| NAT Gateway | A managed NAT service commonly used for outbound connectivity from private subnets |
| Private Subnet | A subnet without a direct route to an Internet Gateway |
| Public Subnet | A subnet with a route to an Internet Gateway |
| Route Association | The relationship between a subnet and a route table |
| Segmentation | Dividing a network into separate security zones |
