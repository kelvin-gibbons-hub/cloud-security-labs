# AWS IAM Lab 03 — Least Privilege Validation

## Objective
Demonstrate how an IAM execution role's permissions determine whether an AWS Lambda function can access Amazon S3.

## Environment
- AWS Lambda function: `lab-iam-observer`
- IAM execution role: `lab-lambda-readonly`
- Runtime: Python with boto3
- Temporary managed policy: `LabAllowS3BucketListing`

## Test 1 — Baseline
**Configuration:** `AWSLambdaBasicExecutionRole` without S3 listing permission.

**Observed outcome:** `DENIED: AccessDenied`

**Explanation:** The Lambda function could assume its execution role, but the role lacked the required S3 authorization.

## Test 2 — Permission Granted
**Change:** Attached a policy allowing `s3:ListAllMyBuckets`.

**Observed outcome:** `ALLOWED`

**Explanation:** The IAM permissions change authorized the bucket-listing operation without modifying the Lambda trust policy.

## Security Findings
- Role assumption and service API authorization are separate decisions.
- IAM permissions should be limited to necessary actions.
- Granting `s3:ListAllMyBuckets` does not grant `s3:GetObject`.
- IAM policy evaluation can also be affected by explicit denies, permission boundaries, and organization-level restrictions.

## Remediation
After testing, detach the temporary S3 listing policy and verify the request is denied again.

## Conclusion
This controlled lab demonstrated least-privilege authorization and the effect of narrowly scoped IAM policy changes.
