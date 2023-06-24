from deepstroy.domain import ForecastingFile
from deepstroy.domain.data_access_layer.session import session


class NewForecastingFileCommand:
    def __init__(self):
        pass

    def create(self, forecast_file_entity: ForecastingFile) -> int:
        current_session = session()
        try:
            current_session.add(forecast_file_entity)
            current_session.commit()
            return forecast_file_entity.id
        finally:
            current_session.close()
