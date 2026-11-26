# IAM Policy Evaluator — Day 26

## Project Overview

This project implements a simplified AWS IAM policy evaluator using Python. It demonstrates how authorization decisions are made by examining policy statements, matching requested actions and resources, and applying explicit-deny precedence.

The evaluator was developed as part of my Cloud Security and AI Security Engineering training to strengthen my understanding of AWS IAM, Python control flow, least-privilege principles, and security testing.

**Important:** This is an offline educational tool, not a complete implementation of AWS IAM authorization logic. It must not be used to make production access-control decisions.

## Purpose

The project has five primary objectives:

1. Understand how IAM policy statements contribute to authorization decisions.
2. Implement action and resource matching using Python.
3. Enforce explicit-deny precedence regardless of statement order.
4. Distinguish explicit Allow from implicit Deny.
5. Verify authorization behavior through positive, negative, and conflicting-policy test cases.

## Supported Features

The evaluator processes a simplified policy dictionary containing a `Statement` list.

Each statement includes:

- `Effect`: Either `Allow` or `Deny`.
- `Action`: A list of exact action names.
- `Resource`: A list of exact resource ARNs or the wildcard `"*"`.

### Authorization Rules

The evaluator applies the following logic:

**1. Explicit Deny**

If any matching statement has `Effect: Deny`, the evaluator immediately returns `DENY`.

**2. Explicit Allow**

If a statement matches and has `Effect: Allow`, the evaluator records that an Allow exists. It continues examining the remaining statements to ensure that no explicit Deny applies.

**3. Implicit Deny**

If no matching Allow or Deny statement is found, the evaluator returns `IMPLICIT_DENY`.

A statement matches only when both its action and resource match the request.

## How It Works

The `evaluate_policy(policy, action, resource)` function:

1. Retrieves the policy's statements.
2. Initializes `allow_found` to `False`.
3. Iterates through each statement.
4. Checks whether the requested action appears in the statement's Action list.
5. Checks whether the requested resource matches an exact resource entry or the statement's Resource list contains `"*"`.
6. Immediately returns `DENY` when an explicit-deny statement matches.
7. Records matching Allow statements without returning prematurely.
8. Returns `ALLOW` after examining all statements if an applicable Allow was found and no explicit Deny matched.
9. Otherwise returns `IMPLICIT_DENY`.

This approach ensures that the order of policy statements does not incorrectly alter the authorization outcome.

## Running the Evaluator

### Requirements

- Python 3
- No third-party Python packages
- No AWS credentials or active AWS account required

### Project Files

```text
lab-04-iam-policy-evaluator/
├── policy_evaluator.py
├── test_policy_evaluator.py
└── README.md
```

### Execute the Tests

From the project directory:

```bash
python test_policy_evaluator.py
```

The test file should verify expected results using Python assertions. Failed assertions raise an `AssertionError`.

## Testing and Verification

The evaluator was tested against synthetic policies covering matching Allows, explicit Denies, implicit Denies, and conflicting policy statements.

### Phase 3 — Authorization Testing

| Test Scenario | Expected Result | Reported Result |
|---|---|---|
| Explicit Deny matches requested action and resource | DENY | PASS |
| Explicit Allow matches with no applicable Deny | ALLOW | PASS |
| No applicable Allow or Deny | IMPLICIT_DENY | PASS |
| Policy statements evaluated in reverse order | DENY | PASS |

### Phase 4 — Adversarial Testing

| Test | Scenario | Expected Decision | Reported Result |
|---|---|---|---|
| A | Read explicitly protected S3 object | DENY | PASS |
| B | Read S3 object covered by broad Allow | DENY | PASS |
| C | List S3 bucket covered by broad Allow | DENY | PASS |
| D | Update code of approved Lambda function | ALLOW | PASS |
| E | Attempt Lambda configuration update without matching permission | IMPLICIT_DENY | PASS |
| G | Conflicting broad Allow and explicit Deny | DENY | PASS |

An additional exploratory test used `"*"` as the requested resource. The evaluator returned `ALLOW` because the applicable policy statement allowed `s3:GetObject` on `"*"`.

