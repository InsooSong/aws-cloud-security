# Day 8 — Route Tables & Internet Gateway

## Topic

AWS VPC Route Tables, Routing Decisions, and Internet Gateway Architecture

---

## Objectives

- Understand the purpose of VPC route tables
- Understand destination and target
- Learn the difference between main and custom route tables
- Understand subnet route table associations
- Understand the local route
- Learn how default routes work
- Understand longest prefix match
- Understand the role of an Internet Gateway
- Learn the difference between IPv4 and IPv6 Internet routes
- Troubleshoot basic AWS routing problems
- Analyze route tables from a cloud security perspective

---

## 1. What is a Route Table?

A route table is a set of rules that determines where network traffic is sent.

Each route contains two important elements:

```text
Destination
+
Target
```

Example:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          igw-xxxxxxxx
```

The route table examines the destination IP address of traffic and determines which target should receive it.

Conceptually:

```text
Packet
   ↓
Destination IP
   ↓
Route Table
   ↓
Matching Route
   ↓
Target
```

---

## 2. Destination

The destination specifies the IP range that a route matches.

Examples:

```text
10.0.0.0/16

10.10.0.0/16

192.168.1.0/24

0.0.0.0/0

::/0
```

Example:

```text
Destination:
10.0.0.0/16
```

means:

```text
Traffic destined for IP addresses
inside 10.0.0.0/16
```

---

## 3. Target

The target specifies where matching traffic should be sent.

Common targets include:

```text
local

Internet Gateway

NAT Gateway

VPC Peering Connection

Transit Gateway

Virtual Private Gateway

Network Interface

VPC Endpoint
```

Example:

```text
Destination        Target

0.0.0.0/0          igw-123456
```

means:

```text
Traffic matching 0.0.0.0/0
        ↓
Internet Gateway
```

---

## 4. Local Route

Every VPC route table contains a local route that enables communication within the VPC.

Example:

```text
VPC CIDR:
10.0.0.0/16
```

Route table:

```text
Destination        Target

10.0.0.0/16        local
```

This allows routing between resources in the VPC.

Example:

```text
Subnet A
10.0.1.0/24

        ↓

local route

        ↓

Subnet B
10.0.2.0/24
```

However, routing does not automatically mean traffic is permitted.

Security Groups and Network ACLs may still restrict the communication.

---

## 5. Example — Communication Inside a VPC

Suppose:

```text
VPC
10.0.0.0/16

Subnet A
10.0.1.0/24

EC2-A
10.0.1.10

Subnet B
10.0.2.0/24

EC2-B
10.0.2.20
```

When EC2-A sends traffic to:

```text
10.0.2.20
```

the route table can match:

```text
10.0.0.0/16
→ local
```

Traffic flow:

```text
EC2-A
   ↓
Route Table
   ↓
10.0.0.0/16 → local
   ↓
EC2-B
```

---

## 6. Main Route Table

When a VPC is created, AWS automatically creates a main route table.

Conceptually:

```text
VPC
│
└── Main Route Table
```

The main route table controls routing for subnets that are not explicitly associated with another route table.

Example:

```text
VPC
│
├── Subnet A
│     └── No explicit association
│
├── Subnet B
│     └── No explicit association
│
└── Main Route Table
```

Both Subnet A and Subnet B use the main route table.

---

## 7. Custom Route Tables

Custom route tables can be created to control routing more precisely.

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
    Database Route Table
```

This makes network intent easier to understand and manage.

---

## 8. Explicit Route Table Association

A subnet can be explicitly associated with a specific route table.

Example:

```text
Public Subnet
      ↓
Public Route Table
```

and:

```text
Private Subnet
      ↓
Private Route Table
```

A subnet can only be associated with one subnet route table at a time.

However, one route table can be associated with multiple subnets.

Example:

```text
Public Route Table
     │
     ├── Public Subnet A
     └── Public Subnet B
```

---

## 9. Public Route Table

A typical public subnet route table may contain:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          igw-123456
```

The important route is:

```text
0.0.0.0/0
→ Internet Gateway
```

This allows IPv4 traffic that does not match a more specific route to be sent toward the Internet Gateway.

---

## 10. Private Route Table

A private application subnet may use:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          nat-123456
```

Internet-bound traffic is sent to:

