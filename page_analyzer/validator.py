from urllib.parse import urlparse
import validators


def validate(url):
    if len(url) > 255:
        return None, "URL превышает 255 символов"

    if not validators.url(url):
        return None, "Некорректный URL"

    return urlparse(url)._replace(
        fragment="",
        path="",
        params="",
        query="",
    ).geturl(), None
