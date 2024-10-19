import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from .text_to_speech import text_to_speech
from .utils import get_transcription

from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from rag.prompts import RAG_PROMPT, SYSTEM_PROMPT
from rag.utils import query_question
from rag.load_db import vector_store
from model import get_client

embeddings = HuggingFaceEmbeddings(
    model_name="Lajavaness/bilingual-embedding-small",
    model_kwargs={"trust_remote_code": True},
)

client = get_client()

load_dotenv()

DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")

STOP_COMMAND = "stop"


class VoiceAssistant:
    def __init__(self):
        self.transcript = ""
        self.embeddings = HuggingFaceEmbeddings(
            model_name="Lajavaness/bilingual-embedding-small",
            model_kwargs={"trust_remote_code": True},
        )
        self.client = get_client()

    async def process_audio(self):
        transcript = await get_transcription(os.getenv("DEEPGRAM_API_KEY"))
        print(f"Transcript in process_audio: {transcript}")
        return transcript

    async def get_ai_response(self, transcript):
        try:
            _, fetched_context = query_question(
                transcript, vector_store, self.embeddings
            )
            print(f"Fetched context: {fetched_context}")
            response = await self.client.ainvoke(
                input=[
                    SystemMessage(SYSTEM_PROMPT),
                    HumanMessage(
                        RAG_PROMPT.format(
                            question=transcript, vector_db_context=fetched_context
                        )
                    ),
                ]
            )
            print(
                RAG_PROMPT.format(
                    question=transcript, vector_db_context=fetched_context
                )
            )
            return response.content
        except Exception as e:
            print(f"Error in getting AI response: {e}")
            return "Sorry, I couldn't process that request."

    async def run(self):
        print("Voice assistant started. Say 'stop' to end the conversation.")
        while True:
            self.transcript = await self.process_audio()
            print(f"Received transcript: {self.transcript}")

            if STOP_COMMAND in self.transcript.lower():
                print("Stopping voice assistant...")
                return
            if self.transcript:
                ai_response = await self.get_ai_response(self.transcript)
                print(f"AI response: {ai_response}")
                text_to_speech(ai_response)
