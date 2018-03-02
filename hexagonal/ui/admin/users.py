from hexagonal import app, User, auth, db
from flask import request, redirect, render_template
from hexagonal.auth.permissions import *
from hexagonal.ui.helpers import loading_list


@app.route('/admin/users')
@required_permission(Permission.manage)
def users_index():
    return render_template('admin/users/index.html', path='/admin/users')


@app.route('/admin/users/load')
@required_permission(Permission.manage)
def users_index_load():
    return render_template('components/item-list.html', type='user', headless=True, items=loading_list(User.query))


@app.route('/admin/users/new')
@required_permission(Permission.manage)
def users_new_view():
    return render_template('admin/users/new.html', path='/admin/users/new')


@app.route('/admin/users/new', methods=['POST'])
@required_permission(Permission.manage)
def users_new():
    auth.register_account(
        login=request.form['login'],
        password=request.form['password'],
        reset_password=False,  # TODO
        role=request.form['role'],
        name=request.form['name'],
        address=request.form['address'],
        phone=request.form['phone'],
        card_number=request.form['card_number']
    )

    return redirect('/admin/users')


@app.route('/admin/users/<int:user_id>/delete')
@required_permission(Permission.manage)
def users_delete(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/users/<int:user_id>/edit')
@required_permission(Permission.manage)
def users_edit_view(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    return render_template('admin/users/edit.html', user=user, path='/admin/users')


@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
@required_permission(Permission.manage)
def users_edit(user_id):
    if 'password' in request.form and len(request.form['password'].strip()) > 0:
        auth.change_password(user_id, request.form['password'])
    user = User.query.filter(User.id == user_id).first()
    user.login = request.form['login']
    user.role = request.form['role']
    user.name = request.form['name']
    user.address = request.form['address']
    user.phone = request.form['phone']
    user.card_number = request.form['card_number']

    db.session.add(user)
    db.session.commit()

    return redirect(request.referrer)


@app.route('/admin/users/<int:user_id>')
@required_permission(Permission.manage)
def users_view(user_id):
    user = User.query.filter(User.id == user_id).first_or_404()
    return render_template('admin/users/view.html', user=user)
