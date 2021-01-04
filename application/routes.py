from .log import logger
import traceback
from flask import Flask, Blueprint
from flask import current_app as app
from flask_restplus import Api, Resource, fields
from sqlalchemy.orm.exc import NoResultFound
from . import db
from .models import Trader, Currency, Item, Trade, CurrentInventory, Offer, Price, CurrencyRate, Report, Country, CurrencyUsed

api = Api(version='1.0', title='my-investments-api')

blueprint = Blueprint('api', __name__, url_prefix='/api')

api.init_app(blueprint)
app.register_blueprint(blueprint)

ns_default = api.default_namespace
api.add_namespace(ns_default)

ns_trader = api.namespace('traders')
api.add_namespace(ns_trader)

ns_currency = api.namespace('currencies')
api.add_namespace(ns_currency)

ns_item = api.namespace('items')
api.add_namespace(ns_item)

ns_trade = api.namespace('trades')
api.add_namespace(ns_trade)

ns_current_inventory = api.namespace('current_inventories')
api.add_namespace(ns_current_inventory)

ns_offer = api.namespace('offers')
api.add_namespace(ns_offer)

ns_price = api.namespace('prices')
api.add_namespace(ns_price)

ns_currency_rate = api.namespace('currency_rates')
api.add_namespace(ns_currency_rate)

ns_report = api.namespace('reports')
api.add_namespace(ns_report)

ns_country = api.namespace('countries')
api.add_namespace(ns_country)

ns_currency_used = api.namespace('currencies_used')
api.add_namespace(ns_currency_used)

trader_fields = api.model('Trader', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True),
    'email': fields.String(required=True)
})

currency_fields = api.model('Currency', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True),
    'name': fields.String(required=True)
})

item_fields = api.model('Item', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True),
    'name': fields.String(required=True)
})

trade_fields = api.model('Trade', {
    'id': fields.Integer(readonly=True)
})

current_inventory_fields = api.model('CurrentInventory', {
    'id': fields.Integer(readonly=True)
})

offer_fields = api.model('Offer', {
    'id': fields.Integer(readonly=True)
})

price_fields = api.model('Price', {
    'id': fields.Integer(readonly=True)
})

currency_rate_fields = api.model('CurrencyRate', {
    'id': fields.Integer(readonly=True)
})

report_fields = api.model('Report', {
    'id': fields.Integer(readonly=True)
})

country_fields = api.model('Country', {
    'id': fields.Integer(readonly=True)
})

currency_used_fields = api.model('CurrencyUsed', {
    'id': fields.Integer(readonly=True)
})


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    logger.exception(message)
    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    logger.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404


@ns_default.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


@ns_trader.route('/')
class TraderCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(TraderCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(trader_fields)
    def get(self):
        return Trader.query.all()

    @api.expect(trader_fields)
    @api.marshal_with(trader_fields, code=201)
    def post(self):
        trader = Trader(
            first_name=api.payload['first_name'],
            last_name=api.payload['last_name'],
            email=api.payload['email']
        )
        db.session.add(trader)
        db.session.commit()

        return trader


@ns_trader.route('/<int:id>')
@api.response(404, 'Trader not found.')
class TraderItem(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(TraderItem, self).__init__(api, args, kwargs)

    @api.marshal_with(trader_fields)
    def get(self, id):
        return Trader.query.filter(Trader.id == id).one()


@ns_currency.route('/')
class CurrencyCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(CurrencyCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(currency_fields)
    def get(self):
        return Currency.query.all()

    @api.expect(currency_fields)
    @api.marshal_with(currency_fields, code=201)
    def post(self):
        currency = Currency(
            code=api.payload['code']
        )
        db.session.add(currency)
        db.session.commit()

        return currency


@ns_item.route('/')
class ItemCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(ItemCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(item_fields)
    def get(self):
        return Item.query.all()

    @api.expect(item_fields)
    @api.marshal_with(item_fields, code=201)
    def post(self):
        item = Item(
            code = api.payload['code'],
            name = api.payload['name']
        )
        db.session.add(item)
        db.session.commit()

        return item


@ns_trade.route('/')
class TradeCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(TradeCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(trade_fields)
    def get(self):
        return Trade.query.all()

    @api.expect(trade_fields)
    @api.marshal_with(trade_fields, code=201)
    def post(self):
        trade = Trade(
        )
        db.session.add(trade)
        db.session.commit()

        return trade


@ns_current_inventory.route('/')
class CurrentInventoryCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(CurrentInventoryCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(current_inventory_fields)
    def get(self):
        return CurrentInventory.query.all()

    @api.expect(current_inventory_fields)
    @api.marshal_with(current_inventory_fields, code=201)
    def post(self):
        current_inventory = CurrentInventory(
        )
        db.session.add(current_inventory)
        db.session.commit()

        return current_inventory


@ns_offer.route('/')
class OfferCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(OfferCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(offer_fields)
    def get(self):
        return Offer.query.all()

    @api.expect(offer_fields)
    @api.marshal_with(offer_fields, code=201)
    def post(self):
        offer = Offer(
        )
        db.session.add(offer)
        db.session.commit()

        return offer


@ns_price.route('/')
class PriceCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(PriceCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(price_fields)
    def get(self):
        return Price.query.all()

    @api.expect(price_fields)
    @api.marshal_with(price_fields, code=201)
    def post(self):
        price = Price(
        )
        db.session.add(price)
        db.session.commit()

        return price


@ns_currency_rate.route('/')
class CurrencyRateCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(CurrencyRateCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(currency_rate_fields)
    def get(self):
        return CurrencyRate.query.all()

    @api.expect(currency_rate_fields)
    @api.marshal_with(currency_rate_fields, code=201)
    def post(self):
        currency_rate = CurrencyRate(
        )
        db.session.add(currency_rate)
        db.session.commit()

        return currency_rate


@ns_report.route('/')
class ReportCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(ReportCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(report_fields)
    def get(self):
        return Report.query.all()

    @api.expect(report_fields)
    @api.marshal_with(report_fields, code=201)
    def post(self):
        report = Report(
        )
        db.session.add(report)
        db.session.commit()

        return report


@ns_country.route('/')
class CountryCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(CountryCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(country_fields)
    def get(self):
        return Country.query.all()

    @api.expect(country_fields)
    @api.marshal_with(country_fields, code=201)
    def post(self):
        country = Country(
        )
        db.session.add(country)
        db.session.commit()

        return country


@ns_currency_used.route('/')
class CurrencyUsedCollection(Resource):

    def __init__(self, api=None, *args, **kwargs):
        super(CurrencyUsedCollection, self).__init__(api, args, kwargs)

    @api.marshal_list_with(currency_used_fields)
    def get(self):
        return CurrencyUsed.query.all()

    @api.expect(currency_used_fields)
    @api.marshal_with(currency_used_fields, code=201)
    def post(self):
        currency_used = CurrencyUsed(
        )
        db.session.add(currency_used)
        db.session.commit()

        return currency_used

