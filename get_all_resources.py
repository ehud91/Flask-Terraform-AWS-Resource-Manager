import boto3
import boto3.session

### Example: {Profile-name}
# [default]
# aws_access_key_id=foo
# aws_secret_access_key=bar

# [dev]
# aws_access_key_id=foo2
# aws_secret_access_key=bar2

# [prod]
# aws_access_key_id=foo3
# aws_secret_access_key=bar3
###

# Initialize a session using AWS credentials
session = boto3.Session(profile_name='dev')

# Initialize clients for specific services
rds_client = session.client('rds')
s3_client = session.client('s3')
lambda_client = session.client('lambda')

resources = []

# RDS Instances
def list_rds_instances():
    rds_instances = rds_client.describe_db_instances()
    for db_instance in rds_instances['DBInstances']:
        arn = db_instance['DBInstanceArn']
        resources.append({'Service': 'RDS', 'ARN': arn})

# S3 Buckets
def list_s3_buckets():
    s3_buckets = s3_client.list_buckets()
    for bucket in s3_buckets['Buckets']:
        arn = f"arn:aws:s3:::{bucket['Name']}"
        resources.append({'Service': 'S3', 'ARN': arn})

# Lambda Functions
def list_lambda_functions():
    lambda_functions = lambda_client.list_functions()
    for function in lambda_functions['Functions']:
        arn = function['FunctionArn']
        resources.append({'Service': 'Lambda', 'ARN': arn})

# Fetch all resources
#list_rds_instances()
#list_s3_buckets()
#list_lambda_functions()

# Print resources with ARNs
#for resource in resources:
#    print(f"Service: {resource['Service']}, ARN: {resource['ARN']}")