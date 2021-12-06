======
gitown
======


.. image:: https://img.shields.io/pypi/v/gitown.svg
        :target: https://pypi.python.org/pypi/gitown

.. image:: https://img.shields.io/travis/milin/gitown.svg
        :target: https://travis-ci.com/milin/gitown

.. image:: https://readthedocs.org/projects/gitown/badge/?version=latest
        :target: https://gitown.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


Keep your github CODEOWNERS file up to date.


* Free software: MIT license
* Documentation: https://gitown.readthedocs.io.


Features
--------

* Keep your github CODEOWNERS_ file up to date.

Why to keep CODEOWNERS_ file up to date?

- Allows for automated code reviewing process and integrates with github auto selecting the reviewer most likely to know the most about the change list.
- Can integrate into slack once code reviewer is auto assigned and helps manage code review process.
- Helps in introducing standard process during team code-reviews.


Details
-------
* If a committer exceeds the ``ownership_threshold`` percentage in a file, then the committer is added to the ``CODEOWNERS`` file.
* Default ``ownership_threshold`` is set to 25%. You can change it by passing ``--ownership_threshold``. Meaning, if a person has 25% of more changes in a file, he is considered a codeowner, and the CODEOWNER file is updated accordingly.
* Can be used as a ``pre-commit`` hook.

**IMPORTANT**

* You need to create a gitownrc_ file and have a mapping of github emails to github usernames in order to use this tool.
* `gitown` reads that file and only those users are considered to be added to the ``CODEOWNERS`` file.

It is best used along with pre-commit_. You can use it along with pre-commit by adding the following hook in your ``.pre-commit-config.yaml`` file.

::

    repos:
    - repo:  https://github.com/milin/gitown
      rev: v0.1.6
      hooks:
      - id:  gitown
        args: ['--ownership_threshold=25', '--codeowners_filename=CODEOWNERS']  # Optional


You need to have precommit setup to use this hook.
--------------------------------------------------
   Install Pre-commit and the commit-msg hook-type.


   ::

        pip install pre-commit
        pre-commit install


.. _pre-commit: https://pre-commit.com/
.. _gitownrc: https://github.com/milin/gitown/blob/master/.gitownrc
.. _CODEOWNERS: https://docs.github.com/en/free-pro-team@latest/github/creating-cloning-and-archiving-repositories/about-code-owners
