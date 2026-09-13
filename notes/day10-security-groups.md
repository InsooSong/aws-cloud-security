# Day 10 — Security Groups

## Topic

Amazon VPC Security Groups and Stateful Network Access Control

---

## Objectives

- Understand what a Security Group is
- Understand inbound and outbound rules
- Understand stateful firewall behavior
- Learn how protocols and ports are controlled
- Understand CIDR-based rules
- Learn Security Group referencing
- Apply least-privilege network access
- Understand Security Group chaining
- Identify common Security Group misconfigurations
- Troubleshoot basic Security Group connectivity issues

---

## 1. What is a Security Group?

A Security Group is a virtual firewall used to control network traffic for supported AWS resources.

Security Groups control:

```text
Inbound Traffic
+
Outbound Traffic
```

Conceptually:

```text
Network
   ↓
Security Group
   ↓
AWS Resource
```

For example:

```text
Internet
   ↓
Security Group
   ↓
EC2 Instance
```

Security Groups are commonly associated with resources such as:

- Amazon EC2 instances
- Elastic Load Balancers
- Amazon RDS databases
- Elastic Network Interfaces
- Other supported VPC resources

---

## 2. Security Group Rules

A Security Group contains rules that define which traffic is allowed.

Each rule can specify:

```text
Protocol
Port
Source / Destination
```

Example inbound rule:

```text
Protocol: TCP
Port: 443
Source: 0.0.0.0/0
```

This means:

```text
Allow HTTPS traffic
from any IPv4 address
```

---

## 3. Inbound Rules

Inbound rules control traffic entering a resource.

Example:

```text
Internet
   ↓
Inbound Rule
   ↓
EC2
```

Example web server rule:

```text
Type: HTTPS
Protocol: TCP
Port: 443
Source: 0.0.0.0/0
```

This allows HTTPS traffic from the Internet.

Another example:

```text
Type: SSH
Protocol: TCP
Port: 22
Source: 203.0.113.10/32
```

This allows SSH access only from one specific IPv4 address.

---

## 4. Outbound Rules

Outbound rules control traffic leaving a resource.

Example:

```text
EC2
   ↓
Outbound Rule
   ↓
Destination
```

A default Security Group configuration commonly allows all outbound IPv4 traffic:

```text
Protocol: All
Destination: 0.0.0.0/0
```

However, outbound permissions can also be restricted.

Example:

```text
Protocol: TCP
Port: 443
Destination: 0.0.0.0/0
```

This allows HTTPS traffic to external IPv4 destinations.

---

## 5. Security Groups Are Stateful

One of the most important Security Group concepts is:

```text
Security Groups are stateful.
```

This means that return traffic for an allowed connection is automatically permitted.

Example:

```text
Client
   ↓
TCP 443
   ↓
EC2
```

Inbound rule:

```text
Allow TCP 443
from Client
```

When EC2 sends the response:

```text
EC2
   ↓
Response
   ↓
Client
```

a separate outbound rule specifically allowing the response path is not required for that established connection.

---

## 6. Stateful Example

Suppose an EC2 web server has:

```text
Inbound:

TCP 443
Source: 0.0.0.0/0
```

A user connects:

```text
Client
   ↓
HTTPS Request
   ↓
EC2
```

The response is automatically allowed as part of the established connection.

Conceptually:

```text
Inbound Request
→ Allowed by Security Group

Return Traffic
→ Automatically Allowed
```

This is the meaning of stateful behavior.

---

## 7. Security Groups Use Allow Rules

Security Groups use allow rules.

They do not contain explicit deny rules.

Conceptually:

```text
Matching Allow Rule
→ Traffic Allowed

No Matching Allow Rule
→ Traffic Not Allowed
```

Unlike Network ACLs:

```text
Security Group
→ Allow rules only

Network ACL
→ Allow and Deny rules
```

Network ACLs will be studied separately.

---

## 8. Default Deny Behavior

If no Security Group rule allows specific traffic, that traffic is not permitted.

Example:

Security Group inbound rules:

```text
TCP 443
Source: 0.0.0.0/0
```

Incoming request:

```text
TCP 22
```

There is no matching SSH rule.

Result:

```text
Traffic Not Allowed
```

This supports a least-privilege network model.

---

## 9. Protocols and Ports

Security Group rules can control traffic based on protocols and ports.

Common examples:

```text
HTTP
TCP 80

HTTPS
TCP 443

SSH
TCP 22

RDP
TCP 3389

MySQL
TCP 3306

PostgreSQL
TCP 5432

DNS
TCP / UDP 53
```

Only required ports should be opened.

---

## 10. Avoid Opening Unnecessary Ports

A risky configuration might be:

```text
Inbound:

All Traffic
All Ports
Source: 0.0.0.0/0
```

This greatly increases the attack surface.

A better approach is:

```text
HTTPS
TCP 443
Source: Required Clients
```

or:

```text
SSH
TCP 22
Source: Administrator IP Only
```

Security Groups should follow the Principle of Least Privilege.

---

## 11. CIDR-Based Rules

Security Group sources and destinations can use CIDR ranges.

Examples:

```text
0.0.0.0/0
```

means:

```text
Any IPv4 address
```

Example:

```text
10.0.0.0/16
```

means:

```text
Any IPv4 address inside 10.0.0.0/16
```

Example:

```text
203.0.113.10/32
```

means:

```text
One specific IPv4 address
```

A smaller allowed range usually provides better security.

---

## 12. IPv6 Rules

IPv6 uses separate CIDR rules.

For example:

```text
::/0
```

means:

```text
Any IPv6 address
```

A Security Group configured with:

```text
0.0.0.0/0
```

does not automatically allow:

```text
::/0
```

IPv4 and IPv6 rules must be considered separately.

---

## 13. Anywhere Rules

Two common broad rules are:

```text
0.0.0.0/0
```

and:

```text
::/0
```

These mean:

```text
Anywhere IPv4

Anywhere IPv6
```

They should only be used when the service intentionally needs public access.

Example:

```text
Public HTTPS Service
TCP 443
Source: 0.0.0.0/0
```

may be appropriate.

However:

```text
SSH
TCP 22
Source: 0.0.0.0/0
```

is usually much more dangerous.

---

## 14. Security Group References

Instead of using IP addresses, a Security Group can reference another Security Group.

Example:

```text
Application-SG

Inbound:
TCP 8080
Source: LoadBalancer-SG
```

Conceptually:

```text
Load Balancer
LoadBalancer-SG
      ↓
TCP 8080
      ↓
Application
Application-SG
```

This allows traffic from resources associated with the referenced Security Group.

---

## 15. Why Security Group References Are Useful

Without Security Group references:

```text
Application SG
Allow TCP 8080
Source: 10.0.1.0/24
```

This allows all matching addresses in that subnet range.

With Security Group referencing:

```text
Application SG
Allow TCP 8080
Source: LoadBalancer-SG
```

The rule is based on workload identity at the Security Group level rather than a broad subnet CIDR.

This can make access control more precise and easier to maintain.

---

## 16. Three-Tier Security Group Design

Consider:

```text
Internet
   ↓
Load Balancer
   ↓
Application Server
   ↓
Database
```

We can create:

```text
ALB-SG

APP-SG

DB-SG
```

---

## 17. Load Balancer Security Group

Example:

```text
ALB-SG

Inbound:

TCP 443
Source: 0.0.0.0/0
```

This allows public HTTPS traffic.

Conceptually:

```text
Internet
   ↓
TCP 443
   ↓
ALB-SG
   ↓
Load Balancer
```

---

## 18. Application Security Group

The application should not accept traffic directly from the entire Internet.

Instead:

```text
APP-SG

Inbound:

TCP 8080
Source: ALB-SG
```

Conceptually:

```text
Internet
   ↓
ALB-SG
   ↓
Load Balancer
   ↓
APP-SG
   ↓
Application Server
```

Only traffic from resources associated with `ALB-SG` is permitted on the application port.

