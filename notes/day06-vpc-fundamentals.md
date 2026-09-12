# Day 6 — Amazon VPC Fundamentals

## Topic

Amazon VPC Fundamentals and Basic AWS Network Architecture

---

## Objectives

- Understand what Amazon VPC is
- Understand CIDR blocks
- Understand private IP address ranges
- Learn the role of subnets
- Understand route tables
- Understand Internet Gateways
- Understand basic AWS network boundaries
- Learn how VPC design affects security
- Build a basic mental model of AWS networking

---

## 1. What is Amazon VPC?

Amazon Virtual Private Cloud (VPC) is a logically isolated virtual network in AWS.

A VPC allows AWS resources to communicate inside a network that I define.

Conceptually:

```text
AWS Region
   ↓
VPC
   ↓
Subnets
   ↓
AWS Resources
```

Examples of resources that can exist inside a VPC include:

- Amazon EC2
- Amazon RDS
- Elastic Load Balancers
- ECS tasks
- EKS worker nodes
- NAT Gateways

A VPC defines the network boundary for these resources.

---

## 2. VPC as a Network Boundary

A VPC can be viewed as a private network inside AWS.

Example:

```text
AWS Region
│
└── VPC
    │
    ├── Subnet A
    ├── Subnet B
    └── Subnet C
```

Resources inside the VPC can communicate based on:

- IP addresses
- Route tables
- Security Groups
- Network ACLs
- Gateways

The VPC itself provides the logical network boundary.

---

## 3. VPC CIDR Block

When creating a VPC, a CIDR block is assigned.

Example:

```text
10.0.0.0/16
```

This defines the IP address range available inside the VPC.

A `/16` network provides a large number of IPv4 addresses.

Conceptually:

```text
VPC
10.0.0.0/16
```

Subnets are then created from smaller portions of this CIDR range.

---

## 4. CIDR Basics

CIDR stands for:

```text
Classless Inter-Domain Routing
```

CIDR notation looks like:

```text
10.0.0.0/16
192.168.1.0/24
172.16.0.0/20
```

The number after `/` represents the network prefix length.

Examples:

```text
/16
→ Larger network

/24
→ Smaller network

/28
→ Even smaller network
```

A larger prefix number means fewer available IP addresses.

---

## 5. Private IPv4 Address Ranges

AWS VPCs commonly use private IPv4 address ranges defined by RFC 1918.

The main ranges are:

```text
10.0.0.0/8

172.16.0.0/12

192.168.0.0/16
```

Examples:

```text
10.0.0.0/16

10.10.0.0/16

172.16.0.0/16

192.168.100.0/24
```

Private IP addresses are not directly routable over the public Internet.

---

## 6. Example VPC Address Space

Suppose I create:

```text
VPC CIDR
10.0.0.0/16
```

I can divide it into smaller subnet ranges.

Example:

```text
VPC: 10.0.0.0/16

├── Subnet A: 10.0.1.0/24
├── Subnet B: 10.0.2.0/24
├── Subnet C: 10.0.11.0/24
└── Subnet D: 10.0.12.0/24
```

Each subnet must use an IP range contained within the VPC CIDR block.

---

## 7. What is a Subnet?

A subnet is a range of IP addresses inside a VPC.

Each subnet belongs to a single Availability Zone.

Example:

```text
VPC
10.0.0.0/16
│
├── AZ-A
│   └── Subnet
│       10.0.1.0/24
│
└── AZ-C
    └── Subnet
        10.0.2.0/24
```

A subnet cannot span multiple Availability Zones.

This is important for both availability and network architecture.

---

## 8. Public and Private Subnets

A subnet is commonly described as public or private depending on its routing configuration.

### Public Subnet

A public subnet has a route to an Internet Gateway.

Conceptually:

```text
Public Subnet
      ↓
Route Table
      ↓
Internet Gateway
      ↓
Internet
```

