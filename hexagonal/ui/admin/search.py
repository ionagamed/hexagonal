from hexagonal import app, Document, User
from hexagonal.auth.permissions import *
from flask import request, redirect, render_template, jsonify, session


def search():
    """
    Perform the actual search by fuzzy_term
    :return: list of matched items
    """

    fuzzy_term = None
    if 'search' in request.args:
        fuzzy_term = request.args['search']
        session['search'] = fuzzy_term

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

    return items


@app.route('/admin/search')
@required_permission(Permission.manage)
def search_view():
    """
    Main search page.
    """

    return render_template('admin/search.html', items=search(), path='/admin/search')


@app.route('/admin/search_inplace')
@required_permission(Permission.manage)
def search_inplace():
    """
    Dynamic function which renders only the item-list of the matched items for the search.
    """

    return render_template('components/item-list.html', items=search())


@app.route('/admin/json_search')
@required_permission(Permission.manage)
def json_search():
    """
    Search and return json-results.
    Used in semantic-ui search built-in.

    :return: json representation (fairly obvious from the code).
    """

    items = search()
    max_results = 5
    if 'max_results' in request.args:
        max_results = request.args['max_results']
    documents = [x[0] for x in items if isinstance(x[0], Document)][:max_results]
    users = [x[0] for x in items if isinstance(x[0], User)][:max_results]
    return jsonify({
        'results': {
            'documents': {
                'name': 'Documents',
                'results': [
                    {
                        'title': item.title,
                        'description': 'By {}<br>Keywords: {}'.format(', '.join(item.authors), ', '.join(item.keywords)),
                        'url': '/admin/documents/{}'.format(item.id)
                    } for item in documents
                ]
            },
            'users': {
                'name': 'Users',
                'results': [
                    {
                        'title': item.name,
                        'description': item.login,
                        'url': '/admin/users/{}'.format(item.id)
                    } for item in users
                ]
            }
        }
    })
