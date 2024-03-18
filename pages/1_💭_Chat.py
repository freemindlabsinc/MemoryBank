import streamlit as st
import src.components.page_configurator as page_config

page_config.initialize_page(
     icon="🪄",
     title="Chat",
     desc="""
     This module lets you chat with the AI using your personal data.
     """,)

page_config.initialize_session_state({     
     'model': 'gpt-3.5-turbo'
     })