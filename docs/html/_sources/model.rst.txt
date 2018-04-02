Model
=====

This part contains overview for used model classes. For a more in-depth explanation see :doc:`classes`

Users
-----

The user model consists currently of five classes:

 * :py:class:`~hexagonal.model.user.User` is an abstract base class for all users
 * :py:class:`~hexagonal.model.librarian.Librarian` is a kind of an admin which can manage everything else
 * :py:class:`~hexagonal.model.patron.Patron` is an abstract base class for all patrons
 * :py:class:`~hexagonal.model.student_patron.StudentPatron` is a class that represents all student-patrons
 * :py:class:`~hexagonal.model.faculty_patron.FacultyPatron` is a class that represents all faculty-patrons

There is a single `root` user throughout the runtime, which is a librarian.
This is done because only a librarian can create new users, and wee need an entry point.


Documents
---------


The document model consists currently of five classes:

 * :py:class:`~hexagonal.model.document.Document` is an abstract base class for all documents, which contains all common fields.
 * :py:class:`~hexagonal.model.document_copy.DocumentCopy` is a class for a copy of a document, which is just linked to a loan and a document.
 * And a class for each document type (:py:class:`~hexagonal.model.book.Book`, :py:class:`~hexagonal.model.av_material.AVMaterial`, :py:class:`~hexagonal.model.journal_article.JournalArticle`).


Booking System
--------------

The :py:class:`~hexagonal.model.loan.Loan` is the single class which represents the booking system.
Each `Loan` has a status (:py:class:`hexagonal.model.loan.Loan.Status`) - it can be:
*requested* - user wants this book. Then librarian can push a button and make the loan
*approved* - which means that it is currently in patron's possession. Then, finally, user brings the book back,
and it becomes *returned*, until a librarian approves the return request, and the loan is removed.
This is the whole lifecycle of one `Loan`.


Priority Queue
==============

The :py:class:`~hexagonal.model.queued_request.QueuedRequest` is the single class responsible for the priority queue.
It uses SQL `ORDER BY`'s to implement the required behaviour, and contains indices for them to be fast enough.
