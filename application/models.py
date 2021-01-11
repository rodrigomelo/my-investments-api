from . import db


class Country(db.Model):
    # __tablename__ = 'country'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(2), index=True, unique=True, nullable=False)
    name = db.Column(db.String(128), index=True, unique=True, nullable=False)

    def __init__(self, code, name):
        self.code = code
        self.name = name


class Currency(db.Model):
    # __tablename__ = 'currency'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(8), index=True, unique=True, nullable=False) # e.g. iso code for currencies
    name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    is_active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    is_base_currency = db.Column(db.Boolean, index=False, unique=False, nullable=False)

    def __init__(self, code, name, is_active, is_base_currency):
        self.code = code
        self.name = name
        self.is_active = is_active
        self.is_base_currency = is_base_currency

# history rates between currencies (base currency and others)
class CurrencyRate(db.Model):
    # __tablename__ = 'currency_rate'

    id = db.Column(db.Integer, primary_key=True)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', backref='currency_rate', lazy=True, foreign_keys = [currency_id])
    base_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    base_currency = db.relationship('Currency', backref='base_currency_rate', lazy=True, foreign_keys = [base_currency_id])
    rate = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    ts = db.Column(db.DateTime, index=False, unique=False, nullable=False)


class CurrencyUsed(db.Model):
    # __tablename__ = 'currency_used'

    id = db.Column(db.Integer, primary_key=True)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref='currency_used', lazy=True, foreign_keys = [country_id])
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', backref='currency_used', lazy=True, foreign_keys = [currency_id])
    date_from = db.Column(db.Date, index=False, unique=False, nullable=False)
    date_to = db.Column(db.Date, index=False, unique=False, nullable=True)


class CurrentInventory(db.Model):
    # __tablename__ = 'current_inventory'

    id = db.Column(db.Integer, primary_key=True)
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'), index=True, unique=True, nullable=False)
    trader = db.relationship('Trader', backref='current_inventory', lazy=True, foreign_keys = [trader_id])
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), index=True, unique=True, nullable=False)
    item = db.relationship('Item', backref='current_inventory', lazy=True, foreign_keys = [item_id])
    quantity = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)


class Item(db.Model):
    # __tablename__ = 'item'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(64), index=True, unique=True, nullable=False)
    name = db.Column(db.String(255), index=False, unique=False, nullable=False)
    is_active = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', backref='item', lazy=True, foreign_keys = [currency_id])
    details = db.Column(db.Text, index=False, unique=False, nullable=True)


# list of all offers avaliable to buy/sell
class Offer(db.Model):
    # __tablename__ = 'offer'

    id = db.Column(db.Integer, primary_key=True)
    trader_id = db.Column(db.Integer, db.ForeignKey('trader.id'), index=True, unique=True, nullable=False)
    trader = db.relationship('Trader', backref='offer', lazy=True, foreign_keys = [trader_id])
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='offer', lazy=True, foreign_keys = [item_id])
    quantity = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    buy = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    sell = db.Column(db.Boolean, index=False, unique=False, nullable=False)
    price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    ts = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    is_active = db.Column(db.Boolean, index=False, unique=False, nullable=False)


# list of history prices (buy & sell)
class Price(db.Model):
    # __tablename__ = 'price'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='price', lazy=True, foreign_keys = [item_id])
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    currency = db.relationship('Currency', backref='price', lazy=True, foreign_keys = [currency_id])
    buy = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    sell = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    ts = db.Column(db.DateTime, index=False, unique=False, nullable=False)


class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    trading_date = db.Column(db.Date, index=True, unique=True, nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), index=True, unique=True, nullable=False)
    item = db.relationship('Item', backref='report', lazy=True, foreign_keys = [item_id])
    currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), index=True, unique=True, nullable=False)
    currency = db.relationship('Currency', backref='report', lazy=True, foreign_keys = [currency_id])
    first_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    last_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    min_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    max_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    avg_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    total_amount = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)
    quantity = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=True)


class Trade(db.Model):
    # __tablename__ = 'trade'

    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'), nullable=False)
    item = db.relationship('Item', backref='trade', lazy=True, foreign_keys = [item_id])
    buyer_id = db.Column(db.Integer, db.ForeignKey('trader.id'), index=True, unique=True, nullable=False)
    buyer = db.relationship('Trader', backref='trade_buyer', lazy=True, foreign_keys = [buyer_id])
    seller_id = db.Column(db.Integer, db.ForeignKey('trader.id'), index=True, unique=True, nullable=True)
    seller = db.relationship('Trader', backref='trade_seller', lazy=True, foreign_keys = [seller_id])
    quantity = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    unit_price = db.Column(db.Numeric(16,6), index=False, unique=False, nullable=False)
    description = db.Column(db.Text, index=False, unique=False, nullable=False)
    offer_id = db.Column(db.Integer, db.ForeignKey('offer.id'), nullable=False)
    offer = db.relationship('Offer', backref='trade', lazy=True, foreign_keys = [offer_id])


class Trader(db.Model):
    # __tablename__ = 'trader'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(64), index=False, unique=False, nullable=False)
    last_name = db.Column(db.String(64), index=False, unique=False, nullable=False)
    user_name = db.Column(db.String(64), index=True, unique=True, nullable=False)
    password = db.Column(db.String(64), index=False, unique=False, nullable=False)
    email = db.Column(db.String(128), index=True, unique=True, nullable=False)
    confirmation_code = db.Column(db.String(128), index=False, unique=False, nullable=False)
    time_registered = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    time_confirmed = db.Column(db.DateTime, index=False, unique=False, nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey('country.id'), nullable=False)
    country = db.relationship('Country', backref='trader', lazy=True, foreign_keys = [country_id])
    preferred_currency_id = db.Column(db.Integer, db.ForeignKey('currency.id'), nullable=False)
    preferred_currency = db.relationship('Currency', backref='trader', lazy=True, foreign_keys = [preferred_currency_id])

    def __repr__(self):
        return '<Trader user_name: {}>'.format(self.user_name)

