from hexagonal import jsonrpc
from hexagonal.auth.helpers import minimum_access_level
from hexagonal.model.document import Document


@jsonrpc.bind('get_available_document_copies')
def get_available_document_copies():
    result = []

    docs = Document.query.all()

    for doc in docs:
        for copy in doc.copies:
            if copy.loan is None:
                result.append(copy)

    return result

