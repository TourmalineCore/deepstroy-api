import os

rabbitmq_host = os.getenv('RABBITMQ_HOST')
rabbitmq_username = os.getenv('RABBITMQ_DEFAULT_USER')
rabbitmq_password = os.getenv('RABBITMQ_DEFAULT_PASS')

if rabbitmq_host is None:
    raise ValueError('You should specify RABBITMQ_HOST to be able to connect to RabbitMQ.')
if rabbitmq_username is None:
    raise ValueError('You should specify RABBITMQ_DEFAULT_USER to be able to connect to RabbitMQ.')
if rabbitmq_password is None:
    raise ValueError('You should specify RABBITMQ_DEFAULT_PASS to be able to connect to RabbitMQ.')


rabbitmq_models_exchange_name = os.getenv('RABBITMQ_MODELS_EXCHANGE_NAME')

if rabbitmq_models_exchange_name is None:
    raise ValueError('You should specify RABBITMQ_MODELS_EXCHANGE_NAME to be able to connect to exchange.')