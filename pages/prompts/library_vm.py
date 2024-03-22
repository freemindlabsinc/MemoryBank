import streamlit as st
from src.models.Prompts import PredefinedPrompt
import src.utils.prompt_fetcher as prompt_fetcher

def save_prompt(prompt: PredefinedPrompt):        
    st.toast(f"[NOT REALLY] Saved {prompt.title} to the database.", icon="✅")    

prompts = prompt_fetcher.get_predefined_prompts()