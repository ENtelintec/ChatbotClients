from flask import Flask
from flask_cors import CORS
from static.extensions import api
from templates.resources.resources_login import ns as ns_login
from templates.resources.resources_whatsapp import ns as ns_whatsapp

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/IA/api/v1/hello')
def hello_world():  # put application's code here
    return 'Hello World!'


api.init_app(app)
api.add_namespace(ns_login)
api.add_namespace(ns_whastapp)


if __name__ == '__main__':
    app.run()
