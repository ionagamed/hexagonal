from flask import request


def comma_to_list(s):
    return list(map(lambda x: x.strip(), s.split(',')))


def loading_list(query):
    limit = int(request.args.get('limit', 20))
    if 'skip' in request.args:
        items = query.offset(request.args['skip']).limit(limit).all()
    else:
        items = query.limit(limit).all()

    return items
