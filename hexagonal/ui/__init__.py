from hexagonal import app
from flask import render_template, redirect, request, session

from hexagonal import auth, User


@app.route('/')
def index():
    return redirect('/login')


@app.route('/login', methods=['GET'])
def login_view():
    if 'role' in session and session['role'] is not None:
        if session['role'] == 'librarian' or session['role'] == 'admin':
            return redirect('/admin/documents')
        else:
            return redirect('/user/borrowed')
    return render_template('login.html')


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

    user = User.query.filter(User.login == session['login']).first()
    if user.reset_password:
        return redirect('/reset_password')

    session['uid'] = user.id

    if session['role'] == 'librarian' or session['role'] == 'admin':
        return redirect('/admin/documents')
    else:
        return redirect('/user/borrowed')


@app.route('/reset_password')
def reset_password_view():
    return render_template('reset_password.html')


@app.route('/reset_password', methods=['POST'])
def reset_password():
    password = request.form['password'].strip()
    confirm = request.form['confirm'].strip()
    if password != confirm:
        return redirect('/reset_password?error=Passwords+do+not+match.')
    auth.change_password(session['login'], password)
    return redirect(request.referrer)


@app.route('/logout')
def logout():
    del session['login']
    del session['role']
    del session['qr_messages']
    return redirect('/login')


from hexagonal.ui.admin import documents, users, loans, search
from hexagonal.ui import filters, user
