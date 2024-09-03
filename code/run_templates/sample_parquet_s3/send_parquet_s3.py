import argparse
import boto3
import os
from cosmotech.coal.utils.logger import LOGGER

parser = argparse.ArgumentParser(description='Send parquet data to s3')
parser.add_argument('--source-folder', help='result file source folder', required=True)
parser.add_argument('--s3-url', help='S3 service URL', required=True)
parser.add_argument('--s3-access-key-id', help='S3 access key id', required=True)
parser.add_argument('--s3-secret-access-key', help='S3 secret access key', required=True)
parser.add_argument('--s3-bucket-name', help='S3 access key id', required=True)
parser.add_argument('--csm-organization-id', help='Cosmo Tech Organization ID', required=True)
parser.add_argument('--csm-workspace-id', help='Cosmo Tech Workspace ID', required=True)
parser.add_argument('--csm-runner-id', help='Cosmo Tech Runner ID', required=True)
parser.add_argument('--csm-run-id', help='Cosmo Tech Runner run ID', required=True)

args = parser.parse_args()

def get_connection(is_client=True):
    connect_function = boto3.client if is_client else boto3.resource
    return connect_function('s3')

s3_client = get_connection()
s3 = boto3.resource('s3')
s3_client.create_bucket(Bucket=args.s3_bucket_name)

def uploadDirectory(path,bucketname):
    for root,dirs,files in os.walk(path):
        for file in files:
            rel_file_path = os.path.join(f"{args.csm_run_id}", root[len(path)+1:], file)
            local_file_path = os.path.join(root,file)
            LOGGER.info(f"Uploading {local_file_path} to {rel_file_path}")
            s3_client.upload_file(local_file_path,bucketname, rel_file_path)

uploadDirectory(args.source_folder,args.s3_bucket_name)
