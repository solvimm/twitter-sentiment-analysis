import json
from datetime import datetime
import locale
import boto3
from botocore.exceptions import ClientError
import os
import requests
import base64


# CONFIGURE AWS SERVICES
secrets_manager_client = boto3.session.Session().client(service_name='secretsmanager', region_name='us-east-1')
secret_name = "prod/solvimm-sales-bi"


# GETS SECRET FROM AWS SECRETS MANAGER
def get_secret(secret):
    try:
        get_secret_value_response = secrets_manager_client.get_secret_value(SecretId=secret_name)
        print(get_secret_value_response)
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
    else:
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary, one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            s = json.loads(get_secret_value_response['SecretString'])[secret]
            return s
        else:
            decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])[secret]
            return decoded_binary_secret
