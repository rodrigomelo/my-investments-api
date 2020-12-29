import logging
import traceback
from flask import Flask, Blueprint
from flask_restplus import Api, Resource, fields
from sqlalchemy.orm.exc import NoResultFound
from src import database
from src.database import db
from src.models import Trader

logging.basicConfig(level=logging.INFO)
handler = logging.FileHandler("my-investments-api.log")

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(handler)

app = Flask("my-investments-api")
app.config['RESTPLUS_VALIDATE'] = True
app.config['ERROR_404_HELP'] = False

database.config_db(app)

api = Api(version='1.0', title='my-investments-api')

blueprint = Blueprint('api', __name__, url_prefix='/api')

api.init_app(blueprint)
app.register_blueprint(blueprint)


@api.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    log.exception(message)
    return {'message': message}, 500


@api.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    log.warning(traceback.format_exc())
    return {'message': 'A database result was required but none was found.'}, 404


ns_default = api.default_namespace


@ns_default.route('/hello')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}


api.add_namespace(ns_default)

ns_trader = api.namespace('traders', description='Operations related to traders')

trader_fields = api.model('Trader', {
    'id': fields.Integer(readonly=True),
    'first_name': fields.String(required=True),
    'last_name': fields.String(required=True)
})


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
            last_name=api.payload['last_name']
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


api.add_namespace(ns_trader)
