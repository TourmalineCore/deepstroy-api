# import io
# import random
# from datetime import datetime
# from http import HTTPStatus
import datetime
from http import HTTPStatus
import json
import pytz
# import imagehash
# from PIL import Image
from flask import Blueprint, request
import requests

from deepstroy.config.rabbitmq_config import rabbitmq_models_exchange_name
from deepstroy.domain.forecasting_files.forecasting_files import ForecastingFile
from deepstroy.helpers.rabbitmq_message_publisher.rabbitmq_message_publisher import RabbitMqMessagePublisher
from deepstroy.helpers.s3_helper import S3Helper
from deepstroy.helpers.s3_paths import create_path_for_file_forecasting
from deepstroy.modules.forecast.commands.new_file_for_forecasting_command import NewForecastingFileCommand
from deepstroy.modules.forecast.queries.get_all_files import GetForecastFileQuery

forecast_blueprint = Blueprint('forecast', __name__, url_prefix='/forecast')


@forecast_blueprint.route('/upload-file/<file_name>', methods=['POST'])
def upload_file_for_forecasting(file_name):
    file_bytes = request.get_data()
    forecasting_file_entity = ForecastingFile(
                                            file_name=file_name,
                                            date_of_upload=datetime.datetime.utcnow(),
                                            path=create_path_for_file_forecasting(),
                                            isModeling=False
                                        )
    S3Helper().s3_upload_file(
        file_path_in_bucket=forecasting_file_entity.path,
        file_bytes=file_bytes,
        public=True,
    )
    id = NewForecastingFileCommand().create(forecasting_file_entity)
    message_with_file_parameters = {
        'file_id': id,
        'path': forecasting_file_entity.path,
    }

    RabbitMqMessagePublisher().publish_message_to_exchange(exchange_name=rabbitmq_models_exchange_name,
                                                           message=message_with_file_parameters)

    return str(id), HTTPStatus.OK

@forecast_blueprint.route('/download-file/<id>', methods=['GET'])
def get_file_path(id):
    res = requests.get(f'http://deepstroy-model-service:5000/model-service/predict/{id}').text
    result_path = "http://localhost:9211/deepstroy/local/" + json.loads(res)["path"]
    return result_path, HTTPStatus.OK

@forecast_blueprint.route('/history', methods=['GET'])
def get_history():

    forecast_files = GetForecastFileQuery().all()
    response = []
    if forecast_files:
        for file in forecast_files:
            response.append({"id": file.id, "dateOfUpload": str(file.date_of_upload), "fileName": file.file_name})

        for i in range(len(response)):
            res = requests.get(f'http://deepstroy-model-service:5000/model-service/predict/{response[i]["id"]}').text
            response[i]["path"] = "http://localhost:9211/deepstroy/local/" + json.loads(res)["path"]

        return json.dumps(response), HTTPStatus.OK
    else:
        return json.dumps([]), HTTPStatus.OK

@forecast_blueprint.route('/result/<id>', methods=['GET'])
def get_forecasted_file(id):
    res = requests.get(f'http://deepstroy-model-service:5000/model-service/predict/{id}').text
    if res != 'Doesnt exist':
        response = "http://localhost:9211/deepstroy/local/" + json.loads(res)["path"]
        return json.dumps(response), HTTPStatus.OK