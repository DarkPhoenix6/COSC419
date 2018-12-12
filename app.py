from flask import Flask, render_template, session, redirect, url_for, flash, abort
from flask import Markup
from flask import request
import random
import os
import sqlite3
MyApp = Flask(__name__)
MyApp.secret_key = os.urandom(16)


def to_dict(keys, items):
    """

    :param keys:
    :param items:
    :return:
    """
    k = {}  # temp dict
    l = []  # list to hold tuples
    m = []  # list to hold dictionaries

    def to_dict_list_gen(it):
        """

        :param it:
        :return:
        """
        c = len(keys) if len(keys) <= len(it) else len(it)
        # for i, j in keys, it:
            # yield (i, j)
        for i in range(c):
            yield (keys[i], it[i])

    if isinstance(items, list) or isinstance(items, tuple):
        if isinstance(items[0], tuple) or isinstance(items[0], list):
            l = [[(u, v) for u, v in to_dict_list_gen(i)] for i in items]  # [[list of tuple key:value pairs]]
            m = [dict(tup) for tup in l]
            return m
        else:
            l = [(u, v) for u, v in to_dict_list_gen(items)]
            m = [dict(l)]
            return m


def login_check(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    """if username == 'chris@cfedun.com' and password == 'P@ssw0rd':
        return True"""
    with sqlite3.connect('lab8.db') as con:
        cur = con.cursor()
        cur.execute('SELECT * FROM users WHERE username == ? AND password == ?', (username, password))
        e = cur.fetchall()
        if not e:
            return False
        return True


def get_email(username):
    """

    :param username:
    :return:
    """
    with sqlite3.connect('lab8.db') as con:
        cur = con.cursor()
        cur.execute('SELECT email FROM users WHERE username == ?', (username,))
        e = cur.fetchone()
        e = e[0]
        return e


def get_current_datetime():
    """

    :return:
    """
    with sqlite3.connect('lab8.db') as con:
        cur = con.cursor()
        cur.execute("SELECT strftime('%Y-%m-%dT%H:%M:%fZ','now')")
        return cur.fetchone()


def session_user():
    """

    :return:
    """
    return session['username']


def is_logged_in():
    """

    :return:
    """
    return session.get('logged_in') == True


def get_countries():
    """
    gets available countries for an option list in a form as injectable HTML code
    :return:
    """
    from countries import my_countries
    #for i in range(len(my_countries)):
        #my_countries[i] = Markup(my_countries[i])
    #return my_countries
    country = ['<option value="CA">Canada</option>', '<option value="US">United States of America</option>']
    for i in range(len(country)):
        country[i] = Markup(country[i])
    return country


def get_cart(username):
    """
    gets the cart of the specified user
    :param username:
    :return:
    """
    m = "%s %s %s %s" % (
        "SELECT * FROM cart", "JOIN (SELECT id AS uid, username, email FROM users) AS u ON (cart.user_id = u.uid)",
        "JOIN (SELECT id AS iid, product_upc, product_name, cost, product_description FROM items) AS i ON (cart.item_id = i.iid)",
        "WHERE item_id != 0 AND user_id = (SELECT id FROM users WHERE username == ?)")
    with sqlite3.connect('lab8.db') as con:
        cur = con.cursor()
        cur.execute(m, (username,))
        e = [('id', 'user_id', 'item_id', 'quantity', 'promo_id', 'created_time', 'modified_time', 'uid', 'username',
              'email', 'iid', 'product_upc', 'product_name', 'cost', 'product_description')] + cur.fetchall()
        #MyApp.logger.warning(e)
        if len(e) > 1:
            f = to_dict(e[0], e[1:])
            #MyApp.logger.warning(f)
            e = f
        else:
            e = None
        return e


def err_func(err):
    """

    :param err:
    :return:
    """
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


useless_sql_code = """
SELECT * FROM cart
                join (SELECT id AS uid, username, email from users) AS u on (cart.user_id = u.uid)
                join (SELECT id AS iid, product_upc, product_name, cost, product_description FROM items) AS i on (cart.item_id = i.iid)
                join (SELECT id AS cid, value, value_type, code_name, start_date, end_date FROM promo_codes) AS code on (cart.promo_id = code.cid);

SELECT * FROM cart
                join (SELECT id AS uid, username, email from users) AS u on (cart.user_id = u.uid)
                join (SELECT id AS iid, product_upc, product_name, cost, product_description FROM items) AS i on (cart.item_id = i.iid)
                WHERE item_id != 0;

SELECT * FROM cart
                join (SELECT id AS uid, username, email from users) AS u on (cart.user_id = u.uid)
                join (SELECT id AS cid, value, value_type, code_name, start_date, end_date FROM promo_codes) AS code on (cart.promo_id = code.cid)
                WHERE item_id == 0;
"""


def my_render(filename, **kwargs):
    """
    a render_template wrapper function
    :param filename:
    :param kwargs:
    :return:
    """
    kargs = dict(kwargs)
    kargs['is_logged_in'] = is_logged_in()
    if is_logged_in():
        kargs['username'] = session_user()
    return render_template(filename, **(kargs))


@MyApp.route("/")
def main_page():
    """

    :return:
    """
    return my_render('index.html', home_current=True, page_title='Homepage')


@MyApp.errorhandler(418)
def teapot_error(error):
    """
    Teapot Error
    :param error:
    :return:
    """
    return err_func(418)


@MyApp.route("/api/loginSubmit", methods=['POST'])
def login_submit():
    return None


@MyApp.route("/user/<username>")
def show_user_profile(username):
    #teapot for now
    abort(418)


@MyApp.route("/account/<username>/checkout")
def show_user_checkout(username):
    """

    :param username:
    :return:
    """
    if not is_logged_in() or username != session_user():
        abort(403)
    cart=None
    promo_codes=None
    email = get_email(session_user());
    country = ['<option value="CA">Canada</option>', '<option value="US">United States of America</option>']
    for i in range(len(country)):
        country[i] = Markup(country[i])
    cart = get_cart(username)
    subtotals = []
    total = 0
    if cart is not None:
        """for i in cart:
            total = total + i['quantity'] * i['cost']
        """
        for i in range(len(cart)):
            subtotals.append(cart[i]['quantity'] * cart[i]['cost'])
            total = total + cart[i]['quantity'] * cart[i]['cost']
            cart[i]['cost'] = format(cart[i]['cost'], '.2f')
        total = format(total, '.2f')
    return my_render('checkout.html', login_current=True, page_title='Checkout', cart=cart, promo_codes=promo_codes,
                     email=email, countries=country, total=total)


@MyApp.route("/account/<username>/cart")
def show_user_cart(username):
    if not is_logged_in() or username != session_user():
        abort(403)
    cart = None
    promo_codes = None
    email = get_email(session_user())
    cart = get_cart(username)
    subtotals = []
    total = 0
    if cart is not None:
        """for i in cart:
            total = total + i['quantity'] * i['cost']
        """
        for i in range(len(cart)):
            subtotals.append(cart[i]['quantity'] * cart[i]['cost'])
            total = total + cart[i]['quantity'] * cart[i]['cost']
            cart[i]['cost'] = format(cart[i]['cost'], '.2f')
        total = format(total, '.2f')
    return my_render('cart.html', login_current=True, page_title='Cart', cart=cart, promo_codes=promo_codes,
                     email=email, total=total, subtotals=subtotals)


@MyApp.route("/account/<username>")
def show_user_account(username):
    #teapot for now
    abort(418)


@MyApp.route("/login", methods=['GET', 'POST'])
def login_route():
    """

    :return:
    """
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
        return my_render('index.html', page2_current=True, page_title='Page2')
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
    return redirect('/')


if __name__ == "__main__":
    MyApp.run()

