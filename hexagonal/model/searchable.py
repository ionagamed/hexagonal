from sqlalchemy import func, or_


class Searchable:
    """
    Searchable base class.
    To add search functionality to the SQLAlchemy model class, just extend it from this class,
    and if you need fuzzy search specify `fuzzy_search_fields` and `fuzzy_array_search_fields`.

    E.g.:`
        class User(db.Model, Searchable):
            fuzzy_search_fields = ['name', 'role']
            fuzzy_array_search_fields = ['notes']
    `
    """

    fuzzy_search_fields = []
    fuzzy_array_search_fields = []

    @classmethod
    def _search_factory(cls, field):
        """
        Produce a function which searches the required field.
        (used later in __getattr__)

        :param field: field in which the search will occur.
        :return: searching function.
        """

        def actual_search(term):
            return cls._search_in_fields(term, [field])
        return actual_search

    @classmethod
    def _search_in_fields(cls, term, fields=None, array_fields=None):
        """
        Perform the actual search in specified fields.

        Search is performed using SQL ILIKE, and all array fields are joined using a comma (',').
        All clauses are OR'ed.
        E.g. `Searchable._search_in_fields('aba', ['title', 'description'], ['keywords'])`
        gives the following SQL:
        `SELECT * FROM whatever WHERE
            title ILIKE 'aba' OR
            description ILIKE 'aba' OR
            array_to_string(keywords, ",") ILIKE 'aba';`
        array_to_string is `sqlalchemy.func.array_to_string`.

        :param term: term to search for.
        :param fields: usual text fields to perform search in.
        :param array_fields: array fields to perform search in.
        :return: list of results.
        """

        if fields is None:
            fields = []
        if array_fields is None:
            array_fields = []
        filters = [
            getattr(cls, field).ilike('%' + term + '%') for field in fields
        ] + [
            func.array_to_string(getattr(cls, field), ',').ilike('%' + term + '%') for field in array_fields
        ]
        return cls.query.filter(or_(*filters)).all()

    @classmethod
    def fuzzy_search(cls, term):
        """
        Perform a search of the specified field through all defined fields.

        :param term: term to search for.
        :return: list of results.
        """
        return cls._search_in_fields(term, cls.fuzzy_search_fields, cls.fuzzy_array_search_fields)

    def __getattr__(self, item):
        if item.startswith('search_by_'):
            return self._search_factory(item[len('search_by_'):])
        else:
            raise AttributeError