```text
NAT Gateway
```

rather than directly to the Internet Gateway.

---

## 11. Isolated Route Table

A sensitive database subnet may contain only:

```text
Destination        Target

10.0.0.0/16        local
```

There is no:

```text
0.0.0.0/0
```

Internet default route.

This makes the subnet isolated from direct IPv4 Internet routing.

---

## 12. Default Route

The IPv4 default route is:

```text
0.0.0.0/0
```

It matches all IPv4 destinations.

Conceptually:

```text
If no more specific route exists
        ↓
Use 0.0.0.0/0
```

Example:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          Internet Gateway
```

Traffic for:

```text
10.0.2.10
```

uses:

```text
10.0.0.0/16 → local
```

Traffic for:

```text
8.8.8.8
```

uses:

```text
0.0.0.0/0 → Internet Gateway
```

---

## 13. Longest Prefix Match

AWS chooses the most specific route that matches the destination IP address.

This is called:

```text
Longest Prefix Match
```

Example route table:

```text
Destination        Target

10.0.0.0/16        local
10.0.1.0/24        Target-A
0.0.0.0/0          Target-B
```

Traffic destination:

```text
10.0.1.50
```

matches all three possible ranges conceptually:

```text
10.0.1.0/24
10.0.0.0/16
0.0.0.0/0
```

The most specific match is:

```text
10.0.1.0/24
```

Therefore:

```text
10.0.1.50
→ Target-A
```

---

## 14. Why Prefix Length Matters

A larger CIDR prefix represents a more specific network.

Example:

```text
0.0.0.0/0
→ Very broad

10.0.0.0/8
→ More specific

10.0.0.0/16
→ More specific

10.0.1.0/24
→ Even more specific
```

For a matching destination:

```text
/24
```

takes priority over:

```text
/16
```

and `/16` takes priority over `/0`.

---

## 15. Longest Prefix Match Example

Route table:

```text
Destination        Target

10.0.0.0/16        local
10.0.2.0/24        pcx-123456
0.0.0.0/0          nat-123456
```

Traffic:

```text
Destination:
10.0.2.50
```

Matching routes:

```text
10.0.0.0/16

10.0.2.0/24

0.0.0.0/0
```

Selected route:

```text
10.0.2.0/24
→ VPC Peering Connection
```

because `/24` is the most specific match.

---

## 16. Route Selection Mental Model

When troubleshooting routing, think:

```text
Destination IP
      ↓
Which routes match?
      ↓
Which matching route is most specific?
      ↓
Use that Target
```

Do not simply look for:

```text
0.0.0.0/0
```

because a more specific route may override it.

---

## 17. What is an Internet Gateway?

An Internet Gateway (IGW) is an AWS-managed VPC component that provides connectivity between a VPC and the Internet.

Conceptually:

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
VPC
```

The Internet Gateway is attached to a VPC.

Example:

```text
AWS Region
│
└── VPC
    │
    └── Internet Gateway
```

---

## 18. Internet Gateway Does Not Automatically Provide Internet Access

Simply attaching an Internet Gateway does not automatically make all VPC resources Internet-accessible.

Several components must work together.

For IPv4:

```text
EC2
│
├── Public IPv4 / Elastic IP
│
├── Correct Security Group
│
├── Correct Network ACL
│
└── Route Table
       │
       └── 0.0.0.0/0
            ↓
       Internet Gateway
```

Therefore:

```text
Attach IGW
≠
Automatic Internet Access
```

---

## 19. Public Subnet and Internet Gateway

A subnet becomes public when its route table has a route to an Internet Gateway.

Typical route:

```text
0.0.0.0/0
→ igw-xxxxxxxx
```

Example:

```text
Internet
    │
    ↓
Internet Gateway
    │
    ↓
Public Route Table
    │
0.0.0.0/0
    │
    ↓
Public Subnet
    │
    ↓
EC2
```

---

## 20. IPv4 Internet Access

For IPv4 Internet access, an EC2 instance typically needs a public IPv4 address or Elastic IP.

Example:

```text
EC2

Private IPv4:
10.0.1.10

Public IPv4:
203.0.113.x
```

Traffic flow:

```text
EC2 Private IP
      ↓
Internet Gateway
      ↓
Public IPv4 Mapping
      ↓
Internet
```

