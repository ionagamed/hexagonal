Model
=====

This part contains overview for used model classes. For a more in-depth explanation see :doc:`classes`

Users
-----

The user model consists currently of five classes:

 * User is an abstract base class for all users
 * Librarian is a kind of an admin which can manage everything else
 * Patron is an abstract base class for all patrons
 * StudentPatron is a class that represents all student-patrons
 * FacultyPatron is a class that represents all faculty-patrons


Documents
---------


The document model consists currently of five classes:

 * Document is an abstract base class for all documents, which contains all common fields.
 * DocumentCopy is a class for a copy of a document, which is just linked to a loan and a document.
 * And a class for each document type (Book, AVMaterial, Article).


Booking System
--------------

Also, a Loan class, which represents the booking system.
One Loan has a status - it can be:
*requested* - user wants this book. Then librarian can push a button and make the loan
*approved* - which means that it is currently in patron's possession. Then, finally, user brings the book back,
and it becomes *returned*, until a librarian approves the return request, and the loan is removed.
This is the whole lifecycle of one Loan.
