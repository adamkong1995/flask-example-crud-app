from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class Asso_deal_to_im(Base):
    __tablename__ = "asso_deal_to_im"
    asso_id = db.Column(db.Integer, primary_key=True)
    deal_id = db.Column(db.Integer, db.ForeignKey('deal.deal_id'))
    im_id = db.Column(db.Integer, db.ForeignKey('investmentManager.im_id'))
    im_role = db.Column(db.String(32)) # {'main', 'support'}
    deal = db.relationship('Deal', back_populates='investmentManager')
    investmentManager = db.relationship('InvestmentManager', back_populates='deal')

    def __init__(self, im_role):
        self.im_role = im_role

    @classmethod
    def get_all_from_db(cls):
        return cls.query.all()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, deal_id):
        return cls.query.filter_by(deal_id=deal_id).first()

    @classmethod
    def find_main_im(cls):
        return cls.query.filter_by(im_role='main').all()