---

## 19. Database Security Group

The database should normally accept traffic only from the application layer.

Example:

```text
DB-SG

Inbound:

TCP 5432
Source: APP-SG
```

for PostgreSQL.

Architecture:

```text
Internet
   ↓
ALB-SG
   ↓
Load Balancer
   ↓
APP-SG
   ↓
Application
   ↓
DB-SG
   ↓
PostgreSQL
```

This creates controlled communication between layers.

---

## 20. Security Group Chaining

This design is sometimes described conceptually as Security Group chaining.

```text
Internet
   ↓
ALB-SG
   ↓
APP-SG
   ↓
DB-SG
```

Each tier allows traffic only from the previous trusted tier.

Example:

```text
ALB-SG
→ HTTPS from Internet

APP-SG
→ Application traffic from ALB-SG

DB-SG
→ Database traffic from APP-SG
```

This is much better than exposing every layer to broad CIDR ranges.

---

## 21. Security Group Reference Does Not Copy Rules

Referencing another Security Group does not copy the rules from that Security Group.

Example:

```text
APP-SG

Source:
ALB-SG
```

does not mean:

```text
Copy every ALB-SG rule into APP-SG
```

Instead, it identifies resources associated with the referenced Security Group as an allowed source for the specified protocol and port.

---

## 22. Security Group and Subnet Relationship

Security Groups are not attached to entire subnets.

They are associated with supported resources or their network interfaces.

Conceptually:

```text
Subnet
│
├── EC2-A
│     └── SG-A
│
├── EC2-B
│     └── SG-B
│
└── EC2-C
      └── SG-C
```

Different resources in the same subnet can therefore use different Security Groups.

---

## 23. Multiple Security Groups

A resource can be associated with multiple Security Groups.

Example:

```text
EC2
│
├── Web-SG
└── Management-SG
```

The effective allowed traffic is based on the combined rules of the associated Security Groups.

Conceptually:

```text
Security Group A
      +
Security Group B
      ↓
Combined Allowed Rules
```

There is no priority ordering between Security Groups.

---

## 24. Example — Web and Management Access

Suppose an EC2 instance has:

```text
Web-SG

Inbound:
TCP 443
Source: 0.0.0.0/0
```

and:

```text
Management-SG

Inbound:
TCP 22
Source: 203.0.113.10/32
```

The instance effectively allows:

```text
HTTPS
from Internet

SSH
from Administrator IP
```

---

## 25. Security Groups and Routing

Security Groups cannot create network connectivity.

There must first be a valid network path.

Conceptually:

```text
Route Table
→ Can traffic reach the resource?

Security Group
→ Is the traffic allowed?
```

Example:

```text
Security Group:
Allow TCP 443
```

but:

```text
No valid route
```

Result:

```text
Connection fails
```

Both routing and Security Group configuration must be correct.

---

## 26. Security Groups and Network ACLs

Traffic may also be affected by Network ACLs.

Conceptually:

```text
Network
   ↓
Route
   ↓
Network ACL
   ↓
Security Group
   ↓
Resource
```

A connection may fail even if the Security Group allows it.

Therefore, troubleshooting should consider:

```text
Routing

Network ACL

Security Group

Operating System Firewall

Application
```

---

## 27. Common Misconfiguration — SSH Open to the Internet

Risky:

```text
SSH
TCP 22
Source: 0.0.0.0/0
```

This allows connection attempts from any IPv4 address.

Better:

```text
SSH
TCP 22
Source: Trusted Administrator IP
```

Even better, when appropriate, administrative access can use AWS Systems Manager instead of exposing SSH directly.

---

## 28. Common Misconfiguration — RDP Open to the Internet

Risky:

```text
RDP
TCP 3389
Source: 0.0.0.0/0
```

This exposes the Windows remote management service to the Internet.

A more restricted configuration might use:

```text
Trusted Corporate Network

VPN

Controlled Administrative Network

Systems Manager
```

depending on the architecture.

---

## 29. Common Misconfiguration — Database Open to Everyone

