import os

from flask import redirect, request, render_template, url_for, flash, session
from flask_paginate import Pagination, get_page_parameter
from datetime import datetime
from wfpblife.forms import SignUpForm, LoginForm, RecipeForm
from wfpblife import app, db, cloudinary, bcrypt

from cloudinary import CloudinaryImage



@app.route('/', methods=['GET', 'POST'])
def index():
    # Get the recipe designated recipe of the week
    from wfpblife.recipe_of_the_week import rotw
    rotw = db.recipes.aggregate(rotw, allowDiskUse = False)

    # Get the search term and redirect to provide user feedback in the URL
    if request.method == 'POST':
        search_term = request.form.get('recipe')
        return redirect(url_for('search', search_term=search_term))

    # Get the five more recently published recipes
    from wfpblife.latest_recipes import latest_recipes
    recipes = db.recipes.aggregate(latest_recipes, allowDiskUse = False)

    # Get the most popular recipe
    from wfpblife.most_popular_recipe import mpr
    mpr = db.recipes.aggregate(mpr, allowDiskUse = False)

    return render_template('index.html', rotw=rotw, recipes=recipes, mpr=mpr)


@app.route('/search')
def search():
    search_term = request.args['search_term']
    searched_recipes = db.recipes.find({ "$or": [ { "title": { "$regex": search_term } }, { "description": { "$regex": search_term } }, { "ingredients": { "$regex": search_term } } ] })
    return render_template('search.html', recipes=searched_recipes)
    


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

                # Password protection
                password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

                db.users.insert_one({
                "username": form.username.data,
                "email": form.email.data,
                "password": password
            })
                # Successful account creation message
                flash('Account successfully created, you can now login!', 'success')

                # Redirect to allow the user to login
                return redirect(url_for('login'))

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
        user = db.users.find_one({'email': email})
        remember = form.remember_me.data
        password = bcrypt.check_password_hash(user['password'], form.password.data)

        if password:
            # Use the user's email as the session object to avoid confusion
            session['email'] = email

            # Update the user login_count for query 'most active user'
            db.users.update_one({'email': email}, {"$inc": {'login_count': 1} })

            flash('You are now logged in', 'success')
            return redirect(url_for('index'))

        # If the login details do not match any user in the database
        else:
            flash('Login unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    # Although logout should not be available as an option without a user being logged in, carry out a failsafe check
    if 'email' in session:
        session.pop('email')
        flash('Keep safe, see you again soon!', 'success')
        return redirect(url_for('index'))


@app.route('/submit_recipe', methods=['GET', 'POST'])
def submit_recipe():
    form = RecipeForm()

    # Restrict access to this route to logged in users
    if 'email' in session:
        if request.method == 'POST':

            # Get the file and upload to cloudinary
            file = request.files['file']
            image = cloudinary.uploader.upload(file, responsive_breakpoints={
                "create_derived": True, "bytes_step": 20000, "min_width": 200, "max_width": 1000}, transformation=[{'width': 1200, 'height': 500, 'gravity': 'auto', 'crop': 'fill'}])

            # Use the remote upload facility to create a resized version of the uploaded image (360 x 270)
            image_small = cloudinary.uploader.upload(
                image['url'], upload_preset='bnpfces4')

            # Get the user
            user = db.users.find_one({"email": session['email']})

            # Retrieve the ingredients form the form
            data = request.form.to_dict(flat=False)
            for quantity in data['quantity']:
                quantity = data['quantity']
                measurement = data['measurement']
                item = data['item']

            # Retrieve the method steps from the form            
            for method in data['method']:
                method = data['method']
            
            # Create empty lists to store ingredients and cooking method
            ingredients = []
            instructions = [] # Changed from method to avoid potential naming conflict

            # Pass values to the ingredients list
            for i in range(len(quantity)):
                ingredients.append({
                    'quantity': quantity[i],
                    'measurement': measurement[i],
                    'item': item[i]
                })
            
            # Pass values to the instructions list
            for j in range(len(method)):
                instructions.append({
                    'step': j+1.0,
                    'text': method[j]
                })

            # Insert the recipe into the database
            inserted_recipe = db.recipes.insert_one({
                'user_id': user['_id'],
                'prep_time': int(request.form.get('prep_time')), # Cast returned value to Int32
                'cook_time': int(request.form.get('cook_time')), # Cast returned value to Int32
                'date_added': datetime.utcnow(),
                'servings': int(request.form.get('servings')), # Cast returned value to Int32
                'title': request.form.get('title'),
                'description': request.form.get('description'),
                'image': image['url'],
                'image_small': image_small['url'],
                'ingredients': ingredients,
                'method': instructions
            }, {"w": "majority"})

            recipe = db.recipes.find_one({"_id": inserted_recipe.inserted_id})
            return render_template('recipe.html', recipe=recipe)
    else:
        flash('You need to be logged in to submit a recipe', 'warning')
        return redirect(url_for('login'))
    return render_template('submit_recipe.html', form=form)


@app.route('/recipe', methods=['GET', 'POST'])
def get_recipe():
    title = request.args.get('title')
    recipe = db.recipes.find_one({'title': title})
    
    return render_template('recipe.html', recipe=recipe)


@app.route('/recipes')
def get_recipes():

    # Get 10 recipes
    from wfpblife.recipes_user_lookup import user_lookup
    recipes = db.recipes.aggregate(user_lookup, allowDiskUse = False)


    return render_template('recipes.html', recipes=recipes)


@app.route('/recipes2')
def get_recipes2():
    recipes = db.recipes.find({}).skip(10).limit(10)
    return render_template('recipes2.html', recipes=recipes)


@app.route('/account')
def account():
    # Restrict access to this route to logged in users
    if 'email' in session:
        # Get the user
        user = db.users.find_one({"email": session['email']})

        recipes = db.recipes.find({"user_id": user['_id']})

    return render_template('account.html', user=user, recipes=recipes)
