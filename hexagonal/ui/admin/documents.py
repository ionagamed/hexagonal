from hexagonal import app, db
from flask import render_template, redirect, request
from hexagonal import Document, Book, DocumentCopy
from hexagonal.ui.helpers import comma_to_list


@app.route('/admin/documents')
# TODO: add guard
def document_index():
    documents = Document.query.all()

    return render_template('admin/documents/index.html',
                           documents=documents,
                           path='/admin/documents')


@app.route('/admin/documents/<int:document_id>/delete')
def document_delete(document_id):
    doc = Document.query.filter(Document.id == document_id).first_or_404()
    db.session.delete(doc)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/documents/new', methods=['GET'])
def document_new_view():
    return render_template('admin/documents/new.html', path='/admin/documents/new')


@app.route('/admin/documents/new', methods=['POST'])
def document_new():
    t = request.form['type']
    if t == 'book':
        doc = Book(
            title=request.form['title'],
            price=request.form['price'],
            keywords=comma_to_list(request.form['keywords']),
            authors=comma_to_list(request.form['authors']),
            edition=request.form['edition'],
            publisher=request.form['publisher'],
            publishment_year=request.form['publishment_year'],
            bestseller='bestseller' in request.form
        )

    for i in range(int(request.form['copies'])):
        dc = DocumentCopy(document=doc)

    db.session.add(doc)
    db.session.commit()

    # TODO
    return redirect('/admin/documents')
