from hexagonal import app
from flask import render_template, redirect, request, session

from hexagonal import auth


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_view():
    if 'role' in session and session['role'] is not None:
        if session['role'] == 'librarian':
            return redirect('/admin/documents')
        else:
            return redirect('/user')
    return render_template('login.html', error=request.args.get('error', None))


@app.route('/login', methods=['POST'])
def login():
    login = request.form['login']
    password = request.form['password']

    try:
        token = auth.login_and_generate_token(login, password)
    except:
        return redirect('/login?error=Incorrect+username+or+password.')

    token_data = auth.decode_token(token)

    session.update(token_data)

    if session['role'] == 'librarian':
        return redirect('/admin/documents')
    else:
        return redirect('/user')


@app.route('/logout')
def logout():
    del session['login']
    del session['role']
    return redirect('/login')


from hexagonal.ui.admin import documents
from hexagonal.ui import filters
