from . import db


class Trader(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=False, unique=False, nullable=False)
    last_name = db.Column(db.String(64), index=False, unique=False, nullable=False)
    # user_name = db.Column(db.String(64), index=False, unique=True, nullable=False)
    # password = db.Column(db.String(64), index=False, unique=False, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=True)
    # confirmation_code = db.Column(db.String(128), index=False, unique=False, nullable=False)
    # time_registered = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    # time_confirmed = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    # country_id = db.Column(db.Integer, index=False, unique=False, nullable=False)
    # preferred_currency_id = db.Column(db.Integer, index=False, unique=False, nullable=False)

    def __repr__(self):
        return '<Trader first_name: {}>'.format(self.first_name)


class Currency(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), index=True, unique=True, nullable=True)
    name = db.Column(db.String(64), index=False, unique=False, nullable=True)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(255), index=False, unique=False, nullable=False)
    trades = db.relationship('Trade', backref='item', lazy=True)


class Trade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)


class CurrentInventory(db.Model):
    # __tablename__ = 'current_inventory'

    id = db.Column(db.Integer, primary_key=True)
    trader_id_id = db.Column(db.Integer, db.ForeignKey('trader.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    quantity = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Price(db.Model):
    # __tablename__ = 'currency_rate'

    id = db.Column(db.Integer, primary_key=True)


class CurrencyRate(db.Model):
    # __tablename__ = 'currency_rate'

    id = db.Column(db.Integer, primary_key=True)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class Country(db.Model):
    id = db.Column(db.Integer, primary_key=True)


class CurrencyUsed(db.Model):
    # __tablename__ = 'currency_used'

    id = db.Column(db.Integer, primary_key=True)
