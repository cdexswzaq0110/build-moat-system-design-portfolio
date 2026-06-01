import ipaddress
from urllib.parse import urlparse, urlunparse


PRIVATE_HOSTS = {"localhost"}
ALLOWED_SCHEMES = {"http", "https"}


def validate_url(raw_url: str) -> str:
    candidate = raw_url.strip()
    if not candidate:
        raise ValueError("URL is required")

    parsed = urlparse(candidate)
    if parsed.scheme not in ALLOWED_SCHEMES:
        raise ValueError("Only http and https URLs are allowed")
    if not parsed.netloc:
        raise ValueError("URL host is required")

    hostname = parsed.hostname
    if hostname is None:
        raise ValueError("URL host is invalid")
    if hostname.lower() in PRIVATE_HOSTS:
        raise ValueError("Private hosts are not allowed")

    try:
        ip_address = ipaddress.ip_address(hostname)
    except ValueError:
        ip_address = None

    if ip_address and (ip_address.is_private or ip_address.is_loopback or ip_address.is_link_local):
        raise ValueError("Private IP URLs are not allowed")

    normalized = parsed._replace(fragment="")
    return urlunparse(normalized)
