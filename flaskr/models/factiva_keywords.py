from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class factiva_keywords(Base):
    __tablename__ = "factiva_keyword"

    keyword_id = db.Column(db.Integer, primary_key=True)
    keyword = db.Column(db.String(256), nullable=False)
    im_id = db.Column(db.Integer, db.ForeignKey('investmentManager.im_id'), nullable=False)
    im = db.relationship('InvestmentManager')

    def __init__(self, keyword, im_id):
        self.keyword = keyword
        self.im_id = im_id
    
    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_from_db(cls):
        return cls.query.order_by(cls.keyword).all()

    @classmethod
    def find_by_id(cls, keyword_id):
        return cls.query.filter_by(keyword_id=keyword_id).first()
