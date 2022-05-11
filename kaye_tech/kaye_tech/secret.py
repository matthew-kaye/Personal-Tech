import boto3
from botocore.exceptions import ClientError
import json


def get_secret(secret_name: str) -> dict:
    session = boto3.session.Session()
    client = session.client(service_name="secretsmanager", region_name="eu-west-2")
    try:
        return json.loads(client.get_secret_value(SecretId=secret_name)["SecretString"])
    except ClientError as e:
        if e.response["Error"]["Code"] == "DecryptionFailureException":
            print(
                "Secrets Manager can't decrypt the protected secret"
                " text using the provided KMS key."
            )
            raise e
        elif e.response["Error"]["Code"] == "InternalServiceErrorException":
            print("An error occurred on the server side.")
            raise e
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            print("You provided an invalid value for a parameter.")
            raise e
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            print(
                "You provided a parameter value that is not valid"
                " for the current state of the resource."
            )
            raise e
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            print("We can't find the resource that you asked for.")
            raise e
