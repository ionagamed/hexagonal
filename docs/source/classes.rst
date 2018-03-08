Classes
=======

This part contains in-depth view of the used classes.
Subclassing with only role changing was used to implement a rather flexible permission system.

User model
----------

In SQL users use single-table inheritance model, which allows for compact data storage, when we do not have
additional fields in subclasses.

.. autoclass:: hexagonal.model.user.User
    :members:

.. autoclass:: hexagonal.model.patron.Patron
    :members:
    :show-inheritance:

.. autoclass:: hexagonal.model.librarian.Librarian
    :members:
    :show-inheritance:

.. autoclass:: hexagonal.model.student_patron.StudentPatron
    :members:
    :show-inheritance:

.. autoclass:: hexagonal.model.faculty_patron.FacultyPatron
    :members:
    :show-inheritance:

Document model
--------------

In SQL documents use joined-table inheritance, so id of any specific document is a foreign key to id of a document.
All common fields are kept in the ``documents`` table, whereas fields unique for the specific type are held in a separate table.

.. autoclass:: hexagonal.model.document.Document
    :members:

.. autoclass:: hexagonal.model.document_copy.DocumentCopy
    :members:

.. autoclass:: hexagonal.model.book.Book
    :members:
    :show-inheritance:

.. autoclass:: hexagonal.model.journal_article.JournalArticle
    :members:
    :show-inheritance:

.. autoclass:: hexagonal.model.av_material.AVMaterial
    :members:
    :show-inheritance:

Booking model
-------------

.. autoclass:: hexagonal.model.loan.Loan
    :members:

Search
------

.. autoclass:: hexagonal.model.searchable.Searchable
    :private-members:
    :members:





