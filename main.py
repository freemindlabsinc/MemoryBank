from abc import ABC
from fastapi.responses import RedirectResponse
import gradio as gr
from fastapi import Depends, FastAPI

from routers.auth import auth_router
from routers.users import users_router

from ui.main import build_gradio_ui

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
    return RedirectResponse("/gradio")    

# experiments