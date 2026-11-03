
# AWS Identity Auditor v1

## Overview

A Python security automation prototype developed as part of
my AI Security Architect training.

The project demonstrates AWS identity inspection concepts,
structured API response handling, and defensive exception handling.


## Current Status — Version 2

Live AWS integration completed.

### Implemented Features

- Temporary AWS authentication using a restricted IAM role
- STS GetCallerIdentity inspection
- IAM GetRole inspection for an authorized resource
- Real-world AccessDenied verification
- Distinct handling for unauthorized, missing, and unexpected results
- Read-only AWS API operations

### Security Controls

- No hardcoded AWS access keys
- Explicit selection of the auditor-live AWS profile
- MFA-protected assumption of SecurityLabOperatorRole
- Least-privilege IAM resource restrictions
- No administrative or destructive API operations

### Limitations

- Auditor currently prints results to the console
- Target role names are hardcoded for lab testing
- Unexpected errors are not yet recorded as structured findings
- Automated unit tests are planned

### Planned Improvements

- JSON audit output
- Reusable IAM inspection functions
- Automated tests using mocked AWS responses
- Improved error handling and exit status codes
- Additional read-only security checks


## Technologies

- Python 3
- boto3 / botocore
- AWS IAM and STS concepts

## Running the Prototype

Create a virtual environment:

    python -m venv .venv

Install dependencies:

    .\.venv\Scripts\python.exe -m pip install boto3 awscrt

Run:

    .\.venv\Scripts\python.exe identity_auditor.py

Note:
    Live execution requires a configured auditor-live profile that obtains temporary credentials through lab-operator.

## Security Design

- No hardcoded credentials
- No long-lived access keys
- Simulated AWS responses for offline development
- Defensive handling of authorization failures
- Planned integration with a restricted IAM role

## Next Version

- Authenticate using temporary AWS credentials
- Use SecurityLabOperatorRole
- Retrieve live STS identity information
- Inspect an explicitly authorized IAM role
- Test allowed and denied API operations
- Add structured audit results and automated tests

## Learning Outcomes

- Python functions and dictionaries
- AWS SDK session and client concepts
- Exception handling
- Separation of concerns
- Least-privilege security design
