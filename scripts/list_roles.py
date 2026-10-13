import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound


PROFILE_NAME = "development"


def list_roles(session):
    iam = session.client("iam")

    paginator = iam.get_paginator("list_roles")

    role_count = 0

    print("=== IAM Roles ===")

    for page in paginator.paginate():
        for role in page.get("Roles", []):
            role_name = role["RoleName"]
            created = role["CreateDate"]
            max_session_duration = role["MaxSessionDuration"]

            print(
                f"Role Name            : {role_name}\n"
                f"Created              : {created}\n"
                f"Max Session Duration : {max_session_duration} seconds\n"
                "------------------------------------------"
            )

            role_count += 1

    if role_count == 0:
        print("No IAM roles found.")


def main():
    try:
        session = boto3.Session(
            profile_name=PROFILE_NAME,
        )

        list_roles(session)

    except ProfileNotFound:
        print(f"[ERROR] AWS profile '{PROFILE_NAME}' was not found.")

    except (BotoCoreError, ClientError) as error:
        print(f"[ERROR] Failed to list IAM roles: {error}")


if __name__ == "__main__":
    main()
