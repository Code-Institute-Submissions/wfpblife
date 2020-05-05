from flask import redirect, request, render_template, url_for, flash, session
from wfpblife.forms import SignUpForm, LoginForm
from wfpblife import app, db


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    session.pop('_flashes', None)

    if form.validate_on_submit():

        # Check whether either the email or username already exists
        username_exists = db.users.find_one({"username": form.username.data})
        email_exists = db.users.find_one({"email": form.email.data})
        if username_exists is None or email_exists is None:
            
            # Email exists condition
            if username_exists is None and email_exists:
                flash('An account with that email already exists', 'warning')

            # Username exists condition
            elif email_exists is None and username_exists:
                flash('Sorry! That username is already taken, try another.', 'warning')

            # Neither username nor email exist, sign up the user with the details entered in the form
            else:
                db.users.insert_one({
                "username": form.username.data,
                "email": form.email.data,
                "password": form.password.data
            })

                # Successful account creation message
                flash(f'Account created for {form.username.data}!', 'success')
                return redirect(url_for('index'))

        # Both username and email exist condition
        else:
            flash('That email already exists', 'warning')
    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    session.pop('_flashes', None)

    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash(f'You are now logged in', 'success')
            return redirect(url_for('index'))
        else:
            if request.form['submit'] == 'login':
                flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)