This result was consistent with the simplified matching rules, but demonstrated that the evaluator does not validate whether a requested resource is a meaningful AWS resource identifier.

**Verification scope:** These are the results observed during development. They do not establish production suitability or exhaustive correctness. The standalone assertion test suite should be executed before final repository submission.

## Bugs Identified and Corrected

### 1. Incorrect Boolean Logic

The original matching condition combined `and` and `or` incorrectly and checked whether the requested resource equaled `"*"`.

This could produce incorrect matches because Python evaluates `and` before `or`.

**Correction:** Separate action matching and resource matching into Boolean variables, then combine them using `and`.

### 2. Multiple Results per Statement

The original implementation used a nested loop over actions, potentially printing multiple Boolean results for one policy statement.

**Correction:** Use membership testing to evaluate the requested action once per statement.

### 3. Printing Instead of Returning

The original Deny implementation printed `"DENY"` without returning it, allowing the function to finish and implicitly return `None`.

**Correction:** Use `return "DENY"` to terminate evaluation and provide the result to the caller.

### 4. Assignment Versus Comparison

An earlier condition attempted to use `=` inside an `if` statement.

**Correction:** Use the Boolean variable directly when deciding whether to return `ALLOW`.

## Limitations

This evaluator intentionally implements only a small subset of AWS IAM policy behavior.

It does not currently support:

- **IAM condition keys:** Context-dependent restrictions such as MFA requirements, source IP conditions, resource tags, and `iam:PassedToService`.
- **Resource-based policies:** Permissions granted by policies attached to AWS resources.
- **Permissions boundaries:** Restrictions on the maximum permissions available to a principal.
- **AWS Organizations Service Control Policies (SCPs):** Organization-level guardrails that can restrict effective permissions.
- **Session policies:** Additional restrictions associated with temporary sessions.
- **Action or resource wildcard patterns:** Expressions such as `s3:*` or resource-name prefixes.
- **NotAction or NotResource:** IAM policy elements that define exclusions.
- **IAM principal and resource-type validation:** The evaluator does not verify whether the requested action is valid for the supplied ARN.
- **Policy syntax validation:** The evaluator assumes correctly formed statements and supported input types.

Real AWS authorization may involve several interacting policy types, trust relationships, and request-context conditions.

Consequently, an Allow returned by this program does not guarantee that AWS would authorize the same request.

## Security Lessons Learned

This project reinforced several important security engineering concepts:

**Explicit Deny Precedence**

A matching explicit Deny must override an Allow, even if the Allow appears earlier in the policy.

**Least Privilege**

Authorization should permit only the actions and resources necessary to perform an approved operation.

**Correct Control Flow**

Small programming mistakes, including incorrect Boolean expressions or premature returns, can produce incorrect security decisions.

**Adversarial Testing**

Passing normal test cases is insufficient. Security logic should also be tested with conflicting statements, unexpected inputs, and different statement orders.

**Architectural Limitations**

A program must be evaluated against its documented security assumptions. A simplified authorization model cannot be treated as equivalent to the AWS IAM authorization engine.

## Future Improvements

Potential extensions include:

1. Support for additional IAM policy elements and wildcard matching.
2. Input and policy schema validation.
3. Tests for malformed or unsupported policies.
4. Structured authorization explanations showing which statements matched.
5. Additional automated regression tests.
6. Exploration of condition evaluation and interactions among AWS policy types.

These improvements would remain educational unless independently validated against authoritative AWS behavior.

## Training Context

**Curriculum:** Cloud Security Engineering → AI Security Engineering → AI Security Architecture

**Session:** Day 26

**Primary skills practiced:**

- AWS IAM authorization concepts
- Python dictionaries, lists, loops, and Boolean logic
- Function return values and control flow
- Explicit-deny precedence
- Least-privilege reasoning
- Security testing and debugging
- Technical documentation

**Project status:** Core evaluator implemented and tested. Repository packaging and final assertion-based verification pending.

---

*This repository contains educational security exercises using synthetic AWS resources and policies. It is not intended to replace AWS IAM, IAM Access Analyzer, or AWS authorization testing.*
