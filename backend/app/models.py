from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    file: str
    start_line: int = Field(ge=1)
    end_line: int = Field(ge=1)
    excerpt: str
    rationale: str

class TraceEvent(BaseModel):
    tool: str
    arguments_summary: str
    result_summary: str

class Report(BaseModel):
    incident_id: str
    exception_type: str | None = None
    probable_cause: str
    status: Literal['hypothesis', 'supported', 'inconclusive']
    evidence: list[Evidence] = Field(default_factory=list)
    proposed_fix: str
    validation_steps: list[str] = Field(default_factory=list)
    tool_trace: list[TraceEvent] = Field(default_factory=list)
    warnings: list[str] = Field(default_factory=list)

class IncidentSummary(BaseModel):
    id: str
    log_filename: str
    source_filename: str
    created_at: datetime
    investigated: bool = False

class ParsedLog(BaseModel):
    exception_type: str | None = None
    timestamp: str | None = None
    stack_frames: list[str] = Field(default_factory=list)
    symbols: list[str] = Field(default_factory=list)
