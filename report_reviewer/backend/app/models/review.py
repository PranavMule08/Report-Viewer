from sqlalchemy import Column, Integer, String, Text, Float, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base


class Review(Base):
    __tablename__ = "reviews"

    id = Column(Integer, primary_key=True, index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    overall_score = Column(Float, nullable=True)
    overall_quality = Column(String(50), nullable=True)
    summary = Column(Text, nullable=True)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    grammar_score = Column(Float, nullable=True)
    content_score = Column(Float, nullable=True)
    structure_score = Column(Float, nullable=True)
    clarity_score = Column(Float, nullable=True)
    academic_style_score = Column(Float, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # String-based references - resolved by SQLAlchemy registry, no import needed
    report = relationship("Report", back_populates="review")
    section_reviews = relationship("SectionReview", back_populates="review", cascade="all, delete-orphan")
    issues = relationship("Issue", back_populates="review", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Review(id={self.id}, overall_score={self.overall_score})>"


class SectionReview(Base):
    __tablename__ = "section_reviews"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    section_name = Column(String(255), nullable=False)
    section_order = Column(Integer, nullable=True)
    score = Column(Float, nullable=True)
    content_preview = Column(Text, nullable=True)
    strengths = Column(JSON, default=list)
    weaknesses = Column(JSON, default=list)
    suggestions = Column(JSON, default=list)
    priority = Column(String(20), nullable=True)  # critical, high, medium, low
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="section_reviews")

    def __repr__(self):
        return f"<SectionReview(id={self.id}, section_name={self.section_name}, score={self.score})>"


class Issue(Base):
    __tablename__ = "issues"

    id = Column(Integer, primary_key=True, index=True)
    review_id = Column(Integer, ForeignKey("reviews.id"), nullable=False)
    category = Column(String(100), nullable=False)
    severity = Column(String(20), nullable=False)  # critical, high, medium, low
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=True)
    suggestion = Column(Text, nullable=True)
    line_number = Column(Integer, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    review = relationship("Review", back_populates="issues")

    def __repr__(self):
        return f"<Issue(id={self.id}, category={self.category}, severity={self.severity})>"
