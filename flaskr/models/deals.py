from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class Deal(Base):
    __tablename__ = "deal"

    deal_id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('deal_group.group_id'))
    deal_group = db.relationship("Deal_group")
    investmentManager = db.relationship("Asso_deal_to_im", back_populates='deal')
    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256))
    dealSize = db.Column(db.Float)
    status = db.Column(db.String(32), nullable=False)
    startDate = db.Column(db.DateTime)
    exitDate = db.Column(db.DateTime)

    def __init__(self, group_id, name, description, dealSize, status, startDate, exitDate):
        self.group_id = group_id
        self.name = name
        self.description = description
        self.dealSize = dealSize
        self.status = status
        self.startDate = startDate
        self.exitDate = exitDate

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
    def find_by_id(cls, deal_id):
        return cls.query.filter_by(deal_id=deal_id).first()
