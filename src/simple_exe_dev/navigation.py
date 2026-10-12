"""Sidebar links and breadcrumbs, derived from the current request."""

from dataclasses import dataclass

from django.http import HttpRequest
from django.urls import Resolver404, resolve, reverse

from exedev import reflection


@dataclass(frozen=True)
class Page:
    title: str
    url_name: str
    icon: str


PAGES = [
    Page('Home', 'index', 'icon-[lucide--house]'),
    Page('Notifications', 'notifications', 'icon-[lucide--bell]'),
    Page('Integrations', 'integrations', 'icon-[lucide--plug]'),
]

TITLES = {page.url_name: page.title for page in PAGES}


@dataclass(frozen=True)
class Crumb:
    title: str
    url: str


def breadcrumbs(path: str) -> list[Crumb]:
    """One crumb per URL prefix: /a/b/ gives Home, /a/, /a/b/."""
    crumbs = [Crumb(TITLES['index'], reverse('index'))]
    prefix = '/'
    for segment in path.strip('/').split('/'):
        if not segment:
            continue
        prefix += segment + '/'
        try:
            url_name = resolve(prefix).url_name
        except Resolver404:
            url_name = None
        crumbs.append(Crumb(TITLES.get(url_name, segment.replace('-', ' ').capitalize()), prefix))
    return crumbs


def navigation(request: HttpRequest) -> dict:
    """Template context processor."""
    match = request.resolver_match
    return {
        'vm': reflection.get_info(),
        'pages': PAGES,
        'current_page': match.url_name if match else None,
        'breadcrumbs': breadcrumbs(request.path),
    }
