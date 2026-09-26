from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List

from app.db.session import get_db
from app.models.user import User
from app.models.report import Report
from app.schemas.schemas import ChatRequest, ChatResponse, ChatMessage
from app.core.dependencies import get_current_user
from app.services.ai_service import AIService, AIServiceError
from app.services.demo_service import DemoService, demo_service
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("", response_model=ChatResponse, tags=["Chat"])
async def chat_about_report(
    chat_request: ChatRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Chat with AI about a specific report.
    The AI uses the report content as context for its responses.
    """
    # Get report context if report_id is provided in the messages or context
    report_context = chat_request.report_context
    report_summary = chat_request.report_summary

    # If no context provided but we have messages mentioning a report, we need context
    # For simplicity, we'll use the provided context

    is_demo = settings.DEMO_MODE or not settings.OPENAI_API_KEY

    try:
        if is_demo:
            # Convert messages to dict format for demo service
            messages_dict = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.messages
            ]
            result = DemoService.generate_demo_chat_response(
                messages_dict,
                report_context or ""
            )
            response_text = result["response"]
            suggested_questions = result["suggested_questions"]
        else:
            # Use real AI service
            ai_service = AIService()
            messages_dict = [
                {"role": msg.role, "content": msg.content}
                for msg in chat_request.messages
            ]

            result = await ai_service.chat_about_report(
                messages_dict,
                report_context,
                report_summary
            )
            response_text = result["response"]
            suggested_questions = result["suggested_questions"]

    except AIServiceError as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat failed: {str(e)}"
        )

    return ChatResponse(
        response=response_text,
        suggested_questions=suggested_questions
    )


@router.get("/suggested-questions", tags=["Chat"])
async def get_suggested_questions(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get suggested questions for a report."""
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

    # Generate questions based on report content
    questions = [
        "How can I improve my introduction?",
        "What is missing from my conclusion?",
        "Can you rewrite my problem statement?",
        "Is my methodology sufficiently explained?",
        "How can I make this more academic?",
    ]

    # Add report-specific questions if we have the content
    if report.extracted_text:
        text_lower = report.extracted_text.lower()
        if "methodology" in text_lower or "method" in text_lower:
            questions.insert(2, "Can you improve my methodology section?")
        if "result" in text_lower or "finding" in text_lower:
            questions.append("How should I present my results?")
        if "literature" in text_lower or "review" in text_lower:
            questions.append("How can I improve my literature review?")

    return {"questions": questions[:8]}


@router.get("/context/{report_id}", tags=["Chat"])
async def get_report_context_for_chat(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get report context for the chat assistant."""
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

    response = {
        "report_id": report.id,
        "filename": report.original_filename,
        "extracted_text": report.extracted_text,
        "has_review": report.review is not None
    }

    if report.review:
        response["review_summary"] = report.review.summary
        response["overall_score"] = report.review.overall_score

    return response
