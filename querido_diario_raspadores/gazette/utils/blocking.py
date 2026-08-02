# Some websites started protecting themselves with Cloudflare Turnstile.
# When a spider (or Zyte Smart Proxy) is challenged, Cloudflare replies with
# an HTTP 200/403/503 response carrying an interstitial HTML page instead of
# the real content. Without this check, that harmless-looking HTML gets
# parsed as if it were the actual gazette page, or saved as if it were the
# gazette PDF file, silently producing wrong results.
CLOUDFLARE_CHALLENGE_MARKERS = (
    b"challenges.cloudflare.com",
    b"cf-turnstile",
    b"cf_chl_opt",
    b"cf-chl-",
    b"Just a moment...",
    b"Attention Required! | Cloudflare",
    b"Checking if the site connection is secure",
)

# Only look at the first few KB: the markers always appear near the top of
# the interstitial page, and PDFs/large files would be costly to scan fully.
_MAX_BODY_BYTES_TO_INSPECT = 8192


def is_cloudflare_challenge(response) -> bool:
    """Return True if `response` is a Cloudflare Turnstile/challenge page
    rather than the content that was actually requested."""
    body = response.body[:_MAX_BODY_BYTES_TO_INSPECT]
    return any(marker in body for marker in CLOUDFLARE_CHALLENGE_MARKERS)
