from flask import Flask, render_template, flash, request, url_for, redirect, session
from flask_wtf import Form

from wtforms import StringField, PasswordField, BooleanField, validators
from wtforms.validators import DataRequired

from passlib.hash import sha256_crypt
from MySQLdb import escape_string as thwart

from content_management import Content
from dbconnect import connection

import gc


app = Flask(__name__)

if __name__ == '__main__':
    app = Flask(__name__)
    app.run(debug=True)

TOPIC_DICT = Content()


@app.route('/')
def index():
    try:
        return render_template('main.html')
    except Exception as e:
        flash(e)  # for debugging
        return render_template('login.html', error=error)


@app.route('/profile/')
def profile():
    flash("you're not logged in!")
    return render_template('profile.html', TOPIC_DICT=TOPIC_DICT)


@app.route('/grades/')
def grades():
    flash("you're not logged in!")
    return render_template('grades.html', TOPIC_DICT=TOPIC_DICT)


@app.route('/listening/')
def listening():
    flash("you're not logged in!")
    return render_template('/listening.html', TOPIC_DICT=TOPIC_DICT)


@app.route('/assignments/')
def assignments():
    flash("you're not logged in!")
    return render_template('/assignments.html', TOPIC_DICT=TOPIC_DICT)


@app.route('/self-assessment/')
def selfAssessment():
    flash("you're not logged in!")
    return render_template('/self-assessment.html', TOPIC_DICT=TOPIC_DICT)


@app.errorhandler(404)
def page_not_found():
    return render_template('/404.html')


@app.errorhandler(405)
def method_not_found():
    return render_template('405.html')


@app.route('/login/', methods=['GET', 'POST'])
def login_page():
    error = ''
    try:
        if request.method == "POST":
            attempted_username = request.form['username']
            attempted_password = request.form['password']

            #            flash(attempted_username)
            #            flash(attempted_password)

            if attempted_username == 'admin' and attempted_password == 'password':
                return redirect(url_for('profile'))
            else:
                error = 'Invalid credentials. Try again.'

        return render_template('login.html', error=error)

    except Exception as e:
        flash(e) #for debugging
        return render_template('login.html', error=error)


class RegistrationForm(Form):
    username = StringField('Username', [validators.Length(min=4, max=20)])
    email = StringField('Email Address', [validators.Length(min=6, max=50)])
    password = PasswordField('Password', [validators.DataRequired(), validators.EqualTo('confirm', message="Passwords must match")])
    confirm = PasswordField('Repeat Password')

    accept_tos = BooleanField('I accept the Terms of Service and the Privacy Notice.', [validators.DataRequired()])


@app.route('/register/', methods=['GET', 'POST'])
def register_page():
    try:
        form = RegistrationForm(request.form)

        if request.method == 'POST' and form.validate():
            username = form.username.data
            email = form.email.data
            password = sha256_crypt.encrypt((str(form.password.data)))
            c, conn = connection()

            x = c.execute('SELECT * FROM names WHERE name = (%s)',
                          (thwart(username)))

            if int(len(x)) > 0:
                flash('That name is already taken, please choose another.')
                return render_template('register.html', form=form)

            else:
                c.execute('INSERT INTO names (name, password, email, tracking) VALUES (%s, %s, %s, %s)',
                          (thwart(username), thwart(password), thwart(email), thwart('/introduction/')))

                conn.commit()
                flash('Thanks!')
                c.close()
                conn.close()
                gc.collect()

                session['logged_in'] = True
                session['username'] = username

                return redirect(url_for('dashboard'))

    except Exception as e:
        return str(e)
