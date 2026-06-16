import sqlite3
from datetime import datetime
from io import BytesIO

import qrcode
from fastapi import APIRouter, HTTPException, Request, Response
from fastapi.responses import RedirectResponse

from .repository import (
    create_link,
    find_link,
    get_scan_analytics,
    is_expired,
    record_scan,
    soft_delete_link,
    update_link,
)
from .schemas import (
    AnalyticsResponse,
    CreateLinkRequest,
    CreateLinkResponse,
    LinkInfoResponse,
    LinkStatusResponse,
    UpdateLinkRequest,
)
from .token_gen import generate_token
from .url_validator import validate_url


router = APIRouter()
redirect_cache: dict[str, str] = {}


@router.get("/health")
def health() -> dict:
    return {"status": "ok"}


@router.post("/links", response_model=CreateLinkResponse)
def create_short_link(request: CreateLinkRequest) -> CreateLinkResponse:
    try:
        normalized_url = validate_url(request.url)
        if request.expires_at:
            datetime.fromisoformat(request.expires_at)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    for _ in range(5):
        token = generate_token()
        try:
            create_link(token, normalized_url, request.expires_at)
            redirect_cache[token] = normalized_url
            return CreateLinkResponse(
                token=token,
                url=normalized_url,
                short_url=f"/r/{token}",
                qr_url=f"/qr/{token}.png",
            )
        except sqlite3.IntegrityError:
            continue

    raise HTTPException(status_code=500, detail="Could not allocate token")


@router.post("/api/qr/create", response_model=CreateLinkResponse)
def create_qr(request: CreateLinkRequest) -> CreateLinkResponse:
    return create_short_link(request)


def serialize_link(link: dict) -> LinkInfoResponse:
    return LinkInfoResponse(
        token=link["token"],
        url=link["target_url"],
        created_at=link["created_at"],
        updated_at=link.get("updated_at"),
        expires_at=link.get("expires_at"),
        is_deleted=bool(link.get("is_deleted")),
    )


def get_active_link_or_error(token: str) -> dict:
    link = find_link(token)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    if link.get("is_deleted"):
        raise HTTPException(status_code=410, detail="Link deleted")
    if is_expired(link):
        raise HTTPException(status_code=410, detail="Link expired")
    return link


@router.get("/api/qr/{token}", response_model=LinkInfoResponse)
def get_link_info(token: str) -> LinkInfoResponse:
    link = find_link(token)
    if link is None or link.get("is_deleted"):
        raise HTTPException(status_code=404, detail="Link not found")
    return serialize_link(link)


@router.patch("/api/qr/{token}", response_model=LinkInfoResponse)
def update_qr(token: str, request: UpdateLinkRequest) -> LinkInfoResponse:
    try:
        normalized_url = validate_url(request.url) if request.url is not None else None
        if request.expires_at:
            datetime.fromisoformat(request.expires_at)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error

    link = update_link(token, target_url=normalized_url, expires_at=request.expires_at)
    if link is None:
        raise HTTPException(status_code=404, detail="Link not found")
    redirect_cache.pop(token, None)
    return serialize_link(link)


@router.delete("/api/qr/{token}")
def delete_qr(token: str) -> dict:
    deleted = soft_delete_link(token)
    if not deleted:
        raise HTTPException(status_code=404, detail="Link not found")
    redirect_cache.pop(token, None)
    return {"status": "deleted", "token": token}


@router.get("/api/qr/{token}/image")
def get_api_qr_image(token: str) -> Response:
    return get_qr_code(token)


@router.get("/api/qr/{token}/analytics", response_model=AnalyticsResponse)
def get_analytics(token: str) -> dict:
    link = find_link(token)
    if link is None or link.get("is_deleted"):
        raise HTTPException(status_code=404, detail="Link not found")
    return get_scan_analytics(token)


@router.get("/api/qr/{token}/check", response_model=LinkStatusResponse)
def check_link(token: str) -> LinkStatusResponse:
    link = find_link(token)
    if link is None:
        return LinkStatusResponse(token=token, status="not_found", redirectable=False)
    if link.get("is_deleted"):
        return LinkStatusResponse(token=token, status="deleted", redirectable=False)
    if is_expired(link):
        return LinkStatusResponse(token=token, status="expired", redirectable=False)
    return LinkStatusResponse(token=token, status="active", redirectable=True)


@router.get("/qr/{token}.png")
def get_qr_code(token: str) -> Response:
    link = get_active_link_or_error(token)

    image = qrcode.make(link["target_url"])
    output = BytesIO()
    image.save(output, format="PNG")
    return Response(content=output.getvalue(), media_type="image/png")


@router.get("/r/{token}")
def redirect(token: str, request: Request) -> RedirectResponse:
    cached_url = redirect_cache.get(token)
    if cached_url:
        link = get_active_link_or_error(token)
        record_scan(
            token,
            user_agent=request.headers.get("user-agent"),
            ip_address=request.client.host if request.client else None,
        )
        return RedirectResponse(link["target_url"], status_code=307)

    link = get_active_link_or_error(token)
    redirect_cache[token] = link["target_url"]
    record_scan(
        token,
        user_agent=request.headers.get("user-agent"),
        ip_address=request.client.host if request.client else None,
    )
    return RedirectResponse(link["target_url"], status_code=307)
