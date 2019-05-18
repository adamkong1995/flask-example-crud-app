from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class Deal_group(Base):
    __tablename__ = "deal_group"

    group_id = db.Column(db.Integer, primary_key=True)
    group_name = db.Column(db.String(128), nullable=False)

    def __init__(self, group_name):
        self.group_name = group_name

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_from_db(cls):
        return cls.query.order_by(cls.group_name).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(group_id=_id).first()

    @classmethod
    def find_by_group_name(cls, _name):
        return cls.query.filter_by(group_name=_name).first()
