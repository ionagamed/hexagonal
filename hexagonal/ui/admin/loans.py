from hexagonal import app, Loan, db, User, DocumentCopy
from flask import request, render_template, redirect
import datetime
from hexagonal.auth.permissions import *


@app.route('/admin/loans')
@required_permission(Permission.manage)
def loans_index():
    return render_template('admin/loans/index.html',  path='/admin/loans')


@app.route('/admin/loans/load')
@required_permission(Permission.manage)
def loan_index_load():
    limit = int(request.args.get('limit', 20))
    if 'skip' in request.args:
        items = Loan.query.offset(request.args['skip']).limit(limit)
    else:
        items = Loan.query.limit(limit).all()
    return render_template('components/item-list.html', type='loan', headless=True, items=items)


@app.route('/admin/loans/requested')
@required_permission(Permission.manage)
def loans_requested_index():
    return render_template('admin/loans/index.html', loans=Loan.get_requested_loans(), path='/admin/loans/requested')


@app.route('/admin/loans/overdue')
@required_permission(Permission.manage)
def loans_overdue_index():
    return render_template('admin/loans/index.html', loans=Loan.get_overdue_loans(), path='/admin/loans/overdue')


@app.route('/admin/loans/returned')
@required_permission(Permission.manage)
def loans_returned_index():
    return render_template('admin/loans/index.html', loans=Loan.get_returned_loans(), path='/admin/loans/returned')


@app.route('/admin/loans/<int:loan_id>/confirm')
@required_permission(Permission.manage)
def loan_confirm(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    loan.status = Loan.Status.approved
    loan.due_date = datetime.date.today() + loan.user.get_checkout_period_for(loan.document_copy.document)
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/refuse')
@required_permission(Permission.manage)
def loan_refuse(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    loan.status = Loan.Status.approved
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/return')
@required_permission(Permission.manage)
def loan_return(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    db.session.delete(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/forge')
@required_permission(Permission.manage)
def loan_forge():
    login = request.args.get('login', 'ionagamed')
    user = User.query.filter(User.login == login).first()
    copy_id = request.args['copy']
    user.checkout(DocumentCopy.query.filter(DocumentCopy.id == copy_id).first())
    return redirect(request.referrer)


