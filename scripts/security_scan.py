import json
from datetime import datetime, timezone
from pathlib import Path

import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound


PROFILE_NAME = "development"

REGIONS = [
    "ap-northeast-1",
]

PUBLIC_IPV4 = "0.0.0.0/0"
PUBLIC_IPV6 = "::/0"

SENSITIVE_PORTS = {
    22: "SSH",
    3389: "RDP",
    3306: "MySQL",
    5432: "PostgreSQL",
}

REPORT_PATH = Path("reports/security-report.json")


def create_finding(
    service,
    resource,
    region,
    issue,
    severity,
):
    return {
        "service": service,
        "resource": resource,
        "region": region,
        "issue": issue,
        "severity": severity,
    }


def verify_identity(session):
    sts = session.client("sts")

    identity = sts.get_caller_identity()

    print("=== AWS Security Scanner ===")
    print(f"Account   : {identity['Account']}")
    print(f"Principal : {identity['Arn']}")
    print(f"Regions   : {', '.join(REGIONS)}")
    print()

    return identity


def check_public_ec2(session, region):
    findings = []

    ec2 = session.client(
        "ec2",
        region_name=region,
    )

    paginator = ec2.get_paginator(
        "describe_instances"
    )

    for page in paginator.paginate():
        for reservation in page.get(
            "Reservations",
            [],
        ):
            for instance in reservation.get(
                "Instances",
                [],
            ):
                instance_id = instance["InstanceId"]

                public_ip = instance.get(
                    "PublicIpAddress"
                )

                if public_ip:
                    findings.append(
                        create_finding(
                            service="EC2",
                            resource=instance_id,
                            region=region,
                            issue=(
                                "EC2 instance has a "
                                "public IPv4 address"
                            ),
                            severity="REVIEW",
                        )
                    )

    return findings


def port_range_contains(
    from_port,
    to_port,
    target_port,
):
    if from_port is None or to_port is None:
        return False

    return (
        from_port
        <= target_port
        <= to_port
    )


def check_security_groups(session, region):
    findings = []

    ec2 = session.client(
        "ec2",
        region_name=region,
    )

    paginator = ec2.get_paginator(
        "describe_security_groups"
    )

    for page in paginator.paginate():
        for group in page.get(
            "SecurityGroups",
            [],
        ):
            group_id = group["GroupId"]

            for rule in group.get(
                "IpPermissions",
                [],
            ):
                protocol = rule.get(
                    "IpProtocol"
                )

                from_port = rule.get(
                    "FromPort"
                )

                to_port = rule.get(
                    "ToPort"
                )

                public_ipv4 = any(
                    ip_range.get("CidrIp")
                    == PUBLIC_IPV4
                    for ip_range
                    in rule.get("IpRanges", [])
                )

                public_ipv6 = any(
                    ip_range.get("CidrIpv6")
                    == PUBLIC_IPV6
                    for ip_range
                    in rule.get(
                        "Ipv6Ranges",
                        [],
                    )
                )

                if not (
                    public_ipv4
                    or public_ipv6
                ):
                    continue

                if protocol == "-1":
                    findings.append(
                        create_finding(
                            service="EC2",
                            resource=group_id,
                            region=region,
                            issue=(
                                "Security Group allows "
                                "all traffic from the internet"
                            ),
                            severity="HIGH",
                        )
                    )

                    continue

                for port, name in SENSITIVE_PORTS.items():
                    if port_range_contains(
                        from_port,
                        to_port,
                        port,
                    ):
                        findings.append(
                            create_finding(
                                service="EC2",
                                resource=group_id,
                                region=region,
                                issue=(
                                    f"{name} port {port} "
                                    "is exposed to the internet"
                                ),
                                severity="HIGH",
                            )
                        )

    return findings


def check_s3_security(session):
    findings = []

    s3 = session.client("s3")

    paginator = s3.get_paginator(
        "list_buckets"
    )

    for page in paginator.paginate():
        for bucket in page.get(
            "Buckets",
            [],
        ):
            bucket_name = bucket["Name"]

            findings.extend(
                check_s3_public_access(
                    s3,
                    bucket_name,
                )
            )

            findings.extend(
                check_s3_encryption(
                    s3,
                    bucket_name,
                )
            )

    return findings


def check_s3_public_access(
    s3,
    bucket_name,
):
    findings = []

    try:
        response = (
            s3.get_public_access_block(
                Bucket=bucket_name
            )
        )

        config = response[
            "PublicAccessBlockConfiguration"
        ]

        required_settings = [
            "BlockPublicAcls",
            "IgnorePublicAcls",
            "BlockPublicPolicy",
            "RestrictPublicBuckets",
        ]

        missing_settings = [
            setting
            for setting in required_settings
            if not config.get(
                setting,
                False,
            )
        ]

        if missing_settings:
            findings.append(
                create_finding(
                    service="S3",
                    resource=bucket_name,
                    region="global",
                    issue=(
                        "Bucket-level Public Access "
                        "Block is not fully enabled: "
                        + ", ".join(
                            missing_settings
                        )
                    ),
                    severity="REVIEW",
                )
            )

    except ClientError as error:
        code = error.response[
            "Error"
        ]["Code"]

        if code == (
            "NoSuchPublicAccessBlockConfiguration"
        ):
            findings.append(
                create_finding(
                    service="S3",
                    resource=bucket_name,
                    region="global",
                    issue=(
                        "Bucket-level Public Access "
                        "Block configuration is missing"
                    ),
                    severity="REVIEW",
                )
            )
        else:
            print(
                f"[ERROR] "
                f"Failed to check Public Access "
                f"Block for {bucket_name}: {code}"
            )

    return findings


