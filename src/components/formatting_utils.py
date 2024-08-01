from typing import List
from src.models.Prompts import PredefinedPrompt

def get_fancy_captions(prompts) -> List[str]:
    res = []
    for p in prompts:
        res.append(f"{p.icon} {p.title}")
    
    return res

def get_prompt_by_fancy_caption(selected_prompt: str, prompts) -> PredefinedPrompt:    
    title_parts = selected_prompt.split(' ', 1)  # Split the title at the first space
    if len(title_parts) > 1:  # Check if there is more than one part
        prompt_id = title_parts[1]  # The text after the first space is the second part
    else:
        prompt_id = ''  # If there is no space in the title, return an empty string

    # get the prompt object
    prompt = next((p for p in prompts if p.title == prompt_id), None)
    
    return prompt