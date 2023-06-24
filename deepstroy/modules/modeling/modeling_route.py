from flask import Blueprint, request
import pandas as pd
import datetime
from http import HTTPStatus
import json
import io

from deepstroy.config.rabbitmq_config import rabbitmq_models_exchange_name
from deepstroy.domain.forecasting_files.forecasting_files import ForecastingFile
from deepstroy.helpers.rabbitmq_message_publisher.rabbitmq_message_publisher import RabbitMqMessagePublisher
from deepstroy.helpers.s3_helper import S3Helper
from deepstroy.helpers.s3_paths import create_path_for_file_forecasting
from deepstroy.modules.forecast.commands.new_file_for_forecasting_command import NewForecastingFileCommand

modeling_blueprint = Blueprint('modeling', __name__, url_prefix='/modeling')


@modeling_blueprint.route('/add', methods=['POST'])
def upload_data_for_modeling():
    request_params = request.json

    dataframe = pd.DataFrame(
        columns=["obj_prg",
                 "obj_subprg",
                 "obj_key",
                 "obj_pwa_key",
                 "obj_shortName",
                 "Кодзадачи",
                 "НазваниеЗадачи",
                 "ПроцентЗавершенияЗадачи",
                 "ДатаНачалаЗадачи",
                 "ДатаОкончанияЗадачи",
                 "ДатаначалаБП0",
                 "ДатаокончанияБП0",
                 "Статуспоэкспертизе",
                 "Экспертиза"]
    )

    steps = request_params.get("steps")

    for step in steps:
        new_row = {
            "obj_prg": request_params.get("project"),
            "obj_subprg": request_params.get("subProject"),
            "obj_key": request_params.get("keyObject"),
            "obj_pwa_key": request_params.get("keyPwa"),
            "obj_shortName": request_params.get("shortName"),
            "Кодзадачи": step["codeTask"],
            "НазваниеЗадачи": step["nameTask"],
            "ПроцентЗавершенияЗадачи": step["completionPercentageTask"],
            "ДатаНачалаЗадачи": step["dateStartTask"],
            "ДатаОкончанияЗадачи": step["dateEndTask"],
            "ДатаначалаБП0": step["dateStartContract"],
            "ДатаокончанияБП0": step["dateEndContract"],
            "Статуспоэкспертизе": step["statusExpertise"],
            "Экспертиза": step["expertise"],
        }
        new_row_list = list(new_row.values())
        dataframe.loc[len(dataframe)] = new_row_list

    mem_file = io.BytesIO()
    dataframe.to_excel(mem_file, engine='xlsxwriter')

    forecasting_file_entity = ForecastingFile(
                                            file_name="file_for_modeling",
                                            date_of_upload=datetime.datetime.utcnow(),
                                            path=create_path_for_file_forecasting(),
                                            isModeling=True
                                        )

    S3Helper().s3_upload_file(
        file_path_in_bucket=forecasting_file_entity.path,
        file_bytes=mem_file.getvalue(),
        public=True,
    )
    id = NewForecastingFileCommand().create(forecasting_file_entity)

    message_with_file_parameters = {
        'file_id': id,
        'path': forecasting_file_entity.path,
    }

    RabbitMqMessagePublisher().publish_message_to_exchange(exchange_name=rabbitmq_models_exchange_name,
                                                           message=message_with_file_parameters)

    return 'Ok.', HTTPStatus.OK
