import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound


PROFILE_NAME = "development"


def list_buckets(session):
    s3 = session.client("s3")

    paginator = s3.get_paginator("list_buckets")

    bucket_count = 0

    print("=== S3 Buckets ===")

    for page in paginator.paginate():
        for bucket in page.get("Buckets", []):
            bucket_name = bucket["Name"]
            creation_date = bucket["CreationDate"]

            print(
                f"Bucket       : {bucket_name}\n"
                f"Created      : {creation_date}\n"
                "------------------------------"
            )

            bucket_count += 1

    if bucket_count == 0:
        print("No S3 buckets found.")


def main():
    try:
        session = boto3.Session(
            profile_name=PROFILE_NAME,
        )

        list_buckets(session)

    except ProfileNotFound:
        print(f"[ERROR] AWS profile '{PROFILE_NAME}' was not found.")

    except (BotoCoreError, ClientError) as error:
        print(f"[ERROR] Failed to list S3 buckets: {error}")


if __name__ == "__main__":
    main()
