from flask import request


def comma_to_list(s):
    """
    Convert a comma-separated string to a list of the respective stripped values.

    :param s: string of comma-separated values.
    :return: the list of respective stripped values.
    """

    return list(map(lambda x: x.strip(), s.split(',')))


def loading_list(query):
    """
    Limit and skip the query from request GET parameters.

    :param query: the query to be limited and skipped.
    :return: list of paged items.
    """

    limit = int(request.args.get('limit', 20))
    if 'skip' in request.args:
        items = query.offset(request.args['skip']).limit(limit).all()
    else:
        items = query.limit(limit).all()

    return items
