# Day 11 — Network ACLs

## Topic

Amazon VPC Network ACLs and Subnet-Level Stateless Traffic Control

---

## Objectives

- Understand what a Network ACL is
- Understand subnet-level network filtering
- Understand stateless firewall behavior
- Learn inbound and outbound NACL rules
- Understand Allow and Deny rules
- Understand NACL rule numbers and evaluation order
- Learn how ephemeral ports affect NACL design
- Compare Network ACLs with Security Groups
- Apply Network ACLs as defense-in-depth controls
- Troubleshoot basic NACL connectivity problems

---

## 1. What is a Network ACL?

A Network Access Control List (Network ACL or NACL) is a subnet-level network traffic control mechanism in Amazon VPC.

Conceptually:

```text
Network
   ↓
Network ACL
   ↓
Subnet
   ↓
AWS Resources
```

A Network ACL controls traffic entering and leaving associated subnets.

Unlike Security Groups, which are associated with resources or network interfaces, NACLs apply to an entire subnet.

---

## 2. NACL Scope

A Network ACL operates at the subnet level.

Example:

```text
VPC
│
├── Subnet A
│     │
│     ├── EC2-A
│     └── EC2-B
│
└── Network ACL
      associated with Subnet A
```

The NACL affects traffic entering and leaving the subnet for both EC2-A and EC2-B.

Conceptually:

```text
Subnet
│
├── Resource A
├── Resource B
└── Resource C

        ↑
    Same NACL
```

---

## 3. Subnet Association

Each subnet is associated with one Network ACL at a time.

One Network ACL can be associated with multiple subnets.

Example:

```text
Network ACL
│
├── Public Subnet A
└── Public Subnet B
```

If a subnet is associated with another NACL, the previous association is replaced.

---

## 4. Inbound and Outbound Rules

A NACL contains separate:

```text
Inbound Rules
+
Outbound Rules
```

Inbound rules control traffic entering the subnet.

```text
Network
   ↓
Inbound NACL
   ↓
Subnet
```

Outbound rules control traffic leaving the subnet.

```text
Subnet
   ↓
Outbound NACL
   ↓
Network
```

Both directions must be considered independently.

---

## 5. Network ACLs Are Stateless

One of the most important NACL concepts is:

```text
Network ACLs are stateless.
```

This means the NACL does not remember whether traffic is part of an already established connection.

Example:

```text
Client
   ↓
TCP 443
   ↓
Web Server
```

If inbound HTTPS traffic is allowed, the response traffic is not automatically allowed.

A separate outbound rule must permit the response traffic.

Conceptually:

```text
Inbound Request
→ Must be Allowed

Outbound Response
→ Must Also Be Allowed
```

---

## 6. Stateless Example

Suppose a client connects to a web server:

```text
Client
203.0.113.10
      ↓
TCP 443
      ↓
Web Server
```

Inbound NACL:

```text
Allow TCP 443
Source: 203.0.113.10/32
```

This allows the request.

However, the web server response uses an ephemeral destination port on the client.

Therefore, outbound NACL rules must also allow the appropriate ephemeral port range.

Example:

```text
Allow TCP 1024-65535
Destination: 203.0.113.10/32
```

Without the outbound rule, the response may be blocked.

---

## 7. NACL Allow and Deny Rules

Unlike Security Groups, Network ACLs support both:

```text
ALLOW

DENY
```

Example:

```text
Rule 100
DENY
Source: 203.0.113.50/32

Rule 200
ALLOW
Source: 0.0.0.0/0
```

This allows general traffic while blocking one specific source.

This is one reason NACLs can be useful as subnet-level guardrails.

---

## 8. Rule Numbers

Every NACL rule has a rule number.

Example:

```text
Rule 100
Rule 110
Rule 200
Rule 300
```

AWS evaluates rules starting with the lowest rule number.

Conceptually:

```text
100
 ↓
110
 ↓
200
 ↓
300
```

The first matching rule is applied.

Once a rule matches, higher-numbered rules are not evaluated.

