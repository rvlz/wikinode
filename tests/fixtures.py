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