### Private Subnet

A private subnet does not have a direct route to an Internet Gateway.

Conceptually:

```text
Private Subnet
      ↓
No direct route to Internet Gateway
```

Important point:

```text
Public or Private
is determined mainly by routing,
not by the subnet name.
```

---

## 9. Route Tables

A route table contains rules that determine where network traffic should be sent.

Example:

```text
Destination        Target
10.0.0.0/16        local
0.0.0.0/0          igw-xxxx
```

The `local` route allows communication within the VPC.

Example:

```text
10.0.0.0/16
→ local
```

This route is automatically created for the VPC.

---

## 10. Local Routing

Suppose:

```text
EC2-A
10.0.1.10

EC2-B
10.0.2.20
```

Both resources are inside:

```text
VPC
10.0.0.0/16
```

The VPC route table contains:

```text
10.0.0.0/16
→ local
```

This allows traffic to be routed between subnets inside the same VPC.

Security Groups and Network ACLs may still control whether the traffic is actually permitted.

---

## 11. Default Route

A default IPv4 route is written as:

```text
0.0.0.0/0
```

This means:

```text
Any IPv4 destination
```

For a public subnet, a route table may contain:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          Internet Gateway
```

The default route sends Internet-bound traffic to the Internet Gateway.

---

## 12. Internet Gateway

An Internet Gateway (IGW) allows communication between a VPC and the Internet.

Conceptually:

```text
Internet
   ↕
Internet Gateway
   ↕
VPC
```

An Internet Gateway is attached to a VPC.

Example:

```text
AWS Region
│
└── VPC
    │
    └── Internet Gateway
```

However, simply attaching an Internet Gateway does not automatically make every resource publicly accessible.

Additional conditions are required.

---

## 13. Requirements for Internet Access

For an EC2 instance to communicate directly with the Internet using IPv4, several elements are typically required.

Conceptually:

```text
EC2 Instance
   ↓
Public IPv4 Address
   ↓
Public Subnet
   ↓
Route Table
0.0.0.0/0 → Internet Gateway
   ↓
Internet Gateway
   ↓
Internet
```

Network security controls must also permit the traffic.

These may include:

```text
Security Group
Network ACL
```

Therefore:

```text
Internet Gateway attached
≠
Instance automatically public
```

---

## 14. Basic Public Subnet Architecture

Example:

```text
Internet
   │
   │
Internet Gateway
   │
   │
VPC 10.0.0.0/16
   │
   └── Public Subnet 10.0.1.0/24
           │
           └── EC2
               Public IP
```

Route table:

```text
10.0.0.0/16
→ local

0.0.0.0/0
→ Internet Gateway
```

This provides a basic path to the Internet.

---

## 15. Basic Private Subnet Architecture

Example:

```text
VPC 10.0.0.0/16
│
├── Public Subnet
│
│   └── Internet-facing resources
│
└── Private Subnet
    │
    ├── Application Server
    └── Database Server
```

A private subnet does not have:

```text
0.0.0.0/0
→ Internet Gateway
```

This reduces direct Internet exposure.

---

## 16. Multi-Tier Architecture

A common AWS architecture separates resources by function.

Example:

```text
Internet
   │
Internet Gateway
   │
Public Subnet
   │
Load Balancer
   │
Private Subnet
   │
Application Server
   │
Private Subnet
   │
Database
```

This creates multiple layers:

```text
Internet Layer

Application Layer

Database Layer
```

Security controls can be applied between each layer.

---

## 17. Availability Zone Design

High-availability architectures often use multiple Availability Zones.

Example:

```text
VPC 10.0.0.0/16

Availability Zone A
│
├── Public Subnet
│   10.0.1.0/24
│
└── Private Subnet
    10.0.11.0/24

Availability Zone C
│
├── Public Subnet
│   10.0.2.0/24
│
└── Private Subnet
    10.0.12.0/24
