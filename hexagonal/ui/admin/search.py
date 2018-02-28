from hexagonal import app, Document, User
from hexagonal.auth.permissions import *
from flask import request, redirect, render_template


@app.route('/admin/search')
@required_permission(Permission.manage)
def search():
    fuzzy_term = None
    if 'search' in request.args:
        fuzzy_term = request.args['search']

    items = []

    searchable_classes = [Document, User]
    for cls in searchable_classes:
        items.extend(
            map(
                lambda x: (x, cls.__name__.lower()),
                cls.fuzzy_search(fuzzy_term)
            )
        )

    print('Found these items for term "{}":'.format(fuzzy_term))
    print(items)

    return render_template("admin/search.html", items=items, path='/admin/search')