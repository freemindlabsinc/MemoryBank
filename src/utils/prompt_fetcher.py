import os
import glob
import streamlit as st
from typing import List
from src.models.Prompts import PredefinedPrompt


@st.cache_data(ttl=10) #seconds
def get_predefined_prompts(prompt_dir:str = 'data/prompts') -> List[PredefinedPrompt]:
    # Get all the prompt directories
    prompt_dirs = glob.glob(os.path.join(prompt_dir, '*'))

    prompt_args = []
    idx = 0
    for index, dir in enumerate(prompt_dirs):
        try:            
            # Read the system.md file if it exists
            system_file = os.path.join(dir, 'system.md')            
            system_prompt = _read_file(system_file)            

            # Read the user.md file if it exists
            user_file = os.path.join(dir, 'user.md')
            user_content = _read_file(user_file)
            
            # Other
            dir_name = os.path.basename(dir)
            title = dir_name_to_title(dir_name)

            prompt = PredefinedPrompt(
                id=dir_name, 
                title=title, 
                system_prompt=system_prompt, 
                user_content=user_content,
                description=get_description(title),
                icon=get_random_emoji()
                )
                
            prompt_args.append(prompt)            

        except Exception as e:
            print(f"Error processing {dir}: {e}")

    #return prompt_args sorted by title
    return sorted(prompt_args, key=lambda x: x.title)
    return prompt_args


def _read_file(filename: str) -> str:
    if (os.path.exists(filename)):
        try:
            with open(filename, 'r') as f:
                txt = f.read()
                if (len(txt)>0):
                    return txt
        except Exception as e:
            return e
    
    return ''  
    
def dir_name_to_title(dir_name: str) -> str:
    res = dir_name.replace('_', ' ').replace('-', ' ')
    
    # capitalize the first letter of each word
    res = ' '.join([word.capitalize() for word in res.split()])
    
    return res

def get_random_emoji():
    import random
    emojis = ["📜"]
    #emojis = ["📚", "📜", "📖", "📝", "📓", "📒", "📔", "📕", "📗", "📘", "📙", "📚", "📜", "📖", "📝", "📓", "📒", "📔", "📕", "📗", "📘", "📙"]
    return random.choice(emojis)

def get_description(title: str) -> str:
    return f"{title} needs a description at some point..."