---

## 9. Rule Evaluation Example

Consider:

```text
Rule 100
DENY
Source: 203.0.113.10/32

Rule 200
ALLOW
Source: 0.0.0.0/0
```

Traffic arrives from:

```text
203.0.113.10
```

Evaluation:

```text
Rule 100
→ Match
→ DENY
```

AWS stops evaluating.

Rule 200 is not considered.

Final result:

```text
DENY
```

---

## 10. Rule Order Matters

Suppose the rules are reversed.

```text
Rule 100
ALLOW
Source: 0.0.0.0/0

Rule 200
DENY
Source: 203.0.113.10/32
```

Traffic from:

```text
203.0.113.10
```

matches:

```text
Rule 100
```

first.

Result:

```text
ALLOW
```

Rule 200 is never evaluated.

Therefore:

```text
Rule Order Matters
```

This is very different from Security Groups.

---

## 11. Leave Gaps Between Rule Numbers

Instead of:

```text
100
101
102
103
```

it is better to use:

```text
100
200
300
400
```

or:

```text
100
110
120
130
```

This makes it easier to insert new rules later.

Example:

```text
100 ALLOW HTTPS

200 ALLOW SSH
```

Later:

```text
150 DENY Suspicious IP
```

can be inserted without renumbering everything.

---

## 12. Default Rule

A Network ACL includes a final catch-all rule:

```text
*
```

Conceptually:

```text
If no earlier rule matches
        ↓
Default Rule
        ↓
DENY
```

Therefore, traffic must match an Allow rule before reaching the final deny.

---

## 13. Default Network ACL

A VPC's default Network ACL normally allows inbound and outbound traffic by default.

Conceptually:

```text
Default NACL

Inbound:
ALLOW ALL

Outbound:
ALLOW ALL
```

This means the default NACL itself usually does not heavily restrict network communication.

Security Groups then provide more specific resource-level protection.

---

## 14. Custom Network ACL

A newly created custom Network ACL starts more restrictively.

Conceptually:

```text
Custom NACL

Inbound:
DENY unless allowed

Outbound:
DENY unless allowed
```

Required rules must be added explicitly.

This makes it important to configure both traffic directions correctly.

---

## 15. Security Group vs Network ACL

The main differences are:

| Security Group | Network ACL |
|---|---|
| Resource / ENI level | Subnet level |
| Stateful | Stateless |
| Allow rules only | Allow and Deny rules |
| Evaluates all applicable rules | Evaluates rules in number order |
| Return traffic automatically allowed | Return traffic must be explicitly allowed |
| Can reference other Security Groups | Primarily uses network criteria such as CIDR |
| Primary resource traffic control | Additional subnet-level control |

A simple mental model:

```text
Security Group
→ Protect the Resource

Network ACL
→ Protect the Subnet Boundary
```

---

## 16. Stateful vs Stateless

### Security Group

```text
Client
   ↓
Allowed Request
   ↓
Server

Response
→ Automatically Allowed
```

### Network ACL

```text
Client
   ↓
Inbound Rule Required
   ↓
Server

Server
   ↓
Outbound Rule Required
   ↓
Client
```

This is the key difference.

---

## 17. Traffic Path

A simplified AWS traffic path may look like:

```text
Internet
   ↓
Internet Gateway
   ↓
Route Table
   ↓
Network ACL
   ↓
Subnet
   ↓
Security Group
   ↓
EC2
```

For return traffic:

```text
EC2
   ↓
Security Group
   ↓
Network ACL
   ↓
Route Table
   ↓
Internet Gateway
   ↓
Internet
```

Both Security Groups and NACLs may affect connectivity.

---

## 18. Ephemeral Ports

Because NACLs are stateless, ephemeral ports are important.

An ephemeral port is a temporary client-side port used for network connections.

Example:

```text
Client
Source Port: 55000
Destination Port: 443
```

Request:

```text
55000 → 443
```

Response:

```text
443 → 55000
```