Risky:

```text
PostgreSQL
TCP 5432
Source: 0.0.0.0/0
```

or:

```text
MySQL
TCP 3306
Source: 0.0.0.0/0
```

Better:

```text
Database SG

Inbound:
TCP 5432
Source: APP-SG
```

The database should usually communicate only with required application resources.

---

## 30. Common Misconfiguration — All Traffic

Example:

```text
All Protocols
All Ports
Source: 0.0.0.0/0
```

This is extremely broad.

Instead, determine:

```text
Required Protocol

Required Port

Required Source
```

and allow only that traffic.

---

## 31. Common Misconfiguration — Unrestricted Outbound Access

Many environments focus only on inbound traffic.

However, outbound rules are also important.

Example:

```text
Outbound:
All Traffic
Destination: 0.0.0.0/0
```

may be broader than necessary for highly sensitive workloads.

Restricting egress can help limit:

- Malware communication
- Command-and-control traffic
- Data exfiltration
- Unnecessary external communication

The appropriate level of restriction depends on the workload.

---

## 32. Least-Privilege Network Access

Least privilege also applies to network traffic.

Instead of:

```text
Allow Everything
```

identify:

```text
Who needs access?

Which protocol?

Which port?

From where?

To what?
```

Then create the smallest required rule.

Example:

```text
Source:
APP-SG

Protocol:
TCP

Port:
5432

Destination:
Database
```

---

## 33. Security Group Design Example

Three-tier application:

```text
    Internet
       │
       │ HTTPS 443
       ↓
┌──────────────┐
│    ALB-SG    │
└──────┬───────┘
       │
       │ TCP 8080
       ↓
┌──────────────┐
│    APP-SG    │
└──────┬───────┘
       │
       │ TCP 5432
       ↓
┌──────────────┐
│     DB-SG    │
└──────────────┘
```

Rules:

### ALB-SG

```text
Inbound:
TCP 443
Source: 0.0.0.0/0
```

### APP-SG

```text
Inbound:
TCP 8080
Source: ALB-SG
```

### DB-SG

```text
Inbound:
TCP 5432
Source: APP-SG
```

This provides controlled access between application tiers.

---

## 34. Security Group Troubleshooting

If a connection fails, identify:

```text
Source

Destination

Protocol

Port
```

Then check the relevant Security Group.

Example problem:

```text
Application cannot connect to PostgreSQL.
```

Expected traffic:

```text
Source:
APP-SG

Destination:
Database

Protocol:
TCP

Port:
5432
```

Check:

```text
Does DB-SG allow TCP 5432 from APP-SG?
```

---

## 35. Troubleshooting Workflow

Use a systematic approach:

```text
Can Source Reach Destination?
        ↓
Check Route Table
        ↓
Check Network ACL
        ↓
Check Security Group
        ↓
Check OS Firewall
        ↓
Check Application
```

For the Security Group specifically:

```text
Correct protocol?

Correct port?

Correct source?

Correct destination?

Correct Security Group attached?

IPv4 or IPv6?
```

---

## 36. Example Troubleshooting — Web Server

Problem:

```text
HTTPS connection fails.
```

Check:

### Route

```text
Does the subnet have the required network route?
```

### Public Address

```text
Does the Internet-facing resource have appropriate addressing?
```

### Security Group

```text
TCP 443
Source: Client Network
```

### Network ACL

```text
Does it permit the required traffic?
```

### Application

```text
Is the web server listening on TCP 443?
```

Security Group configuration is only one part of connectivity.

---

## 37. Example Troubleshooting — Database

Problem:

```text
Application server cannot connect to RDS PostgreSQL.
```

Check:

```text
Application
APP-SG

        ↓ TCP 5432

RDS
DB-SG
```

DB-SG should contain:

```text
Protocol:
TCP

Port:
5432

Source:
APP-SG
```

If the source is incorrect, the connection will fail.

---

## 38. Security Group Rule Descriptions

Rules can include descriptions.

Example:

