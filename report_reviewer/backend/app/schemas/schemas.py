from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# User schemas
class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    email: EmailStr
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    class Config:
        from_attributes = True


# Report schemas
class ReportCreate(BaseModel):
    filename: str
    original_filename: str
    file_path: str
    file_size: int
    file_type: str


class ReportStatusUpdate(BaseModel):
    status: str
    error_message: Optional[str] = None


class ReportResponse(BaseModel):
    id: int
    user_id: int
    filename: str
    original_filename: str
    file_size: int
    file_type: str
    extracted_text: Optional[str] = None
    upload_date: datetime
    status: str
    error_message: Optional[str] = None

    class Config:
        from_attributes = True


class ReportListResponse(BaseModel):
    id: int
    original_filename: str
    file_size: int
    file_type: str
    upload_date: datetime
    status: str
    overall_score: Optional[float] = None

    class Config:
        from_attributes = True


# Review schemas
class ReviewBase(BaseModel):
    overall_score: Optional[float] = None
    overall_quality: Optional[str] = None
    summary: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    recommendations: List[str] = []
    grammar_score: Optional[float] = None
    content_score: Optional[float] = None
    structure_score: Optional[float] = None
    clarity_score: Optional[float] = None
    academic_style_score: Optional[float] = None


class ReviewResponse(ReviewBase):
    id: int
    report_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class SectionReviewBase(BaseModel):
    section_name: str
    section_order: Optional[int] = None
    score: Optional[float] = None
    content_preview: Optional[str] = None
    strengths: List[str] = []
    weaknesses: List[str] = []
    suggestions: List[str] = []
    priority: Optional[str] = None


class SectionReviewResponse(SectionReviewBase):
    id: int

    class Config:
        from_attributes = True


class IssueBase(BaseModel):
    category: str
    severity: str
    description: str
    location: Optional[str] = None
    suggestion: Optional[str] = None
    line_number: Optional[int] = None


class IssueResponse(IssueBase):
    id: int

    class Config:
        from_attributes = True


class ReviewDetailResponse(BaseModel):
    review: ReviewResponse
    sections: List[SectionReviewResponse]
    issues: List[IssueResponse]

    class Config:
        from_attributes = True


# AI Improvement schemas
class ImprovementRequest(BaseModel):
    text: str = Field(..., min_length=1)
    improvement_type: str = Field(
        ...,
        pattern=r"^(rewrite|academic|concise|expand|grammar|technical|simplify|custom)$"
    )
    instructions: Optional[str] = None
    report_context: Optional[str] = None


class ImprovementResponse(BaseModel):
    original_text: str
    improved_text: str
    improvement_type: str
    explanation: Optional[str] = None


# Chat schemas
class ChatMessage(BaseModel):
    role: str = Field(..., pattern=r"^(user|assistant|system)$")
    content: str


class ChatRequest(BaseModel):
    messages: List[ChatMessage] = Field(..., min_length=1)
    report_context: Optional[str] = None
    report_summary: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    suggested_questions: List[str] = []


# Dashboard schemas
class DashboardStats(BaseModel):
    total_reports: int
    processing_reports: int
    completed_reports: int
    average_score: Optional[float] = None
    recent_reports: List[ReportListResponse] = []

    class Config:
        from_attributes = True


# API Response wrappers
class APIResponse(BaseModel):
    success: bool
    message: str
    data: Optional[dict] = None


class ErrorResponse(BaseModel):
    success: bool = False
    message: str
    detail: Optional[str] = None
