import os
from pathlib import Path

from flask import Flask, abort, send_from_directory

BASE_DIR = Path(__file__).resolve().parent
STATIC_ROOT = BASE_DIR / "_site"

if not STATIC_ROOT.exists():
    raise RuntimeError("_site directory not found. Build the site before deploying.")

app = Flask(__name__, static_folder=str(STATIC_ROOT), static_url_path="")

_SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "default-src 'self'; "
        "script-src 'self' https://www.googletagmanager.com https://www.google-analytics.com https://www.gstatic.com https://platform.twitter.com https://cdn.syndication.twimg.com https://syndication.twitter.com; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https://www.google-analytics.com https://www.googletagmanager.com https://pbs.twimg.com https://ton.twimg.com https://abs.twimg.com; "
        "font-src 'self' data:; "
        "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com https://stats.g.doubleclick.net https://region1.google-analytics.com https://platform.twitter.com https://cdn.syndication.twimg.com https://syndication.twitter.com https://api.twitter.com; "
        "frame-src https://platform.twitter.com https://syndication.twitter.com; "
        "frame-ancestors 'self'; "
        "object-src 'none'; "
        "base-uri 'self'; "
        "form-action 'self'; "
        "manifest-src 'self'; "
        "upgrade-insecure-requests"
    ),
    "X-Frame-Options": "SAMEORIGIN",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": (
        "accelerometer=(), camera=(), geolocation=(), gyroscope=(), "
        "microphone=(), payment=(), usb=()"
    ),
}


@app.after_request
def apply_security_headers(response):
    for header, value in _SECURITY_HEADERS.items():
        response.headers[header] = value
    return response


def _resolve_static_path(requested: str) -> Path:
    safe_path = (STATIC_ROOT / requested).resolve()
    if STATIC_ROOT not in safe_path.parents and safe_path != STATIC_ROOT:
        abort(404)

    if safe_path.is_dir():
        safe_path = safe_path / "index.html"

    if not safe_path.exists():
        alt = (STATIC_ROOT / requested / "index.html").resolve()
        if alt.exists() and STATIC_ROOT in alt.parents:
            return alt
        abort(404)

    return safe_path


@app.route("/", defaults={"requested": ""})
@app.route("/<path:requested>")
def serve_static(requested: str):
    path = requested or "index.html"
    file_path = _resolve_static_path(path)
    relative = file_path.relative_to(STATIC_ROOT)
    return send_from_directory(app.static_folder, str(relative))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))
