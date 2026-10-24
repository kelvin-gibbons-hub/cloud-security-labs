# AWS IAM Lab 02 — S3 Access Denied and Least Privilege

## Objective

Demonstrate AWS IAM least-privilege enforcement by attempting an unauthorized Amazon S3 operation from an AWS Lambda function.

Verify that successful IAM role assumption does not automatically grant access to other AWS services.

## AWS Services Used

- AWS Identity and Access Management (IAM)
- AWS Lambda
- Amazon S3
- Amazon CloudWatch Logs

## Lab Environment

- Lambda runtime: Python
- IAM managed policy: `AWSLambdaBasicExecutionRole`
- Tested S3 API operation: `ListBuckets`
- Required IAM permission: `s3:ListAllMyBuckets`
- Lambda test payload: `{}`

## Initial IAM Permissions

The Lambda execution role was configured with the AWS-managed policy `AWSLambdaBasicExecutionRole`.

This policy provides permissions for AWS Lambda to write logs to Amazon CloudWatch.

It does not provide permission to list Amazon S3 buckets.

Therefore, attempting to list S3 buckets should result in an authorization failure.

## Lab Procedure

1. Opened the AWS Lambda function used in Lab 01.
2. Verified the IAM execution role assigned to the function.
3. Examined the execution role's attached IAM policies.
4. Confirmed the role had basic CloudWatch Logs permissions.
5. Configured the Python Lambda function to call the Amazon S3 `ListBuckets` API.
6. Deployed the updated Lambda function code.
7. Invoked the Lambda function using an empty JSON test event.
8. Examined the response returned by AWS.
9. Compared the requested S3 action against the IAM role's permissions.

## Expected Behavior

The Lambda function should successfully assume its assigned IAM execution role.

However, the attempt to list Amazon S3 buckets should fail because the execution role lacks the required permission:

`s3:ListAllMyBuckets`

The expected outcome was an AccessDenied error.

## Observed Test Results

**RESULT: PASS**

The Lambda function returned:

```text
DENIED: AccessDenied
```

The Lambda function executed, but AWS denied the request to list Amazon S3 buckets.

This demonstrated that the execution role did not have the necessary S3 permission.

The observed denial matched the expected security behavior.

## Security Analysis

### 1. IAM Role Assumption

The Lambda function operated under its assigned IAM execution role.

Successful role assumption establishes the function's AWS identity but does not automatically authorize access to every AWS resource.

### 2. IAM Authorization

AWS evaluates IAM permissions when a principal requests an AWS operation.

In this lab, the Lambda function attempted to call the Amazon S3 `ListBuckets` API.

The required IAM action was:

`s3:ListAllMyBuckets`

The execution role did not have an applicable permission allowing this action.

AWS therefore denied the request.

### 3. Principle of Least Privilege

The principle of least privilege requires that an application receive only the permissions necessary to perform its intended functions.

The Lambda execution role had permissions for basic logging operations.

It did not have general Amazon S3 access.

This reduced the function's available capabilities and limited its potential impact if compromised.

### 4. Default Deny

AWS IAM follows a default-deny authorization model.

When an applicable Allow is absent, access is denied.

An explicit Deny also overrides an applicable Allow.

In this test, the missing S3 permission resulted in an AccessDenied response.

## Security Concepts Demonstrated

- AWS IAM execution roles
- IAM identity-based policies
- IAM authorization evaluation
- AWS Lambda permissions
- Amazon S3 API authorization
- Principle of least privilege
- Default-deny security model
- Cloud security validation

## Key Lessons Learned

1. Successfully assuming an IAM role does not mean the role can perform every AWS operation.

2. IAM permission policies determine which actions a role is authorized to perform.

3. The AWS-managed `AWSLambdaBasicExecutionRole` policy does not provide general Amazon S3 permissions.

4. An AccessDenied response can demonstrate that a security restriction is functioning correctly.

5. Testing both allowed and denied operations is important when validating least-privilege configurations.

6. Cloud security engineers must distinguish between successful application execution and successful authorization of individual API requests.

## Lab Status

**COMPLETED — PASS**

The expected AccessDenied response was successfully observed.

The result confirmed that the Lambda execution role lacked authorization to list Amazon S3 buckets.

## Next Lab

### Lab 03 — Lambda IAM Least-Privilege Enforcement

Modify the IAM execution role's permissions and observe how changes affect authorization.

Planned validation sequence:

1. Attempt to list S3 buckets without the required permission.
2. Confirm the request is DENIED.
3. Attach a policy granting `s3:ListAllMyBuckets`.
4. Retest the Lambda function.
5. Confirm the request is ALLOWED.
6. Remove the S3 permission.
7. Retest the Lambda function.
8. Confirm the request is DENIED again.

This demonstrates how IAM policy changes directly affect authorization decisions.

## Portfolio Relevance

This lab demonstrates practical experience with AWS IAM authorization, serverless security, and least-privilege enforcement.

The skills demonstrated are relevant to:

- Cloud Security Engineer
- AWS Security Engineer
- IAM Engineer
- DevSecOps Engineer
- AI Security Architect

Understanding IAM authorization boundaries is essential when designing secure cloud applications, automated workflows, and AI agents that interact with AWS services.
