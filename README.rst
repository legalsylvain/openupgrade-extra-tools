Installation
============

* create python virtual env

``virtualenv ./env --python=python3.10``

* Install dependencies

``./env/bin/pip install -r ./requirements.txt``

* Create a private configuration file, named ``private_config.py``
  and write inside:
  ``token = "my_private_github_token"``

Usage
=====

* Check if opened PRs are OK to be merged, regarding dependencies.

``./env/bin/python ./check_dependency.py``

Get all the opened PRs defined in the issue "Migration to version xx"

For each PR:

* if all the dependencies are marked as "done" (or "nothing to do"):
    * remove the label 'Blocked by dependency' (if set)
    * set the label 'Dependency OK'

* else:
    * remove the label 'Dependency OK' (if set)
    * set the label 'Blocked by dependency'
