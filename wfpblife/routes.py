import os

from bson.son import SON
from datetime import datetime
from flask import flash, redirect, request, render_template, session, url_for
from wfpblife.forms import LoginForm, RecipeForm, SignUpForm
from wfpblife import app, bcrypt, cloudinary, db


@app.errorhandler(404)
def page_not_found(e):
    # 404 status set explicitly
    return render_template('404.html'), 404


@app.route('/', methods=['GET', 'POST'])
def index():
    
    # Get the recipe designated recipe of the week
    from wfpblife.recipe_of_the_week import rotw
    rotw = db.recipes.aggregate(rotw, allowDiskUse = False)

    # Get the search term and redirect to provide user feedback in the URL
    if request.method == 'POST':
        search_term = request.form.get('recipe')
        search_term = search_term.lower()
        return redirect(url_for('search', search_term=search_term))

    # Get the five most recently published recipes
    username_lookup = user_lookup()
    searched_recipes = db.recipes.find({}).sort('date_added', -1).limit(5)
    results = populate_recipes(username_lookup, searched_recipes)

    mpr = popular_recipes(1)

    return render_template('index.html', rotw=rotw, recipes=results, mpr=mpr)


@app.route('/search', methods=['GET', 'POST'])
def search():

    # Clear any previous flashed messages
    session.pop('_flashes', None)

    search_term = request.args['search_term']
    search_term = search_term.lower()
    username_lookup = user_lookup()

    if search_term:
        # If user enters a search term, search the database
        searched_recipes = db.recipes.find({ "$or": [ { "title": { "$regex": search_term } }, { "description": { "$regex": search_term } }, { "ingredients": { "$regex": search_term } } ] })
    else:
        # Display response if user fails to enter search term
        searched_recipes = []
        flash('Please enter a search term', 'warning')


    # Filter the search results by author
    recipes = []
    results = []

    filtered_recipes = []

    for lookup in username_lookup:
        for recipe in searched_recipes:
            recipes.append(recipe['_id'])
        for recipe in recipes:
            if lookup['_id'] == recipe:
                results.append(lookup)
    
    authors = filter(results)

    # Filter the search results
    # Recipes need to be reacquired for filtering purposes
    searched_recipes = db.recipes.find({"$or": [{"title": {"$regex": search_term}}, {
                                       "description": {"$regex": search_term}}, {"ingredients": {"$regex": search_term}}]})

    total = db.recipes.find()

    select = None # To prevent reference before assignment error

    # If the user enters another search term into the field
    if request.method == 'POST':
        if 'search' in request.form:
            search_term = request.form.get('recipe')
            return redirect(url_for('search', search_term=search_term))

    # Prevent filtering if search term field is empty
    if search_term:
        # Filter only when the Apply Filter button is clicked
        if 'filter' in request.form:
            select = request.form.get('author_select')

            for result in results:
                if result['username']  == select:
                    filtered_recipes.append(result)
            return render_template('search.html', authors=authors, filtered_recipes=filtered_recipes, recipes=results, search_term=search_term)

        elif 'search' in request.form:
            search_term = request.form.get('recipe')
            return redirect(url_for('search', search_term=search_term))
     
    return render_template('search.html', authors=authors, filtered_recipes=filtered_recipes, recipes=results, search_term=search_term)


@app.route('/search/filter')
def filter(results):
    authors = []
    for result in results:
        authors.append(result['username'])
    return authors


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        # Clear any previous flashed messages
        session.pop('_flashes', None)

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
                "password": password,
                "login_count": 0
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

        # Check if the user is in the database
        user = db.users.find_one({'email': email})

        if user:
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

            file = None
            # Get the file and upload to cloudinary
            if form.validate_on_submit():
                file = request.files['file']
                if file:

                    # If the user uploads an image force the image size to 2000 * 1000 focussing at the centre
                    image = cloudinary.uploader.upload(file, upload_preset='wfpblife')

                    # Use the remote upload facility to create a resized version of the uploaded image (360 x 270)
                    image_small = cloudinary.uploader.upload(
                        image['url'], upload_preset='bnpfces4')
                else:
                    # If no image provided by user, use a default image
                    image = cloudinary.uploader.upload('https://res.cloudinary.com/bogtrotter72/image/upload/v1590854650/wfpblife/qiyk0brqjrht5vh0dt7d.jpg', upload_preset='wfpblife')
                    image_small = cloudinary.uploader.upload(
                        image['url'], upload_preset='bnpfces4')

            # Get the user
            user = db.users.find_one({"email": session['email']})

            # Retrieve the ingredients from the form
            data = request.form.to_dict(flat=False)

            
            # Create empty lists to store ingredients and cooking method
            ingredients = []
            instructions = [] # Changed from method to avoid potential naming conflict

            populate_recipe(data, ingredients, instructions)

            if form.validate_on_submit():

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
        flash('You must be logged in to submit a recipe', 'danger')
        return redirect(url_for('login'))

    return render_template('submit_recipe.html', form=form)


