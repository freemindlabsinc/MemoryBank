import streamlit as st
import src.components.page_configurator as page_config

page_config.initialize_page(
     icon="🪄",
     title="Chat",
     desc="""This module will let you chat with an LLM using your data.     
     """,)