```

This allows workloads to be distributed across independent infrastructure.

Benefits include:

- High availability
- Fault tolerance
- Better resilience
- Reduced impact of an AZ failure

---

## 18. Example Secure VPC Layout

A simple secure architecture might look like:

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
VPC 10.0.0.0/16
│
├── Public Subnet A
│   └── Load Balancer
│
├── Public Subnet B
│   └── Load Balancer
│
├── Private Application Subnet A
│   └── EC2
│
├── Private Application Subnet B
│   └── EC2
│
├── Private Database Subnet A
│   └── RDS
│
└── Private Database Subnet B
    └── RDS
```

The general security principle is:

```text
Expose only what must be exposed.
```

---

## 19. Network Segmentation

Network segmentation separates resources into different network areas.

Instead of:

```text
One Large Subnet
│
├── Web Server
├── Application Server
└── Database
```

A better design can be:

```text
Public Subnet
→ Web / Load Balancer

Private Application Subnet
→ Application Servers

Private Database Subnet
→ Databases
```

Benefits include:

- Reduced attack surface
- Better access control
- Easier traffic filtering
- Better security monitoring
- Improved architecture clarity

---

## 20. VPC Security Perspective

When reviewing a VPC, a security engineer should ask:

```text
What is the VPC CIDR?

Are IP ranges overlapping?

Which subnets are public?

Which subnets are private?

Which resources require Internet access?

What routes exist?

Is there a default route?

Where does 0.0.0.0/0 point?

Which resources have public IP addresses?

Are workloads properly segmented?

Are databases exposed unnecessarily?
```

These questions help identify network security risks.

---

## 21. VPC Is Not a Security Control by Itself

Creating a VPC does not automatically make resources secure.

Security depends on multiple controls.

Conceptually:

```text
VPC
│
├── Routing
├── Security Groups
├── Network ACLs
├── IAM
├── Logging
└── Resource Configuration
```

For example:

```text
Private Subnet
+
Overly Permissive Security Group
```

can still create security problems.

Likewise:

```text
Public Subnet
+
Strict Security Controls
```

may be appropriate for some Internet-facing resources.

Security depends on the overall architecture.

---

## 22. VPC and Security Groups

Security Groups act as virtual firewalls for supported AWS resources.

Conceptually:

```text
Internet / Network
       ↓
Route
       ↓
Security Group
       ↓
EC2
```

Security Groups control allowed inbound and outbound traffic.

They will be studied in more detail later.

---

## 23. VPC and Network ACLs

Network ACLs operate at the subnet level.

Conceptually:

```text
Network
   ↓
Network ACL
   ↓
Subnet
   ↓
Security Group
   ↓
Resource
```

Network ACLs provide another layer of traffic control.

They will also be studied in detail later.

---

## 24. Route Table Security Risks

Incorrect routing can expose resources or create unintended connectivity.

Examples include:

```text
Private subnet accidentally receives
0.0.0.0/0 → Internet Gateway

Unexpected routes are added

Traffic is routed to the wrong network

Overlapping CIDR ranges cause routing problems
```

Therefore, route tables should be reviewed as part of a cloud security assessment.

---

## 25. CIDR Planning

CIDR ranges should be planned before creating networks.

Poor planning can cause problems later.

Example:

```text
VPC-A
10.0.0.0/16

VPC-B
10.0.0.0/16
```

If these networks later need to communicate, overlapping CIDR ranges can create routing difficulties.

A better design may use:

```text
VPC-A
10.10.0.0/16

VPC-B
10.20.0.0/16

VPC-C
10.30.0.0/16
```

This makes future network connectivity easier to manage.

---

## 26. Example Address Plan

Example:

```text
VPC
10.0.0.0/16

Public Subnets
10.0.1.0/24
10.0.2.0/24

Private Application Subnets
10.0.11.0/24
10.0.12.0/24

Private Database Subnets
10.0.21.0/24
10.0.22.0/24
```

