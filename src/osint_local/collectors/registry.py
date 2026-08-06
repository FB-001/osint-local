"""Registro central dos coletores disponíveis."""

from collections.abc import Callable

from osint_local.collectors.github_username import (
    search_github_username,
)
from osint_local.collectors.gitlab_username import (
    search_gitlab_username,
)
from osint_local.models.username_result import UsernameResult


UsernameCollector = Callable[[str], UsernameResult]


REGISTERED_USERNAME_COLLECTORS = (
    search_github_username,
    search_gitlab_username,
)