The EC2 operating system normally sees its private IP address.

AWS handles the public-to-private IPv4 address mapping through the Internet Gateway.

---

## 21. IPv6 Internet Routing

IPv6 uses a different default route.

IPv4:

```text
0.0.0.0/0
```

IPv6:

```text
::/0
```

Example public route table:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          igw-123456

2001:db8::/56      local
::/0               igw-123456
```

IPv4 and IPv6 routes are evaluated separately.

---

## 22. IPv4 vs IPv6

One important difference is that IPv6 does not use public/private address translation in the same way as public IPv4 addressing.

Conceptually:

```text
IPv4

Private IP
   ↓
Internet Gateway NAT
   ↓
Public IPv4
```

Compared with:

```text
IPv6

Globally Unique IPv6 Address
   ↓
Internet Gateway
   ↓
Internet
```

Security Groups, Network ACLs, and routing are therefore especially important when using IPv6.

---

## 23. Egress-Only Internet Gateway

For IPv6, AWS provides an Egress-Only Internet Gateway for workloads that should initiate outbound Internet connections without accepting new inbound connections from the Internet.

Conceptually:

```text
Private IPv6 Workload
       ↓
Egress-Only Internet Gateway
       ↓
Internet
```

This is conceptually similar to the outbound-only goal often achieved with NAT for IPv4, although the underlying mechanism is different.

---

## 24. Example IPv6 Private Routing

Example:

```text
Destination        Target

2001:db8:1234::/56 local
::/0               eigw-123456
```

Traffic flow:

```text
Private IPv6 Instance
        ↓
Route Table
        ↓
::/0
        ↓
Egress-Only Internet Gateway
        ↓
Internet
```

---

## 25. Route Table Example — Public Subnet

```text
VPC
10.0.0.0/16

Public Subnet
10.0.1.0/24
```

Route table:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          igw-123456
```

Traffic:

```text
10.0.2.10
→ local

8.8.8.8
→ Internet Gateway
```

---

## 26. Route Table Example — Private Subnet

```text
Private Subnet
10.0.11.0/24
```

Route table:

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          nat-123456
```

Traffic:

```text
10.0.2.10
→ local

8.8.8.8
→ NAT Gateway
```

---

## 27. Route Table Example — Isolated Database

```text
Database Subnet
10.0.21.0/24
```

Route table:

```text
Destination        Target

10.0.0.0/16        local
```

Traffic:

```text
10.0.11.10
→ local

8.8.8.8
→ No matching Internet route
```

The database has no default Internet route.

---

## 28. Multiple Route Targets

A route table can contain routes to multiple network destinations.

Example:

```text
Destination        Target

10.0.0.0/16        local

10.20.0.0/16       pcx-123456

172.16.0.0/12      tgw-123456

0.0.0.0/0          nat-123456
```

This might represent:

```text
10.0.0.0/16
→ Current VPC

10.20.0.0/16
→ Peer VPC

172.16.0.0/12
→ Corporate Network

Everything Else
→ NAT Gateway
```

---

## 29. Route Priority Example

Suppose:

```text
Destination        Target

0.0.0.0/0          NAT Gateway

10.20.0.0/16       VPC Peering

10.20.10.0/24      Transit Gateway
```

Traffic to:

```text
10.20.10.50
```

matches:

```text
0.0.0.0/0

10.20.0.0/16

10.20.10.0/24
```

Selected:

```text
10.20.10.0/24
→ Transit Gateway
```

because it is the longest prefix match.

---

## 30. Routing and Security

Routing determines:

```text
Where traffic can go
```

Security Groups and Network ACLs determine:

```text
Whether traffic is permitted
```

Conceptually:

```text
Route Table
→ Is there a network path?

Security Group / NACL
→ Is traffic allowed?
```

Both must be considered when troubleshooting connectivity.

---

## 31. Common Routing Problem — Missing Default Route

Suppose:

```text
EC2 has Public IP

Security Group allows HTTPS

