from hexagonal import app, Loan, db, User, DocumentCopy
from flask import request, render_template, redirect, session
import datetime
from hexagonal.auth.permissions import *
from hexagonal.ui.helpers import loading_list
from hexaongal import log


@app.route('/admin/loans')
@required_permission(Permission.manage)
def loans_index():
    """
    Loan index view.
    """

    return render_template('admin/loans/index.html', path='/admin/loans')


@app.route('/admin/loans/load')
@required_permission(Permission.manage)
def loan_index_load():
    """
    Endpoint for dynamic loading of loans.
    Returns rendered cards from item-list, but headless.
    """

    return render_template('components/item-list.html', type='loan', headless=True, items=loading_list(Loan.query))


@app.route('/admin/loans/requested')
@required_permission(Permission.manage)
def loans_requested_index():
    """
    Requested loan index view.
    """

    return render_template('admin/loans/index.html', path='/admin/loans/requested')


@app.route('/admin/loans/requested/load')
@required_permission(Permission.manage)
def loans_requested_loan():
    """
    Endpoint for dynamic loading of requested loans.
    Returns rendered cards from item-list, but headless.
    """

    return render_template('components/item-list.html', type='loan', headless=True,
                           items=loading_list(Loan.requested_loan_query()))


@app.route('/admin/loans/overdue')
@required_permission(Permission.manage)
def loans_overdue_index():
    """
    Overdue loan index view.
    """

    return render_template('admin/loans/index.html', loans=Loan.get_overdue_loans(), path='/admin/loans/overdue')


@app.route('/admin/loans/overdue/load')
def loans_overdue_load():
    """
    Endpoint for dynamic loading of overdue loans.
    Returns rendered cards from item-list, but headless.
    """

    return render_template('components/item-list.html', type='loan', headless=True,
                           items=loading_list(Loan.overdue_loan_query()))


@app.route('/admin/loans/returned')
@required_permission(Permission.manage)
def loans_returned_index():
    """
    Returned loan index view.
    """

    return render_template('admin/loans/index.html', loans=Loan.get_returned_loans(), path='/admin/loans/returned')


@app.route('/admin/loans/returned/load')
@required_permission(Permission.manage)
def loans_returned_load():
    """
    Endpoint for dynamic loading of returned loans.
    Returns rendered cards from item-list, but headless.
    """

    return render_template('components/item-list.html', type='loan', headless=True,
                           items=loading_list(Loan.returned_loan_query()))


@app.route('/admin/loans/<int:loan_id>/confirm')
@required_permission(Permission.manage)
def loan_confirm(loan_id):
    """
    Confirm the loan request by id.
    Changes the status to approved, and sets due_date to calculated date for user.
    """

    log(session['login'], 'confirmed', 'loan {}'.format(loan_id))

    loan = Loan.query.filter(Loan.id == loan_id).first()
    loan.status = Loan.Status.approved
    loan.due_date = datetime.date.today() + loan.user.get_checkout_period_for(loan.document_copy.document)
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/refuse')
@required_permission(Permission.manage)
def loan_refuse(loan_id):
    """
    Refuse the loan request by id.
    Deletes the loan from the db.
    """

    log(session['login'], 'confirmed', 'loan {}'.format(loan_id))

    loan = Loan.query.filter(Loan.id == loan_id).first()
    db.session.delete(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/return')
@required_permission(Permission.manage)
def loan_return(loan_id):
    """
    Confirm the returning of the loan by id.
    Deletes the loan from the db.
    """

    log(session['login'], 'confirmed return of', 'loan {}'.format(loan_id))

    loan = Loan.query.filter(Loan.id == loan_id).first()
    db.session.delete(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/forge')
@required_permission(Permission.manage)
def loan_forge():
    """
    Forge a loan. Not exposed function, mainly used for testing.
    Creates a loan with specified parameters without explicit request from a user.
    TODO: shall be removed in production
    """
    login = request.args.get('login', 'ionagamed')
    user = User.query.filter(User.login == login).first()
    copy_id = request.args['copy']
    user.checkout(DocumentCopy.query.filter(DocumentCopy.id == copy_id).first())
    return redirect(request.referrer)
