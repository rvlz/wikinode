from wikinode.exceptions import QueryAmbiguousError


body = {
    "type": "standard",
    "title": '"Hello, World!" program',
    "description": "Traditional beginners' computer program",
    "extract": (
        'A "Hello, World!" program generally ' "is a computer program..."
    ),
    "content_urls": {"desktop": {"page": "..."}, "mobile": {"page": "..."}},
}

body_not_found = {
    "title": "Not found.",
    "method": "get",
    "detail": "Page or revision not found.",
}

body_ambiguous = {
    "title": "Micro",
    "type": "disambiguation",
}

body_redirect = {
    "type": "standard",
    "title": "Saint Petersburg",
    "description": "Federal city in the Northwestern federal district, Russia",
    "extract": "Saint Petersburg, formerly known as Petrograd (Петроград)...",
    "content_urls": {"desktop": {"page": "..."}, "mobile": {"page": "..."}},
}

fetch_results = [
    {
        "query": "hello world",
        "title": '"Hello, World!" program',
        "description": "Traditional beginners' computer program",
        "extract": (
            'A "Hello, World!" program generally is a computer program...'
        ),
    },
    {
        "query": "python language",
        "title": "Python (programming language)",
        "description": "General-purpose, high-level programming language",
        "extract": "Python is an interpreted, high-level, general-purpose...",
    },
    {
        "query": "Chicago",
        "title": "Chicago",
        "description": (
            "City and county seat of Cook County, Illinois, United States"
        ),
        "extract": (
            "Chicago, officially the City of Chicago, is the most populous"
        ),
    },
]

fetch_results_ambiguous = [
    {
        "query": "hello world",
        "title": '"Hello, World!" program',
        "description": "Traditional beginners' computer program",
        "extract": (
            'A "Hello, World!" program generally is a computer program...'
        ),
    },
    {
        "query": "python language",
        "title": "Python (programming language)",
        "description": "General-purpose, high-level programming language",
        "extract": "Python is an interpreted, high-level, general-purpose...",
    },
    # "micro" query
    QueryAmbiguousError("micro"),
]

fetch_results_not_found = [
    {
        "query": "hello world",
        "title": '"Hello, World!" program',
        "description": "Traditional beginners' computer program",
        "extract": (
            'A "Hello, World!" program generally is a computer program...'
        ),
    },
    {
        "query": "python language",
        "title": "Python (programming language)",
        "description": "General-purpose, high-level programming language",
        "extract": "Python is an interpreted, high-level, general-purpose...",
    },
    {},  # "hello123" query
]

fetch_results_mixed = [
    {
        "query": "hello world",
        "title": '"Hello, World!" program',
        "description": "Traditional beginners' computer program",
        "extract": (
            'A "Hello, World!" program generally is a computer program...'
        ),
    },
    # "micro" query
    QueryAmbiguousError("micro"),
    {
        "query": "python language",
        "title": "Python (programming language)",
        "description": "General-purpose, high-level programming language",
        "extract": "Python is an interpreted, high-level, general-purpose...",
    },
    {},  # "hello123" query
    {
        "query": "Chicago",
        "title": "Chicago",
        "description": (
            "City and county seat of Cook County, Illinois, United States"
        ),
        "extract": (
            "Chicago, officially the City of Chicago, is the most populous"
        ),
    },
]
