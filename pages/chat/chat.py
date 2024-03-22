import streamlit as st
import src.components.page_header as page_config
from st_pages import add_page_title

add_page_title()

page_config.initialize_page(
     desc="""This module will let you chat with an LLM using your data.     
     """,)
