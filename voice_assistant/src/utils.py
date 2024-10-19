from dotenv import load_dotenv
import os
import asyncio
import pyaudio
from deepgram import (
    DeepgramClient,
    LiveTranscriptionEvents,
    LiveOptions,
)

load_dotenv()


def remove_redundancy_with_punctuation(transcript):
    sentences = transcript.split(". ")
    unique_segments = []
    seen_segments = set()
    for sentence in sentences:
        words = sentence.split()
        normalized_sentence = " ".join(words).lower()
        if normalized_sentence not in seen_segments:
            seen_segments.add(normalized_sentence)
            unique_segments.append(sentence)
    cleaned_transcript = " ".join(unique_segments)
    cleaned_transcript = cleaned_transcript.replace("..", ".")
    cleaned_transcript = cleaned_transcript.strip()
    return cleaned_transcript


async def get_transcription(
    api_key, model="nova-2", language="fr-FR", endpointing=1000
):
    final_transcription = ""
    transcription_done = asyncio.Event()
    try:
        deepgram = DeepgramClient(api_key)
        dg_connection = deepgram.listen.websocket.v("1")

        def on_message(_, result, **kwargs):
            nonlocal final_transcription
            sentence = result.channel.alternatives[0].transcript
            if sentence:
                print(f"Transcript: {sentence}")
                final_transcription += sentence + " "
                if result.speech_final:
                    transcription_done.set()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model=model,
            smart_format=True,
            language=language,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            interim_results=True,
            utterance_end_ms=endpointing,
            vad_events=True,
        )

        if not dg_connection.start(options):
            print("Failed to connect to Deepgram")
            return ""

        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
        )
        try:
            while not transcription_done.is_set():
                data = stream.read(1024)
                dg_connection.send(data)
        except KeyboardInterrupt:
            print("\nStopped listening.")
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()
            dg_connection.finish()

        return remove_redundancy_with_punctuation(final_transcription.strip())
    except Exception as e:
        print(f"Error: {e}")
        return ""


if __name__ == "__main__":
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    transcript = asyncio.run(get_transcription(DEEPGRAM_API_KEY))
    print(f"Final transcription: {transcript}")
