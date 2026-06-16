from typing import Optional

from pydantic import BaseModel, Field


class CreateLinkRequest(BaseModel):
    url: str = Field(..., min_length=1)
    expires_at: Optional[str] = None


class CreateLinkResponse(BaseModel):
    token: str
    url: str
    short_url: str
    qr_url: str


class LinkInfoResponse(BaseModel):
    token: str
    url: str
    created_at: str
    updated_at: str | None = None
    expires_at: Optional[str] = None
    is_deleted: bool = False


class UpdateLinkRequest(BaseModel):
    url: Optional[str] = None
    expires_at: Optional[str] = None


class ScanDay(BaseModel):
    date: str
    count: int


class AnalyticsResponse(BaseModel):
    token: str
    total_scans: int
    scans_by_day: list[ScanDay]


class LinkStatusResponse(BaseModel):
    token: str
    status: str
    redirectable: bool
