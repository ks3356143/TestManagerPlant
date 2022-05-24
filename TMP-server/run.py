# -*- coding:utf-8 -*-
from flask import Flask
from apis.user import app_user
from apis.product import app_product
from apis.apps import app_application
from apis.testmanager import test_manager
from apis.dashboard import dashboard_test
from flask_cors import CORS

app = Flask(__name__)
CORS(app, supports_credentials=True) #解决跨域请求
app.register_blueprint(app_user)
app.register_blueprint(app_product)
app.register_blueprint(app_application)
app.register_blueprint(test_manager)
app.register_blueprint(dashboard_test)

@app.route("/api/hello")
def hello():
    return "Hello,World!"

if __name__ == "__main__":
    app.run(debug=True)
    