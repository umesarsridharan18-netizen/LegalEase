# LegalEase — AI-Powered Legal Document Generator

LegalEase is a FastAPI + Streamlit + Google Gemini application based on the supplied project documentation.

## Features
- Generate legal-document drafts from document type, parties, terms, and effective date
- Gemini AI integration
- Editable generated text
- TXT, DOCX and PDF export
- Branded DOCX/PDF with a generated LegalEase logo
- FastAPI health and generation APIs
- Streamlit frontend
- CORS configuration
- Environment-variable configuration
- Local mock generation mode for testing without an API key

> LegalEase generates document drafts for informational/educational use. It is not a substitute for advice from a qualified lawyer.

## Project structure

```text
LegalEase/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── schemas.py
│   ├── routes/
│   │   └── routes.py
│   ├── ai_core/
│   │   └── gemini_generator.py
│   ├── services/
│   │   └── document_service.py
│   └── utils/
│       └── text_utils.py
├── frontend/
│   └── app.py
├── assets/
│   └── logo.png
├── tests/
│   └── test_api.py
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Requirements
- Python 3.10+
- Internet connection for Gemini generation
- A Gemini API key for live AI generation

## Windows setup in VS Code

### 1. Extract the ZIP
Extract `LegalEase.zip` somewhere such as:

```text
C:\Users\<YourName>\Documents\LegalEase
```

Open that **LegalEase folder** in VS Code.

### 2. Open a terminal
VS Code:
`Terminal` → `New Terminal`

Check Python:

```powershell
python --version
```

### 3. Create a virtual environment

```powershell
python -m venv .venv
```

### 4. Activate it

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt in VS Code:

```cmd
.venv\Scripts\activate
```

You should see `(.venv)` at the start of the terminal line.

### 5. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Create the environment file

Copy:

```text
.env.example
```

and rename the copy to:

```text
.env
```

Put your Gemini API key in `.env`.

Example:

```env
GEMINI_API_KEY=your_real_key_here
GEMINI_MODEL=gemini-3.8-flash
BACKEND_URL=http://127.0.0.1:8000
CORS_ORIGINS=http://localhost:8501,http://127.0.0.1:8501
```

The model is configurable because model availability changes over time. Do not put your API key into source code.

### 7. Start the FastAPI backend

Keep terminal 1 open:

```powershell
python -m uvicorn backend.main:app --reload --host 127.0.0.1 --port 8000
```

Test in the browser:

```text
http://127.0.0.1:8000/
```

You should see a JSON response showing the backend is running.

API documentation:

```text
http://127.0.0.1:8000/docs
```

### 8. Start Streamlit

Open **another VS Code terminal** and activate the environment again if necessary:

```powershell
.\.venv\Scripts\Activate.ps1
```

Then:

```powershell
streamlit run frontend/app.py
```

Open the Streamlit URL shown in the terminal, normally:

```text
http://localhost:8501
```

## 9. Test the application

Use these sample values:

Document Type:
```text
Freelance Work Contract
```

Parties:
```text
Jane Doe (Service Provider), TechNova Inc. (Client)
```

Terms:
```text
Payment to be made within 30 days of invoice;
The provider agrees to deliver work by the agreed deadline;
Confidentiality must be maintained;
Either party may terminate with 15 days notice
```

Effective Date:
```text
October 1, 2026
```

Click **Generate Document**.

Then:
1. Review the generated draft.
2. Edit the text if needed.
3. Download TXT.
4. Download DOCX.
5. Download PDF.

## Testing without Gemini

If you do not have a Gemini API key yet, set:

```env
MOCK_AI=true
```

Then restart FastAPI.

The app will generate a clearly labelled demo document without calling Gemini. This lets you test the complete frontend/backend/export pipeline first.

For live Gemini generation:

```env
MOCK_AI=false
GEMINI_API_KEY=your_real_key
```

## API

### GET /
Health/status endpoint.

### GET /health
Health endpoint.

### POST /generate

Request:

```json
{
  "document_type": "Non-Disclosure Agreement",
  "parties": "Jane Doe (Disclosing Party), TechNova Inc. (Receiving Party)",
  "terms": "Confidentiality; No unauthorized disclosure; Return confidential information",
  "effective_date": "October 1, 2026"
}
```

Response:

```json
{
  "document": "generated text...",
  "model": "configured model name",
  "mock": false
}
```

## Common Windows issue

If you get:

```text
npm ERR! enoent Could not read package.json
```

do not use `npm` for this project. LegalEase is a Python FastAPI + Streamlit application, so use:

```powershell
pip install -r requirements.txt
```

and start it with the Python/Streamlit commands in this README.

## Troubleshooting

### ModuleNotFoundError
Make sure `(.venv)` is active and run:

```powershell
pip install -r requirements.txt
```

### Port 8000 already in use

```powershell
python -m uvicorn backend.main:app --reload --port 8001
```

Then update `.env`:

```env
BACKEND_URL=http://127.0.0.1:8001
```

### Streamlit cannot connect to backend
Confirm FastAPI is running first:

```text
http://127.0.0.1:8000/health
```

### Gemini error
Check:
- API key is correct
- `.env` is in the LegalEase root folder
- `MOCK_AI=false`
- configured model is available to your Gemini API account

You can temporarily use:

```env
MOCK_AI=true
```

to verify that the rest of the application works.

## Production note

Before public deployment, add authentication, rate limiting, persistent storage, audit logging, secrets management, stronger privacy controls, and legal review of generated templates.
