import os
import time
import argparse

from kafka import KafkaProducer
import json

from cosmotech.coal.utils.logger import LOGGER


parser = argparse.ArgumentParser(description='Notify kafka')
parser.add_argument('--notify-kafka', help='Send notification to kafka', required=True)
parser.add_argument('--kafka-broker', help='Kafka broker', required=True)
parser.add_argument('--kafka-topic', help='Kafka topic', required=True)
parser.add_argument('--kafka-username', help='Kafka username', required=True)
parser.add_argument('--kafka-password', help='Kafka password', required=True)

LOGGER.debug('parcing args')
args = parser.parse_args()


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
    if CSM_ORC_IS_SUCCESS:
        message = f"Run {CSM_RUN_ID} Success"
    else:
        message = f"Run {CSM_RUN_ID} FAIL"

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


if args.notify_kafka.lower() == "true":
    notifyKafka()
