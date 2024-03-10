import gradio as gr
from transformers import pipeline
import numpy as np

# See
# https://discuss.huggingface.co/t/how-to-get-the-microphone-streaming-input-file-when-using-blocks/37204/2

transcriber = pipeline("automatic-speech-recognition", model="openai/whisper-base.en")
def transcribe(stream, new_chunk):
    sr, y = new_chunk
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    if stream is not None:
        stream = np.concatenate([stream, y])
    else:
        stream = y
        
    txt = transcriber({"sampling_rate": sr, "raw": stream})["text"]
    return stream, txt


def create_voice_tab():
    with gr.Blocks() as demo:
        state = gr.State(value="")
        with gr.Row():
            with gr.Column():
                audio = gr.Audio(sources=["microphone"], type="filepath") 
            with gr.Column():
                textbox = gr.Textbox()
        audio.stream(fn=transcribe, inputs=[audio, state], outputs=[textbox, state])
    return demo