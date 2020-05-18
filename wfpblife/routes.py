from flask import redirect, request, render_template, url_for, flash, session
from datetime import datetime
from wfpblife.forms import SignUpForm, LoginForm, IngredientsForm
from wfpblife import app, db


@app.route('/')
def index():
    # Get the recipe designated recipe of the week
    from wfpblife.recipe_of_the_week import rotw
    rotw = db.recipes.aggregate(rotw, allowDiskUse = False)

    # Get the five more recently published recipes
    from wfpblife.latest_recipes import latest_recipes
    recipes = db.recipes.aggregate(latest_recipes, allowDiskUse = True)

    from wfpblife.most_popular_recipe import mpr
    mpr = db.recipes.aggregate(mpr, allowDiskUse = False)

    return render_template('index.html', rotw=rotw, recipes=recipes, mpr=mpr)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    # Clear any previous flashed messages
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

    if form.validate_on_submit():
        # Clear any previous flashed messages
        session.pop('_flashes', None)
        
        email = form.email.data
        password = form.password.data
        user = db.users.find_one({'email': email})
        if user['password'] == password:
            session['email'] = email
            flash('You are now logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    if 'email' in session:
        session.pop('email')
        flash('Keep safe, see you again soon!', 'success')
        return redirect(url_for('index'))


@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    form = IngredientsForm()
    if 'email' in session:
        if request.method == 'POST':

            data = request.form.to_dict(flat=False)
            for quantity in data['quantity']:
                quantity = data['quantity']
                measurement = data['measurement']
                item = data['item']
            
            ingredients = []

            for i in range(len(quantity)):
                ingredients.append({
                    'quantity': quantity[i],
                    'measurement': measurement[i],
                    'item': item[i]
                })

            inserted_recipe = db.recipes.insert_one({
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'ingredients': ingredients
            }, {"w": "majority"})
            recipe = db.recipes.find_one({"_id": inserted_recipe.inserted_id})
            return render_template('recipe.html', recipe=recipe)
    else:
        flash('You need to be logged in to submit a recipe', 'warning')
        return redirect(url_for('login'))
    return render_template('submit_recipe.html', form=form)


@app.route('/recipe')
def get_recipe():
    title = request.args.get('title')
    recipe = db.recipes.find_one({'title': title})
    return render_template('recipe.html', recipe=recipe)


@app.route('/recipes')
def get_recipes():
    recipes = db.recipes.find({}).limit(10)
    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes2')
def get_recipes2():
    recipes = db.recipes.find({}).skip(10).limit(10)
    return render_template('recipes2.html', recipes=recipes)