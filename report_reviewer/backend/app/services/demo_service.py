import random
import re
from typing import Dict, List


class DemoService:
    """
    Demo mode service that generates realistic-looking analysis
    when the AI API is not available.
    This is EXPLICITLY marked as demo/simulated output.
    """

    @staticmethod
    def generate_demo_analysis(text: str, title: str = "Report") -> Dict:
        """Generate a demo analysis for testing purposes."""

        # Basic text analysis to make demo somewhat realistic
        word_count = len(text.split())
        sentence_count = len(re.split(r'[.!?]+', text))
        avg_sentence_length = word_count / max(sentence_count, 1)

        # Detect potential sections
        sections = DemoService._detect_sections(text)

        # Generate issues based on text analysis
        issues = DemoService._generate_demo_issues(text, sections)

        # Calculate scores based on simple heuristics
        grammar_score = DemoService._calculate_grammar_score(text)
        content_score = DemoService._calculate_content_score(word_count, sections)
        structure_score = DemoService._calculate_structure_score(sections)
        clarity_score = DemoService._calculate_clarity_score(avg_sentence_length)
        academic_score = DemoService._calculate_academic_score(text)

        overall_score = int(
            grammar_score * 0.2 +
            content_score * 0.25 +
            structure_score * 0.2 +
            clarity_score * 0.2 +
            academic_score * 0.15
        )

        quality_levels = ["Excellent", "Good", "Fair", "Needs Improvement", "Poor"]
        quality_index = min(4, max(0, overall_score // 25))
        overall_quality = quality_levels[quality_index]

        demo_notice = "⚠️ DEMO MODE: This is simulated analysis for demonstration purposes. Connect an AI API key for real analysis."

        return {
            "overall_score": overall_score,
            "overall_quality": overall_quality,
            "summary": f"This report contains approximately {word_count} words across {len(sections)} detected sections. {demo_notice}",
            "grammar_score": grammar_score,
            "content_score": content_score,
            "structure_score": structure_score,
            "clarity_score": clarity_score,
            "academic_style_score": academic_score,
            "strengths": [
                f"Report contains {word_count} words of content",
                "Document structure is present",
                "Topic coverage appears adequate"
            ],
            "weaknesses": [
                "Some sentences may be too long or complex",
                "Academic tone could be strengthened",
                "Consider adding more specific examples and evidence"
            ],
            "recommendations": [
                "Review sentence structure for clarity",
                "Add more technical details to support claims",
                "Ensure consistent use of terminology throughout",
                "Proofread for grammar and spelling errors",
                "Add a clear conclusion summarizing key findings"
            ],
            "sections": DemoService._generate_section_reviews(sections, text),
            "issues": issues,
            "demo_mode": True,
            "demo_notice": demo_notice
        }

    @staticmethod
    def _detect_sections(text: str) -> List[Dict]:
        """Detect potential sections in the text."""
        common_sections = [
            "abstract", "introduction", "background", "problem statement",
            "objectives", "literature review", "methodology", "methods",
            "system design", "implementation", "results", "findings",
            "discussion", "analysis", "conclusion", "references",
            "acknowledgements", "appendix"
        ]

        sections = []
        lines = text.split('\n')
        current_section = None
        current_content = []

        for line in lines:
            line_lower = line.lower().strip()
            # Check if line is a section heading
            is_heading = False
            detected_section = None

            for section in common_sections:
                if line_lower.startswith(section) and len(line) < 100:
                    is_heading = True
                    detected_section = section.title()
                    break

            # Also check for numbered sections
            if re.match(r'^\d+\.?\s+\w+', line.strip()) and len(line) < 100:
                is_heading = True
                detected_section = line.strip()[:50]

            if is_heading and current_section:
                # Save previous section
                sections.append({
                    "section_name": current_section,
                    "content": ' '.join(current_content)[-500:] if current_content else "",
                    "word_count": len(' '.join(current_content).split())
                })
                current_content = []

            if is_heading:
                current_section = detected_section
            else:
                current_content.append(line)

        # Save last section
        if current_section:
            sections.append({
                "section_name": current_section,
                "content": ' '.join(current_content)[-500:] if current_content else "",
                "word_count": len(' '.join(current_content).split())
            })

        return sections

    @staticmethod
    def _generate_section_reviews(sections: List[Dict], full_text: str) -> List[Dict]:
        """Generate demo section reviews."""
        reviews = []

        for i, section in enumerate(sections):
            word_count = section.get("word_count", 0)
            base_score = 60 + random.randint(-10, 20)

            # Adjust score based on section content
            if word_count < 50:
                base_score -= 20  # Too short
            elif word_count > 500:
                base_score += 10  # Substantial content

            review = {
                "section_name": section["section_name"],
                "section_order": i + 1,
                "score": min(100, max(0, base_score)),
                "content_preview": section.get("content", "")[:200],
                "strengths": DemoService._generate_section_strengths(section),
                "weaknesses": DemoService._generate_section_weaknesses(section),
                "suggestions": DemoService._generate_section_suggestions(section),
                "priority": "medium" if base_score < 70 else "low"
            }
            reviews.append(review)

        return reviews

    @staticmethod
    def _generate_section_strengths(section: Dict) -> List[str]:
        """Generate demo strengths for a section."""
        strengths = []
        word_count = section.get("word_count", 0)
        name = section.get("section_name", "")

        if word_count > 100:
            strengths.append(f"Contains substantial content ({word_count} words)")
        if "introduction" in name.lower():
            strengths.append("Introduces the topic clearly")
        elif "methodology" in name.lower() or "method" in name.lower():
            strengths.append("Describes the approach being used")
        elif "result" in name.lower() or "finding" in name.lower():
            strengths.append("Presents findings")
        elif "conclusion" in name.lower():
            strengths.append("Provides concluding remarks")

        if not strengths:
            strengths.append("Section content is present")

        return strengths[:2]

    @staticmethod
    def _generate_section_weaknesses(section: Dict) -> List[str]:
        """Generate demo weaknesses for a section."""
        weaknesses = []
        word_count = section.get("word_count", 0)
        name = section.get("section_name", "")

        if word_count < 50:
            weaknesses.append("Section appears too brief - consider expanding")
        elif word_count < 100:
            weaknesses.append("Could benefit from more detailed explanation")

        if "introduction" in name.lower():
            weaknesses.append("Could better establish the research context")
        elif "methodology" in name.lower():
            weaknesses.append("Consider adding more specific details about the approach")
        elif "conclusion" in name.lower():
            weaknesses.append("Could better summarize key findings and implications")

        if not weaknesses:
            weaknesses.append("Some areas could be elaborated further")

        return weaknesses[:2]

    @staticmethod
    def _generate_section_suggestions(section: Dict) -> List[str]:
        """Generate demo suggestions for a section."""
        suggestions = []
        name = section.get("section_name", "")

        if "introduction" in name.lower():
            suggestions.append("Add more context about why this topic is important")
            suggestions.append("Clearly state the research objectives or questions")
        elif "methodology" in name.lower():
            suggestions.append("Describe the specific methods and tools used")
            suggestions.append("Explain the rationale for choosing this approach")
        elif "result" in name.lower() or "finding" in name.lower():
            suggestions.append("Include more specific data and measurements")
            suggestions.append("Use tables or figures to present results clearly")
        elif "conclusion" in name.lower():
            suggestions.append("Summarize the main contributions of the work")
            suggestions.append("Suggest directions for future work")

        if not suggestions:
            suggestions.append("Review and refine the content for clarity")

        return suggestions[:2]

    @staticmethod
    def _generate_demo_issues(text: str, sections: List[Dict]) -> List[Dict]:
        """Generate demo issues based on text analysis."""
        issues = []

        # Check for common issues
        if len(text) < 500:
            issues.append({
                "category": "content",
                "severity": "high",
                "description": "Report appears to be very short",
                "location": "entire document",
                "suggestion": "Expand the report with more detail and analysis"
            })

        # Check for repeated words (simple repetition check)
        words = text.lower().split()
        word_freq = {}
        for word in words:
            if len(word) > 3:
                word_freq[word] = word_freq.get(word, 0) + 1

        repeated_words = [w for w, c in word_freq.items() if c > len(words) * 0.05]
        if repeated_words:
            issues.append({
                "category": "style",
                "severity": "medium",
                "description": f"Word repetition detected: {', '.join(repeated_words[:3])}",
                "location": "throughout document",
                "suggestion": "Use synonyms and vary vocabulary"
            })

        # Check for very long sentences
        sentences = re.split(r'[.!?]+', text)
        long_sentences = [s.strip() for s in sentences if len(s.split()) > 30]
        if long_sentences:
            issues.append({
                "category": "clarity",
                "severity": "medium",
                "description": f"Found {len(long_sentences)} sentences longer than 30 words",
                "location": "various locations",
                "suggestion": "Break long sentences into shorter ones for better readability"
            })

        # Add section-specific issues
        for section in sections:
            if section.get("word_count", 0) < 50:
                issues.append({
                    "category": "content",
                    "severity": "medium",
                    "description": f"Section '{section['section_name']}' is very brief",
                    "location": section["section_name"],
                    "suggestion": "Expand this section with more detail"
                })

        # Add some grammar-style issues (simulated)
        if len(issues) < 3:
            issues.append({
                "category": "grammar",
                "severity": "low",
                "description": "Some sentences may have subject-verb agreement issues",
                "location": "throughout document",
                "suggestion": "Proofread carefully for grammar errors"
            })

        return issues[:10]

    @staticmethod
    def _calculate_grammar_score(text: str) -> int:
        """Simple heuristic grammar score."""
        score = 85

        # Penalize for common issues
        if "  " in text:  # Double spaces
            score -= 5

        # Check for common misspellings (basic)
        common_errors = ["teh", "recieve", "seperate", "occured", "definately"]
        found_errors = [e for e in common_errors if e in text.lower()]
        if found_errors:
            score -= len(found_errors) * 3

        return max(0, min(100, score))

    @staticmethod
    def _calculate_content_score(word_count: int, sections: List[Dict]) -> int:
        """Simple heuristic content score."""
        score = 70

        if word_count > 1000:
            score += 10
        elif word_count < 300:
            score -= 15

        section_count = len(sections)
        if section_count >= 5:
            score += 10
        elif section_count < 3:
            score -= 10

        return max(0, min(100, score))

    @staticmethod
    def _calculate_structure_score(sections: List[Dict]) -> int:
        """Simple heuristic structure score."""
        score = 75

        section_count = len(sections)
        if section_count >= 6:
            score += 10
        elif section_count < 3:
            score -= 15

        # Check for typical report structure
        section_names = [s["section_name"].lower() for s in sections]
        has_intro = any("intro" in s for s in section_names)
        has_conclusion = any("conclusion" in s for s in section_names)

        if has_intro and has_conclusion:
            score += 5
        else:
            score -= 5

        return max(0, min(100, score))

    @staticmethod
    def _calculate_clarity_score(avg_sentence_length: float) -> int:
        """Simple heuristic clarity score based on sentence length."""
        score = 80

        if avg_sentence_length > 25:
            score -= 10
        elif avg_sentence_length < 10:
            score -= 5

        return max(0, min(100, score))

    @staticmethod
    def _calculate_academic_score(text: str) -> int:
        """Simple heuristic academic style score."""
        score = 70

        # Check for informal language
        informal_phrases = ["i think", "in my opinion", "cool", "awesome", "stuff"]
        found_informal = [p for p in informal_phrases if p in text.lower()]
        if found_informal:
            score -= len(found_informal) * 5

        # Check for first person
        first_person_count = len(re.findall(r'\b(i|we|our)\b', text.lower()))
        if first_person_count > 10:
            score -= 5

        # Check for technical vocabulary
        technical_terms = ["analysis", "method", "data", "result", "study",
                          "research", "experiment", "system", "algorithm", "performance"]
        found_technical = [t for t in technical_terms if t in text.lower()]
        score += min(10, len(found_technical))

        return max(0, min(100, score))

    @staticmethod
    def generate_demo_improvement(original_text: str, improvement_type: str) -> Dict:
        """Generate demo text improvement."""
        if not original_text:
            return {
                "original_text": original_text,
                "improved_text": original_text,
                "improvement_type": improvement_type,
                "explanation": "No text to improve"
            }

        improved = original_text  # Default: no change

        if improvement_type == "grammar":
            # Simple "improvements" - in real demo, this would be more sophisticated
            improved = original_text.replace("  ", " ")  # Remove double spaces
            explanation = "Removed extra spaces and performed basic grammar check."
        elif improvement_type == "concise":
            # Truncate to simulate conciseness
            words = original_text.split()
            if len(words) > 50:
                improved = ' '.join(words[:50]) + "..."
            explanation = "Condensed the text while preserving key information."
        elif improvement_type == "academic":
            explanation = "Rewritten in more formal academic language. (Demo: actual rewording requires AI)"
        else:
            explanation = f"Text improvement applied for type: {improvement_type}. (Demo mode: connect AI API for real improvements)"

        return {
            "original_text": original_text,
            "improved_text": improved,
            "improvement_type": improvement_type,
            "explanation": explanation
        }

    @staticmethod
    def generate_demo_chat_response(messages: List[Dict], report_context: str = "") -> Dict:
        """Generate demo chat response."""
        last_message = messages[-1] if messages else {"content": "Hello"}
        user_question = last_message.get("content", "").lower()

        # Generate contextual response
        if "introduction" in user_question:
            response = "Your introduction provides a good starting point. To strengthen it, consider adding: 1) More context about why this topic matters, 2) Clear research objectives, 3) A brief overview of your methodology. (Demo response - connect AI API for personalized feedback)"
        elif "conclusion" in user_question:
            response = "A good conclusion should: 1) Summarize your main findings, 2) Discuss implications, 3) Acknowledge limitations, 4) Suggest future work. Review your conclusion against these points. (Demo response)"
        elif "methodology" in user_question:
            response = "For your methodology section, ensure you clearly describe: 1) Your research approach, 2) Data collection methods, 3) Analysis techniques, 4) Why you chose this approach. (Demo response)"
        elif "improve" in user_question or "rewrite" in user_question:
            response = "I can help improve that section. In production mode with an AI API connected, I would provide specific rewrites and suggestions. For now, consider: using clearer language, adding specific examples, and ensuring logical flow. (Demo response)"
        else:
            response = f"Thank you for your question about '{last_message.get('content', '')}'. I'd be happy to help you improve your report. Try asking specific questions about sections you'd like to improve. (Demo response - connect AI API for real analysis)"

        suggested_questions = [
            "How can I improve my introduction?",
            "What's missing from my conclusion?",
            "Can you review my methodology?",
            "How can I make this more academic?",
        ]

        return {
            "response": response,
            "suggested_questions": suggested_questions,
            "demo_mode": True
        }


# Singleton instance
demo_service = DemoService()
