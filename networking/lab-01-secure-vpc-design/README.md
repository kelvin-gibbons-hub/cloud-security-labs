# AWS Networking Lab 01 — Secure VPC Architecture

## Objective
Design a segmented AWS VPC for a three-tier healthcare application, protecting application servers and databases from unnecessary public internet exposure.

**Lab type:** Architecture design and traffic-flow simulation. No AWS infrastructure deployed.

## VPC and Subnet Design

**VPC CIDR:** `10.0.0.0/16`

| Subnet | CIDR | Purpose |
|---|---|---|
| Public | `10.0.1.0/24` | Internet-facing application load balancer |
| Private application | `10.0.2.0/24` | Application servers |
| Isolated database | `10.0.3.0/24` | PostgreSQL database |

Each `/24` subnet contains 256 IPv4 addresses, with 251 available for AWS resources.

## Routing

**Public subnet**
- `10.0.0.0/16` → local
- `0.0.0.0/0` → Internet Gateway

**Private application subnet**
- `10.0.0.0/16` → local
- Optional `0.0.0.0/0` → NAT Gateway for outbound IPv4 connectivity

**Isolated database subnet**
- `10.0.0.0/16` → local
- No default internet route

## Security Group Rules

**Load balancer**
- Allow inbound TCP 443 from internet clients.
- Allow outbound application traffic on TCP 8080.

**Application servers**
- Allow inbound TCP 8080 from the load balancer security group.
- Allow outbound TCP 5432 to the database security group.

**Database**
- Allow inbound TCP 5432 from the application security group.
- Do not allow general internet access.

These rules illustrate intended application communication paths; other required operational traffic must be assessed separately.

## Security Principles

1. Public, private, and isolated network segmentation.
2. CIDR allocation without subnet overlap.
3. Route tables determine network paths.
4. Security groups control resource-level network access.
5. Stateful security groups versus stateless network ACLs.
6. Least-privilege application-to-database communication.

## Assessment Results

- CIDR and VPC architecture: **4/4**
- Network traffic-flow assessment: **5/5**

Both assessments were conceptual exercises.

## Production Improvements

A production implementation would need multiple Availability Zones, appropriate redundancy, encryption, secrets management, logging, monitoring, recovery planning, and infrastructure-as-code validation.

## Conclusion

This design exercise demonstrated foundational AWS VPC architecture and network access-control reasoning. Infrastructure deployment and live connectivity testing remain future milestones.
