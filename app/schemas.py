# app/schemas.py

from pydantic import BaseModel


class QueryRequest(BaseModel):
    query: str


class SummaryResponse(BaseModel):
    query: str
    summary: str
    source_url: str
