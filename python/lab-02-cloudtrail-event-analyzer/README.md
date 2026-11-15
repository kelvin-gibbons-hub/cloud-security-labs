# Lab 02 — AWS CloudTrail Event Analyzer

## Objective

Develop a Python security automation tool that analyzes synthetic AWS CloudTrail-style events, identifies selected security-relevant API operations, and produces chronological security findings.

## Features

- Load AWS CloudTrail-style JSON records.
- Detect `AttachRolePolicy`, `PutRolePolicy`, and `StopLogging` events.
- Preserve relevant event evidence.
- Extract timestamps, API actions, principal ARNs, and resource targets.
- Classify outcomes as `SUCCESS`, `DENIED`, or `ERROR`.
- Sort findings chronologically without modifying the original findings list.
- Handle missing or null identity and request-parameter objects.

## Technologies

Python 3, JSON, dictionaries, sets, functions, list comprehensions, and lambda-based sorting.

## Project Files

- `cloudtrail_analyzer.py` — Event parsing, detection, and reporting.
- `sample_events.json` — Synthetic CloudTrail-style input data.
- `README.md` — Lab documentation.

## Run

Place the Python script and sample JSON file in the same directory.

```bash
python cloudtrail_analyzer.py
```

## Testing

The following adversarial scenarios were tested successfully:

| Test | Scenario | Result |
|---|---|---|
| A | Null user identity | PASS |
| B | Null request parameters | PASS |
| C | API throttling error | PASS |

The analyzer also identified three security-relevant events from a four-record sample.

## Security Considerations

Flagged operations require investigation; they do not automatically indicate malicious behavior.

Limitations:

- Synthetic events only; no live AWS integration.
- Limited predefined API detection rules.
- Simplified outcome classification.
- Assumes consistent UTC timestamp formatting.
- Does not comprehensively validate malformed records.
- Missing error codes are treated as success for this lab.

## Lessons Learned

This lab reinforced JSON parsing, evidence preservation, IAM activity detection, nested dictionary handling, chronological analysis, and troubleshooting malformed input.

It also demonstrated the importance of testing security automation against incomplete and unexpected telemetry.

## Status

Introductory analyzer implemented and tested with the specified synthetic scenarios. Further hardening and independent validation are required before production use.
