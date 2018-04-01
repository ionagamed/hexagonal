"""
User routes
"""

from hexagonal import app, User, Loan, db, Document, DocumentCopy
from flask import request, redirect, render_template, session
from hexagonal.auth.permissions import *


@app.route('/user/borrowed')
@required_permission(Permission.checkout)
def user_borrowed_index():
    """
    Index of all loans which are in borrowed state for user.
    """

    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.loan_query().all(), path='/user/borrowed', user=user)


@app.route('/user/borrowed/requests')
@required_permission(Permission.checkout)
def user_requested_index():
    """
    Index of all loans which are in requested state for user.
    """

    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_requested_loans(), path='/user/borrowed/requests',
                           user=user)


@app.route('/user/borrowed/overdue')
@required_permission(Permission.checkout)
def user_overdue_index():
    """
    Index of all loans which are overdue for user.
    """

    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_overdue_loans(), path='/user/borrowed/overdue',
                           user=user)


@app.route('/user/borrowed/returned')
@required_permission(Permission.checkout)
def user_returned_index():
    """
    Index of all loans which are requested for return approval for user.
    """

    user = User.query.filter(User.login == session['login']).first()
    return render_template('user/borrowed.html', loans=user.get_returned_loans(), path='/user/borrowed/returned',
                           user=user)


@app.route('/user/borrowed/<int:loan_id>/return')
@required_permission(Permission.checkout)
def user_return(loan_id):
    """
    Request return approval for a loan by id.
    """

    loan = Loan.query.filter(Loan.id == loan_id).first_or_404()
    loan.status = Loan.Status.returned
    db.session.add(loan)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/user/browse')
@required_permission(Permission.checkout)
def user_browse_index():
    """
    Browse view for user.
    """

    user = User.query.filter(User.login == session['login']).first()
    documents = list(map(
        lambda x: (x, Loan.query.filter(Loan.document == x, Loan.user == user).count() > 0),
        Document.query.all()
    ))
    return render_template('user/browse.html', documents=documents, path='/user/browse', user=user)


@app.route('/user/claim/<int:document_id>')
@required_permission(Permission.checkout)
def user_claim(document_id):
    """
    Claim first available copy of the specified document.
    """

    copy = DocumentCopy.query.filter(DocumentCopy.document_id == document_id, DocumentCopy.loan == None).first_or_404()
    user = User.query.filter(User.login == session['login']).first()
    user.checkout(copy)
    return redirect(request.referrer)


@app.route('/user/enqueue/<int:document_id>')
@required_permission(Permission.checkout)
def user_enqueue(document_id):
    """
    Enqueue the document. Patron will get a notification when the copy is available.
    """

    from hexagonal import QueuedRequest

    user = User.query.filter(User.login == session['login']).first()
    document = Document.query.filter(Document.id == document_id).first()
    if not user or not document:
        return 'no such document or user', 404
    if document in user.queued_documents:
        return 'already queued to that doc', 403

    qr = QueuedRequest(
        patron=user,
        document=document
    )
    db.session.add(qr)
    db.session.commit()

    return redirect(request.referrer)


def update_qr_dates():
    from hexagonal import QueuedRequest
    import datetime

    qrs = QueuedRequest.query.all()
    for qr in qrs:
        if len(qr.document.available_copies) > 0:
            qr.resolve()
            db.session.add(qr)

    db.session.commit()

    qrs = QueuedRequest.query.all()

    for qr in qrs:
        if qr.resolved_at is not None and datetime.datetime.now() - qr.resolved_at > datetime.timedelta(days=1):
            db.session.delete(qr)

    db.session.commit()


@app.before_request
def user_notify():
    from hexagonal import QueuedRequest

    update_qr_dates()

    if 'uid' in session:
        session['qr_messages'] = []

        qrs = QueuedRequest.query.filter(QueuedRequest.patron_id == session['uid'], QueuedRequest.resolved_at != None).all()
        for qr in qrs:
            session['qr_messages'].append(
                'Document \'{}\' you requested is now available! <a href="/user/claim/{}">Claim</a> it now, you only have one '
                'day! '.format(qr.document.title, qr.document.id)
            )
