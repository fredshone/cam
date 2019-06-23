import boto3

BUCKET_NAME = "test-cam-dump"

s3_resource = boto3.resource('s3')

s3_resource.create_bucket(Bucket=BUCKET_NAME,
                          CreateBucketConfiguration={
                              'LocationConstraint': 'eu-west-2'})
