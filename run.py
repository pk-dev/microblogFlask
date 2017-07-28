#!flask/bin/python
from app import app
app.run(debug=True)

#a script that starts up the development web server with our application.
#second line imports app variable from our app package.
#third line invoke the run method of app
