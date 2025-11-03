import os
from dotenv import load_dotenv

load_dotenv()

class Secrets:
    def __init__(self):
        self.gemini_api_key = "GEMINI_API_KEY"
        self.gemini_api_model = "GEMINI_MODEL"
        self.gemini_base_url = "https://generativelanguage.googleapis.com/v1beta/openai/"
        self.modal_summarizer_url = "MODAL_WEB_ENDPOINT_URL"