The server-side NACL must allow the outbound response to the client's ephemeral port.

---

## 19. Ephemeral Port Example

Suppose:

```text
Client
203.0.113.10:55000

Web Server
10.0.1.10:443
```

Inbound:

```text
203.0.113.10:55000
        ↓
10.0.1.10:443
```

NACL inbound:

```text
Allow TCP 443
Source: 203.0.113.10/32
```

Return traffic:

```text
10.0.1.10:443
       ↓
203.0.113.10:55000
```

NACL outbound must allow:

```text
TCP 1024-65535
Destination: 203.0.113.10/32
```

depending on the expected client ephemeral port range.

---

## 20. Why Ephemeral Port Ranges Can Be Broad

Different operating systems and AWS services may use different ephemeral port ranges.

Therefore, a common architecture may allow:

```text
TCP 1024-65535
```

for response traffic.

However, the exact design should reflect the systems that communicate with the workload.

NACL rules should not be copied blindly without understanding the traffic flow.

---

## 21. Example — Public Web Subnet

Suppose a public subnet contains a web server.

Required traffic:

```text
Internet
   ↓
HTTPS 443
   ↓
Web Server
```

Possible inbound NACL:

```text
Rule 100

Protocol:
TCP

Port:
443

Source:
0.0.0.0/0

Action:
ALLOW
```

Possible outbound response rule:

```text
Rule 100

Protocol:
TCP

Port:
1024-65535

Destination:
0.0.0.0/0

Action:
ALLOW
```

The exact ephemeral range should reflect expected clients and architecture.

---

## 22. Example — Blocking a Suspicious IP

One useful NACL scenario is blocking traffic from a known unwanted source.

Example:

```text
Rule 100

Source:
203.0.113.50/32

Protocol:
All

Action:
DENY
```

Then:

```text
Rule 200

Source:
0.0.0.0/0

Protocol:
TCP

Port:
443

Action:
ALLOW
```

Traffic from the blocked IP matches Rule 100 first and is denied.

Other HTTPS traffic can match Rule 200.

---

## 23. NACL as a Guardrail

Because a NACL applies to an entire subnet, it can provide a broad network boundary.

Example:

```text
Application Subnet
       ↓
NACL
       ↓
Only required traffic ranges
```

Even if an instance inside the subnet accidentally has an overly permissive Security Group, the NACL can provide an additional layer of control.

Conceptually:

```text
NACL
→ Subnet Guardrail

Security Group
→ Resource Firewall
```

---

## 24. Defense in Depth

Using Security Groups and NACLs together can provide defense in depth.

Example:

```text
Internet
   ↓
NACL
   ↓
Subnet
   ↓
Security Group
   ↓
Application
```

Security Group:

```text
Allow HTTPS to the application
```

NACL:

```text
Allow required subnet traffic
Deny known unwanted traffic
```

One control does not completely replace the other.

---

## 25. NACLs Should Not Replace Security Groups

Security Groups are generally more flexible for workload-level access control.

Security Groups support:

```text
Stateful filtering

Security Group references

Resource-level rules
```

NACLs are more suitable for:

```text
Subnet-level guardrails

Broad network filtering

Explicit deny scenarios

Additional defense-in-depth
```

Therefore, a common model is:

```text
Security Group
→ Primary Network Access Control

Network ACL
→ Secondary Subnet Guardrail
```

---

## 26. Example — Three-Tier Architecture

Consider:

```text
Internet
   ↓
Public Subnet
   ↓
Application Subnet
   ↓
Database Subnet
```

Each subnet can use its own NACL.

Example:

```text
Public-NACL

Application-NACL

Database-NACL
```

This provides subnet-level separation in addition to Security Groups.

---

## 27. Public Subnet NACL

Example purpose:

```text
Allow public HTTPS traffic

Allow required response traffic

Deny known unwanted traffic
```

Conceptually:

```text
Internet
   ↓
Public-NACL
   ↓
ALB
```

---

## 28. Application Subnet NACL

The application subnet may only need traffic from expected network ranges.

