# hexagonal
Bachelors project at Innopolis university (Spring semester 2018)

### How to run

    $ ./run.sh    # not too hard, is it?
    
    
### How to run tests

    $ ./run-tests.sh  # seems harder this time
    
### API reference

Under development, but you can see all available methods by
first running the application, and then issuing the `jsonrpc.get_available_methods` call

    $ http --json POST localhost:5000/api/v1/rpc \
        jsonrpc=2.0 method='jsonrpc.get_available_methods'
        
    HTTP/1.0 200 OK
    Content-Length: 1889
    Content-Type: text/html; charset=utf-8
    Date: Sun, 04 Feb 2018 10:47:56 GMT
    Server: Werkzeug/0.14.1 Python/3.6.3
    {
        "id": null,
        "jsonrpc": "2.0",
        "result": {
            "account.crud.create": "\n                Create an instance of account.\n                Automatically generated method.\n\n                :param fields: fields of the target class\n                :return: newly created instance of account\n                ",
            "account.crud.delete": "\n                Delete instances of account that match the specified filters.\n\n                :param filters: search criteria\n                :return: None\n                ",
            "account.crud.delete_by_id": "\n                    Delete one instance of account by id.\n\n                    :param account_id: required id\n                    :return: None\n                    ",
            "account.crud.get": "\n                Get all instances of account that match the passed filter.\n\n                :param filters: search criteria\n                :return: list of all instances of account that match (may be empty)\n                ",
            "account.crud.get_by_id": "\n                    Get an instance of account that has specified id.\n\n                    :param account_id: required id\n                    :return: instance that has id = account_id or None\n                    ",
            "account.crud.update": "\n                Update instances of account filtered by `filters`.\n\n                :param filters: search criteria\n                :param fields: actual update\n                :return: None\n                ",
            "account.crud.update_by_id": "\n                    Update one instance of account by id.\n\n                    :param account_id: required id\n                    :return: the updated instance of account\n                    ",
            "auth.login": null,
            "auth.register": null,
            "jsonrpc.get_available_methods": "\n    Get all available methods registered in jsonrpc.\n\n    :return: dict of 'function_name': 'docstring' or null\n    "
        }
    }
