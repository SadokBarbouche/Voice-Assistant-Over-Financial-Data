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

async def get_transcription(api_key, model="nova-2", language="fr-FR", endpointing=500):
    final_transcription = ""
    transcription_done = asyncio.Event()

    try:
        deepgram = DeepgramClient(api_key)
        dg_connection = deepgram.listen.websocket.v("1")

        def on_message(self, result, **kwargs):
            nonlocal final_transcription  # Use the outer variable
            sentence = result.channel.alternatives[0].transcript
            if len(sentence) > 0:
                print(f"Transcript: {sentence}")
                final_transcription = sentence
                if result.speech_final:
                    transcription_done.set()

        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model=model,
            language=language,
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            interim_results=True,
            utterance_end_ms="1000",
            vad_events=True,
            endpointing=endpointing,
        )

        if not dg_connection.start(options):
            print("Failed to connect to Deepgram")
            return ""

        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paInt16,
                        channels=1,
                        rate=16000,
                        input=True,
                        frames_per_buffer=1024)

        print("Listening... Press Ctrl+C to stop.")
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

        return final_transcription
    except Exception as e:
        print(f"Error: {e}")
        return ""

if __name__ == "__main__":
    DEEPGRAM_API_KEY = os.getenv("DEEPGRAM_API_KEY")
    transcript = asyncio.run(get_transcription(DEEPGRAM_API_KEY))
    print(f"Final transcription: {transcript}")
