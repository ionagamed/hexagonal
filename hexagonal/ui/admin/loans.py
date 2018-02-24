from hexagonal import app, Loan, db, User, DocumentCopy
from flask import request, render_template, redirect
import datetime


@app.route('/admin/loans')
def loans_index():
    return render_template('admin/loans/index.html', loans=Loan.query.all(), path='/admin/loans')


@app.route('/admin/loans/requested')
def loans_requested_index():
    return render_template('admin/loans/index.html', loans=Loan.get_requested_loans(), path='/admin/loans/requested')


@app.route('/admin/loans/overdue')
def loans_overdue_index():
    return render_template('admin/loans/index.html', loans=Loan.get_overdue_loans(), path='/admin/loans/overdue')


@app.route('/admin/loans/returned')
def loans_returned_index():
    return render_template('admin/loans/index.html', loans=Loan.get_returned_loans(), path='/admin/loans/returned')


@app.route('/admin/loans/<int:loan_id>/confirm')
def loan_confirm(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    loan.status = Loan.Status.approved
    loan.due_date = datetime.date.today() + loan.user.get_checkout_period_for(loan.document_copy.document)
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/refuse')
def loan_refuse(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    loan.status = Loan.Status.approved
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/<int:loan_id>/return')
def loan_return(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first()
    db.session.delete(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/loans/forge')
def loan_forge():
    login = request.args.get('login', 'ionagamed')
    user = User.query.filter(User.login == login).first()
    copy_id = request.args['copy']
    user.checkout(DocumentCopy.query.filter(DocumentCopy.id == copy_id).first())
    return redirect(request.referrer)


