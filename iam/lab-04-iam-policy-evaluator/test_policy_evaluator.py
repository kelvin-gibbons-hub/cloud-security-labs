from policy_evaluator import evaluate_policy

policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["lambda:UpdateFunctionCode"],
            "Resource": [
                "arn:aws:lambda:us-east-1:111122223333:function:ApprovedFunction"
            ]
        },
        {
            "Effect": "Deny",
            "Action": ["iam:AttachRolePolicy"],
            "Resource": ["*"]
        }
    ]
}

adversarial_policy = {
    "Statement": [
        {
            "Sid": "BroadRead",
            "Effect": "Allow",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": ["*"]
        },
        {
            "Sid": "ProtectedObject",
            "Effect": "Deny",
            "Action": ["s3:GetObject"],
            "Resource": [
                "arn:aws:s3:::financial-records/payroll.csv"
            ]
        },
        {
            "Sid": "LambdaDeployment",
            "Effect": "Allow",
            "Action": ["lambda:UpdateFunctionCode"],
            "Resource": [
                "arn:aws:lambda:us-east-1:111122223333:function:ProductionAPI"
            ]
        },
        {
            "Sid": "BroadRead2",
            "Effect": "Deny",
            "Action": ["s3:GetObject", "s3:ListBucket"],
            "Resource": ["*"]
        }
    ]
}


s3_policy = {
    "Statement": [
        {
            "Effect": "Allow",
            "Action": ["s3:GetObject"],
            "Resource": ["*"]
        },
        {
            "Effect": "Deny",
            "Action": ["s3:GetObject"],
            "Resource": [
                "arn:aws:s3:::sensitive-bucket/private.txt"
            ]
        }
    ]
}

tests = [
    (
        "A",
        "s3:GetObject",
        "arn:aws:s3:::financial-records/payroll.csv"
    ),
    (
        "B",
        "s3:GetObject",
        "arn:aws:s3:::financial-records/public-report.csv"
    ),
    (
        "C",
        "s3:ListBucket",
        "arn:aws:s3:::financial-records"
    ),
    (
        "D",
        "lambda:UpdateFunctionCode",
        "arn:aws:lambda:us-east-1:111122223333:function:ProductionAPI"
    ),
    (
        "E",
        "lambda:UpdateFunctionConfiguration",
        "arn:aws:lambda:us-east-1:111122223333:function:ProductionAPI"
    ),
    (
        "G",
        "s3:GetObject",
        "arn:aws:s3:::financial-records"
    )

]

for test_id, action, resource in tests:
    result = evaluate_policy(
        adversarial_policy,
        action,
        resource
    )
    print(test_id, result)

result = evaluate_policy(
    policy,
    "iam:AttachRolePolicy",
    "arn:aws:iam::111122223333:role/AdminRole"
)

print(result)

assert evaluate_policy(
    s3_policy,
    "s3:GetObject",
    "arn:aws:s3:::sensitive-bucket/private.txt"
) == "DENY"
