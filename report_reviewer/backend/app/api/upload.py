import os
import uuid
import asyncio
import logging
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import Optional

from app.db.session import get_db
from app.models.user import User
from app.models.report import Report, ReportStatus
from app.schemas.schemas import ReportResponse, ReportCreate
from app.core.security import decode_access_token
from app.services.file_extractor import FileExtractor, FileExtractionError
from app.core.config import settings
from app.core.dependencies import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/upload", response_model=ReportResponse, tags=["File Upload"])
async def upload_file(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Upload a report file (PDF, DOCX, or TXT).
    The file will be saved and its text will be extracted.
    """
    # Validate file
    filename = file.filename or "unknown"
    content_type = file.content_type or ""

    # Check file extension
    file_ext = filename.lower().split('.')[-1] if '.' in filename else ''
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type '.{file_ext}' is not supported. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )

    # Read file content to check size and save
    content = await file.read()
    file_size = len(content)

    # Validate file size
    is_valid, error_msg = FileExtractor.validate_file(filename, file_size)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )

    # Generate unique filename
    unique_id = uuid.uuid4().hex[:12]
    safe_filename = f"{unique_id}_{filename}"
    file_path = os.path.join(settings.UPLOAD_DIR, safe_filename)

    # Save file
    try:
        with open(file_path, 'wb') as f:
            f.write(content)
    except Exception as e:
        logger.error(f"Failed to save file: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save uploaded file"
        )

    # Create report record
    report_data = ReportCreate(
        filename=safe_filename,
        original_filename=filename,
        file_path=file_path,
        file_size=file_size,
        file_type=file_ext
    )

    new_report = Report(
        user_id=current_user.id,
        filename=report_data.filename,
        original_filename=report_data.original_filename,
        file_path=report_data.file_path,
        file_size=report_data.file_size,
        file_type=report_data.file_type,
        status=ReportStatus.UPLOADED.value
    )

    db.add(new_report)
    await db.commit()
    await db.refresh(new_report)

    # Start async text extraction in background with its own DB session
    # Note: In a production app, this would be done with a task queue
    import asyncio
    asyncio.create_task(process_report_async(new_report.id, file_path, file_ext))

    return new_report


@router.get("/status/{report_id}", tags=["File Upload"])
async def get_upload_status(
    report_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get the processing status of a report."""
    result = await db.execute(
        select(Report).where(Report.id == report_id, Report.user_id == current_user.id)
    )
    report = result.scalar_one_or_none()

    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found"
        )

    return {
        "id": report.id,
        "filename": report.original_filename,
        "status": report.status,
        "error_message": report.error_message,
        "upload_date": report.upload_date,
        "extracted_text_length": len(report.extracted_text) if report.extracted_text else 0
    }


async def process_report_async(report_id: int, file_path: str, file_type: str):
    """Background task to process a report (extract text and analyze)."""
    # Create a fresh session - the request-scoped session is closed after the response
    from app.db.session import AsyncSessionLocal

    async with AsyncSessionLocal() as db:
        try:
            # Update status to processing
            await db.execute(
                update(Report)
                .where(Report.id == report_id)
                .values(status=ReportStatus.PROCESSING.value)
            )
            await db.commit()

            # Extract text (run sync extraction in a thread to avoid blocking)
            extracted_text = await asyncio.to_thread(
                FileExtractor.extract_text_sync, file_path, file_type
            )

            # Update report with extracted text
            await db.execute(
                update(Report)
                .where(Report.id == report_id)
                .values(
                    extracted_text=extracted_text,
                    status=ReportStatus.COMPLETED.value
                )
            )
            await db.commit()

            logger.info(f"Successfully extracted text from report {report_id}")

        except FileExtractionError as e:
            logger.error(f"Extraction error for report {report_id}: {str(e)}")
            await db.execute(
                update(Report)
                .where(Report.id == report_id)
                .values(
                    status=ReportStatus.FAILED.value,
                    error_message=str(e)
                )
            )
            await db.commit()
        except Exception as e:
            logger.error(f"Unexpected error processing report {report_id}: {str(e)}")
            await db.execute(
                update(Report)
                .where(Report.id == report_id)
                .values(
                    status=ReportStatus.FAILED.value,
                    error_message=f"Processing error: {str(e)}"
                )
            )
            await db.commit()


@router.get("/files", response_model=list[ReportResponse], tags=["File Upload"])
async def list_user_uploads(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all uploads for the current user."""
    result = await db.execute(
        select(Report)
        .where(Report.user_id == current_user.id)
        .order_by(Report.upload_date.desc())
    )
    reports = result.scalars().all()
    return reports
