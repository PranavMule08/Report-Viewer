from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import selectinload
from typing import Optional, List
import os
import logging

from app.db.session import get_db
from app.models.user import User
from app.models.report import Report, ReportStatus
from app.models.review import Review, SectionReview, Issue
from app.schemas.schemas import (
    ReportResponse, ReportListResponse, DashboardStats,
    ReviewResponse, SectionReviewResponse, IssueResponse
)
from app.core.dependencies import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()


@router.get("", response_model=List[ReportListResponse], tags=["Reports"])
async def list_reports(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all reports for the current user."""
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.review))
        .where(Report.user_id == current_user.id)
        .order_by(Report.upload_date.desc())
        .offset(skip)
        .limit(limit)
    )
    reports = result.scalars().all()

    response = []
    for report in reports:
        response.append(ReportListResponse(
            id=report.id,
            original_filename=report.original_filename,
            file_size=report.file_size,
            file_type=report.file_type,
            upload_date=report.upload_date,
            status=report.status,
            overall_score=report.review.overall_score if report.review else None
        ))

    return response


@router.get("/dashboard", response_model=DashboardStats, tags=["Reports"])
async def get_dashboard_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get dashboard statistics for the current user."""
    logger.info(f'Getting dashboard for user {current_user.id}')
    
    # Total reports
    result = await db.execute(
        select(func.count(Report.id))
        .where(Report.user_id == current_user.id)
    )
    total_reports = result.scalar() or 0
    logger.info(f'Total reports: {total_reports}')

    # Processing reports
    result = await db.execute(
        select(func.count(Report.id))
        .where(Report.user_id == current_user.id)
        .where(Report.status == ReportStatus.PROCESSING.value)
    )
    processing_reports = result.scalar() or 0

    # Completed reports
    result = await db.execute(
        select(func.count(Report.id))
        .where(Report.user_id == current_user.id)
        .where(Report.status == ReportStatus.COMPLETED.value)
    )
    completed_reports = result.scalar() or 0

    # Average score
    result = await db.execute(
        select(func.avg(Review.overall_score))
        .join(Report)
        .where(Report.user_id == current_user.id)
    )
    avg_score = result.scalar()

    # Recent reports
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.review))
        .where(Report.user_id == current_user.id)
        .order_by(Report.upload_date.desc())
        .limit(5)
    )
    recent_reports = result.scalars().all()

    recent_reports_response = []
    for report in recent_reports:
        recent_reports_response.append(ReportListResponse(
            id=report.id,
            original_filename=report.original_filename,
            file_size=report.file_size,
            file_type=report.file_type,
            upload_date=report.upload_date,
            status=report.status,
            overall_score=report.review.overall_score if report.review else None
        ))

    return DashboardStats(
        total_reports=total_reports,
        processing_reports=processing_reports,
        completed_reports=completed_reports,
        average_score=round(avg_score, 1) if avg_score else None,
        recent_reports=recent_reports_response
    )


@router.get("/{report_id}", response_model=ReportResponse, tags=["Reports"])
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific report by ID."""
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.review))
        .where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return report


@router.get("/{report_id}/review", tags=["Reports"])
async def get_report_review(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the full review for a report."""
    result = await db.execute(
        select(Report)
        .options(
            selectinload(Report.review).selectinload(Review.section_reviews),
            selectinload(Report.review).selectinload(Review.issues),
        )
        .where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if not report.review:
        return {
            "review": None,
            "sections": [],
            "issues": [],
            "message": "No review available for this report"
        }

    review_data = ReviewResponse(
        id=report.review.id,
        report_id=report.review.report_id,
        overall_score=report.review.overall_score,
        overall_quality=report.review.overall_quality,
        summary=report.review.summary,
        strengths=report.review.strengths or [],
        weaknesses=report.review.weaknesses or [],
        recommendations=report.review.recommendations or [],
        grammar_score=report.review.grammar_score,
        content_score=report.review.content_score,
        structure_score=report.review.structure_score,
        clarity_score=report.review.clarity_score,
        academic_style_score=report.review.academic_style_score,
        created_at=report.review.created_at
    )

    sections_data = []
    for section in report.review.section_reviews:
        sections_data.append(SectionReviewResponse(
            id=section.id,
            section_name=section.section_name,
            section_order=section.section_order,
            score=section.score,
            content_preview=section.content_preview,
            strengths=section.strengths or [],
            weaknesses=section.weaknesses or [],
            suggestions=section.suggestions or [],
            priority=section.priority
        ))

    issues_data = []
    for issue in report.review.issues:
        issues_data.append(IssueResponse(
            id=issue.id,
            category=issue.category,
            severity=issue.severity,
            description=issue.description,
            location=issue.location,
            suggestion=issue.suggestion,
            line_number=issue.line_number
        ))

    return {
        "review": review_data,
        "sections": sections_data,
        "issues": issues_data
    }


@router.delete("/{report_id}", tags=["Reports"])
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a report and its associated data."""
    result = await db.execute(
        select(Report)
        .options(selectinload(Report.review))
        .where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    # Delete file from disk
    if os.path.exists(report.file_path):
        try:
            os.remove(report.file_path)
        except Exception:
            # Log error but continue with database deletion
            pass

    # Delete children explicitly (async sessions can't lazy-load for cascades)
    if report.review:
        await db.execute(delete(Issue).where(Issue.review_id == report.review.id))
        await db.execute(delete(SectionReview).where(SectionReview.review_id == report.review.id))
        await db.delete(report.review)

    await db.delete(report)
    await db.commit()

    return {"message": "Report deleted successfully"}


@router.get("/{report_id}/text", tags=["Reports"])
async def get_report_text(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the extracted text from a report."""
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if not report.extracted_text:
        return {"text": None, "message": "Text extraction not completed yet"}

    return {"text": report.extracted_text}
