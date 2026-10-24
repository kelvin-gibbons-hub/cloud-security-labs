# AWS Identity and Access Management (IAM) Security Labs

## Overview

This collection documents hands-on AWS IAM security labs focused on execution roles, authorization boundaries, and least-privilege enforcement.

The labs demonstrate progressively more advanced security concepts through controlled AWS Lambda and Amazon S3 experiments. This is an evolving collection of 

hands-on AWS IAM security labs. New exercises will be added as training progresses.

The labs listed below represent completed and documented exercises to date.

## Lab Directory

### Lab 01 — Lambda Execution Role Identity

[View Lab 01](lab-01-lambda-role-identity/README.md)

**Objective:** Verify the AWS identity assumed by a Lambda function.

**Implementation:**
- Configured an IAM execution role for AWS Lambda.
- Used AWS STS GetCallerIdentity to verify the active identity.
- Troubleshot Lambda handler configuration.
- Confirmed the function operated under its assigned execution role.

**Result:** PASS — Lambda execution identity successfully verified.

### Lab 02 — S3 Access Denied and Least Privilege

[View Lab 02](lab-02-s3-access-denied/README.md)

**Objective:** Verify that an AWS Lambda execution role cannot perform unauthorized Amazon S3 operations.

**Implementation:**
- Configured Lambda to request an S3 bucket listing.
- Tested an execution role without the required S3 permission.
- Examined the authorization response.
- Validated IAM default-deny behavior.

**Result:** PASS — Unauthorized S3 access was denied.

### Lab 03 — IAM Permission Enforcement

[View Lab 03](lab-03-lambda-least-privilege/README.md)

**Objective:** Demonstrate how IAM permission changes affect AWS authorization decisions.

**Implementation:**
- Tested S3 access without the required permission.
- Attached a policy granting s3:ListAllMyBuckets.
- Verified that the operation became authorized.
- Removed the additional permission.
- Confirmed that access was denied again.

**Result:** PASS — DENIED → ALLOWED → DENIED.

## Skills Demonstrated

- AWS Identity and Access Management
- IAM roles and trust policies
- IAM identity-based permission policies
- AWS Lambda execution roles
- AWS Security Token Service
- Amazon S3 authorization
- Least-privilege security design
- Access-control validation
- Cloud security troubleshooting

## Security Engineering Takeaways

These labs demonstrate the distinction between authentication, role assumption, and authorization.

They establish how AWS IAM permission policies control an application's capabilities and how security engineers can validate least-privilege configurations through controlled testing.

## Professional Development

These exercises are part of my ongoing development toward cloud security engineering and AI security architecture.

Future work will expand into cloud networking, infrastructure security, automation, secure AI applications, and enterprise security architecture.