Internet Gateway is attached
```

but the subnet route table contains only:

```text
10.0.0.0/16
→ local
```

There is no:

```text
0.0.0.0/0
→ Internet Gateway
```

Result:

```text
No Internet Route
```

Even though other components are configured.

---

## 32. Common Routing Problem — Wrong Route Table Association

Example:

```text
Public Subnet
```

was accidentally associated with:

```text
Private Route Table
```

Instead of:

```text
Public Route Table
```

Result:

```text
Expected:
0.0.0.0/0 → Internet Gateway

Actual:
0.0.0.0/0 → NAT Gateway
```

The subnet does not behave as intended.

This is why route table associations are important.

---

## 33. Common Routing Problem — Wrong Target

Example:

```text
Private Subnet

Expected:
0.0.0.0/0 → NAT Gateway
```

but configured as:

```text
0.0.0.0/0 → Internet Gateway
```

This changes the intended network architecture.

A security review should verify both:

```text
Destination

and

Target
```

---

## 34. Common Routing Problem — Overlapping Networks

Suppose:

```text
VPC-A
10.0.0.0/16

VPC-B
10.0.0.0/16
```

If these VPCs need to communicate, overlapping CIDR ranges create routing ambiguity and connectivity problems.

A better design could be:

```text
VPC-A
10.10.0.0/16

VPC-B
10.20.0.0/16
```

Network address planning is therefore an important part of cloud architecture.

---

## 35. Common Routing Problem — Blackhole Route

A route can become invalid when its target is no longer available.

Conceptually:

```text
Route

10.20.0.0/16
→ Deleted / unavailable target
```

The route may no longer be able to forward traffic correctly.

When troubleshooting, verify that the target resource still exists and is available.

---

## 36. Route Troubleshooting Method

When communication fails, check routing systematically.

### Step 1 — Identify Source

```text
Where is traffic coming from?
```

### Step 2 — Identify Destination

```text
What IP address is traffic going to?
```

### Step 3 — Find Subnet

```text
Which subnet contains the source?
```

### Step 4 — Identify Route Table

```text
Which route table is associated with the subnet?
```

### Step 5 — Find Matching Routes

```text
Which routes match the destination IP?
```

### Step 6 — Apply Longest Prefix Match

```text
Which matching route is most specific?
```

### Step 7 — Check Target

```text
Where does the selected route send traffic?
```

### Step 8 — Check Security Controls

```text
Security Group

Network ACL
```

This creates a systematic troubleshooting workflow.

---

## 37. Example Troubleshooting Scenario

Problem:

```text
EC2 cannot access the Internet.
```

Check:

```text
Does the EC2 have the appropriate IP configuration?

        ↓

Which subnet is the EC2 in?

        ↓

Which route table is associated?

        ↓

Is there a default route?

        ↓

Where does 0.0.0.0/0 point?

        ↓

Is the Internet Gateway attached?

        ↓

Are Security Group rules correct?

        ↓

Are Network ACL rules correct?
```

Do not immediately modify firewall rules before confirming the route.

---

## 38. Security Perspective — Route Review

When reviewing AWS networking, I should ask:

```text
Which route tables exist?

Which subnets use each route table?

Where does 0.0.0.0/0 point?

Where does ::/0 point?

Are there unexpected Internet Gateway routes?

Are private subnets routed through NAT?

Are sensitive subnets isolated?

Are there routes to external networks?

Are routes more permissive than necessary?

Are there overlapping CIDR ranges?

Are there unused or invalid routes?
```

---

## 39. Route Tables as Security-Relevant Configuration

A route table is not a firewall, but its configuration affects the possible attack surface.

Example:

```text
Private Database Subnet

Before:
10.0.0.0/16 → local

After:
0.0.0.0/0 → Internet Gateway
```

The network architecture has changed significantly.

Therefore, route changes should be treated as security-relevant configuration changes.

---

## 40. Internet Gateway Security Perspective

An Internet Gateway provides a path between a VPC and the Internet.

It does not decide application-level authorization.

Security still depends on:

```text
Route Tables

Public IP Configuration

Security Groups

Network ACLs

Application Security

Operating System Security
```

A useful mental model is:

```text
Internet Gateway
→ Connectivity

Route Table
→ Path

Security Group / NACL
→ Traffic Control

IAM
→ AWS API Authorization

Application Security
→ Application Protection
```

---

## 41. Example Secure Three-Tier Routing

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
Public Route Table
   │
   ↓
Load Balancer
   │
   ↓
Private Application Route Table
   │
   ↓
Application Server
   │
   ↓
Database Route Table
   │
   ↓
Database
```