@app.route('/recipe', methods=['GET', 'POST'])
def get_recipe():

    # Set initial conditions
    user = None
    owner = False
    comments = []

    # Find the recipe
    title = request.args.get('title')
    recipe = db.recipes.find_one({'title': title})

    username_lookup = user_lookup()
    searched_recipes = db.recipes.find({'title': title})

    results = populate_recipes(username_lookup, searched_recipes)

    for result in results:
        username = result['username']

    if 'email' in session:
        user = db.users.find_one({"email": session['email']})
        if recipe:
            # Check if the session user is the recipe owner
            if user['_id'] == recipe['user_id']:
                owner = True
            else:
                owner = False

    # Get the all comments and aggregate the author's username
    from wfpblife.recipe_comments import recipe_comments
    comments_aggregate = db.recipes.aggregate(
        recipe_comments, allowDiskUse=False)

    # Select only those comments that are relevant to this recipe and append to the empty comments list
    for comment in comments_aggregate:
        if recipe:
            if recipe['_id'] == comment['_id']:
                comments.append(comment)
        else:
            return render_template('404.html')
    
    if request.method == 'POST':
        # Editing an existing comment
        if 'edit' in request.form:
            old_title = request.form.get('old-comment-title')
            new_title = request.form.get('comment-title')

            old_content = request.form.get('old-comment-content')
            new_content = request.form.get('comment-content')

            # Find the exacting matching comment and update it
            db.recipes.update_one({"comments": {"$elemMatch": { "title": old_title, "content": old_content }}}, {"$set": {"comments.$": { "title": new_title, "content": new_content, "date": datetime.utcnow(), "user_id": user['_id']}}})

        # Deleting an existing comment
        if 'delete' in request.form:
            comment_title = request.form.get('comment-title')
            comment_content = request.form.get('comment-content')

            db.recipes.update_one({"title": title}, {"$pull": {"comments": { "title": comment_title, "content": comment_content }}})
        
        # Submitting a new comment
        if 'submit' in request.form:
            comment_title = request.form.get('comment-title')
            comment_content = request.form.get('comment-content')

            db.recipes.update_one( {"title": title }, {"$push": {"comments": { "title": comment_title, "content": comment_content, "date": datetime.utcnow(), "user_id": user['_id'] }}} )

        title = title
        recipe = db.recipes.find({'title': title})
        return redirect(url_for('get_recipe', recipe=recipe, username=username, title=title, owner=owner, user=user, comments=comments))

    
    return render_template('recipe.html', recipe=recipe, username=username, owner=owner, user=user, comments=comments)


@app.route('/recipes')
def get_recipes():
    username_lookup = user_lookup()
    searched_recipes = db.recipes.find({}).sort('title', 1).limit(10)

    results = populate_recipes(username_lookup, searched_recipes)
    return render_template('recipes.html', recipes=results)


@app.route('/recipes2')
def get_recipes2():
    username_lookup = user_lookup()
    searched_recipes = db.recipes.find({}).sort('title', 1).skip(10).limit(10)

    results = populate_recipes(username_lookup, searched_recipes)
    return render_template('recipes2.html', recipes=results)


