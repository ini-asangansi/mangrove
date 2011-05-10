First Install Steps:
=====================

Requirements
-------------------

* Python 2.7
* Python headers (sudo apt-get install python-dev)
* CouchDB (sudo apt-get install couchdb)

1. Create a virtualenv
--------------------
virtualenv ve && source ve/bin/activate
    or with virtualenvwrapper
mkvirtualenv mangrove

2. Install required python packages
--------------------
pip install -r requirements.pip

Run tests!
=====================
nosetests

Push to GitHub
=====================
And hopefully hudson will run tests, and they will pass.
