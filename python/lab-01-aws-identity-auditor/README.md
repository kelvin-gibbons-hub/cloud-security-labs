
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


## Version 3 — Structured Security Findings

The AWS Identity Auditor now generates machine-readable JSON
reports from live AWS security checks.

### Features

- Retrieves the active AWS identity using STS
- Inspects an IAM role authorized by least-privilege policy
- Verifies that access to an unauthorized role is denied
- Produces structured security finding dictionaries
- Generates audit_results.json
- Validates JSON report contents using Python assertions

### Finding Classifications

- PASS: Expected security behavior observed
- FAIL: Unexpected authorization success
- INCONCLUSIVE: Target resource not found
- ERROR: Unexpected AWS error

### Running

Run the auditor:

    python identity_auditor.py

Validate its output:

    python test_audit_report.py

### Security Notes

Authentication uses temporary AWS credentials through
the auditor-live profile.

The generated JSON report is excluded from version control
because it may contain account identifiers and role ARNs.

No AWS permissions are modified by the auditor.

### Future Improvements

- Unit tests with mocked AWS responses
- Graceful handling of authentication failures
- Reusable audit-check functions
- Timestamped reports
- Additional IAM and cloud security checks


## Version 4 — Automated Security Testing

Refactored authorization classification into a reusable,
AWS-independent Python module.

### Improvements

- Added security_checks.py for authorization classification
- Separated AWS API operations from security decision logic
- Added five automated tests using Python unittest
- Verified PASS, FAIL, INCONCLUSIVE, and ERROR outcomes
- Demonstrated regression detection through deliberate
  defect injection and repair
- Integrated tested classification into the live IAM auditor

### Running Tests

    python -m unittest -v test_security_checks

### Current Limitations

- AWS API failures outside the classification function
  need additional exception handling
- Authorized role inspection requires more negative-path tests
- Live authentication must be refreshed when sessions expire
- Additional mock-based AWS client tests are planned

The project uses read-only AWS operations and temporary
credentials through an MFA-protected restricted role.

## Version 5 — Resilient AWS Error Handling

Added reusable exception classification and an audit execution
wrapper to prevent individual AWS failures from terminating
the entire audit.

### Features

- Classifies missing credentials and credential retrieval failures
- Identifies AWS endpoint connection errors
- Preserves AWS service error codes
- Distinguishes operational ERROR results from security findings
- Records structured errors with check names
- Includes five offline exception-handling tests
- Verifies safe behavior using simulated authentication failures

### Limitations

- The execution wrapper catches exceptions at the audit boundary
- The auditor does not yet implement automatic retries
- Unexpected exceptions are classified but not fully diagnosed
- Additional structured identity and logging improvements are planned