Example:

```text
Public / Load Balancer Subnets
         ↓
Application NACL
         ↓
Application Servers
```

The exact rule design depends on the application's network architecture.

---

## 29. Database Subnet NACL

A database subnet may use stricter controls.

Example:

```text
Application Subnet
      ↓
Database Port
      ↓
Database NACL
      ↓
Database
```

The database subnet generally does not need broad Internet access.

This provides another layer of segmentation.

---

## 30. Common Misconfiguration — Return Traffic Blocked

Problem:

```text
Inbound HTTPS works conceptually

but the connection fails
```

Inbound rule:

```text
ALLOW TCP 443
```

But outbound response ports are not allowed.

Because the NACL is stateless:

```text
Request
→ Allowed

Response
→ Blocked
```

Result:

```text
Connection Failure
```

This is one of the most important NACL troubleshooting scenarios.

---

## 31. Common Misconfiguration — Wrong Rule Order

Rules:

```text
100 ALLOW 0.0.0.0/0

200 DENY 203.0.113.50/32
```

Expected:

```text
Block 203.0.113.50
```

Actual:

```text
Rule 100 matches first
→ ALLOW
```

Fix:

```text
100 DENY 203.0.113.50/32

200 ALLOW 0.0.0.0/0
```

Lower-numbered specific deny rules must be evaluated before broader allow rules.

---

## 32. Common Misconfiguration — Overly Broad Allow Rules

Example:

```text
Rule 100

ALLOW ALL
0.0.0.0/0
```

If this appears before more specific deny rules, those deny rules may never be evaluated.

Always review:

```text
Rule Number

Protocol

Port

CIDR

Action
```

together.

---

## 33. Common Misconfiguration — Editing Only Inbound Rules

Because Security Groups are stateful, it is easy to become accustomed to focusing mostly on inbound rules.

With NACLs:

```text
Inbound
AND
Outbound
```

must both be considered.

Whenever adding a NACL rule, ask:

```text
What does the return traffic look like?
```

---

## 34. Common Misconfiguration — Incorrect Ephemeral Ports

A request may reach the server correctly, but the response may be blocked because the ephemeral destination port is not allowed.

Example:

```text
Client Port:
55000

Server Port:
443
```

If outbound NACL rules do not permit:

```text
TCP 55000
```

the response may fail.

---

## 35. Network ACL Troubleshooting

When connectivity fails, identify:

```text
Source IP

Destination IP

Protocol

Destination Port

Source Port

Subnet

NACL
```

Then check:

```text
Inbound Rules

Outbound Rules

Rule Order

Ephemeral Ports
```

---

## 36. Troubleshooting Workflow

Use a systematic approach:

```text
Source
   ↓
Route Table
   ↓
Source NACL
   ↓
Network
   ↓
Destination NACL
   ↓
Security Group
   ↓
Destination Resource
```

Then verify the return path:

```text
Destination
   ↓
Security Group
   ↓
NACL
   ↓
Route
   ↓
Source
```

Network communication requires both forward and return paths.

---

## 37. Example Troubleshooting — HTTPS

Problem:

```text
Internet user cannot connect to HTTPS service.
```

Check:

### Routing

```text
Is there a valid route?
```

### Inbound NACL

```text
TCP 443 allowed?
```

### Security Group

```text
TCP 443 allowed?
```

### Application

```text
Is the service listening on TCP 443?
```

### Outbound NACL

```text
Are ephemeral response ports allowed?
```

All layers must be configured correctly.

---

## 38. Example Troubleshooting — Application to Database

Architecture:

```text
Application
10.0.11.10

        ↓ TCP 5432

Database
10.0.21.10
```

Check:

```text
Application Subnet NACL

Database Subnet NACL

Database Security Group

Routing

Database Listener
```

Because NACLs are stateless, verify both:

```text
Application → Database

and

Database → Application
```

traffic requirements.

---

## 39. Security Group vs NACL Troubleshooting

A useful comparison:

### Security Group

