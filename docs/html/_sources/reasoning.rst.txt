Reasoning
=========

The part in which we describe why we chose what we chose.

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
    Other SQL (MS SQL, Oracle) are too much enterprise for such project.
