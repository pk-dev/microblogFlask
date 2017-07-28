from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config.from_object('config') #use our config file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app) #initialize our db



import os
from flask_login import LoginManager  #flask_login will handle users' logged in state.
from flask_openid import OpenID  #flask_openid will provide openid authentication.
from config import basedir
lm=LoginManager()
lm.init_app(app)
lm.login_view='login'
oid=OpenID(app,os.path.join(basedir,'tmp')) # openid requires a path to a folder where files can be stored



from app import views, models