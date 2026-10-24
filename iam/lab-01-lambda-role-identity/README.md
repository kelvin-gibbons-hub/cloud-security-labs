# AWS IAM Lab 01 — Lambda Execution Role Identity

## Objective
Demonstrate how AWS Lambda assumes an IAM execution role and verify the AWS identity under which a function runs.

## AWS Services Used
- AWS Identity and Access Management (IAM)
- AWS Lambda
- AWS Security Token Service (STS)
- Amazon CloudWatch Logs

## Lab Environment
- Lambda function: `lab-iam-observer`
- IAM execution role: `lab-lambda-readonly`
- Runtime: Python
- Identity verification: AWS STS GetCallerIdentity

## Lab Procedure
1. Configured an IAM execution role for AWS Lambda.
2. Associated the role with the Lambda function `lab-iam-observer`.
3. Configured the Python Lambda handler.
4. Investigated and corrected a handler/module naming issue.
5. Deployed the corrected Lambda function.
6. Invoked the function to retrieve its AWS caller identity.
7. Examined the returned assumed-role ARN.

## Expected Behavior
When Lambda runs, AWS assumes the configured execution role and supplies temporary role credentials to the function.

Calling STS GetCallerIdentity should identify the assumed role used during execution.

## Observed Results
**PASS — Execution role identity verified.**

The Lambda function executed successfully after the handler issue was corrected.

AWS STS returned an assumed-role ARN associated with `lab-lambda-readonly`.

This confirmed that the function ran under the intended IAM execution role.

## Security Concepts Demonstrated

### IAM Role Assumption
Lambda uses an execution role rather than long-term IAM user credentials.

### Trust Policies
The role trust policy determines which AWS service principal may assume the role.

### Temporary Credentials
AWS supplies temporary credentials to the function when it assumes the configured role.

### Identity Versus Authorization
Successfully assuming a role confirms the function's execution identity. It does not mean that role is authorized to access every AWS resource.

## Troubleshooting
An initial Lambda handler/module configuration issue prevented successful execution.

After correcting the handler/file configuration and redeploying, the identity check succeeded.

## Security Takeaways
- AWS Lambda operates using the permissions of its configured execution role.
- IAM trust policies and permission policies serve different purposes.
- STS GetCallerIdentity helps establish which identity an application is using.
- Role assumption does not automatically grant access to unrelated AWS services.
- Effective troubleshooting requires separating application configuration errors from IAM authorization failures.

## Lab Status
**Completed — PASS**

## Next Lab
Lab 02 — Test an unauthorized Amazon S3 request using the Lambda execution role to verify least-privilege enforcement.

## Portfolio Relevance
This lab demonstrates foundational AWS IAM knowledge, serverless identity verification, role assumption, and practical Lambda troubleshooting.

These skills are relevant to Cloud Security Engineer, IAM Engineer, AWS Security Engineer, and AI Security Architect roles.
