import os
import httpx
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal
from fpdf import FPDF


API_KEY = "AIzaSyDAbfL_bXHaWvW8Ebp-XjYKpnLhD-YQgAo" 
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent"

app = FastAPI(title="Professional Legal AI Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


TaskMode = Literal[
    'correct', 'draft_affidavit', 'legal_notice', 'complaint_letter', 
    'contract_maker', 'document_summarizer', 'term_explainer', 
    'format_checker', 'tone_improver', 'contract_review'
]

class ProcessTextRequest(BaseModel):
    text: str
    mode: TaskMode

class ProcessTextResponse(BaseModel):
    processed_text: str

class PdfRequest(BaseModel):
    text: str
    title: str


@app.post("/process", response_model=ProcessTextResponse)
async def process_legal_text(request: ProcessTextRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")
    
    prompt = create_prompt_for_mode(request.text, request.mode)
    
    try:
        gemini_response = await call_gemini_api(prompt)
        return ProcessTextResponse(processed_text=gemini_response)
    except Exception as e:
        print(f"Error processing text with mode '{request.mode}': {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-pdf")
async def generate_pdf(request: PdfRequest):
    try:
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Times", 'B', 16)
        pdf.cell(0, 10, request.title, 0, 1, 'C')
        pdf.ln(10)
        pdf.set_font("Times", '', 12)
        cleaned_text = request.text.encode('latin-1', 'replace').decode('latin-1')
        pdf.multi_cell(0, 10, cleaned_text)
        pdf_output = pdf.output(dest='S').encode('latin-1')
        return Response(content=pdf_output, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=\"{request.title.replace(' ', '_')}.pdf\""})
    except Exception as e:
        print(f"PDF Generation Error: {e}")
        raise HTTPException(status_code=500, detail="An internal error occurred during PDF creation.")


def create_prompt_for_mode(text: str, mode: TaskMode) -> str:
    base_prompt = "You are an expert AI assistant for a law firm. Your response must be professional, accurate, and directly address the user's task. Only return the requested output and nothing else.\n\n"
    prompts = {
        'correct': "TASK: Correct the grammar, spelling, and punctuation of the following text. Preserve all legal terms, names, and dates. Maintain a formal tone.\n\nTEXT:\n'''{}'''",
        'draft_affidavit': "TASK: Draft a formal affidavit using the following details. Include a title, deponent introduction, numbered factual paragraphs, and a jurat for signature.\n\nDETAILS:\n'''{}'''",
        'legal_notice': "TASK: Draft a formal legal notice based on the following situation. Clearly state the sender, recipient, subject, the facts of the matter, the legal basis of the claim, and the relief sought.\n\nSITUATION:\n'''{}'''",
        'complaint_letter': "TASK: Write a formal complaint letter based on the user's description. Structure it professionally with sender/recipient details, date, a clear subject line, a body explaining the issue, and a call to action or desired resolution.\n\nDESCRIPTION:\n'''{}'''",
        'contract_maker': "TASK: Generate a simple, standard agreement or contract based on the user's requirements. Include standard clauses like parties, effective date, scope, payment terms, and governing law.\n\nREQUIREMENTS:\n'''{}'''",
        'document_summarizer': "TASK: Provide a concise, executive-level summary of the following legal document. Focus on the key facts, legal arguments, and the final outcome or conclusion.\n\nDOCUMENT:\n'''{}'''",
        'term_explainer': "TASK: Explain the following legal term or phrase in simple, clear language suitable for a non-lawyer. Provide a brief definition and a simple example.\n\nTERM:\n'''{}'''",
        'format_checker': "TASK: Review the following text for common legal document formatting errors. Check for consistent numbering, proper headings, and standard signature block format. Provide a list of suggested formatting improvements.\n\nTEXT:\n'''{}'''",
        'tone_improver': "TASK: Rewrite the following text to have a more professional, formal, and authoritative legal tone, suitable for court filings or official correspondence.\n\nORIGINAL TEXT:\n'''{}'''",
        'contract_review': "TASK: Act as a senior lawyer reviewing the following contract clause. Identify potential risks, ambiguities, or clauses that are unfavorable to your client. Present your findings as a bulleted list of concerns.\n\nCONTRACT CLAUSE:\n'''{}'''"
    }
    prompt_template = prompts.get(mode)
    return base_prompt + prompt_template.format(text)

async def call_gemini_api(prompt: str) -> str:
    headers = {'Content-Type': 'application/json', 'X-goog-api-key': API_KEY}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    async with httpx.AsyncClient(timeout=90.0) as client:
        response = await client.post(GEMINI_API_URL, json=payload, headers=headers)
        if response.status_code != 200:
            raise Exception(f"API call failed with status {response.status_code}: {response.text}")
        response_data = response.json()
        try:
            return response_data['candidates'][0]['content']['parts'][0]['text']
        except (KeyError, IndexError):
            raise Exception(f"Could not parse Gemini response: {response_data}")
