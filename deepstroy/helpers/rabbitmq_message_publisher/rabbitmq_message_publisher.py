import json
import logging

import pika
from pika import ConnectionParameters, PlainCredentials

from deepstroy.config.rabbitmq_config import rabbitmq_host, rabbitmq_username, rabbitmq_password

PARAMETERS = ConnectionParameters(
    host=rabbitmq_host,
    credentials=PlainCredentials(rabbitmq_username, rabbitmq_password),
)


class RabbitMqMessagePublisher:
    def __init__(self):
        pass

    @staticmethod
    def publish_message_to_exchange(exchange_name,
                                    message,
                                    exchange_type='fanout'):
        connection = pika.BlockingConnection(PARAMETERS)
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name,
                                 exchange_type=exchange_type)

        try:
            channel.basic_publish(
                exchange=exchange_name,
                routing_key='',
                body=json.dumps(message).encode('utf-8'),
                properties=pika.BasicProperties(
                    delivery_mode=2,
                )
            )
        except Exception:
            logging.warning('Aborting...')
            connection.close()
