# Day 9 — NAT Gateway

## Topic

Amazon VPC NAT Gateway and Private Subnet Internet Access

---

## Objectives

- Understand Network Address Translation (NAT)
- Understand why private subnets use NAT Gateway
- Learn how public NAT Gateway works
- Understand NAT Gateway routing
- Compare NAT Gateway and Internet Gateway
- Understand NAT Gateway high availability
- Learn basic NAT Gateway security considerations
- Understand when VPC endpoints can reduce NAT usage

---

## 1. What is NAT?

NAT stands for:

```text
Network Address Translation
```

NAT allows a resource using a private IP address to communicate with networks outside its private network.

In AWS, NAT Gateway is commonly used when resources in private subnets need outbound Internet access.

Example:

```text
Private EC2
10.0.11.10
     ↓
NAT Gateway
     ↓
Internet Gateway
     ↓
Internet
```

The EC2 instance can initiate communication with the Internet without requiring direct inbound Internet connectivity.

---

## 2. Why Use NAT Gateway?

A private EC2 instance may need to access the Internet for tasks such as:

- Downloading software packages
- Installing operating system updates
- Accessing external APIs
- Downloading application dependencies

However, we may not want the instance to be directly reachable from the Internet.

NAT Gateway provides a solution:

```text
Outbound Connection
Private EC2 → Internet
✓ Allowed

Unsolicited Inbound Connection
Internet → Private EC2
✕ Not directly allowed through NAT
```

---

## 3. Basic NAT Gateway Architecture

A public NAT Gateway is placed in a public subnet.

```text
Internet
   │
   ↓
Internet Gateway
   │
   ↓
Public Subnet
   │
   └── NAT Gateway
          ↑
          │
Private Subnet
   │
   └── EC2
```

Typical architecture:

```text
VPC 10.0.0.0/16
│
├── Public Subnet
│   10.0.1.0/24
│
│   └── NAT Gateway
│
└── Private Subnet
    10.0.11.0/24

    └── EC2
```

---

## 4. Required Routes

### Private Subnet Route Table

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          NAT Gateway
```

Internet-bound IPv4 traffic is sent to the NAT Gateway.

### Public Subnet Route Table

```text
Destination        Target

10.0.0.0/16        local
0.0.0.0/0          Internet Gateway
```

The NAT Gateway can then communicate with the Internet through the Internet Gateway.

---

## 5. Traffic Flow

Suppose:

```text
Private EC2:
10.0.11.10
```

The instance sends traffic to:

```text
8.8.8.8
```

Traffic flow:

```text
Private EC2
10.0.11.10
     ↓
Private Route Table
0.0.0.0/0 → NAT Gateway
     ↓
NAT Gateway
     ↓
Public Route Table
0.0.0.0/0 → Internet Gateway
     ↓
Internet
```

The response follows the established connection back through the NAT Gateway.

---

## 6. NAT Gateway vs Internet Gateway

NAT Gateway and Internet Gateway have different purposes.

| Internet Gateway | NAT Gateway |
|---|---|
| Connects a VPC with the Internet | Provides address translation for outbound connectivity |
| Used by public subnets | Commonly used by private subnets |
| Target of public subnet default route | Target of private subnet default route |
| Supports Internet-facing resources | Helps keep workloads from direct inbound Internet access |

Typical design:

```text
Public Subnet
0.0.0.0/0
    ↓
Internet Gateway
```

Compared with:

```text
Private Subnet
0.0.0.0/0
    ↓
NAT Gateway
    ↓
Internet Gateway
```

---

## 7. Public NAT Gateway

A public NAT Gateway is created in a public subnet.

It uses an Elastic IP address for Internet communication.

Conceptually:

```text
Private EC2
   ↓
Private IP
   ↓
NAT Gateway
   ↓
Elastic IP
   ↓
Internet
```

The private EC2 instance itself does not need a public IPv4 address.

---

## 8. NAT Gateway and Security Groups

A NAT Gateway does not use Security Groups.

Security Groups should instead be applied to resources such as:

```text
EC2
RDS
Load Balancer
```

Example:

```text
EC2 Security Group
        ↓
