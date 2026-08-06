from osint_local.analyzers.username_search import search_username
from osint_local.presenters.username_summary import (
    format_username_results,
)


username = "FB-001"

results = search_username(username)

print(
    format_username_results(
        username,
        results,
    )
)