Ask:

```text
Is the requested traffic allowed?
```

Return traffic is handled statefully.

### NACL

Ask:

```text
Is forward traffic allowed?

Is return traffic allowed?

Which numbered rule matches first?
```

This distinction is important during troubleshooting.

---

## 40. Security Perspective

When reviewing a NACL, ask:

```text
Which subnets use this NACL?

What traffic should enter the subnet?

What traffic should leave the subnet?

Are explicit deny rules required?

Are rule numbers ordered correctly?

Are broad allow rules hiding later deny rules?

Are ephemeral ports handled correctly?

Does the subnet require Internet access?

Are sensitive subnets more restricted?

Is the NACL providing useful defense-in-depth?
```

---

## 41. Hands-on Practice

For today's practice, review Network ACLs in the Amazon VPC console.

Identify:

- NACL ID
- Associated VPC
- Associated subnets
- Inbound rules
- Outbound rules
- Rule numbers
- Allow / Deny actions
- CIDR ranges

For each rule, identify:

```text
Rule Number

Protocol

Port Range

Source / Destination

Allow or Deny
```

---

## 42. Optional Practice Scenario

Design a NACL for a public web subnet.

Requirements:

```text
Allow HTTP

Allow HTTPS

Allow response traffic

Deny all other traffic
```

Example concept:

### Inbound

```text
100
ALLOW TCP 80
Source: 0.0.0.0/0

110
ALLOW TCP 443
Source: 0.0.0.0/0

*
DENY ALL
```

### Outbound

```text
100
ALLOW TCP 1024-65535
Destination: 0.0.0.0/0

*
DENY ALL
```

The appropriate rules depend on the actual application and client behavior.

---

## Security Checklist

When reviewing Network ACLs, I should ask:

```text
Is the correct NACL associated with each subnet?

Are inbound rules correct?

Are outbound rules correct?

Are rule numbers ordered intentionally?

Are specific deny rules evaluated before broad allow rules?

Are ephemeral ports handled correctly?

Are broad allow-all rules necessary?

Does each rule have a clear purpose?

Are sensitive subnets more restricted?

Do Security Groups provide the primary workload-level control?

Is the NACL adding useful defense-in-depth rather than unnecessary complexity?
```

---

## Key Takeaways

- Network ACLs operate at the subnet level.
- A subnet can be associated with one NACL at a time.
- A NACL can be associated with multiple subnets.
- Network ACLs are stateless.
- Forward and return traffic must both be explicitly permitted.
- NACLs support both Allow and Deny rules.
- Rules are evaluated from the lowest rule number upward.
- Evaluation stops at the first matching rule.
- Rule ordering is therefore extremely important.
- Ephemeral ports must be considered when configuring return traffic.
- Security Groups are stateful and operate at the resource level.
- Security Groups are generally the primary network access control.
- NACLs are useful as subnet-level guardrails and defense-in-depth controls.

---

## Reflection

Today I learned that Network ACLs provide subnet-level network filtering and behave very differently from Security Groups.

The most important difference is that Network ACLs are stateless. Allowing an inbound request does not automatically allow the response, so both directions of traffic must be considered.

I also learned that NACL rule ordering is critical. AWS evaluates rules starting with the lowest rule number and stops when the first matching rule is found.

Because NACLs support explicit Deny rules, they can be useful for blocking specific traffic at the subnet boundary.

However, Security Groups remain more suitable for detailed workload-level access control, while Network ACLs provide an additional defense-in-depth layer for subnets.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Ephemeral Port | A temporary client-side port used during network communication |
| Explicit Deny | A rule that specifically blocks matching traffic |
| Guardrail | A broad control that limits what traffic or actions are permitted |
| Network ACL | A subnet-level network traffic control mechanism |
| Return Traffic | Traffic sent back in response to an incoming request |
| Rule Number | The number that determines NACL evaluation order |
| Stateless | Treating each packet independently without tracking connection state |
| Subnet-Level Control | A security control applied to an entire subnet |
