import os
import glob
from typing import List, Tuple

class PredefinedPrompt:
    def __init__(self, title, system_content, user_content):
        self.title = title
        self.system_content = system_content
        self.user_content = user_content 

def get_predefined_prompts(prompt_dir:str, default_prompt:str='extract_wisdom') -> Tuple[List[PredefinedPrompt], int]:
    # Get all the prompt directories
    prompt_dirs = glob.glob(os.path.join(prompt_dir, '*'))

    prompt_args = []
    default_prompt_index = None

    for index, dir in enumerate(prompt_dirs):
        try:
            # break if the path is 'improve_prompt'
            if dir == 'prompts\improve_prompt':
                continue
            
            title = os.path.basename(dir)
            system_file = os.path.join(dir, 'system.md')
            user_file = os.path.join(dir, 'user.md')

            system_content = None
            user_content = None

            # Read the system.md file if it exists
            if os.path.exists(system_file):
                with open(system_file, 'r') as f:
                    txt = f.read()
                    if (len(txt)>0):
                        system_content = txt

            # Read the user.md file if it exists
            if os.path.exists(user_file):
                with open(user_file, 'r') as f:
                    txt = f.read()
                    if (len(txt)>0):
                        user_content = txt

            prompt = PredefinedPrompt(title, system_content, user_content)
            prompt_args.append(prompt)

            if title == default_prompt:
                default_prompt_index = index

        except Exception as e:
            print(f"Error processing {dir}: {e}")

    return prompt_args, default_prompt_index