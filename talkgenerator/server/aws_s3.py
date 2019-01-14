import boto3  
import botocore

singleton_s3 = None

def get_s3():
    global singleton_s3
    if not singleton_s3:
        try:
            #TODO pull client keys from .env 
            s3 = boto3.client('s3')
            singleton_s3 = s3 
            
        except Exception as error:
            print("AWS S3 Client error")
            print(error)
    
    return singleton_s3


def check_for_object(bucket, key):
    try:
        get_s3().head_bucket(Bucket=bucket)
    except botocore.exceptions.ClientError as e:
        # If a client error is thrown, then check that it was a 404 error.
        # If it was a 404 error, then the bucket does not exist.
        error_code = e.response['Error']['Code']
        if error_code == '404':
            print('AWS Talk bucket not found.')
            return None
        else: 
            print('AWS S3 connect error' + error_code)
            return None
    
    try:
        get_s3().head_object(Bucket=bucket, Key=key)
    except botocore.exceptions.ClientError:
        # Not found
        return None

    return True
    
def store_file(bucket, key, file):
    get_s3().upload_file(file, bucket, key, ExtraArgs={'ACL':'public-read'})
    return

