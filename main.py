from abc import ABC
import gradio as gr
from fastapi import Depends, FastAPI

from routers.auth import auth_router
from routers.users import users_router

from ui.gradio import build_gradio_ui

app = FastAPI()

# Gradio app
ui = build_gradio_ui()
app = gr.mount_gradio_app(app, ui, path="/gradio")

# Routers
app.include_router(auth_router)
app.include_router(users_router)

# Web Root
@app.get("/")
def read_main():
    return {"message": "This is your main app"}

# experiments

class Tools:
    def __init__(self):
        pass

    def get(self, username: str):

class UserDB(ABC): 
    def __init__(self, Tools: Tools):
        pass
    
    async def get_user(self, username: str):
        from security.fake_users import fake_users_db
        fake_users_db. get(username)
    pass

