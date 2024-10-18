from langchain_google_genai import ChatGoogleGenerativeAI
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))


def get_client():
    return ChatGoogleGenerativeAI(
        model="gemini-pro", convert_system_message_to_human=True
    )
