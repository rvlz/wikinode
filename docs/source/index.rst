Welcome to wikinode's documentation!
====================================

.. image:: https://travis-ci.org/rvlz/wikinode.svg?branch=master
    :target: https://travis-ci.org/rvlz/wikinode

Installation
------------

To install wikinode, run the command below in your terminal::

    $ pip install wikinode

Alternatively, clone the git repo::

    $ git clone https://github.com/rvlz/wikinode.git

and then run::

    $ cd wikinode
    $ python setup.py install

Quick look
----------

Get an article summary:

.. code-block:: python

    >>> wikinode.fetch("hello world")
    {
      'query': 'hello world',
      'title': '"Hello, World!" program',
      'description': "Traditional beginners' computer program",
      'extract': 'A "Hello, World!" program generally is a computer program...'
    }

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   summary
   license


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
