from flask import Flask, render_template, url_for, redirect, flash, request
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from app import app, db, models
from .forms import LoginForm, RegisterForm, mealDealForm, changePasswordForm
from flask_bcrypt import Bcrypt
import json

bcrypt = Bcrypt(app)

login_manager = LoginManager() # Allow our app and login manager to work together
login_manager.init_app(app)  
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = models.User.query.filter_by(username=form.username.data).first() # Check to see that username exists
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data): # Check the hashed password with the database
                login_user(user)
                return redirect(url_for('home'))
            else:
                flash('Incorrect Username or Password.')
        else:
            flash('Incorrect Username or Password.')
    return render_template('login-register.html', form=form, title="Login")


def getLikes(meal):
    return meal.likes

@app.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    meals = models.Meal.query.all()
    
    # Order by likes
    meals.sort(key=getLikes, reverse=True)
    return render_template('home.html',
                            meals=meals,
                            user=current_user,
                            title='Home')

@app.route('/explore', methods=['GET', 'POST'])
@login_required
def explore():
    meals = models.Meal.query.all()
    meals.reverse() # show most recently added meal deals first
    return render_template('explore.html',
                            meals=meals,
                            user=current_user,
                            title='Explore')

@app.route('/userMeals', methods=['GET', 'POST'])
@login_required
def userMeals():
    return render_template('usermeals.html',
                            user=current_user,
                            title= current_user.username + "'s" + ' meals')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        used_name = models.User.query.filter_by(username=form.username.data).first() # Check to see that username exists
        if used_name:
            flash("This username has been taken, please choose another one.") # If the username is taken flash this message
            return render_template('login-register.html', form=form, title="Register")

        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = models.User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('login-register.html', form=form, title="Register")

@app.route('/addMealDeal', methods=['GET', 'POST'])
@login_required
def addMealDeal():
    form = mealDealForm()
    if form.validate_on_submit():
        # Format the entries
        Main = form.main.data.title().strip()
        Snack = form.snack.data.title().strip()
        Drink = form.drink.data.title().strip()
        Name = form.name.data.title().strip()
        Description = form.description.data

        # Test to see if the name matches any names in the database
        existingName = models.Meal.query.filter_by(name=Name).first()
        if existingName:
            flash("This name is taken, please enter a different one...")
        else:
            # Add the meal to the database
            newMeal = models.Meal(main=Main, snack=Snack, drink=Drink, name=Name, description=Description, likes=0)
            current_user.meals.append(newMeal) # Add the meal to users meals
            db.session.add(newMeal)
            db.session.commit()
            return redirect(url_for('explore'))
    return render_template('addmealdeal.html', 
                            form=form,
                            title="Add a meal deal")

# Route that allows users to save posts.
@app.route('/saveMealDeal', methods=['GET', 'POST'])
@login_required
def saveMealDeal():
    # Load the JSON data and use the id
    data = json.loads(request.data)
    meal_id = int(data.get('MealId'))
    chosenMeal = models.Meal.query.get(meal_id)
    userMeals = current_user.meals

    # Check to see if the user has already saved the meal
    for Meal in userMeals:
        if(Meal.id == chosenMeal.id):
            return json.dumps({'status':'OK', 'likes':chosenMeal.likes, 'saved':True })

    current_user.meals.append(chosenMeal) # Add the meal to the users's meals
    chosenMeal.likes += 1 # Increment the meals likes
    db.session.commit()
    return json.dumps({'status':'OK', 'likes':chosenMeal.likes, 'saved':False })

# Route that allows users to remove posts from their collection.
@app.route('/removeMealDeal/<int:meal_id>', methods=['GET','POST'])
@login_required
def removeMealDeal(meal_id):
    chosenMeal = models.Meal.query.filter_by(id=meal_id).first()
    print(current_user.meals, chosenMeal)

    current_user.meals.remove(chosenMeal)
    if(chosenMeal.likes != 0):
        chosenMeal.likes -= 1 # Decrement the meals likes
    db.session.commit()
    return redirect(url_for('userMeals'))

# Route for the setting page
@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    form = changePasswordForm()

    # User's can change password
    if form.validate_on_submit():
        if bcrypt.check_password_hash(current_user.password, form.oldPassword.data): # Check the hashed password with the database
            # Change the password
            newPassword = bcrypt.generate_password_hash(form.newPassword.data)
            current_user.password = newPassword
            db.session.commit()
            flash('Successfully Changed Password.')
        else :
            flash('Incorrect password')

    return render_template('settings.html',
                            form=form,
                            title='Settings')