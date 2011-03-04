Developer Practices
===================

* We are using Git_ as the Source Control Manager (SCM)
* Our Documentation style is restructuredtext_ (RST)
* Our python coding style guide is PEP8_
 	
	- 4 spaces per indentation level
 	- Soft tabs (indentation is with spaces only)
* We have a continuous integration server set up using hudson_. It can be viewed on http://173.255.238.6:8080/
* We have detailed test reports and code coverage for every build
* We are using nose_ tests to write unit tests. You are requested to maintain the unit test suit for every code you check in. Please make sure that the test coverage for code is high :)   
* Our functional tests are written in WebDriver_ (Selenium 2.0)
* We are using fabric_ for automatic deployment
* We use virtualenv_ and pip_ to set up our python environment


Other important links
---------------------
* Our transport layer is managed by VUMI_

.. _VUMI: https://github.com/praekelt/vumi 
.. _Git: http://git-scm.com/
.. _restructuredtext: http://docutils.sourceforge.net/rst.html
.. _PEP8: http://www.python.org/dev/peps/pep-0008/
.. _hudson: http://hudson-ci.org/
.. _nose: http://ivory.idyll.org/articles/nose-intro.html
.. _WebDriver: http://code.google.com/p/selenium/wiki/GettingStarted
.. _fabric: http://docs.fabfile.org/0.9.4/
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _pip: http://pypi.python.org/pypi/pip
