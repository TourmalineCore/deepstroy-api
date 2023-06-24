from deepstroy.domain.data_access_layer.db import db


class ForecastingFile(db.Model):
    __tablename__ = 'forecasting_files'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    file_name = db.Column(db.String(2048), nullable=False)
    date_of_upload = db.Column(db.DateTime, nullable=False)
    path = db.Column(db.String(2048), nullable=False)
    isModeling = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Forecast {self.id!r} name: {self.file_name!r}, date: {self.date_of_upload!r}, path: {self.path!r}>'