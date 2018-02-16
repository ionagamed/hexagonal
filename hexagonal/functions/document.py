from hexagonal import jsonrpc, Document
from hexagonal.auth.helpers import minimum_access_level


@jsonrpc.bind('document.get')
@minimum_access_level('librarian')
def get_documents():
    return list(Document.query.all())
