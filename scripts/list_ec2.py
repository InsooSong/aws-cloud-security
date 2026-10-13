import boto3
from botocore.exceptions import BotoCoreError, ClientError, ProfileNotFound


PROFILE_NAME = "development"
REGION = "ap-northeast-1"


def list_instances(session):
    ec2 = session.client(
        "ec2",
        region_name=REGION,
    )

    paginator = ec2.get_paginator("describe_instances")

    instance_count = 0

    print(f"=== EC2 Instances ({REGION}) ===")

    for page in paginator.paginate():
        for reservation in page.get("Reservations", []):
            for instance in reservation.get("Instances", []):
                instance_id = instance["InstanceId"]
                state = instance["State"]["Name"]
                public_ip = instance.get("PublicIpAddress", "None")
                private_ip = instance.get("PrivateIpAddress", "None")

                print(
                    f"Instance ID : {instance_id}\n"
                    f"State       : {state}\n"
                    f"Public IP   : {public_ip}\n"
                    f"Private IP  : {private_ip}\n"
                    "------------------------------"
                )

                instance_count += 1

    if instance_count == 0:
        print("No EC2 instances found.")


def main():
    try:
        session = boto3.Session(
            profile_name=PROFILE_NAME,
            region_name=REGION,
        )

        list_instances(session)

    except ProfileNotFound:
        print(f"[ERROR] AWS profile '{PROFILE_NAME}' was not found.")

    except (BotoCoreError, ClientError) as error:
        print(f"[ERROR] Failed to list EC2 instances: {error}")


if __name__ == "__main__":
    main()
