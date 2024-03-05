import gradio as gr
from transformers import pipeline

get_completion = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

def get_completion(input):
    try:
        output = get_completion(input)
        return output[0]['summary_text']
    except Exception as e:
        return str(e)

def create_summarization_tab():
    gr.close_all()
    tab = gr.Interface(fn=get_completion, 
                    inputs=[gr.Textbox(label="Text to summarize", lines=6)],
                    outputs=[gr.Textbox(label="Result", lines=3)],
                    title="Text summarization with distilbart-cnn",
                    description="Summarize any text using the `shleifer/distilbart-cnn-12-6` model under the hood!"
                   )
    return tab