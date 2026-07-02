import os
import json
import google.generativeai as genai
from backend.services.db_service import get_latest_snapshot

# Configure the Gemini API (Ensure GEMINI_API_KEY is in your .env or Render dashboard)
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def query_fiscal_ai(user_prompt: str) -> str:
    """Combines live database context with the user's prompt and queries the LLM."""
    
    # 1. Get current data context
    current_data = get_latest_snapshot()
    
    # 2. Build the System Prompt with RAG context
    system_instruction = f"""
    You are the US Fiscal Intelligence AI Assistant. 
    Your job is to answer user questions about the US economy based strictly on the current real-time data provided below.
    If the user asks something outside the scope of macroeconomics or the provided data, politely decline to answer.
    Be concise, professional, and use formatting (bullet points, bold text) to make numbers easy to read. Do not use markdown headers.
    
    CURRENT FISCAL DATA SNAPSHOT (JSON):
    {json.dumps(current_data, indent=2)}
    """
    
    try:
        # We use Gemini 1.5 Flash as it is lightning fast for chatbot responses
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_instruction
        )
        
        response = model.generate_content(user_prompt)
        return response.text
        
    except Exception as e:
        print(f"[AI Agent Error] {e}")
        return "I am currently experiencing connectivity issues with my intelligence core. Please try again later."
