from hexagonal import app, db, AVMaterial, JournalArticle
from flask import render_template, redirect, request
from hexagonal import Document, Book, DocumentCopy
from hexagonal.ui.helpers import comma_to_list, loading_list
from hexagonal.auth.permissions import required_permission, Permission


@app.route('/admin/documents')
@required_permission(Permission.manage)
def document_index():
    return render_template('admin/documents/index.html',
                           path='/admin/documents' + ('/search' if 'search' in request.args else ''))


@app.route('/admin/documents/load')
@required_permission(Permission.manage)
def document_index_load():
    return render_template('components/item-list.html', type='document', headless=True,
                           items=loading_list(Document.query))


@app.route('/admin/documents/<int:document_id>/delete')
@required_permission(Permission.manage)
def document_delete(document_id):
    doc = Document.query.filter(Document.id == document_id).first_or_404()
    db.session.delete(doc)
    db.session.commit()
    return redirect(request.referrer)


@app.route('/admin/documents/new', methods=['GET'])
@required_permission(Permission.manage)
def document_new_view():
    return render_template('admin/documents/new.html', path='/admin/documents/new')


@app.route('/admin/documents/new', methods=['POST'])
@required_permission(Permission.manage)
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
    elif t == 'av':
        doc = AVMaterial(
            title=request.form['title'],
            price=request.form['price'],
            keywords=comma_to_list(request.form['keywords']),
            authors=comma_to_list(request.form['authors'])
        )
    elif t == 'article':
        doc = JournalArticle(
            title=request.form['title'],
            price=request.form['price'],
            keywords=comma_to_list(request.form['keywords']),
            authors=comma_to_list(request.form['authors']),
            issue_editor=request.form['issue_editor'],
            issue_publication_date=request.form['issue_publication_date'],
            journal=request.form['journal']
        )

    for i in range(int(request.form['copies'])):
        dc = DocumentCopy(document=doc)

    db.session.add(doc)
    db.session.commit()

    # TODO
    return redirect('/admin/documents')


@app.route('/admin/documents/<int:document_id>/edit')
@required_permission(Permission.manage)
def document_edit_view(document_id):
    doc = Document.query.filter(Document.id == document_id).first_or_404()
    return render_template('admin/documents/edit.html', document=doc, path='/admin/documents')


@app.route('/admin/documents/<int:document_id>/edit', methods=['POST'])
@required_permission(Permission.manage)
def document_edit(document_id):
    doc = Document.query.filter(Document.id == document_id).first_or_404()
    doc.title = request.form['title']
    doc.price = request.form['price']
    doc.keywords = comma_to_list(request.form['keywords'])
    doc.authors = comma_to_list(request.form['authors'])
    try:
        copy_delta = int(request.form.get('copy_delta', 0))
    except:
        copy_delta = 0
    if copy_delta > 0:
        for _ in range(copy_delta):
            dc = DocumentCopy(document=doc)
    elif copy_delta < 0:
        if -copy_delta <= len(doc.get_available_copies()):
            dcs = DocumentCopy.query.filter(DocumentCopy.document == doc, DocumentCopy.loan == None).limit(
                -copy_delta).all()
            for dc in dcs:
                db.session.delete(dc)
            db.session.commit()
    if doc.type == 'book':
        doc.edition = request.form['edition']
        doc.publisher = request.form['publisher']
        doc.publishment_year = request.form['publishment_year']
        doc.bestseller = 'bestseller' in request.form

    db.session.add(doc)
    db.session.commit()

    return redirect(request.referrer)


@app.route('/admin/documents/<int:document_id>')
@required_permission(Permission.manage)
def document_view(document_id):
    doc = Document.query.filter(Document.id == document_id).first_or_404()
    return render_template('admin/documents/view.html', document=doc)
