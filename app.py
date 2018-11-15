from flask import Flask, render_template, session, redirect, url_for, flash, abort
from flask import Markup
from flask import request
import random
import os
import sqlite3
MyApp = Flask(__name__)
MyApp.secret_key = os.urandom(16)

con = sqlite3.connect('lab8.db')
cur = con.cursor()

def login_check(username, password):
	"""if username == 'chris@cfedun.com' and password == 'P@ssw0rd':
		return True"""
	cur.execute('SELECT * FROM users WHERE username == ? AND password == ?' , (username, password))
	e = cur.fetchall()
	if not e:
		return False
	return True

def session_user():
	return session['username']
	
def is_logged_in():
	return session.get('logged_in') == True
	
def err_func(err):
	err_code = str(err) + " "
	err_title = str(err) + " "
	err_msg = "Error!"
	if err == 418:
		err_title = err_title + "Teapot"
		err_code = err_code + "Teapot Error"
		err_msg = "I'm a teapot!"
	if err == 404:
		err_title = err_title + "Not Found"
		err_code = err_title
		err_msg = "The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
	if err == 403:
		err_title = err_title + "Forbidden"
		err_code = "Forbidden"
		err_msg = "You don't have the permission to access the requested resource. It is either read-protected or not readable by the server."
	return render_template('error.html', err_title=err_title, err_code=err_code, err_msg=err_msg, err=err), int(err)

"""def my_render(filename, home_current=False, login_current=False, about_current=False, contact_current=False, page2_current=False, page_title=""):
	if is_logged_in():
		return render_template(filename, home_current=home_current, login_current=login_current, about_current=about_current, contact_current=contact_current, page2_current=page2_current, page_title=page_title, is_logged_in=is_logged_in(), username=session_user())
	else:
		return render_template(filename, home_current=home_current, login_current=login_current, about_current=about_current, contact_current=contact_current, page2_current=page2_current, page_title=page_title, is_logged_in=is_logged_in())
"""

def my_render(filename, **kwargs):
	kargs = dict(kwargs)
	kargs['is_logged_in'] = is_logged_in()
	if is_logged_in():
		kargs['username'] = session_user()
	return render_template(filename, **(kargs))
	

@MyApp.route("/")
def main_page():
	return my_render('index.html', home_current=True)

@MyApp.errorhandler(418)
def teapot_error(error):
	return err_func(418)


@MyApp.route("/api/loginSubmit", methods=['POST'])
def login_submit():
	return None
	
@MyApp.route("/user/<username>")
def show_user_profile(username):
	#teapot for now
	abort(418)
	
@MyApp.route("/account/<username>")
def show_user_account(username):
	#teapot for now
	abort(418)
	
@MyApp.route("/login", methods=['GET', 'POST'])
def login_route():
	if is_logged_in():
		return redirect("/")
	if request.method == 'POST':
		un = request.form['username']
		password = request.form['password']
		#do db check
		
		if login_check(un, password):
			#do stuff
			session['username'] = un
			session['logged_in'] = True
			return redirect("/")
		else:
			flash("Username or password is incorrect!")
	
	return my_render('login.html', login_current=True)
	

@MyApp.route('/teapot')
def teapot():
	abort(418)


@MyApp.route("/page2")
def page2_page():
	if is_logged_in():
		return my_render('index.html', page2_current=True)
	else:
		r = random.randint(0,9999)
		r = r % 2
		if r == 1:
			abort(418)
		else:
			flash("You need to be logged in to view this page")
			return redirect("/")

@MyApp.route("/contact", methods=['GET', 'POST'])
def contact_page():
	kw = dict()
	kw['contact_current'] = True
	kw['page_title'] = "Contact"
	if request.method == 'POST':
		# do db stuff
		kw['contact_success'] = True
	return my_render('contact.html', **(kw))

@MyApp.route("/about")
def about_page():
	return my_render('about.html', about_current=True, page_title="About")

@MyApp.route("/api/getCurrentUser", methods=['GET', 'POST'])
def get_current_user():
		return session_user()
		
@MyApp.route('/logout')
def logout():
	# remove the username from the session if it's there
	session.pop('username', None)
	session['logged_in'] = False
	return redirect(url_for('index'))

if __name__ == "__main__":
	MyApp.run()
