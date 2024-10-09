import os
import argparse
import time

import boto3
from botocore.config import Config
from kafka import KafkaProducer
import json

from cosmotech.coal.utils.logger import LOGGER
import logging


parser = argparse.ArgumentParser(description='Send parquet data to s3')
parser.add_argument('--source-folder', help='result file source folder', required=True)
parser.add_argument('--s3-url', help='S3 service URL', required=True)
parser.add_argument('--s3-access-key-id', help='S3 access key id', required=True)
parser.add_argument('--s3-secret-access-key', help='S3 secret access key', required=True)
parser.add_argument('--s3-bucket-name', help='S3 access key id', required=True)
parser.add_argument('--s3-use-ssl', help='Use or not SSL for S3 connection', required=True)
parser.add_argument('--s3-ca-pem', help='ca cert for SSL S3 connection', required=True)
parser.add_argument('--csm-organization-id', help='Cosmo Tech Organization ID', required=True)
parser.add_argument('--csm-workspace-id', help='Cosmo Tech Workspace ID', required=True)
parser.add_argument('--csm-runner-id', help='Cosmo Tech Runner ID', required=True)
parser.add_argument('--csm-run-id', help='Cosmo Tech Runner run ID', required=True)
parser.add_argument('--notify-kafka', help='Send notification to kafka', required=True)
parser.add_argument('--kafka-broker', help='Kafka broker', required=True)
parser.add_argument('--kafka-topic', help='Kafka topic', required=True)
parser.add_argument('--kafka-username', help='Kafka username', required=True)
parser.add_argument('--kafka-password', help='Kafka password', required=True)

LOGGER.debug('parcing args')
args = parser.parse_args()


def uploadDirectory(path, bucketname):
    LOGGER.debug('create boto3 client')
    s3_client = boto3.client(
        "s3",
        use_ssl=True if args.s3_use_ssl.lower() == "true" else False,
        aws_access_key_id=args.s3_access_key_id,
        aws_secret_access_key=args.s3_secret_access_key,
        endpoint_url=args.s3_url,
        config=Config(signature_version='s3v4'),
        verify=False if args.s3_ca_pem == "False" else args.s3_ca_pem
    )
    LOGGER.debug('create s3 bucket')
    s3_client.create_bucket(Bucket=args.s3_bucket_name)

    for root, dirs, files in os.walk(path):
        for file in files:
            rel_file_path = os.path.join(f"{args.csm_run_id}", root[len(path) + 1:], file)
            local_file_path = os.path.join(root, file)
            LOGGER.info(f"Uploading {local_file_path} to {rel_file_path}")
            s3_client.upload_file(local_file_path, bucketname, rel_file_path)


def notifyKafka():
    LOGGER.debug('create kafka producer')
    producer = KafkaProducer(
        bootstrap_servers=args.kafka_broker,
        security_protocol='SASL_SSL',
        sasl_mechanism='PLAIN',
        sasl_plain_username=args.kafka_username,
        sasl_plain_password=args.kafka_password,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    # Produce a message
    message = "Hello, Kafka with TLS!"
    try:
        LOGGER.debug('send message to producer')
        producer.send(args.kafka_topic, value=message)
        producer.flush()  # Ensure all messages are sent
        LOGGER.info(f"Message '{message}' sent to topic '{args.kafka_topic}'")
    except Exception as e:
        LOGGER.info(f"Error sending message: {e}")
    finally:
        producer.close()
        return


uploadDirectory(args.source_folder, args.s3_bucket_name)
if args.notify_kafka.lower() == "true":
    notifyKafka()