@app.route('/edit_recipe/<title>', methods=['GET', 'POST'])
def edit_recipe(title):
    if 'email' in session:
        user = db.users.find_one({"email": session['email']})
    
    recipe = db.recipes.find_one({'title': title})

    # Check if the session user is the recipe owner
    if user['_id'] == recipe['user_id']:
        owner = True
    else:
        owner = False
        # Security feature - 'should' not happen
        flash('You may only edit your own recipes', 'danger')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
            # Retrieve the ingredients form the form
            data = request.form.to_dict(flat=False)
            
            # # Create empty lists to store ingredients and cooking method
            ingredients = []
            instructions = [] # Changed from method to avoid potential naming conflict

            populate_recipe(data, ingredients, instructions)

            # Insert the recipe into the database
            db.recipes.update({"title": title}, {
                
                # Using set to prevent overwriting elements not required here
                "$set": {
                    'user_id': user['_id'],
                    'prep_time': int(request.form.get('prep_time')), # Cast returned value to Int32
                    'cook_time': int(request.form.get('cook_time')), # Cast returned value to Int32
                    'date_added': datetime.utcnow(),
                    'servings': int(request.form.get('servings')), # Cast returned value to Int32
                    'title': request.form.get('title'),
                    'description': request.form.get('description'),
                    'ingredients': ingredients,
                    'method': instructions
                }
            })

            # Reacquire the recipe
            recipe = db.recipes.find_one({'_id': recipe['_id']})
            title = recipe['title']

            # Display it for the user to review
            return redirect(url_for('get_recipe', owner=owner, title=title, recipe=recipe))

    return render_template('edit_recipe.html', owner=owner, recipe=recipe)


@app.route('/delete_recipe/<title>')
def delete_recipe(title):

    # Additional failsafe to prevent recipe deletion from other user
    if 'email' in session:
        user = db.users.find_one({"email": session['email']})
    
    recipe = db.recipes.find_one({'title': title})

    # Check if the session user is the recipe owner
    if not user['_id'] == recipe['user_id']:
        flash('You may only delete your own recipes', 'danger')
        return redirect(url_for('index'))

    db.recipes.delete_one({'title': title})
    return redirect(url_for('account'))


@app.route('/account', methods=['GET', 'POST'])
def account():
    if request.method == 'POST':
        if 'edit' in request.form:
            db.users.update_one({"email": session['email']}, {"$set": {
                "username": request.form.get('username'),
                "email": request.form.get('email')
            }})
            # Get the user
            session['email'] = request.form.get('email')
            user = db.users.find_one({"email": session['email']})

        if 'delete' in request.form:
            db.users.delete_one({"email": session['email']})
            session.pop('email')
            return redirect(url_for('index'))

    # Restrict access to this route to logged in users
    if 'email' in session:
        # Get the user
        user = db.users.find_one({"email": session['email']})

        username_lookup = user_lookup()
        searched_recipes = db.recipes.find({"user_id": user['_id']})

    results = populate_recipes(username_lookup, searched_recipes)
        
    if 'delete' in request.form:
        print(user)

    return render_template('account.html', user=user, recipes=results)


def populate_recipe(data, ingredients, instructions):
    for quantity in data['quantity']:
        quantity = data['quantity']
        measurement = data['measurement']
        item = data['item']

    # Retrieve the method steps from the form            
    for method in data['method']:
        method = data['method']

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

    return ingredients, instructions



def user_lookup():
    recipes = db.recipes.aggregate([
        {
            u"$match": {}
        }, 
        {
            u"$lookup": {
                u"from": u"users",
                u"let": {
                    u"id": u"$user_id"
                },
                u"pipeline": [
                    {
                        u"$match": {
                            u"$expr": {
                                u"$eq": [
                                    u"$_id",
                                    u"$$id"
                                ]
                            }
                        }
                    }
                ],
                u"as": u"user"
            }
        }, 
        {
            u"$unwind": {
                u"path": u"$user",
                u"preserveNullAndEmptyArrays": False
            }
        }, 
        {
            u"$addFields": {
                u"username": u"$user.username"
            }
        }, 
        {
            u"$project": {
                u"user": 0.0
            }
        }
    ])
    return recipes


def populate_recipes(username_lookup, searched_recipes):
    recipes = []
    results = []

    for lookup in username_lookup:
        for recipe in searched_recipes:
            recipes.append(recipe['_id'])
        for recipe in recipes:
            if lookup['_id'] == recipe:
                results.append(lookup)

    results.sort(key=lambda item: item.get('title'))
    return results


def popular_recipes(limit):
    recipes = db.recipes.aggregate([
        {
            u"$addFields": {
                u"ratings_total": {
                    u"$sum": u"$ratings.value"
                }
            }
        },
        {
            u"$sort": SON([(u"ratings_total", -1)])
        },
        {
            u"$limit": limit
        }
    ])
    return recipes