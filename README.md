# wikinode

[![Build Status](https://travis-ci.org/rvlz/wikinode.svg?branch=master)](https://travis-ci.org/rvlz/wikinode)
[![Documentation Status](https://readthedocs.org/projects/wikinode/badge/?version=latest)](https://wikinode.readthedocs.io/en/latest/?badge=latest)

A python library that helps you fetch data from Wikipedia.

## Installation

To install wikinode, run the command below in your terminal:

```shell
$ pip install wikinode
```

Alternatively, clone the git repo

```shell
$ git clone https://github.com/rvlz/wikinode.git
```

and then run

```shell
$ cd wikinode
$ python setup.py install
```

## Usage

First import wikinode

```s
>>> import wikinode
```

### Single summary

Get a single summary

```s
>>> wikinode.fetch("hello world")
{
  'query': 'hello world',
  'description': "Traditional beginners' computer program",
  'extract': 'A "Hello, World!" program generally is a computer program...'
}
```

### Multiple summaries

Get multiple summaries

```s
>>> wikinode.fetch_many(["hello world", "python language"])
[
  {
    'query': 'hello world',
    'description': "Traditional beginners' computer program",
    'extract': 'A "Hello, World!" program generally is a computer program...'
  },
  {
    'query': 'python language',
    'description': 'General-purpose, high-level programming language',
    'extract': 'Python is an interpreted, high-level, general-purpose...'
  }
]
```

Only get summary descriptions

```s
>>> wikinode.fetch_many(["hello world", "python language"], short=True)
[
  {
    'query': 'hello world',
    'description': "Traditional beginners' computer program"
  },
  {
    'query': 'python language',
    'description': 'General-purpose, high-level programming language'
  }
]
```

Get metadata for multiple summaries

```s
>>> wikinode.fetch_many(["hello world", "python language", "123hello"], meta=True)
{
  'hits': 2,
  'not_found': ['123hello'],  # Couldn't find summary for "123hello"
  'ambiguous': [],  # no ambiguous query
  'results': [
    {
      'query': 'hello world',
      'description': "Traditional beginners' computer program",
      'extract': 'A "Hello, World!" program generally is a computer program...'
    },
    {
      'query': 'python language',
      'description': 'General-purpose, high-level programming language',
      'extract': 'Python is an interpreted, high-level, general-purpose...'
    }
  ]
}
```
