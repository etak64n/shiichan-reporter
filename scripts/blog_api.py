"""Client for the blog's ingest API, authenticated with GitHub Actions OIDC.

Local testing: set BLOG_DEV_TOKEN to use it instead of OIDC (pairs with the
blog's .dev.vars DEV_BEARER_TOKEN).
"""

import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

BLOG_API_URL = os.environ.get("BLOG_API_URL", "https://blog.shiichan.etak64n.dev")
OIDC_AUDIENCE = os.environ.get("OIDC_AUDIENCE", "https://blog.shiichan.etak64n.dev")

# Cloudflare's Browser Integrity Check rejects the default python-urllib UA (403/1010)
UA = "sheechan-reporter/1.0 (+https://blog.shiichan.etak64n.dev)"


def get_token() -> str:
    """Return a bearer token: BLOG_DEV_TOKEN if set, otherwise a fresh OIDC token."""
    dev_token = os.environ.get("BLOG_DEV_TOKEN")
    if dev_token:
        return dev_token

    req_url = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_URL")
    req_token = os.environ.get("ACTIONS_ID_TOKEN_REQUEST_TOKEN")
    if not req_url or not req_token:
        raise RuntimeError(
            "OIDC env vars missing; the workflow needs `permissions: id-token: write`"
        )
    audience = urllib.parse.quote(OIDC_AUDIENCE, safe="")
    req = urllib.request.Request(
        f"{req_url}&audience={audience}",
        headers={"Authorization": f"Bearer {req_token}"},
    )
    # GitHub's OIDC endpoint occasionally returns 5xx; retry with backoff
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=30) as res:
                return json.load(res)["value"]
        except urllib.error.HTTPError as e:
            if e.code < 500 or attempt == 4:
                raise
            time.sleep(2**attempt)
    raise AssertionError("unreachable")


def post_article(token: str, article: dict) -> None:
    """Raises RuntimeError with the API's error detail on a non-2xx response."""
    body = json.dumps(article, ensure_ascii=False).encode()
    req = urllib.request.Request(
        f"{BLOG_API_URL}/api/articles",
        data=body,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
            "User-Agent": UA,
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as res:
            res.read()
    except urllib.error.HTTPError as e:
        detail = e.read().decode(errors="replace")[:500]
        raise RuntimeError(f"HTTP {e.code}: {detail}") from e
