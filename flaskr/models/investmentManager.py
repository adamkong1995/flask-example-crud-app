from flaskr.services.flask_sqlalchemy import db
from flaskr.models.base import Base


class InvestmentManager(Base):
    __tablename__ = "investmentManager"

    im_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    display_name = db.Column(db.String(256))
    dn = db.Column(db.String(128))
    email = db.Column(db.String(128))
    member_of = db.Column(db.String(512))
    isActive = db.Column(db.Boolean, default=True)
    authenticated = db.Column(db.Boolean, default=False)
    deal = db.relationship('Asso_deal_to_im', back_populates='investmentManager')

    def __init__(self, name, dn):
        self.name = name
        self.dn = dn

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def is_active(self):
        """True, as all users are active."""
        return True

    def get_id(self):
        """Return the email address to satisfy Flask-Login's requirements."""
        return self.dn

    def is_authenticated(self):
        """Return True if the user is authenticated."""
        return self.authenticated

    def is_anonymous(self):
        """False, as anonymous users aren't supported."""
        return False

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def get_all_from_db(cls):
        return cls.query.order_by(cls.name).all()

    @classmethod
    def get_all_active(cls):
        return cls.query.filter_by(isActive=True).order_by(cls.name).all()

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(im_id=_id).first()

    @classmethod
    def find_by_dn(cls, _dn):
        return cls.query.filter_by(dn=_dn).first()
