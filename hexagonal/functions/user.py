from hexagonal import jsonrpc
from hexagonal.auth.helpers import minimum_access_level
from hexagonal.model.user import User


@jsonrpc.bind('user.get_borrowed_copies')
@minimum_access_level('librarian')
def user_get_borrowed_copies(user_id):
    return User.query.filter(User.id == user_id).first().get_borrowed_document_copies()
