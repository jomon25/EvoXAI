"""Extract structured trading concepts from research PDFs."""
import os, json, PyPDF2
from loguru import logger

class PaperParser:
    def __init__(self):
        self.use_openai = bool(os.getenv('OPENAI_API_KEY'))

    def extract_text(self, pdf_path: str, max_chars: int = 8000) -> str:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            text = ' '.join(p.extract_text() or '' for p in reader.pages)
            return text[:max_chars]

    def extract_concepts(self, pdf_path: str) -> list[dict]:
        text = self.extract_text(pdf_path)
        prompt = self._build_prompt(text)
        if self.use_openai:
            return self._call_openai(prompt)
        return self._call_ollama(prompt)

    def _build_prompt(self, text: str) -> str:
        return f'''Extract trading concepts. Return ONLY a JSON array: 
 [{{'concept':'name','style':'smc|ict|snr|intraday|swing|scalping',
 'entry_condition':'rule','exit_condition':'rule',
 'filters':['f1'],'confidence':0.0}}]
 Paper: {text}'''

    def _call_openai(self, prompt: str) -> list[dict]:
        from openai import OpenAI
        client = OpenAI()
        rsp = client.chat.completions.create(
            model='gpt-4', temperature=0.2,
            messages=[{'role':'user','content':prompt}])
        return json.loads(rsp.choices[0].message.content)

    def _call_ollama(self, prompt: str) -> list[dict]:
        import requests
        rsp = requests.post('http://localhost:11434/api/generate',
            json={'model':'llama3','prompt':prompt,'stream':False})
        return json.loads(rsp.json()['response'])
