from sqlalchemy import func, or_


class Searchable:
    fuzzy_search_fields = []
    fuzzy_array_search_fields = []

    @classmethod
    def _search_factory(cls, field):
        def actual_search(term):
            return cls._search_in_fields(term, [field])
        return actual_search

    @classmethod
    def _search_in_fields(cls, term, fields=None, array_fields=None):
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
        return cls._search_in_fields(term, cls.fuzzy_search_fields, cls.fuzzy_array_search_fields)

    def __getattr__(self, item):
        if item.startswith('search_by_'):
            return self._search_factory(item[len('search_by_'):])
        else:
            raise AttributeError
