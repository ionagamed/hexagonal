"""
Contains a `bind_crud` helpers to bind classes to jsonrpc with CRUD operations
"""


from hexagonal.jsonrpc import bind
from hexagonal import db


CRUD_ALLOWED_METHODS = ['create', 'get', 'update', 'delete']
"""
Allowed methods for the methods param of the `bind_crud` function
"""


def bind_crud(class_name=None, methods=None, crud_namespace='crud', generate_by_id_methods=True):
    """
    Bind all CRUD operations for the decorated class.

    Function names are formed by appending
    the lowercase class name + '.' + crud_namespace + '.' (if crud_namespace is not None (default 'crud')) +
    method name, where method name could be any of ['get', 'update', 'create', 'delete'].

    Cls in the following specifications stands for the passed class name, or the lowercase actual class name.

    Methods' signatures are:
     * cls.create(**fields) - fields are passed directly to SQLAlchemy model constructor
     * cls.get(**filters) - filters are passed directly to SQLAlchemy. Returns a list
     * cls.update(**filters, **update) - update is a dict, whose members are new field values for the instance
     * cls.delete(**filters) - explains itself

    If `generate_by_id_methods` is True (default) then the following are generated:
     * cls.get_by_id(cls_id) - returns a single instance
     * cls.update_by_id(cls_id, **update)
     * cls.delete_by_id(cls_id)

    :param class_name: required class name. If None (default) - lowercase actual decorated class name is used
    :param methods: allowed methods. Must be a subset of ['create', 'get', 'update', 'delete'], or None, if all are good
    :param crud_namespace: namespace used to split other defined methods from generated
    :param generate_by_id_methods: generates methods
    :return: wrapper function
    """

    if methods is None:
        methods = CRUD_ALLOWED_METHODS[:]

    for i in methods:
        if i not in CRUD_ALLOWED_METHODS:
            raise ValueError('method ' + i + ' is not a possible crud action')

    def wrapper(cls):
        if not isinstance(cls, type):
            raise ValueError(str(cls) + ' is not a class')

        class_name_ = class_name
        if class_name_ is None:
            class_name_ = cls.__name__.lower()

        prefix = class_name_ + '.'
        if crud_namespace is not None:
            prefix += crud_namespace + '.'

        id_name = class_name_ + '_id'

        if 'create' in methods:
            @bind(prefix + 'create')
            def create(**fields):
                instance = cls(**fields)
                db.session.add(instance)
                db.session.commit()

        if 'get' in methods:
            @bind(prefix + 'get')
            def get(**filters):
                instances = cls.query.filter_by(**filters).all()
                return instances

            if generate_by_id_methods:
                @bind(prefix + 'get_by_id')
                def get_by_id(**kwargs):
                    if id_name not in kwargs:
                        raise ValueError('kwargs doesn\'t contain {}'.format(id_name))
                    instance = cls.query.filter_by(id=kwargs[id_name]).first()
                    return instance

        if 'update' in methods:
            @bind(prefix + 'update')
            def update(**filter, **fields):
                instances = cls.query.filter_by(filter)
                for i in instances:
                    for k, v in fields.items():
                        setattr(i, k, v)
                    db.session.add(i)
                db.session.commit()

            if generate_by_id_methods:
                @bind(prefix + 'update_by_id')
                def update_by_id(**kwargs):
                    if id_name not in kwargs:
                        raise ValueError('kwargs doesn\'t contain {}'.format(id_name))
                    instance = cls.query.filter_by(id=kwargs[id_name]).first()
                    return instance

        if 'delete' in methods:
            @bind(prefix + 'delete')
            def delete(**filter):
                cls.query.filter_by(filter).delete()

            if generate_by_id_methods:
                @bind(prefix + 'delete_by_id')
                def delete_by_id(**kwargs):
                    if id_name not in kwargs:
                        raise ValueError('kwargs doesn\'t contain {}'.format(id_name))
                    cls.query.filter_by(id=kwargs[id_name]).delete()

        return cls

    return wrapper
