from deepstroy.domain import ForecastingFile
from deepstroy.domain.data_access_layer.session import session


class GetForecastFileQuery():
    def __init__(self):
        pass

    def all(self) -> ForecastingFile:
        current_session = session()

        try:
            return current_session\
                .query(ForecastingFile)\
                .filter(ForecastingFile.isModeling == False)\
                .all()

        finally:
            current_session.close()