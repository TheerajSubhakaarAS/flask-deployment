import os
import random
from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_wtf.csrf import CSRFProtect
import hashlib

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

csrf = CSRFProtect(app)

def hash_text(text):
    return hashlib.sha256(text.encode('utf-8')).hexdigest()
# Fake user database (replace this with a proper user authentication mechanism)
users = {
    hash_text('user1'): hash_text('password1'),
    hash_text('user2'): hash_text('password2')
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    captcha = PasswordField('Captcha', validators=[InputRequired()])
    submit = SubmitField('Login')

@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = hash_text(form.username.data)
        password = hash_text(form.password.data)
        captcha_input = form.captcha.data

        # New logic: Allow login if captcha has exactly 5 characters
        if username in users and users[username] == password and len(captcha_input) == 5:
            flash('Login successful!', 'success')
            return redirect('/dashboard')
        else:
            flash('Invalid username, password, or captcha', 'error')
            return redirect('/')
    captcha_img = random_captcha_image()
    session['captcha_solution'] = captcha_img.split('.')[0]
    return render_template('login.html', form=form, captcha_img=captcha_img)

@app.route('/dashboard')
def dashboard():
    return render_template('cv.html', image_path='face_img/20211120_142611.jpg')

# Helper function to get a random captcha image
def random_captcha_image():
    captcha_images_folder = os.path.join(app.static_folder, 'captcha_images')
    captcha_images = os.listdir(captcha_images_folder)
    return random.choice(captcha_images)

if __name__ == '__main__':
    app.run(debug=True)
