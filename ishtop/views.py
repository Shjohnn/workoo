"""
Custom i18n helpers. Django's translate_url() does not rewrite prefixed URLs
(e.g. /ru/) to unprefixed URLs for the default language when
prefix_default_language=False, so LocaleMiddleware keeps using the path language.
"""
from urllib.parse import urlsplit, urlunsplit

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import translate_url
from django.utils.http import url_has_allowed_host_and_scheme
from django.utils.translation import check_for_language


def _localize_path_for_language(url: str, lang_code: str) -> str:
    """
    Map URL path between default language (no prefix) and prefixed languages.
    Used when translate_url() leaves the URL unchanged for default language.
    """
    parsed = urlsplit(url)
    path = parsed.path or "/"
    default_lang = settings.LANGUAGE_CODE

    # Strip non-default language prefix: /ru/ishlar/ -> /ishlar/, /ru/ -> /
    stripped = path
    for code, _ in settings.LANGUAGES:
        if code == default_lang:
            continue
        prefix = f"/{code}/"
        if stripped.startswith(prefix):
            rest = stripped[len(prefix) :].lstrip("/")
            stripped = "/" + rest if rest else "/"
            break
        if stripped in (f"/{code}", f"/{code}/"):
            stripped = "/"
            break

    if lang_code == default_lang:
        if not stripped.startswith("/"):
            stripped = "/" + stripped
        return urlunsplit(
            (parsed.scheme, parsed.netloc, stripped or "/", parsed.query, parsed.fragment)
        )

    # Non-default language: add /{code}/ prefix
    if stripped in ("/", ""):
        new_path = f"/{lang_code}/"
    else:
        if not stripped.startswith("/"):
            stripped = "/" + stripped
        new_path = f"/{lang_code}{stripped}"
    return urlunsplit(
        (parsed.scheme, parsed.netloc, new_path, parsed.query, parsed.fragment)
    )


def set_language(request):
    """
    Same behavior as django.views.i18n.set_language, plus correct redirects
    from /ru/... back to /... when choosing the default language.
    """
    next_url = request.POST.get("next", request.GET.get("next"))
    if (next_url or request.accepts("text/html")) and not url_has_allowed_host_and_scheme(
        url=next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        next_url = request.META.get("HTTP_REFERER")
        if not url_has_allowed_host_and_scheme(
            url=next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            next_url = "/"

    response = HttpResponseRedirect(next_url) if next_url else HttpResponse(status=204)

    if request.method == "POST":
        lang_code = request.POST.get("language")
        if lang_code and check_for_language(lang_code):
            if next_url:
                next_trans = translate_url(next_url, lang_code)
                if next_trans == next_url:
                    next_trans = _localize_path_for_language(next_url, lang_code)
                if next_trans != next_url:
                    response = HttpResponseRedirect(next_trans)

            response.set_cookie(
                settings.LANGUAGE_COOKIE_NAME,
                lang_code,
                max_age=settings.LANGUAGE_COOKIE_AGE,
                path=settings.LANGUAGE_COOKIE_PATH,
                domain=settings.LANGUAGE_COOKIE_DOMAIN,
                secure=settings.LANGUAGE_COOKIE_SECURE,
                httponly=settings.LANGUAGE_COOKIE_HTTPONLY,
                samesite=settings.LANGUAGE_COOKIE_SAMESITE,
            )

    return response