Private EC2
        ↓
NAT Gateway
```

Network ACLs can still affect traffic at the subnet level.

---

## 9. NAT Gateway High Availability

A NAT Gateway is created within a specific Availability Zone.

For workloads distributed across multiple Availability Zones, a common resilient design is to deploy a NAT Gateway in each Availability Zone.

Example:

```text
Availability Zone A

Private Subnet A
      ↓
NAT Gateway A
      ↓
Internet


Availability Zone B

Private Subnet B
      ↓
NAT Gateway B
      ↓
Internet
```

Each private subnet uses the NAT Gateway in the same Availability Zone.

This reduces cross-AZ dependency.

---

## 10. Single NAT Gateway Design

A smaller environment may use one NAT Gateway.

Example:

```text
Private Subnet A ─┐
                  │
                  ├── NAT Gateway A
                  │
Private Subnet B ─┘
```

This design may reduce cost, but it creates a dependency on the Availability Zone containing the NAT Gateway.

For production environments, availability requirements should be considered.

---

## 11. Multi-AZ NAT Design

A more resilient design is:

```text
AZ-A
│
├── Public Subnet A
│   └── NAT Gateway A
│
└── Private Subnet A
    └── 0.0.0.0/0 → NAT Gateway A


AZ-B
│
├── Public Subnet B
│   └── NAT Gateway B
│
└── Private Subnet B
    └── 0.0.0.0/0 → NAT Gateway B
```

This provides better Availability Zone independence.

---

## 12. NAT Gateway Security Perspective

NAT Gateway reduces the need to assign public IPv4 addresses to private workloads.

Instead of:

```text
Private Application
+
Public IP
+
Direct Internet Route
```

we can use:

```text
Private Application
+
Private IP
+
NAT Gateway
```

This reduces direct exposure.

However:

```text
NAT Gateway
≠
Complete Security
```

Security still depends on:

- Security Groups
- Network ACLs
- IAM
- Operating system security
- Application security
- Logging
- Monitoring

---

## 13. NAT Is Mainly an Egress Design

A useful mental model is:

```text
NAT Gateway
→ Outbound connectivity for private workloads
```

Example:

```text
Private EC2
→ External API
```

The external service can respond to the established connection.

But NAT Gateway is not designed to expose the private instance as an Internet-facing server.

For Internet-facing applications, architectures commonly use components such as:

```text
Application Load Balancer
```

in front of private workloads.

---

## 14. NAT Gateway Cost Considerations

NAT Gateway can create additional AWS costs.

Cost considerations commonly include:

- NAT Gateway running charges
- Data processing charges
- Data transfer patterns
- Cross-AZ traffic

Therefore, architecture should consider whether all traffic actually needs to pass through NAT Gateway.

---

## 15. VPC Endpoints

Traffic to some AWS services can avoid NAT Gateway by using VPC endpoints.

Example:

```text
Private EC2
    ↓
NAT Gateway
    ↓
Internet Gateway
    ↓
Amazon S3
```

may be replaced with:

```text
Private EC2
    ↓
VPC Endpoint
    ↓
Amazon S3
```

This can provide private connectivity to supported AWS services.

Potential benefits include:

- Reduced Internet dependency
- Reduced NAT Gateway traffic
- Reduced attack surface
- Potential cost optimization

---

## 16. Example — S3 Access

Suppose an EC2 instance in a private subnet only needs to access Amazon S3.

Option 1:

```text
EC2
 ↓
NAT Gateway
 ↓
Internet path
 ↓
S3
```

Option 2:

```text
EC2
 ↓
S3 Gateway Endpoint
 ↓
S3
```

The second design can avoid routing S3 traffic through the NAT Gateway.

---

## 17. NAT Gateway Troubleshooting

If a private EC2 instance cannot access the Internet, check the network path systematically.

```text
Private EC2
    ↓
Private Route Table
    ↓