Example route tables:

### Public

```text
10.0.0.0/16 → local
0.0.0.0/0   → Internet Gateway
```

### Application

```text
10.0.0.0/16 → local
0.0.0.0/0   → NAT Gateway
```

### Database

```text
10.0.0.0/16 → local
```

This separates Internet-facing, application, and data workloads.

---

## 42. Hands-on Practice

For today's practice, I explored route tables in the Amazon VPC console.

I reviewed:

- Main route table
- Custom route tables
- Route table associations
- Local routes
- Default routes
- Internet Gateway targets
- NAT Gateway targets

For each route table, I identified:

```text
Destination

Target

Associated Subnets

Expected Network Role
```

Example:

```text
Route Table:
Public-RT

Routes:
10.0.0.0/16 → local
0.0.0.0/0   → igw-xxxxxxxx

Associated Subnets:
Public-A
Public-B

Role:
Public Internet Routing
```

---

## 43. Longest Prefix Match Practice

Consider:

```text
10.0.0.0/16  → local

10.0.10.0/24 → Target-A

0.0.0.0/0    → Target-B
```

### Destination 1

```text
10.0.10.50
```

Result:

```text
10.0.10.0/24
→ Target-A
```

### Destination 2

```text
10.0.20.50
```

Result:

```text
10.0.0.0/16
→ local
```

### Destination 3

```text
8.8.8.8
```

Result:

```text
0.0.0.0/0
→ Target-B
```

---

## 44. Security Checklist

When reviewing AWS route tables, I should ask:

```text
Does every subnet use the intended route table?

Is 0.0.0.0/0 required?

Where does the IPv4 default route point?

Is ::/0 configured intentionally?

Are private resources accidentally using an Internet Gateway route?

Are sensitive subnets isolated?

Are NAT routes configured correctly?

Are there more-specific routes that override expected routes?

Are external network routes expected?

Are CIDR ranges overlapping?

Are there invalid or blackhole routes?

Are routing changes being monitored?
```

---

## Key Takeaways

- Route tables determine where VPC network traffic is directed.
- Each route contains a destination and a target.
- Every VPC route table contains a local route for VPC communication.
- The main route table controls subnets without explicit route table associations.
- Custom route tables provide more granular routing control.
- `0.0.0.0/0` represents the IPv4 default route.
- `::/0` represents the IPv6 default route.
- AWS uses the longest prefix match to select the most specific applicable route.
- A route to an Internet Gateway makes a subnet public.
- An Internet Gateway must be attached to the VPC and referenced by routing.
- IPv4 Internet access also requires appropriate public IPv4 addressing.
- IPv4 and IPv6 routing should be evaluated separately.
- Routing provides connectivity, while Security Groups and Network ACLs control traffic.
- Route tables should be reviewed as security-relevant configuration.

---

## Reflection

Today I learned that AWS route tables control network paths by matching destination IP addresses to routing targets.

The most important concept is longest prefix match. When multiple routes match the same destination, AWS selects the most specific matching route rather than simply using the default route.

I also learned that the Internet Gateway itself does not automatically provide Internet access. Routing, IP addressing, Security Groups, and Network ACLs must all be configured correctly.

From a security perspective, route tables are important because an incorrect route can unintentionally change the connectivity and exposure of a subnet.

When troubleshooting AWS network connectivity, I should first identify the source, destination, associated route table, matching route, and selected target before modifying security controls.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Blackhole Route | A route whose target is unavailable or invalid |
| Custom Route Table | A route table created for more specific routing control |
| Default Route | A route that matches destinations not covered by more specific routes |
| Destination | The IP range that a route matches |
| Egress-Only Internet Gateway | A gateway that supports outbound-initiated IPv6 Internet communication |
| Internet Gateway | A VPC component that provides connectivity between a VPC and the Internet |
| Local Route | A route that enables communication within a VPC |
| Longest Prefix Match | Selecting the most specific route that matches a destination |
| Main Route Table | The default route table created with a VPC |
| Route Association | The relationship between a subnet and its route table |
| Route Table | A set of rules that determines where network traffic is directed |
| Target | The network component that receives matching traffic |
