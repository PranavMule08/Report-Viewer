from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import os
import enum


class ReportStatus(str, enum.Enum):
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    file_size = Column(Integer, nullable=False)  # in bytes
    file_type = Column(String(20), nullable=False)
    extracted_text = Column(Text, nullable=True)
    upload_date = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(String(20), default=ReportStatus.UPLOADED.value)
    error_message = Column(Text, nullable=True)

    # String-based references - resolved by SQLAlchemy registry, no import needed
    user = relationship("User", back_populates="reports")
    review = relationship("Review", back_populates="report", uselist=False, cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Report(id={self.id}, filename={self.filename}, status={self.status})>"
