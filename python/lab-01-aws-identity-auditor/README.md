
# AWS Identity Auditor v1

## Overview

A Python security automation prototype developed as part of
my AI Security Architect training.

The project demonstrates AWS identity inspection concepts,
structured API response handling, and defensive exception handling.

## Current Status

Version 1 is an offline prototype.

- Uses a simulated AWS STS identity response
- Extracts Account, UserId, and Arn from a Python dictionary
- Simulates an AWS AccessDenied response using ClientError
- Handles the expected exception without crashing
- Uses reusable functions and a main entry point

No live AWS API calls are performed in this version.

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
