# Lab 03 — AI Security Repeat Offender Report

## Objective

Build a Python detection engineering tool that analyzes AI Security Gateway audit logs and identifies request fingerprints associated with repeated BLOCK decisions across multiple distinct users.

## Detection Rules

A fingerprint becomes an investigation candidate when both thresholds are met:

- At least 3 distinct user IDs
- At least 5 BLOCK events

A matching fingerprint does not establish malicious intent, shared identity, or coordinated attacker activity.

## Technologies

Python 3, JSON Lines (JSONL), dictionaries, sets, datetime, exception handling, and conditional detection logic.

## Features

- Read and process JSONL audit records
- Aggregate events by request fingerprint
- Count unique users and BLOCK decisions
- Track earliest and latest valid timestamps
- Validate missing or incomplete event fields
- Track data-quality problems
- Continue processing when individual records contain malformed JSON
- Generate threshold-based detection candidates

## Running the Project

Place the analyzer alongside a compatible `audit.log` file.

```bash
python3 repeat_offender_report.py
```

Do not upload sensitive production logs, credentials, or private prompt contents to GitHub.

## Initial Lab Results

The recovered synthetic/development gateway dataset contained:

| Metric | Result |
|---|---:|
| Processed records | 97 |
| Missing fingerprints | 3 |
| Fingerprint groups | 10 |
| Invalid decisions | 12 |
| Invalid timestamps | 0 |
| Initial detection candidates | 1 |

The initial candidate used fingerprint value `na`. Its meaning must be verified before treating it as a valid correlation indicator.

These figures represent the initial execution, prior to final malformed-input regression verification.

## Limitations

- Historical events are analyzed without a rolling time window.
- Duplicate records are not deduplicated.
- Missing user IDs reduce attribution confidence.
- Invalid decisions remain visible but do not count as BLOCK.
- Missing fingerprints are excluded from correlation.
- Placeholder fingerprints require special handling.
- The current implementation is a training prototype, not a production detection service.

## Security Engineering Lessons

Reliable detection requires more than matching thresholds. Input validation, event attribution, timestamp handling, data quality, and explicit uncertainty directly influence the reliability of security findings.
