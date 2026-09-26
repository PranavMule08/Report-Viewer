import os
import logging
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from typing import Optional, List

from app.db.session import get_db
from app.models.user import User
from app.models.report import Report
from app.models.review import Review, SectionReview, Issue
from app.schemas.schemas import (
    ReviewResponse, SectionReviewResponse, IssueResponse,
    ImprovementRequest, ImprovementResponse,
    ReviewDetailResponse
)
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService, AIServiceError
from app.services.demo_service import DemoService, demo_service
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/{report_id}/analyze", tags=["Reviews"])
async def analyze_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Trigger AI analysis for a report.
    This will analyze the extracted text and generate a comprehensive review.
    """
    # Get the report
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

    if not report.extracted_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report text not extracted yet. Please wait for processing to complete."
        )

    if len(report.extracted_text.strip()) < 50:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Report content is too short for meaningful analysis"
        )

    # Check if demo mode
    is_demo = settings.DEMO_MODE or not settings.OPENAI_API_KEY

    try:
        if is_demo:
            # Use demo service
            analysis = DemoService.generate_demo_analysis(
                report.extracted_text,
                report.original_filename
            )
        else:
            # Use real AI service
            ai_service = AIService()
            analysis = await ai_service.analyze_report(
                report.extracted_text,
                report.original_filename
            )

    except AIServiceError as e:
        logger.error(f"AI analysis error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AI analysis failed: {str(e)}"
        )
    except Exception as e:
        logger.error(f"Unexpected error during analysis: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Analysis failed: {str(e)}"
        )

    # Save analysis to database
    # Delete any existing review for this report
    if report.review:
        await db.delete(report.review)
        await db.commit()

    # Create new review
    new_review = Review(
        report_id=report.id,
        overall_score=analysis.get("overall_score", 50),
        overall_quality=analysis.get("overall_quality", "Needs Review"),
        summary=analysis.get("summary", ""),
        strengths=analysis.get("strengths", []),
        weaknesses=analysis.get("weaknesses", []),
        recommendations=analysis.get("recommendations", []),
        grammar_score=analysis.get("grammar_score", 50),
        content_score=analysis.get("content_score", 50),
        structure_score=analysis.get("structure_score", 50),
        clarity_score=analysis.get("clarity_score", 50),
        academic_style_score=analysis.get("academic_style_score", 50),
    )

    db.add(new_review)
    await db.flush()  # Get the review ID

    # Save section reviews
    for section_data in analysis.get("sections", []):
        section_review = SectionReview(
            review_id=new_review.id,
            section_name=section_data.get("section_name", "Unknown"),
            section_order=section_data.get("section_order"),
            score=section_data.get("score", 50),
            content_preview=section_data.get("content_preview", "")[:500],
            strengths=section_data.get("strengths", []),
            weaknesses=section_data.get("weaknesses", []),
            suggestions=section_data.get("suggestions", []),
            priority=section_data.get("priority", "medium"),
        )
        db.add(section_review)

    # Save issues
    for issue_data in analysis.get("issues", []):
        issue = Issue(
            review_id=new_review.id,
            category=issue_data.get("category", "general"),
            severity=issue_data.get("severity", "medium"),
            description=issue_data.get("description", ""),
            location=issue_data.get("location"),
            suggestion=issue_data.get("suggestion", ""),
            line_number=issue_data.get("line_number"),
        )
        db.add(issue)

    await db.commit()

    return {
        "success": True,
        "message": "Analysis complete",
        "demo_mode": is_demo,
        "analysis": analysis
    }


@router.get("/{report_id}/review-data", response_model=ReviewDetailResponse, tags=["Reviews"])
async def get_review_data(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the complete review data for a report."""
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No review available for this report"
        )

    review = report.review

    return ReviewDetailResponse(
        review=ReviewResponse(
            id=review.id,
            report_id=review.report_id,
            overall_score=review.overall_score,
            overall_quality=review.overall_quality,
            summary=review.summary,
            strengths=review.strengths or [],
            weaknesses=review.weaknesses or [],
            recommendations=review.recommendations or [],
            grammar_score=review.grammar_score,
            content_score=review.content_score,
            structure_score=review.structure_score,
            clarity_score=review.clarity_score,
            academic_style_score=review.academic_style_score,
            created_at=review.created_at
        ),
        sections=[
            SectionReviewResponse(
                id=sr.id,
                section_name=sr.section_name,
                section_order=sr.section_order,
                score=sr.score,
                content_preview=sr.content_preview,
                strengths=sr.strengths or [],
                weaknesses=sr.weaknesses or [],
                suggestions=sr.suggestions or [],
                priority=sr.priority
            )
            for sr in sorted(review.section_reviews, key=lambda x: (x.section_order or 0))
        ],
        issues=[
            IssueResponse(
                id=issue.id,
                category=issue.category,
                severity=issue.severity,
                description=issue.description,
                location=issue.location,
                suggestion=issue.suggestion,
                line_number=issue.line_number
            )
            for issue in review.issues
        ]
    )


@router.post("/improve", response_model=ImprovementResponse, tags=["Reviews"])
async def improve_text(
    improvement_data: ImprovementRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Use AI to improve a section of text.
    improvement_type options: rewrite, academic, concise, expand, grammar, technical, simplify, custom
    """
    is_demo = settings.DEMO_MODE or not settings.OPENAI_API_KEY

    try:
        if is_demo:
            # Use demo service
            result = DemoService.generate_demo_improvement(
                improvement_data.text,
                improvement_data.improvement_type
            )
        else:
            # Use real AI service
            ai_service = AIService()
            result = await ai_service.improve_text(
                improvement_data.text,
                improvement_data.improvement_type,
                improvement_data.instructions,
                improvement_data.report_context
            )

    except AIServiceError as e:
        logger.error(f"Text improvement error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Text improvement failed: {str(e)}"
        )

    return ImprovementResponse(
        original_text=result["original_text"],
        improved_text=result["improved_text"],
        improvement_type=result["improvement_type"],
        explanation=result.get("explanation", "")
    )


@router.get("/categories/scores", tags=["Reviews"])
async def get_category_scores(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get scores broken down by category for a report."""
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    if not report.review:
        return {
            "review_available": False,
            "scores": {}
        }

    return {
        "review_available": True,
        "scores": {
            "overall": report.review.overall_score,
            "grammar": report.review.grammar_score,
            "content": report.review.content_score,
            "structure": report.review.structure_score,
            "clarity": report.review.clarity_score,
            "academic_style": report.review.academic_style_score
        }
    }