```text
TCP 443
Source: 0.0.0.0/0
Description:
Public HTTPS access
```

Descriptions help administrators understand why rules exist.

Instead of:

```text
TCP 5432
10.0.0.0/8
```

without explanation, use:

```text
TCP 5432
APP-SG
Description:
Allow application tier to PostgreSQL
```

Good documentation reduces configuration mistakes.

---

## 39. Security Group Review Questions

When reviewing a Security Group, ask:

```text
What resource uses this Security Group?

Why does each rule exist?

Is 0.0.0.0/0 necessary?

Is ::/0 necessary?

Can CIDR access be replaced with Security Group references?

Are administrative ports publicly exposed?

Are database ports publicly exposed?

Are unused rules present?

Are outbound permissions broader than necessary?

Can any rules be removed?
```

---

## 40. Hands-on Practice

For today's practice, review Security Groups in the AWS Management Console.

Locate:

- Security Group name
- Security Group ID
- Associated VPC
- Inbound rules
- Outbound rules
- Associated resources

Review several rules and identify:

```text
Protocol

Port

Source / Destination

Purpose
```

---

## 41. Optional Practice

Create a conceptual three-tier Security Group design.

### ALB-SG

```text
Inbound:

HTTPS
TCP 443
Source: 0.0.0.0/0
```

### APP-SG

```text
Inbound:

Custom TCP
TCP 8080
Source: ALB-SG
```

### DB-SG

```text
Inbound:

PostgreSQL
TCP 5432
Source: APP-SG
```

Then trace the allowed traffic:

```text
Internet
   ↓ 443
ALB
   ↓ 8080
Application
   ↓ 5432
Database
```

---

## Security Checklist

When reviewing Security Groups, I should ask:

```text
Are only required ports open?

Are administrative ports restricted?

Is 0.0.0.0/0 actually required?

Is ::/0 actually required?

Can Security Group references be used?

Are database ports restricted to application workloads?

Are unnecessary rules present?

Are outbound rules broader than required?

Are Security Groups clearly named and documented?

Are multiple application tiers separated?

Is the correct Security Group attached to each resource?

Are IPv4 and IPv6 rules both reviewed?
```

---

## Key Takeaways

- Security Groups act as virtual firewalls for supported AWS resources.
- Security Groups control inbound and outbound traffic.
- Security Groups are stateful.
- Return traffic for established allowed connections is automatically permitted.
- Security Groups contain allow rules rather than explicit deny rules.
- Traffic without a matching allow rule is not permitted.
- Rules can specify protocols, ports, CIDR ranges, prefix lists, or Security Group references.
- Security Group references can provide more precise workload-to-workload access control.
- Public administrative and database ports should be avoided when possible.
- Multiple Security Groups can contribute allowed rules to the same resource.
- Security Groups do not replace routing or application security.
- Network access should follow the Principle of Least Privilege.

---

## Reflection

Today I learned that Security Groups are one of the primary network security controls in Amazon VPC.

The most important concept is that Security Groups are stateful. When a connection is allowed, response traffic for that connection is automatically permitted.

I also learned that Security Group references can provide better access control than broad CIDR-based rules.

For example, an application Security Group can allow traffic only from a load balancer Security Group, while a database Security Group can allow traffic only from the application Security Group.

This creates a security model based on application tiers instead of broad network ranges.

From a security perspective, I should continuously review Security Groups for unnecessary ports, unrestricted Internet access, broad outbound permissions, and unused rules.

---

## Vocabulary

| Word | Meaning |
|---|---|
| CIDR | A notation used to represent an IP address range |
| Egress | Outbound network traffic |
| Inbound | Network traffic entering a resource |
| Ingress | Inbound network traffic |
| Outbound | Network traffic leaving a resource |
| Port | A logical endpoint used by network services |
| Protocol | A communication standard such as TCP, UDP, or ICMP |
| Security Group | A stateful virtual firewall for supported AWS resources |
| Security Group Reference | Using another Security Group as the source or destination of a rule |
| Stateful | Automatically allowing return traffic for an established connection |
