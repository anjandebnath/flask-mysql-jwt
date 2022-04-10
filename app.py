from flask import Flask, request, jsonify, make_response, render_template, session, send_from_directory
import jwt
from datetime import datetime, timedelta
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec_webframeworks.flask import FlaskPlugin
from marshmallow import Schema, fields

# Since we are using swagger/open api standard RESTFUL JSON response so include this template folder
app = Flask(__name__, template_folder='swagger/templates')

# JWT token authorization signature
app.config['SECRET_KEY'] = '\xee[\xdc\x15\x88\xe8\xdf\xac\x85\xb4\x87\x16'
# SQLAlchemy MYSQL connector
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:rootadmin@localhost/vrbo'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)



###Model####
class Product(db.Model):

    __tablename__ = "property"
    id = db.Column(db.Integer, primary_key=True)
    propertyTitle = db.Column(db.String(20))
    propertyDescription = db.Column(db.String(100))
    propertyBrand = db.Column(db.String(20))
    propertyPrice = db.Column(db.Integer)

    def create(self):
      db.session.add(self)
      db.session.commit()
      return self

    def __init__(self, propertyTitle, propertyDescription, propertyBrand, propertyPrice):
        self.propertyTitle = propertyTitle
        self.propertyDescription = propertyDescription
        self.propertyBrand = propertyBrand
        self.propertyPrice = propertyPrice

    def __repr__(self):
        return '<Property %r>' % self.propertyTitle


# configure APIspecification
# with open api, to get api response
spec = APISpec(
    title='flask-api-swagger-doc',
    version='1.0.0',
    openapi_version='3.0.2',
    plugins=[FlaskPlugin()]
)


# when we call this url
# the open api response will be returned
@app.route('/api/swagger.json')
def create_swagger_spec():
    return jsonify(spec.to_dict())


# in the open api response the "paths"
# contain the apis that will be configured through Marshmallow Schema

# Here we will define an api which will respond list of Properties
class VrboPropertyResponseSchema(Schema):
    id = fields.Int()
    propertyTitle = fields.Str()
    propertyDescription = fields.Str()
    propertyBrand = fields.Str()
    propertyPrice = fields.Int()



# define the actual api response
@app.route('/property', methods= ['GET'])
def properties():
    """Get List of Properties
       ---
       get:
           description: Get List of Properties
           responses:
                 200:
                    description: Return a Property list
                    content:
                        application/json:
                            schema: VrboPropertyResponseSchema

    """
    properties = Product.query.all()
    # for p in properties:
    #    print("title:"+p.propertyTitle+", price:"+str(p.propertyPrice))
    properties_schema = VrboPropertyResponseSchema(many=True)
    products = properties_schema.dump(properties)
    return make_response(jsonify({"product": products}))



with app.test_request_context():
    spec.path(view=properties)



# A decorator is a function that
# 1. takes a function to be wrapped as its only parameter and
# 2. returns a wrapping function
def token_required(func):

    # When you are using a decorator, you are replacing wrapped function with wrapping function signature.
    #
    # functools.wraps() helps to keep the signature of the wrapped function i.e: _name_, __doc__
    # instead of wrapping function.

    @wraps(func) # functools.wraps() keeps the signature of the wrapped function.
    def decorated(*args, **kwargs): # it takes positional arguments and keyword arguments
        token = request/args.get('token')
        if not token:
            return jsonify({'Alert!':'Token is missing!'})
        try:
            payload = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'Alert': 'Invalid Token!'})

    return decorated


# Next, we use the route decorator to help define which
# routes should be navigated to the following function.

# Home
@app.route('/')
def home():
    # if user is not loggedin then redirect or render a page called login else loggedin currently
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # return 'Logged in currently!'
        return render_template('login.html')

# Public
@app.route('/public')
def public():
    return 'For Public'


# Authenticated decorator
@app.route('/auth')
@token_required
def auth():
    return 'JWT is verified. Welcome to your dashboard!'



@app.route('/login', methods=['POST'])
def login():
    if request.form['username'] and request.form['password'] == '123456':
        session['logged_in'] = True # set this List index True
        # create a JWT token with the combination of username + expiry time + SERVER_SECRET_KEY
        token = jwt.encode({
            'user':request.form['username'],
            'expiration': str(datetime.utcnow() + timedelta(seconds=120)) # expired in 2 min
        },app.config['SECRET_KEY'])

        return jsonify({'token': token})
    else:
        return make_response('Unable to verify', 403, {'WWW-Authenticate' : 'Basic realm: "Authentication Failed!"'})


@app.route('/docs')
@app.route('/docs/<path:path>')
def swagger_docs(path=None):
    if not path or path == 'index.html':
        return render_template('index.html', base_url='/docs')

    else:
        return send_from_directory('./swagger/static', path)


if __name__ == "__main__":
    app.run(debug=True)