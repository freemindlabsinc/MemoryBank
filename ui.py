import random
import time
import gradio as gr
from security.fake_users import fake_users_db



# Gradio app
def build_ui(check_credentials):
    if not check_credentials:
        raise ValueError("check_credentials is required")
    
    with gr.Blocks() as ui:
        ui.auth = check_credentials
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
            bot_message = random.choice([f"How are you {un}?", f"I love you {un}", f"I'm very hungry, {un}"])
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
