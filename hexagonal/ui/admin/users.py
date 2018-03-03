from hexagonal import app, User, auth, db
from flask import request, redirect, render_template
from hexagonal.auth.permissions import *
from hexagonal.ui.helpers import loading_list


@app.route('/admin/users')
@required_permission(Permission.manage)
def users_index():
    """
    User index view.
    """

    return render_template('admin/users/index.html', path='/admin/users')


@app.route('/admin/users/load')
@required_permission(Permission.manage)
def users_index_load():
    """
    Endpoint for dynamic loading of users.
    Returns rendered cards from item-list, but rendered.
    """

    return render_template('components/item-list.html', type='user', headless=True, items=loading_list(User.query))


@app.route('/admin/users/new')
@required_permission(Permission.manage)
def users_new_view():
    """
    View for new user form.
    """

    return render_template('admin/users/new.html', path='/admin/users/new')


@app.route('/admin/users/new', methods=['POST'])
@required_permission(Permission.manage)
def users_new():
    """
    Create a new user from form parameters.
    Actually registers a new account.
    """

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
    """
    Delete a user by id.
    """

    user = User.query.filter(User.id == user_id).first_or_404()
    db.session.delete(user)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/users/<int:user_id>/edit')
@required_permission(Permission.manage)
def users_edit_view(user_id):
    """
    Edit view for a user by id.
    """

    user = User.query.filter(User.id == user_id).first_or_404()
    return render_template('admin/users/edit.html', user=user, path='/admin/users')


@app.route('/admin/users/<int:user_id>/edit', methods=['POST'])
@required_permission(Permission.manage)
def users_edit(user_id):
    """
    Actually update the user from the form parameters.
    If password changes (if it is present and non-empty in form), then set reset_password of user to True).
    """

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
    """
    Detail view of a user.
    """

    user = User.query.filter(User.id == user_id).first_or_404()
    return render_template('admin/users/view.html', user=user)
