Contributing to opstools-ansible
================================

You can contribute bug fixes or enhancements to the
`opstools-ansible <https://github.com/centos-opstools/opstools-ansible/>`__
project by submitting a patch review via git review following the same
process as described in `submitting a
patch <http://docs.openstack.org/infra/manual/developers.html#submitting-a-change-for-review>`__.
The required .gitreview file is already contained in the repository.

Conventions
-----------

When creating or modifying Ansible roles, please use YAML format for
module arguments as in:

::

    - debug:
        var: somevar

Instead of the legacy format:

::

    - debug: var=somevar

We extract documentation automatically out of ``defaults/main.yml`` in
each role. In order for this to work correctly, each variable in that
file should be preceded by a comment with no intervening whitespace, and
should be separated from other variables by one (or more) blank linkes,
like this:

::

    # This is some documentation.
    some_variable: some value

    # This is documentation for another_variable.
    another_variable:
      - this
      - is
      - a
      - test

Running tests
-------------

To perform some simple YAML validations, run:

::

    tox

You should do this *before* submitting pull requests. Arranging to run
``tox`` via your local Git ``pre-commit`` hook will save you the
inconvenience of submitting a pull request only to have it rejected by
our CI testing.

Updating the documentation
--------------------------

The role documentation in ``README.rst`` is generated automatically from
(a) comments in the ``defaults/main.yml`` file for each role and (b) a
``README.rst`` included in each role.

After making changes, you can regenerate the documentation by running
``python setup.py build_sphinx`` in the top level of the repository.
