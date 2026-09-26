import os
import json
import logging
import re
from typing import Dict, List, Optional, Any
from datetime import datetime
import aiohttp
from app.core.config import settings

logger = logging.getLogger(__name__)


class AIServiceError(Exception):
    """Custom exception for AI service errors."""
    pass


class AIService:
    """
    Service for interacting with Generative AI API.
    Supports both real OpenAI API and demo mode.
    """

    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.model = settings.OPENAI_MODEL
        self.max_tokens = settings.OPENAI_MAX_TOKENS
        self.temperature = settings.OPENAI_TEMPERATURE
        self.base_url = settings.OPENAI_BASE_URL or "https://api.openai.com/v1"
        self.demo_mode = settings.DEMO_MODE or not self.api_key

    def _build_headers(self) -> Dict[str, str]:
        """Build API request headers."""
        if self.demo_mode:
            return {}
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _build_url(self, endpoint: str) -> str:
        """Build full API URL."""
        if self.demo_mode:
            return ""
        return f"{self.base_url}/{endpoint}"

    async def _make_request(self, payload: Dict[str, Any]) -> str:
        """
        Make request to AI API.
        Returns the response content or raises AIServiceError.
        """
        if self.demo_mode:
            # In demo mode, we won't make real API calls
            raise AIServiceError("API key not configured. Set OPENAI_API_KEY in .env file.")

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self._build_url("chat/completions"),
                    headers=self._build_headers(),
                    json=payload,
                    timeout=aiohttp.ClientTimeout(total=120)
                ) as response:
                    if response.status == 429:
                        raise AIServiceError("Rate limit exceeded. Please try again later.")
                    elif response.status == 401:
                        raise AIServiceError("Invalid API key. Please check your configuration.")
                    elif response.status != 200:
                        error_text = await response.text()
                        raise AIServiceError(f"API error: {response.status} - {error_text}")

                    data = await response.json()

                    if not data.get("choices") or not data["choices"][0].get("message"):
                        raise AIServiceError("Invalid response from AI API")

                    return data["choices"][0]["message"]["content"]

        except aiohttp.ClientError as e:
            logger.error(f"Network error: {str(e)}")
            raise AIServiceError(f"Network error: {str(e)}")
        except json.JSONDecodeError as e:
            logger.error(f"JSON decode error: {str(e)}")
            raise AIServiceError(f"Failed to parse API response: {str(e)}")

    def _chunk_text(self, text: str, max_chunk_size: int = 3000) -> List[str]:
        """
        Split text into chunks for processing large documents.
        Tries to split at paragraph boundaries.
        """
        if len(text) <= max_chunk_size:
            return [text]

        chunks = []
        paragraphs = text.split('\n\n')
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) + 2 > max_chunk_size and current_chunk:
                chunks.append(current_chunk.strip())
                current_chunk = para + "\n\n"
            else:
                if current_chunk:
                    current_chunk += para + "\n\n"
                else:
                    current_chunk = para + "\n\n"

        if current_chunk.strip():
            chunks.append(current_chunk.strip())

        # Limit number of chunks
        return chunks[:settings.MAX_CHUNKS]

    def _merge_chunk_results(self, chunks: List[Dict], full_text: str) -> Dict:
        """Merge results from multiple chunks into a single analysis."""
        # Combine strengths, weaknesses, issues from all chunks
        all_strengths = []
        all_weaknesses = []
        all_issues = []
        all_recommendations = []
        section_scores = {}
        section_reviews = []

        for chunk_result in chunks:
            if not chunk_result:
                continue

            all_strengths.extend(chunk_result.get("strengths", []))
            all_weaknesses.extend(chunk_result.get("weaknesses", []))
            all_issues.extend(chunk_result.get("issues", []))
            all_recommendations.extend(chunk_result.get("recommendations", []))

            # Merge section scores (average if same section appears multiple times)
            for section in chunk_result.get("sections", []):
                sec_name = section.get("section_name", "").lower()
                if sec_name:
                    if sec_name in section_scores:
                        # Average the scores
                        old = section_scores[sec_name]
                        new_score = section.get("score", 0)
                        section_scores[sec_name] = {
                            "section_name": section.get("section_name"),
                            "score": (old.get("score", 0) + new_score) / 2,
                            "strengths": list(set(old.get("strengths", []) + section.get("strengths", []))),
                            "weaknesses": list(set(old.get("weaknesses", []) + section.get("weaknesses", []))),
                            "suggestions": list(set(old.get("suggestions", []) + section.get("suggestions", []))),
                        }
                    else:
                        section_scores[sec_name] = section

        # Convert section_scores dict back to list
        section_reviews = list(section_scores.values())

        # Re-score overall based on section scores
        if section_reviews:
            avg_section_score = sum(s.get("score", 0) for s in section_reviews) / len(section_reviews)
        else:
            avg_section_score = 0

        # Calculate category scores
        grammar_score = self._calculate_category_score(all_issues, "grammar")
        content_score = self._calculate_category_score(all_issues, "content")
        structure_score = self._calculate_category_score(all_issues, "structure")
        clarity_score = self._calculate_category_score(all_issues, "clarity")
        academic_score = self._calculate_category_score(all_issues, "academic")

        # Overall score is weighted average
        overall_score = (
            avg_section_score * 0.4 +
            grammar_score * 0.15 +
            content_score * 0.15 +
            structure_score * 0.15 +
            clarity_score * 0.1 +
            academic_score * 0.05
        )
        overall_score = max(0, min(100, round(overall_score)))

        return {
            "overall_score": overall_score,
            "grammar_score": round(grammar_score),
            "content_score": round(content_score),
            "structure_score": round(structure_score),
            "clarity_score": round(clarity_score),
            "academic_style_score": round(academic_score),
            "summary": chunks[0].get("summary", "No summary available") if chunks else "",
            "strengths": all_strengths[:10],  # Limit to top 10
            "weaknesses": all_weaknesses[:10],
            "recommendations": all_recommendations[:10],
            "sections": section_reviews,
            "issues": all_issues[:20],  # Limit to top 20
        }

    def _calculate_category_score(self, issues: List[Dict], category: str) -> float:
        """Calculate score for a specific category based on issues."""
        category_issues = [i for i in issues if i.get("category", "").lower() == category.lower()]
        if not category_issues:
            return 90  # No issues in this category = high score

        # Calculate penalty based on severity
        severity_weights = {"critical": 15, "high": 10, "medium": 5, "low": 2}
        total_penalty = sum(severity_weights.get(i.get("severity", "low"), 2) for i in category_issues)
        score = max(0, 100 - total_penalty)
        return score

    async def analyze_report(self, extracted_text: str, report_title: str = "Report") -> Dict:
        """
        Analyze a report using AI and return structured review.
        """
        if not extracted_text or len(extracted_text.strip()) < 50:
            raise AIServiceError("Report content is too short for meaningful analysis")

        # Check if we need to chunk the text
        chunks = self._chunk_text(extracted_text)

        if len(chunks) == 1:
            # Single chunk - process directly
            result = await self._analyze_single_chunk(chunks[0], report_title)
            return self._validate_and_format_result(result)
        else:
            # Multiple chunks - process each and merge
            chunk_results = []
            for i, chunk in enumerate(chunks):
                logger.info(f"Processing chunk {i+1}/{len(chunks)}")
                try:
                    result = await self._analyze_single_chunk(chunk, f"{report_title} (Part {i+1})")
                    chunk_results.append(result)
                except AIServiceError as e:
                    logger.warning(f"Error processing chunk {i+1}: {str(e)}")
                    # Continue with other chunks
                    continue

            if not chunk_results:
                raise AIServiceError("Failed to process any chunks of the report")

            merged = self._merge_chunk_results(chunk_results, extracted_text)
            return self._validate_and_format_result(merged)

    async def _analyze_single_chunk(self, text: str, title: str) -> Dict:
        """Analyze a single chunk of text."""
        prompt = self._build_analysis_prompt(text, title)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert academic reviewer and editor. You analyze project reports and provide detailed, constructive feedback. Always respond in valid JSON format."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
        }

        response = await self._make_request(payload)
        return self._parse_json_response(response)

    def _build_analysis_prompt(self, text: str, title: str) -> str:
        """Build the prompt for AI analysis."""
        return f"""
You are an expert academic reviewer and editor. Analyze the following project report and provide a comprehensive review.

REPORT TITLE: {title}

REPORT CONTENT:
{text[:8000]}  # Limit text to avoid token issues

Please analyze the report and provide a detailed review in the following JSON format:

{{
    "overall_score": <number 0-100>,
    "overall_quality": "<Excellent/Good/Fair/Poor>",
    "summary": "<2-3 sentence overall assessment>",
    "grammar_score": <number 0-100>,
    "content_score": <number 0-100>,
    "structure_score": <number 0-100>,
    "clarity_score": <number 0-100>,
    "academic_style_score": <number 0-100>,
    "strengths": ["<strength 1>", "<strength 2>"],
    "weaknesses": ["<weakness 1>", "<weakness 2>"],
    "recommendations": ["<recommendation 1>", "<recommendation 2>"],
    "sections": [
        {{
            "section_name": "<section name>",
            "score": <number 0-100>,
            "strengths": ["<strength>"],
            "weaknesses": ["<weakness>"],
            "suggestions": ["<suggestion>"],
            "priority": "<critical|high|medium|low>"
        }}
    ],
    "issues": [
        {{
            "category": "<grammar|spelling|content|structure|clarity|academic|style|formatting|consistency>",
            "severity": "<critical|high|medium|low>",
            "description": "<issue description>",
            "location": "<section or paragraph reference>",
            "suggestion": "<how to fix>"
        }}
    ]
}}

Focus on:
1. Grammar, spelling, and punctuation
2. Sentence quality and clarity
3. Academic writing style and tone
4. Content completeness and depth
5. Logical flow and structure
6. Section organization
7. Technical accuracy and explanation quality
8. Consistency in terminology and formatting
9. Missing information or weak explanations
10. Overall academic quality

You MUST respond with valid JSON only. Do not include any text outside the JSON object.
"""

    def _parse_json_response(self, response: str) -> Dict:
        """Parse JSON from AI response, handling various formats."""
        # Try to extract JSON from response
        # Remove markdown code blocks if present
        json_match = re.search(r'\{[\s\S]*\}', response)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = response

        try:
            data = json.loads(json_str)
            return data
        except json.JSONDecodeError:
            logger.error(f"Failed to parse JSON response: {response[:500]}")
            # Return a fallback structure
            return self._get_fallback_analysis(text_preview=response[:200])

    def _get_fallback_analysis(self, text_preview: str = "") -> Dict:
        """Return a fallback analysis when AI parsing fails."""
        return {
            "overall_score": 50,
            "overall_quality": "Needs Review",
            "summary": "Unable to complete full AI analysis. Please try again or contact support.",
            "grammar_score": 50,
            "content_score": 50,
            "structure_score": 50,
            "clarity_score": 50,
            "academic_style_score": 50,
            "strengths": ["Report uploaded successfully"],
            "weaknesses": ["AI analysis encountered an issue"],
            "recommendations": ["Try uploading the report again"],
            "sections": [],
            "issues": [{
                "category": "system",
                "severity": "medium",
                "description": "AI analysis was unable to complete",
                "suggestion": "Please try again or use the demo mode"
            }]
        }

    def _validate_and_format_result(self, result: Dict) -> Dict:
        """Validate and ensure result has all required fields."""
        validated = {
            "overall_score": result.get("overall_score", 50),
            "overall_quality": result.get("overall_quality", "Needs Review"),
            "summary": result.get("summary", ""),
            "grammar_score": result.get("grammar_score", 50),
            "content_score": result.get("content_score", 50),
            "structure_score": result.get("structure_score", 50),
            "clarity_score": result.get("clarity_score", 50),
            "academic_style_score": result.get("academic_style_score", 50),
            "strengths": result.get("strengths", []),
            "weaknesses": result.get("weaknesses", []),
            "recommendations": result.get("recommendations", []),
            "sections": result.get("sections", []),
            "issues": result.get("issues", []),
        }

        # Ensure scores are within range
        for key in ["overall_score", "grammar_score", "content_score", "structure_score",
                     "clarity_score", "academic_style_score"]:
            if key in validated:
                validated[key] = max(0, min(100, validated[key] or 50))

        # Ensure sections are properly formatted
        for section in validated["sections"]:
            section.setdefault("score", 50)
            section.setdefault("strengths", [])
            section.setdefault("weaknesses", [])
            section.setdefault("suggestions", [])
            section.setdefault("priority", "medium")

        # Ensure issues are properly formatted
        for issue in validated["issues"]:
            issue.setdefault("severity", "medium")
            issue.setdefault("category", "general")
            issue.setdefault("suggestion", "")

        return validated

    async def improve_text(self, text: str, improvement_type: str,
                           instructions: Optional[str] = None,
                           report_context: Optional[str] = None) -> Dict:
        """
        Improve a section of text using AI.
        improvement_type: rewrite, academic, concise, expand, grammar, technical, simplify, custom
        """
        if not text or len(text.strip()) < 10:
            raise AIServiceError("Text is too short to improve")

        prompt = self._build_improvement_prompt(text, improvement_type, instructions, report_context)

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": "You are an expert academic editor. Help improve the given text according to the request. Return a JSON response with the improved text and explanation."},
                {"role": "user", "content": prompt}
            ],
            "max_tokens": min(self.max_tokens, len(text) * 3),
            "temperature": 0.3,
        }

        response = await self._make_request(payload)
        return self._parse_improvement_response(response, text, improvement_type)

    def _build_improvement_prompt(self, text: str, improvement_type: str,
                                   instructions: Optional[str],
                                   report_context: Optional[str]) -> str:
        """Build prompt for text improvement."""
        type_instructions = {
            "rewrite": "Rewrite the text to improve clarity, flow, and readability while maintaining the original meaning.",
            "academic": "Rewrite the text in formal academic language appropriate for a research paper or project report.",
            "concise": "Make the text more concise by removing redundancy and unnecessary words while preserving key information.",
            "expand": "Expand the text by adding more detail, explanation, and depth to make it more comprehensive.",
            "grammar": "Fix all grammar, spelling, punctuation, and syntax errors in the text.",
            "technical": "Improve the technical explanation and precision of the text. Make it more technically accurate and clear.",
            "simplify": "Simplify the text to make it easier to understand without losing important information.",
            "custom": instructions or "Improve the text according to best practices."
        }

        context_info = ""
        if report_context:
            context_info = f"\n\nREPORT CONTEXT:\n{report_context[:2000]}"

        return f"""
You are an expert academic editor. Help improve the following text.

IMPROVEMENT TYPE: {improvement_type}
INSTRUCTIONS: {type_instructions.get(improvement_type, "Improve the text")}
{context_info}

ORIGINAL TEXT:
{text}

Please improve the text and respond in this JSON format:
{{
    "improved_text": "<improved version of the text>",
    "explanation": "<brief explanation of what was changed and why>"
}}

You MUST respond with valid JSON only.
"""

    def _parse_improvement_response(self, response: str, original: str,
                                     improvement_type: str) -> Dict:
        """Parse improvement response from AI."""
        try:
            json_match = re.search(r'\{[\s\S]*\}', response)
            if json_match:
                data = json.loads(json_match.group(0))
                return {
                    "original_text": original,
                    "improved_text": data.get("improved_text", original),
                    "improvement_type": improvement_type,
                    "explanation": data.get("explanation", "")
                }
        except (json.JSONDecodeError, AttributeError):
            pass

        # Fallback: return improved text as-is if we can't parse
        return {
            "original_text": original,
            "improved_text": original,
            "improvement_type": improvement_type,
            "explanation": "Unable to process improvement request. Please try again."
        }

    async def chat_about_report(self, messages: List[Dict],
                                 report_context: Optional[str] = None,
                                 report_summary: Optional[str] = None) -> Dict:
        """
        Chat with AI about a specific report.
        messages: List of {"role": "user"|"assistant", "content": "..."}
        """
        # Build context from report
        context_parts = []
        if report_summary:
            context_parts.append(f"REPORT SUMMARY:\n{report_summary}")
        if report_context:
            # Include relevant portions of the report
            context_parts.append(f"REPORT CONTENT (relevant portions):\n{report_context[:3000]}")

        context = "\n\n".join(context_parts) if context_parts else "No report context available."

        # Build message history
        system_message = {
            "role": "system",
            "content": f"""You are an AI assistant helping a student improve their project report.
You have access to the following report information:
{context}

Provide helpful, specific, and constructive advice. Reference the report content when giving suggestions.
If asked to rewrite something, provide an improved version.
If asked about scores, explain what factors contribute to the score and how to improve."""
        }

        payload_messages = [system_message] + messages[-10:]  # Keep last 10 messages

        payload = {
            "model": self.model,
            "messages": payload_messages,
            "max_tokens": 1000,
            "temperature": 0.7,
        }

        response = await self._make_request(payload)

        # Generate suggested questions
        suggested_questions = self._generate_suggested_questions(messages, report_context)

        return {
            "response": response,
            "suggested_questions": suggested_questions
        }

    def _generate_suggested_questions(self, messages: List[Dict],
                                       report_context: Optional[str]) -> List[str]:
        """Generate suggested follow-up questions based on context."""
        suggestions = [
            "How can I improve my introduction?",
            "What is missing from my conclusion?",
            "Can you rewrite my problem statement?",
            "Is my methodology sufficiently explained?",
            "How can I make this more academic?",
        ]

        # Customize based on report content if available
        if report_context:
            lower_context = report_context.lower()
            if "methodology" in lower_context or "method" in lower_context:
                suggestions.append("Can you improve my methodology section?")
            if "result" in lower_context or "finding" in lower_context:
                suggestions.append("How should I present my results?")

        return suggestions[:5]

    async def is_api_available(self) -> bool:
        """Check if the AI API is available and configured."""
        if self.demo_mode:
            return False
        try:
            # Simple test request
            payload = {
                "model": self.model,
                "messages": [{"role": "user", "content": "Test"}],
                "max_tokens": 5,
            }
            await self._make_request(payload)
            return True
        except AIServiceError:
            return False


# Singleton instance
ai_service = AIService()
