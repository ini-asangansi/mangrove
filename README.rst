First Install Steps:
=====================

1. Create a virtualenv
--------------------
virtualenv ve && source ve/bin/activate
    or with virtualenvwrapper
mkvirtualenv mangrove

2. Install required python packages
--------------------
pip install -r requirements.pip

3. Create a local_settings.py
--------------------
Create local_settings.py
    cp example_files/local_settings_example.py local_settings.py

And edit the contents for your development environment

Run tests!
=====================
nosetests

Push to GitHub
=====================
And hopefully hudson will run tests, and they will pass.