NAT Gateway
    ↓
Public Subnet
    ↓
Internet Gateway
    ↓
Internet
```

Check:

1. Is the NAT Gateway available?
2. Is the NAT Gateway in the correct subnet?
3. Does the private route table contain `0.0.0.0/0 → NAT Gateway`?
4. Does the NAT Gateway subnet have `0.0.0.0/0 → Internet Gateway`?
5. Is the Internet Gateway attached to the VPC?
6. Do Security Groups allow required outbound traffic?
7. Do Network ACLs allow the traffic?
8. Is DNS working if the application uses domain names?

---

## 18. Example Architecture

```text
                       Internet
                           │
                           ↓
                   Internet Gateway
                           │
                ┌──────────┴──────────┐
                │                     │
             AZ-A                  AZ-B
                │                     │
        Public Subnet A       Public Subnet B
                │                     │
          NAT Gateway A         NAT Gateway B
                ↑                     ↑
                │                     │
        Private Subnet A      Private Subnet B
                │                     │
              EC2                   EC2
```

Private subnet routes:

```text
Private Subnet A
0.0.0.0/0 → NAT Gateway A

Private Subnet B
0.0.0.0/0 → NAT Gateway B
```

---

## Hands-on Practice

For today's practice, review NAT Gateway configuration in the Amazon VPC console.

Check:

- NAT Gateway location
- Connectivity type
- Associated subnet
- Elastic IP
- NAT Gateway status
- Private route tables
- Public route tables

Trace the expected path:

```text
Private Instance
      ↓
Private Route Table
      ↓
NAT Gateway
      ↓
Internet Gateway
      ↓
Internet
```

---

## Security Checklist

When reviewing NAT architecture, ask:

```text
Does this workload actually need Internet access?

Can the resource remain in a private subnet?

Does the private route table point to the correct NAT Gateway?

Is the NAT Gateway placed correctly?

Are workloads using NAT Gateways in the appropriate Availability Zone?

Can VPC endpoints replace some NAT traffic?

Are Security Group outbound rules broader than necessary?

Are Network ACLs configured correctly?

Is unnecessary outbound Internet access being allowed?
```

---

## Key Takeaways

- NAT Gateway allows private workloads to initiate connections outside the VPC.
- Private instances do not need public IPv4 addresses when using NAT Gateway.
- A public NAT Gateway is commonly placed in a public subnet.
- Private subnet routes commonly use `0.0.0.0/0 → NAT Gateway`.
- The NAT Gateway requires a path to an Internet Gateway for Internet access.
- NAT Gateway does not provide unsolicited inbound Internet access to private instances.
- NAT Gateway does not use Security Groups.
- Multi-AZ architectures should consider NAT availability for each Availability Zone.
- VPC endpoints can reduce the need to route AWS service traffic through NAT Gateway.
- NAT architecture should consider both security and cost.

---

## Reflection

Today I learned how NAT Gateway allows resources in private subnets to access external networks without assigning public IPv4 addresses directly to those resources.

The key routing relationship is:

```text
Private Subnet
→ NAT Gateway
→ Internet Gateway
→ Internet
```

I also learned that NAT Gateway primarily solves outbound connectivity and does not replace Security Groups, Network ACLs, IAM, or workload security.

For production environments, NAT Gateway architecture should consider Availability Zones, routing, cost, and whether VPC endpoints can provide more private connectivity to AWS services.

---

## Vocabulary

| Word | Meaning |
|---|---|
| Address Translation | Replacing one network address with another |
| Cross-AZ Traffic | Traffic that moves between Availability Zones |
| Dependency | A component required for another component to operate |
| Egress | Traffic leaving a network or workload |
| Elastic IP | A static public IPv4 address in AWS |
| NAT | Network Address Translation |
| NAT Gateway | An AWS-managed NAT service |
| Outbound Connectivity | Network communication initiated from a resource |
| Resilience | The ability to continue operating despite failures |
| VPC Endpoint | Private connectivity between a VPC and supported services |
