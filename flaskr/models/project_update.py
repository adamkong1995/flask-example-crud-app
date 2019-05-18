from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class Project_update(Base):
    __tablename__ = "project_update"

    update_id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.deal_id'))
    deal = db.relationship("Deal")
    update_content = db.Column(db.String(2048), nullable=False)
    isSent = db.Column(db.String(1))

    def __init__(self, deal_id, update_content, isSent):
        self.deal_id = deal_id
        self.update_content = update_content
        self.isSent = isSent

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_from_db(cls):
        return cls.query.all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(update_id=_id).first()

    @classmethod
    def find_by_deal_id(cls, _id):
        return cls.query.filter_by(deal_id=_id).first()
