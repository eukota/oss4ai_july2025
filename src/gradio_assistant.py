import gradio as gr
import tempfile
import scipy.io.wavfile
import numpy as np
from dotenv import load_dotenv

from livekit.plugins import (
    # openai,
    cartesia,
    deepgram,
    silero,
    noise_cancellation,
    google,
)
from tools import get_weather, search_web, translate_text
from prompts import AGENT_INSTRUCTION
from livekit.agents import Agent

load_dotenv()


# Minimal Assistant class without AgentSession or LiveKit
class Assistant:
    def __init__(self):
        self.stt = deepgram.STT(model="nova-3", language="multi")
        self.llm = google.LLM(model="gemini-1.5-flash")
        self.tts = cartesia.TTS(model="sonic-2", voice="78ab82d5-25be-4f7d-82b3-7ad64e5b85b2")
        self.vad = silero.VAD.load()

    # def transcribe(self, wav_path):
    #     return self.stt.transcribe(wav_path).text

    def respond(self, text):
        # Optionally add tools and instructions here
        return self.llm.respond(text)

    def synthesize(self, text):
        return self.tts.synthesize(text)


agent = Assistant()


# def handle_audio(audio_np, sample_rate):
def handle_audio(audio_tuple):
    if not isinstance(audio_tuple, (tuple, list)) or len(audio_tuple) != 2:
        raise ValueError(f"Expected (sample_rate, np_array) tuple but got: {audio_tuple}")

    sample_rate, audio_np = audio_tuple

    if not hasattr(audio_np, "dtype"):
        raise TypeError(f"Expected second element to be a NumPy array, got: {type(audio_np)}")

    # Save to WAV
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp:
        scipy.io.wavfile.write(tmp.name, sample_rate, audio_np)
        wav_path = tmp.name

    # transcript = agent.transcribe(wav_path)
    # print("Transcript:", transcript)

    response = agent.respond(transcript)
    print("LLM Response:", response)

    speech = agent.synthesize(response.text)

    return transcript, response.text, (speech.sample_rate, speech.samples)


iface = gr.Interface(
    fn=handle_audio,
    inputs=gr.Audio(sources="microphone", type="numpy", label="Speak"),
    outputs=[
        gr.Textbox(label="Transcript"),
        gr.Textbox(label="LLM Response"),
        gr.Audio(label="Spoken Reply")
    ],
    title="LiveKit Voice Agent (Local Gradio)",
)

if __name__ == "__main__":
    iface.launch(server_name="0.0.0.0", server_port=7860)
