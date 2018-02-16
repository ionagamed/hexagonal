def ids(collection):
    """
    Transform collection of objects into collection of their ids.

    :param collection: collection of objects
    :return: list of their respective ids
    """

    if not isinstance(collection, list):
        raise TypeError('list expected')
    return map(lambda x: x.id, collection)
