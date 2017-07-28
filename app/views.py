from flask import render_template, flash, redirect, session, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from app import app, db, lm, oid
from .forms import LoginForm
from .models import User


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user # {'nickname': 'Priya'}  # fake user

    posts = [  # fake array of posts
              {
                'author': {'nickname': 'John'},
                'body': 'Beautiful day in Portland!'
              },
             {
                'author': {'nickname': 'Susan'},
                'body': 'The Avengers movie was so cool!'
             }
         ]
    return render_template("index.html",
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/login', methods=['GET','POST'])
@oid.loginhandler # tells Flask-Openid that this is our login view function.
def login():
    if g.user is not None and g.user.is_authenticated:
        return redirect(url_for('index'))
    #Note: g is a global setup by Flask as a place to store and
    # share data during the life of a request.

    form=LoginForm()
    if form.validate_on_submit():
        session['remember_me']=form.remember_me.data
        return oid.try_login(form.openId.data, ask_for=['nickname','email'])

        '''print("validated true")
        flash('Login requested for OpenID="%s", remember_me="%s"'%(form.openId.data,str(form.remember_me.data)))
        return redirect('/index')

    print("validated false")'''

    return render_template('login.html', title='Sign In', form=form,
                           providers=app.config['OPENID_PROVIDERS'])

@oid.after_login #flask-openid will call the function with this decorator if authentication is successful.
def after_login(resp): # resp is the response from openid provider.
    #validation
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))

    # search in our database for the email provided
    user=User.query.filter_by(email=resp.email).first()
    if user is None: # if not founbd, add this user to our db.
        nickname=resp.nickname
        if nickname is None or nickname == "":
            nickname=resp.email.split('@')[0]
        user=User(nickname=nickname,email=resp.email)
        db.session.add(user)
        db.session.commit()

    # load remember_me value from flask session
    remember_me=False
    if 'remember_me' in session:
        remember_me=session['remember_me']
        session.pop('remember_me',None)

    # register this as a valid login
    login_user(user,remember=remember_me)
    # redirect to next page provided by request or to index page.
    return redirect(request.args.get('next') or url_for('index'))



@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request # will run before the view function each time a request is received.
def before_request():
    g.user=current_user # the current_user global is set by Flask-Login.


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))