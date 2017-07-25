#Enable the csrf prevention.
WTF_CSRF_ENABLED = True
SECRET_KEY = 'you-will-never-guess'

#defining the list of OpenId providers that we support
OPENID_PROVIDERS = [
    {'name': 'Google', 'url': 'https://www.google.com/accounts/o8/id'},
    {'name': 'Yahoo', 'url': 'https://me.yahoo.com'},
    {'name': 'AOL', 'url': 'http://openid.aol.com/<username>'},
    {'name': 'Flickr', 'url': 'http://www.flickr.com/<username>'},
    {'name': 'MyOpenID', 'url': 'https://www.myopenid.com'}]


#set up database details
import os
basedir =  os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir,'app.db') #path of our database file.
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir,'db_repository') #folder where we'll store the migrate data files.


#