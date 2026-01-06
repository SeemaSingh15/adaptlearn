import google.generativeai as genai
from config import settings
import requests
import json

# Configure Gemini
if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)

class LLMService:
    def __init__(self):
        self.provider = settings.LLM_PROVIDER
        self.ollama_base = settings.OLLAMA_BASE_URL
        self.ollama_model = settings.OLLAMA_MODEL

    async def generate_text(self, prompt: str) -> str:
        if self.provider == "gemini":
            return await self._generate_gemini(prompt)
        else:
            return await self._generate_ollama(prompt)

    async def generate_quiz(self, context: str) -> str:
        prompt = f"""
        Based on the following learning context, create a short multiple-choice quiz (1 question).
        Return purely valid JSON with no markdown headers. Format:
        {{
            "question": "The question string",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0, // Index of correct option
            "explanation": "Why this is correct"
        }}

        Context: {context}
        """
        if self.provider == "gemini":
            return await self._generate_gemini(prompt, json_mode=True)
        else:
            return await self._generate_ollama(prompt, json_mode=True)

    async def _generate_gemini(self, prompt: str, json_mode: bool = False) -> str:
        try:
            model = genai.GenerativeModel('gemini-pro')
            # Enhance prompt if not json (already enhanced for quiz)
            final_prompt = prompt
            if not json_mode:
                final_prompt = f"You are an expert tutor. Format your answer in clean Markdown. Use bold for key terms, bullet points for lists, and code blocks for code. \n\nUser Question: {prompt}"
            
            response = await model.generate_content_async(final_prompt)
            text = response.text
            if json_mode:
                # Cleanup if model returns markdown wrapping
                text = text.replace("```json", "").replace("```", "").strip()
            return text
        except Exception as e:
            if json_mode:
                 return json.dumps({"error": str(e)}) # Return empty JSON-like error
            return f"Error with Gemini: {str(e)}"

    async def _generate_ollama(self, prompt: str, json_mode: bool = False) -> str:
        try:
            url = f"{self.ollama_base}/generate"
            final_prompt = prompt
            if not json_mode:
                final_prompt = f"You are an expert tutor. Format your answer in clean Markdown. Use bold for key terms, bullet points for lists, and code blocks for code. \n\nUser Question: {prompt}"
            
            payload = {
                "model": self.ollama_model,
                "prompt": final_prompt,
                "stream": False,
                "format": "json" if json_mode else None
            }
            # Using synchronous requests for simplicity here
            response = requests.post(url, json=payload)
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Ollama Error: {response.text}"
        except Exception as e:
            return f"Error with Ollama (is it running?): {str(e)}"

llm_service = LLMService()
