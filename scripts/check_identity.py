import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound


PROFILE_NAME = "development"
DEFAULT_REGION = "ap-northeast-1"


def main():
    try:
        session = boto3.Session(
            profile_name=PROFILE_NAME,
            region_name=DEFAULT_REGION,
        )

        sts = session.client("sts")

        identity = sts.get_caller_identity()

        print("=== AWS Identity ===")
        print(f"Account   : {identity['Account']}")
        print(f"Principal : {identity['Arn']}")
        print(f"Region    : {session.region_name}")

    except ProfileNotFound:
        print(f"[ERROR] AWS profile '{PROFILE_NAME}' was not found.")

    except (BotoCoreError, ClientError) as error:
        print(f"[ERROR] Failed to retrieve AWS identity: {error}")


if __name__ == "__main__":
    main()
