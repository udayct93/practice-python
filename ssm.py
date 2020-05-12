
import boto3
client=boto3.client("secretsmanager")

response = client.get_secret_value(
    SecretId='CM_BIO_PRODUCTS_99999'
    # VersionId='string',
    # VersionStage='string'
)
print(response)