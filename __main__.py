import ibm_boto3
from ibm_botocore.client import Config, ClientError
import os
# Constants for IBM COS values
credentials = {
        "COS_ENDPOINT": os.environ.get("COS_ENDPOINT", None),
        "COS_API_KEY_ID": os.environ.get("COS_API_KEY_ID", None),
        "COS_INSTANCE_CRN": os.environ.get("COS_INSTANCE_CRN", None),
        "COS_BUCKET": os.environ.get("COS_BUCKET", None),
        } 
        
# Create client
cos = ibm_boto3.client(
    "s3",
    ibm_api_key_id=credentials['COS_API_KEY_ID'],
    ibm_service_instance_id=credentials['COS_INSTANCE_CRN'],
    config=Config(signature_version="oauth"),
    endpoint_url=credentials['COS_ENDPOINT']
) 
def GetFile(bucket_name, object_name):
    print("Get item: {0}".format(object_name))
    try:
        response = cos.get_object(
            Bucket=bucket_name,
            Key=object_name
        )
        return response["Body"].read()
    except ClientError as be:
        print("CLIENT ERROR: {0}\n".format(be))
        return False
    except Exception as e:
        print("Unable to create text file: {0}".format(e))
        return False
        
def main(params):    
  bucket_name = params.get("bucket_name","transcripts" )
  object_name = params.get("object_name","transcript.txt")  
  response = GetFile(bucket_name, object_name)
  return {
        "headers": {
            "Content-Type": "application/json",
        },
        "statusCode": 200,
        "body": response
  }        