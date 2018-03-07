.. hexagonal documentation master file, created by
   sphinx-quickstart on Thu Feb  1 16:02:00 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to hexagonal's documentation!
=====================================

hexagonal is an LMS (library management system) build as a first year bachelors' project at Innopolis University.
Class diagram can be found at hexagonal.docs.hexagonal-classes.uml. Also a
:download:`rendered version <_static/BON DIAGRAM MODEL.pdf>`.

It should also be noted that as a dynamic by nature language, Python doesn't have native support for class attribute
documentation. This is also a bad practice, because it hurts readability of code.


Technology stack
----------------

Our technology stack is mainly focused on flexibility and ease-of-use:

 * Flask was used over django because it is definitely more lightweight, and is more flexible.
 * SQLAlchemy was used because of its, again, flexibility and speed of development.
   SQLAlchemy uses data-mapper model instead of Django's familiar Active Record, and it allows for some interesting
   features such as association proxies.
 * Itsdangerous is a small library with 'good' cryptography. It is a common knowledge that you shouldn't implement
   cryptography by yourself, and this library contains a lot of neat things to help with that.
 * PostgreSQL was chosen for backend because it is feature-rich, stable, and easy to use.
   SQLite didn't have ARRAY builtin type and full index support for JSON.
   MySQL just tends to fall apart randomly (from my experience).
   Other SQL (MS SQL, Oracle) are too much enterprise for such project

Model
-----

The user model consists currently of four classes:

 * User is an abstract base class for all users
 * Librarian is a kind of an admin which can manage everything else
 * Patron is an abstract base class for all patrons
 * StudentPatron is a class that represents all student-patrons
 * FacultyPatron is a class that represents all faculty-patrons


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
This is the whole lifecycle of one Loan.m
