from hexagonal import app, User, Loan, db, Document, DocumentCopy
from flask import request, redirect, render_template, session


@app.route('/user/borrowed')
def user_borrowed_index():
    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.loan_query().all(), path='/user/borrowed', user=user)


@app.route('/user/borrowed/requests')
def user_requested_index():
    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_requested_loans(), path='/user/borrowed/requests', user=user)


@app.route('/user/borrowed/overdue')
def user_overdue_index():
    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_overdue_loans(), path='/user/borrowed/overdue', user=user)


@app.route('/user/borrowed/returned')
def user_returned_index():
    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_returned_loans(), path='/user/borrowed/returned', user=user)


@app.route('/user/borrowed/<int:loan_id>/return')
def user_return(loan_id):
    loan = Loan.query.filter(Loan.id == loan_id).first_or_404()
    loan.status = Loan.Status.returned
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/user/browse')
def user_browse_index():
    user = User.query.filter(User.login == session['login']).first()
    documents = map(
        lambda x: (x, Loan.query.with_transformation(Loan.document == x).count() > 0),
        Document.query.all()
    )
    return render_template('user/browse.html', documents=documents, path='/user/browse', user=user)


@app.route('/user/claim/<int:document_id>')
def user_claim(document_id):
    copy = DocumentCopy.query.filter(DocumentCopy.document_id == document_id, DocumentCopy.loan == None).first_or_404()
    user = User.query.filter(User.login == session['login']).first()
    user.checkout(copy)
    return redirect(request.referrer)

