import os
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from .text_to_speech import text_to_speech
from .utils import get_transcription
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage
import sys

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)

from rag.prompts import (
    ANSWER_PROMPT,
    FIXING_QUESTION_PROMPT,
    FIXING_CONTEXT_PROMPT,
    TESTING_PROMPT,
)
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
            fixing_prompt = PromptTemplate(
                input_variables=["question"],
                template=FIXING_QUESTION_PROMPT,
            )

            fixing_chain = fixing_prompt | self.client | StrOutputParser()
            fixed_question = fixing_chain.invoke({"question": transcript})

            print(f"fixed question : {fixed_question}")

            fetched_question, fetched_context = query_question(
                fixed_question, vector_store, self.embeddings
            )
            # This chain is used for checking similarities between the fetched question from the db and the one fixed by the llm
            testing_prompt = PromptTemplate(
                input_variables=["q1", "q2"], template=TESTING_PROMPT
            )
            testing_chain = testing_prompt | self.client | StrOutputParser()
            test = testing_chain.invoke({"q1": fixed_question, "q2": fetched_question})
            print(f"test: {test}")
            if "false" in test.lower():
                "Desole. La question n'esxiste pas dans la base."
                return

            fixing_prompt = PromptTemplate(
                input_variables=["retrived_context"],
                template=FIXING_CONTEXT_PROMPT,
            )
            fixing_chain = fixing_prompt | self.client | StrOutputParser()
            fixed_context = fixing_chain.invoke({"retrived_context": fetched_context})

            print(f"fixed context : {fixed_context}")

            response = await self.client.ainvoke(
                input=[
                    HumanMessage(
                        ANSWER_PROMPT.format(
                            question=fixed_question, context=fixed_context
                        )
                    ),
                ]
            )
            print(f"response : {response}")

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