def check_s3_encryption(
    s3,
    bucket_name,
):
    findings = []

    try:
        response = (
            s3.get_bucket_encryption(
                Bucket=bucket_name
            )
        )

        rules = response[
            "ServerSideEncryptionConfiguration"
        ]["Rules"]

        for rule in rules:
            default = rule.get(
                "ApplyServerSideEncryptionByDefault",
                {},
            )

            algorithm = default.get(
                "SSEAlgorithm"
            )

            if algorithm == "AES256":
                findings.append(
                    create_finding(
                        service="S3",
                        resource=bucket_name,
                        region="global",
                        issue=(
                            "Bucket uses SSE-S3 "
                            "default encryption"
                        ),
                        severity="INFO",
                    )
                )

            elif algorithm == "aws:kms":
                pass

    except ClientError as error:
        code = error.response[
            "Error"
        ]["Code"]

        print(
            f"[ERROR] "
            f"Failed to check encryption "
            f"for {bucket_name}: {code}"
        )

    return findings


def get_guardduty_findings(
    session,
    region,
):
    findings = []

    guardduty = session.client(
        "guardduty",
        region_name=region,
    )

    detectors = guardduty.list_detectors().get(
        "DetectorIds",
        [],
    )

    if not detectors:
        findings.append(
            create_finding(
                service="GuardDuty",
                resource="Region",
                region=region,
                issue=(
                    "No GuardDuty detector "
                    "found in this Region"
                ),
                severity="REVIEW",
            )
        )

        return findings

    detector_id = detectors[0]

    paginator = guardduty.get_paginator(
        "list_findings"
    )

    finding_ids = []

    for page in paginator.paginate(
        DetectorId=detector_id
    ):
        finding_ids.extend(
            page.get(
                "FindingIds",
                [],
            )
        )

    # GuardDuty GetFindings accepts a limited
    # number of IDs per request, so process
    # them in small batches.
    batch_size = 50

    for index in range(
        0,
        len(finding_ids),
        batch_size,
    ):
        batch = finding_ids[
            index:index + batch_size
        ]

        response = (
            guardduty.get_findings(
                DetectorId=detector_id,
                FindingIds=batch,
            )
        )

        for finding in response.get(
            "Findings",
            [],
        ):
            severity = (
                guardduty_severity(
                    finding.get(
                        "Severity",
                        0,
                    )
                )
            )

            resource = finding.get(
                "Resource",
                {},
            ).get(
                "ResourceType",
                "Unknown",
            )

            findings.append(
                create_finding(
                    service="GuardDuty",
                    resource=resource,
                    region=region,
                    issue=finding.get(
                        "Title",
                        finding.get(
                            "Type",
                            "GuardDuty finding",
                        ),
                    ),
                    severity=severity,
                )
            )

    return findings


def guardduty_severity(score):
    if score >= 9:
        return "CRITICAL"

    if score >= 7:
        return "HIGH"

    if score >= 4:
        return "MEDIUM"

    return "LOW"


def get_inspector_findings(
    session,
    region,
):
    findings = []

    inspector = session.client(
        "inspector2",
        region_name=region,
    )

    paginator = inspector.get_paginator(
        "list_findings"
    )

    for page in paginator.paginate():
        for finding in page.get(
            "findings",
            [],
        ):
            resources = finding.get(
                "resources",
                [],
            )

            resource_id = "Unknown"

            if resources:
                resource_id = resources[0].get(
                    "id",
                    "Unknown",
                )

            findings.append(
                create_finding(
                    service="Inspector",
                    resource=resource_id,
                    region=region,
                    issue=finding.get(
                        "title",
                        "Inspector finding",
                    ),
                    severity=finding.get(
                        "severity",
                        "UNKNOWN",
                    ),
                )
            )

    return findings


def write_report(
    identity,
    findings,
):
    REPORT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    report = {
        "generated_at": (
            datetime.now(
                timezone.utc
            ).isoformat()
        ),
        "account": identity["Account"],
        "summary": {
            "finding_count": len(findings)
        },
        "findings": findings,
    }

    with REPORT_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            report,
            file,
            indent=2,
            default=str,
        )

    print()
    print(
        f"Report written to "
        f"{REPORT_PATH}"
    )


def print_summary(findings):
    print()
    print("=== Scan Summary ===")

    if not findings:
        print("No findings detected.")
        return

    severity_order = [
        "CRITICAL",
        "HIGH",
        "MEDIUM",
        "REVIEW",
        "LOW",
        "INFO",
    ]

    for severity in severity_order:
        count = sum(
            1
            for finding in findings
            if finding["severity"]
            == severity
        )

        if count:
            print(
                f"{severity}: {count}"
            )


def main():
    try:
        session = boto3.Session(
            profile_name=PROFILE_NAME,
        )

        identity = verify_identity(
            session
        )

        findings = []

        for region in REGIONS:
            print(
                f"Checking region: "
                f"{region}"
            )

            findings.extend(
                check_public_ec2(
                    session,
                    region,
                )
            )

            findings.extend(
                check_security_groups(
                    session,
                    region,
                )
            )

            findings.extend(
                get_guardduty_findings(
                    session,
                    region,
                )
            )

            findings.extend(
                get_inspector_findings(
                    session,
                    region,
                )
            )

        findings.extend(
            check_s3_security(
                session
            )
        )

        print_summary(findings)

        write_report(
            identity,
            findings,
        )

    except ProfileNotFound:
        print(
            f"[ERROR] AWS profile "
            f"'{PROFILE_NAME}' "
            f"was not found."
        )

    except (
        BotoCoreError,
        ClientError,
    ) as error:
        print(
            f"[ERROR] AWS API error: "
            f"{error}"
        )


if __name__ == "__main__":
    main()
