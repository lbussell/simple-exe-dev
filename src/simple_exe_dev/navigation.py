"""Sidebar links and breadcrumbs, derived from the current request."""

from dataclasses import dataclass
from urllib.parse import unquote

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
    Page('Services', 'services', 'icon-[lucide--server]'),
    Page('Settings', 'settings', 'icon-[lucide--settings]'),
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
        if url_name in TITLES:
            title = TITLES[url_name]
        elif url_name:
            title = unquote(segment)  # a page named by its URL, like a service
        else:
            title = segment.replace('-', ' ').capitalize()
        crumbs.append(Crumb(title, prefix))
    return crumbs


def current_page(path: str) -> str:
    """The sidebar page whose URL is the longest prefix of path."""
    urls = {page.url_name: reverse(page.url_name) for page in PAGES}
    return max((name for name, url in urls.items() if path.startswith(url)), key=lambda name: len(urls[name]))


def navigation(request: HttpRequest) -> dict:
    """Template context processor."""
    return {
        'vm': reflection.get_info(),
        'pages': PAGES,
        'current_page': current_page(request.path),
        'breadcrumbs': breadcrumbs(request.path),
    }
