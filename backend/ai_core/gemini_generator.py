from google import genai
from google.genai import types

from backend.config import GEMINI_API_KEY, GEMINI_MODEL, MOCK_AI
from backend.utils.text_utils import sanitize_text


class GeminiDocumentGenerator:
    """Gemini-backed legal document draft generator."""

    def __init__(self) -> None:
        self.model = GEMINI_MODEL
        self.mock = MOCK_AI
        self.client = None

        if not self.mock:
            if not GEMINI_API_KEY:
                raise RuntimeError(
                    "GEMINI_API_KEY is missing. Add it to .env or set MOCK_AI=true."
                )
            self.client = genai.Client(api_key=GEMINI_API_KEY)

    def generate_document(
        self,
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        if self.mock:
            return self._mock_document(
                document_type, parties, terms, effective_date
            )

        prompt = self._build_prompt(
            document_type, parties, terms, effective_date
        )

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(
                temperature=0.25,
                max_output_tokens=5000,
            ),
        )

        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")

        return sanitize_text(text)

    @staticmethod
    def _build_prompt(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        return f"""
You are the drafting engine for LegalEase, an AI-assisted legal document
drafting application.

Create a clear, professional LEGAL DOCUMENT DRAFT using the information below.

Document type:
{document_type}

Parties:
{parties}

Effective date:
{effective_date}

Terms and conditions:
{terms}

Requirements:
1. Create a professional title.
2. Include the effective date and identify the parties.
3. Organize the document into logical numbered sections.
4. Include the supplied terms without silently changing their meaning.
5. Add reasonable standard clauses relevant to the document type, such as
   definitions, obligations, confidentiality, termination, governing law,
   notices, severability, entire agreement, and signatures when appropriate.
6. Do not invent names, addresses, amounts, dates, laws, registration numbers,
   or other specific facts that were not provided. Use [TO BE COMPLETED] for
   necessary missing details.
7. Keep the language formal but readable.
8. End with signature blocks where appropriate.
9. Do not claim that the document is guaranteed legally valid or suitable for
   every jurisdiction.
10. Return only the document draft, without markdown code fences and without
    commentary about the drafting process.
""".strip()

    @staticmethod
    def _mock_document(
        document_type: str,
        parties: str,
        terms: str,
        effective_date: str,
    ) -> str:
        term_items = [
            item.strip().lstrip("-•").strip()
            for item in terms.replace("\n", ";").split(";")
            if item.strip()
        ]

        lines = [
            document_type.upper(),
            "",
            f"Effective Date: {effective_date}",
            f"Parties: {parties}",
            "",
            "1. PURPOSE",
            f"This document records the principal terms of the {document_type}.",
            "",
            "2. TERMS AND CONDITIONS",
        ]

        for index, item in enumerate(term_items, start=1):
            lines.append(f"{index}. {item}")

        lines.extend(
            [
                "",
                "3. CONFIDENTIALITY",
                "Each party should protect confidential information received in connection with this agreement, subject to applicable law.",
                "",
                "4. TERMINATION",
                "The parties may terminate this arrangement according to the termination terms agreed by them.",
                "",
                "5. GOVERNING LAW",
                "[TO BE COMPLETED: Insert the applicable jurisdiction and governing-law provision.]",
                "",
                "6. ENTIRE AGREEMENT",
                "This document represents the agreed terms identified by the parties, subject to applicable law and any incorporated documents.",
                "",
                "7. SIGNATURES",
                "",
                "Party 1: ______________________________",
                "Name: [TO BE COMPLETED]",
                "Date: _________________________________",
                "",
                "Party 2: ______________________________",
                "Name: [TO BE COMPLETED]",
                "Date: _________________________________",
                "",
                "DEMO MODE: This draft was generated locally without a Gemini API call.",
            ]
        )
        return "\n".join(lines)
