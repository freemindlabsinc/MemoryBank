import random
import time
import gradio as gr
from security.functions import Authentication
from ui.summarization import create_summarization_tab
from ui.image_captioning import create_image_captioning_tab
from ui.entity_recognition import create_entity_recognition_tab
from ui.chat import create_chat_tab
from ui.voice import create_voice_tab
# Gradio app

def build_gradio_ui():
    summarization_tab = create_summarization_tab()
    imagecaptioning_tab = create_image_captioning_tab()
    entity_recognition_tab = create_entity_recognition_tab()
    chat_tab = create_chat_tab()
    voice_tab = create_voice_tab()
    
    demo = gr.TabbedInterface(
        title="Machine Learning & Streaming Chat",
        # [voice_tab, file_manager_tab], 
        interface_list= [summarization_tab, imagecaptioning_tab, entity_recognition_tab, chat_tab, voice_tab], 
        #["Voice", "File Manager"])
        tab_names = ["Summarization", "Image Captioning", "Entity Recognition", "Chat", "Voice"],         
        css="footer {visibility: hidden}",
    )
    demo.auth = Authentication.authenticate_user
    demo.auth_message = None
    
    return demo

def build_gradio_ui_old():
    with gr.Blocks() as ui:
        ui.auth = Authentication.authenticate_user
        ui.auth_message = None        
        
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        clear = gr.ClearButton([msg, chatbot])
        gr.Button("Logout", link="/logout", scale=0, min_width=50)

        def user(user_message, history, request: gr.Request):
            if request:
                un = request.username
                pass
            
            return gr.update(value="", interactive=False), history + [[user_message, None]]

        def bot(history, request: gr.Request):
            un = request.username or "Unknown"
            bot_message = random.choice([f"How are you {un}?", f"I care about you {un}", f"I'm very hungry, {un}"])
            history[-1][1] = ""
            for character in bot_message:
                history[-1][1] += character
                time.sleep(0.05)
                yield history

        response = msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
            bot, chatbot, chatbot
        )
        response.then(lambda: gr.update(interactive=True), None, [msg], queue=False)

        ui.queue()
        
        return ui

    
    