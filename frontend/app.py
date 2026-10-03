import os
import sys
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv

# Project root
ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# Load local .env
load_dotenv(ROOT_DIR / ".env")

# LegalEase modules
from backend.ai_core.gemini_generator import GeminiDocumentGenerator
from backend.services.document_service import (
    format_docx,
    format_pdf,
    format_txt,
)
from backend.utils.text_utils import text_to_html


# Page configuration
st.set_page_config(
    page_title="LegalEase - AI Legal Document Generator",
    page_icon="⚖️",
    layout="wide",
)


# Title
st.title("⚖️ LegalEase")
st.subheader("AI-Powered Legal Document Generator")

st.write(
    "Create professional legal document drafts using the information "
    "you provide."
)

st.info(
    "LegalEase generates AI-assisted legal document drafts. "
    "Please review the generated document before using it."
)


# Sidebar
with st.sidebar:
    st.header("About LegalEase")

    st.write(
        "LegalEase helps generate customizable legal document drafts "
        "such as contracts, agreements, NDAs and lease documents."
    )

    st.divider()

    st.write("**Technology**")
    st.write("• Python")
    st.write("• Streamlit")
    st.write("• FastAPI")
    st.write("• Google Gemini")


# Input section
st.header("📄 Document Details")

document_type = st.text_input(
    "Document Type",
    placeholder="Example: Freelance Work Contract",
)

parties = st.text_area(
    "Parties",
    placeholder=(
        "Example:\n"
        "Client: ABC Technologies Pvt. Ltd.\n"
        "Freelancer: John Doe"
    ),
    height=120,
)

terms = st.text_area(
    "Terms and Conditions",
    placeholder=(
        "Example:\n"
        "Project: Website Development\n"
        "Duration: 3 months\n"
        "Payment: Rs. 50,000\n"
        "Work Location: Remote\n"
        "Confidentiality: Client information must remain confidential"
    ),
    height=220,
)

effective_date = st.date_input(
    "Effective Date"
)


# Generate button
if st.button(
    "🚀 Generate Legal Document",
    type="primary",
    use_container_width=True,
):

    # Validate inputs
    if not document_type.strip():
        st.error("Please enter the Document Type.")
        st.stop()

    if not parties.strip():
        st.error("Please enter the Parties.")
        st.stop()

    if not terms.strip():
        st.error("Please enter the Terms and Conditions.")
        st.stop()

    effective_date_string = effective_date.strftime("%Y-%m-%d")

    try:

        with st.spinner("🤖 Generating your legal document..."):

            generator = GeminiDocumentGenerator()

            generated_text = generator.generate_document(
                document_type=document_type.strip(),
                parties=parties.strip(),
                terms=terms.strip(),
                effective_date=effective_date_string,
            )

        if not generated_text:
            st.error("Gemini returned an empty document.")
            st.stop()

        st.session_state["generated_document"] = generated_text

        st.success("✅ Legal document generated successfully!")

    except Exception as exc:

        st.error("❌ Document generation failed.")

        st.error(str(exc))

        st.stop()


# Generated document section
if "generated_document" in st.session_state:

    st.divider()

    st.header("📝 Generated Document")

    edited_document = st.text_area(
        "Edit Document",
        value=st.session_state["generated_document"],
        height=600,
    )

    st.session_state["generated_document"] = edited_document

    # Preview
    st.subheader("👀 Preview")

    preview_html = text_to_html(edited_document)

    st.markdown(
        f"""
        <div style="
            border: 1px solid #cccccc;
            border-radius: 10px;
            padding: 25px;
            background-color: white;
            color: black;
            line-height: 1.7;
        ">
            {preview_html}
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Downloads
    st.divider()

    st.subheader("⬇️ Download Document")

    try:

        txt_data = format_txt(edited_document)
        docx_data = format_docx(edited_document)
        pdf_data = format_pdf(edited_document)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                "📄 Download TXT",
                data=txt_data,
                file_name="LegalEase_Document.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col2:
            st.download_button(
                "📝 Download DOCX",
                data=docx_data,
                file_name="LegalEase_Document.docx",
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True,
            )

        with col3:
            st.download_button(
                "📕 Download PDF",
                data=pdf_data,
                file_name="LegalEase_Document.pdf",
                mime="application/pdf",
                use_container_width=True,
            )

    except Exception as exc:

        st.error("Download preparation failed.")
        st.error(str(exc))


st.divider()

st.caption(
    "LegalEase © 2026 | AI-assisted legal document drafting tool"
)