This structure makes the purpose of each IP range easier to understand.

---

## 27. Hands-on Practice

For today's practice, I explored the Amazon VPC console.

I located the following components:

- VPCs
- Subnets
- Route tables
- Internet Gateways
- Security Groups
- Network ACLs

I reviewed the default VPC configuration and identified:

```text
VPC CIDR

Existing Subnets

Availability Zones

Route Tables

Internet Gateway
```

The goal was to understand how AWS networking components are connected.

---

## 28. Optional Practice Architecture

I can design a simple VPC using the following address plan:

```text
VPC
10.0.0.0/16

Public Subnet A
10.0.1.0/24

Public Subnet B
10.0.2.0/24

Private Subnet A
10.0.11.0/24

Private Subnet B
10.0.12.0/24
```

Architecture:

```text
AWS Region
│
└── VPC 10.0.0.0/16
    │
    ├── Availability Zone A
    │   │
    │   ├── Public Subnet
    │   │   10.0.1.0/24
    │   │
    │   └── Private Subnet
    │       10.0.11.0/24
    │
    └── Availability Zone B
        │
        ├── Public Subnet
        │   10.0.2.0/24
        │
        └── Private Subnet
            10.0.12.0/24
```

This architecture can be expanded in future lessons.

---

## Security Checklist

When reviewing a VPC, I should ask:

```text
Is the VPC CIDR properly planned?

Are CIDR ranges overlapping with other networks?

Are public and private workloads separated?

Does each subnet have the correct route table?

Does any private subnet have an unintended route to an Internet Gateway?

Which resources have public IP addresses?

Are resources distributed across multiple Availability Zones?

Are sensitive databases placed in private subnets?

Is unnecessary Internet exposure minimized?

Are routing changes monitored?
```

---

## Key Takeaways

- A VPC is a logically isolated virtual network in AWS.
- A VPC is created with one or more CIDR blocks.
- Subnets divide the VPC address space into smaller network segments.
- Each subnet exists in one Availability Zone.
- Public and private subnet behavior is primarily determined by routing.
- Route tables determine where network traffic is sent.
- `0.0.0.0/0` represents the default IPv4 route.
- An Internet Gateway provides a path between a VPC and the Internet.
- Attaching an Internet Gateway does not automatically expose every resource.
- Network segmentation reduces unnecessary exposure.
- CIDR planning is important for future network connectivity.
- A VPC alone does not provide complete security.
- Secure AWS networking requires proper routing, segmentation, firewall controls, and monitoring.

---

## Reflection

Today I learned that Amazon VPC is the foundation of AWS networking.

A VPC defines the logical network boundary, while subnets divide the network into smaller segments.

I also learned that a subnet is not public simply because it is called a public subnet. Its routing configuration determines whether it has a direct path to an Internet Gateway.

CIDR planning is also important because poorly designed or overlapping IP ranges can create problems when connecting multiple networks later.

From a security perspective, VPC design should minimize unnecessary Internet exposure and separate workloads based on their roles and sensitivity.

I will continue to evaluate AWS networks by looking at IP ranges, routing, segmentation, public exposure, and network security controls.

---

## Vocabulary

| Word | Meaning |
|---|---|
| CIDR | A notation used to define an IP network range |
| Default Route | A route used when no more specific route matches |
| Internet Gateway | A VPC component that provides connectivity to the Internet |
| Network Boundary | A logical or physical separation between network environments |
| Network Segmentation | Dividing a network into separate areas for security and management |
| Private IP | An IP address not directly routable on the public Internet |
| Private Subnet | A subnet without a direct route to an Internet Gateway |
| Public Subnet | A subnet whose routing provides a direct path to an Internet Gateway |
| Route Table | A set of rules that determines where network traffic is sent |
| Subnet | A smaller IP network inside a VPC |
| VPC | A logically isolated virtual network in AWS |
