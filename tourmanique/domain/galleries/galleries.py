from tourmanique.domain.data_access_layer.db import db


class Gallery(db.Model):
    __tablename__ = 'galleries'

    id = db.Column(db.BigInteger, primary_key=True, autoincrement=True)
    name = db.Column(db.String(2048), nullable=True)
    user_id = db.Column(db.BigInteger, nullable=True)
    deleted_at_utc = db.Column(db.DateTime, nullable=True)

    photos = db.relationship('Photo', back_populates='galleries')

    def __repr__(self):
        return f'<Gallery {self.id!r} name: {self.name!r}>'
