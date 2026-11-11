# AWS CloudTrail Incident Investigation — CT-023

**Lab:** Day 23 — Cloud Security Incident Investigation  
**Environment:** Synthetic AWS production environment  
**Account:** 111122223333 (fictional)  
**Incident date:** November 10, 2026  
**Status:** Initial remediation observed; containment not verified  
**Classification:** Suspected unauthorized IAM privilege escalation

## 1. Executive Summary

CloudTrail records indicate that an assumed `OperationsRole` session successfully attached the AWS-managed `AdministratorAccess` policy to `AppDeployRole`.

Approximately two minutes later, a deployment-service identity successfully assumed `AppDeployRole`. That role session subsequently attempted to stop CloudTrail logging, but the request was denied.

A security response session later detached `AdministratorAccess`. Although the detachment succeeded, the available evidence does not establish complete containment.

The incident requires additional investigation to determine authorization, remaining permissions, session validity, and possible follow-on activity.

## 2. Incident Timeline

All timestamps are UTC.

| Time | Event | Finding |
|---|---|---|
| 07:09:12 | E01 — GetRole | OperationsRole successfully inspected AppDeployRole |
| 07:13:40 | E02 — PutRolePolicy | An attempt to create or update the EmergencyAdmin inline policy was denied |
| 07:14:03 | E03 — AttachRolePolicy | AdministratorAccess was successfully attached to AppDeployRole |
| 07:16:11 | E04 — AssumeRole | deployment-service successfully assumed AppDeployRole |
| 07:18:20 | E05 — StopLogging | The AppDeployRole session attempted to stop ProductionTrail logging; access was denied |
| 07:23:55 | E06 — DetachRolePolicy | SecurityResponseRole successfully detached AdministratorAccess |

## 3. Identity and Attribution

The privilege escalation was initiated by:

`arn:aws:sts::111122223333:assumed-role/OperationsRole/alex-session`

The subsequent role assumption was initiated by:

`arn:aws:iam::111122223333:user/deployment-service`

The provided records do not conclusively establish the human responsible for either identity's actions.

Additional session, authentication, change-management, and service execution records are required for attribution.

## 4. Confirmed Findings

- An IAM managed policy granting administrator-level access was attached to AppDeployRole.
- The preceding inline-policy modification attempt was denied.
- AppDeployRole was subsequently assumed successfully.
- An attempt to stop ProductionTrail logging was denied.
- AdministratorAccess was subsequently detached successfully.

## 5. Unverified Risks

- Whether the policy attachment was authorized
- Whether previously issued temporary role sessions retain effective elevated access
- Whether other privileged policies or changes remain
- Whether the OperationsRole principal can repeat the escalation
- Whether additional API operations occurred during the exposure window
- Whether CloudTrail logging and event coverage remained complete

## 6. Recommended Containment and Investigation

**Priority 1 — Restrict continued access**

Review and, where appropriate, revoke affected temporary sessions. Investigate the involved identities and prevent further unauthorized role assumptions or policy modifications while coordinating with system owners.

**Priority 2 — Verify permissions**

Confirm AdministratorAccess is detached. Inspect all remaining inline and managed policies, role trust relationships, and the permissions enabling the original policy attachment.

**Priority 3 — Establish incident scope**

Verify CloudTrail logging status and investigate related events involving the OperationsRole, AppDeployRole, deployment-service, and affected AWS resources.

**Priority 4 — Validate recovery**

Confirm the role has returned to its approved least-privilege configuration, establish that inappropriate sessions cannot continue privileged operations, and monitor for repeated changes.

## 7. Conclusion

The available evidence supports a suspected privilege-escalation incident followed by a successful administrative detachment of the elevated policy.

Containment is **partial and not independently verified**.

The incident should remain open pending permissions review, session investigation, additional CloudTrail analysis, and confirmation of operational recovery.

---

**Evidence note:** This report analyzes six synthetic CloudTrail-like events supplied for a training exercise. Findings are limited to those records and do not describe an actual security incident.
