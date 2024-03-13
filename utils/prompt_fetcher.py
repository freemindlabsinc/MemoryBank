import os
import glob
from typing import List

class PredefinedPrompt:
    def __init__(self, title, system_content, user_content):
        self.title = title
        self.system_content = system_content
        self.user_content = user_content 

def get_predefined_prompts(prompt_dir) -> List[PredefinedPrompt]:
    # Get all the prompt directories
    prompt_dirs = glob.glob(os.path.join(prompt_dir, '*'))

    prompt_args = []

    for dir in prompt_dirs:
        try:
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

            # Create a new PromptArguments instance and add it to the list            
            prompt_args.append(PredefinedPrompt(title, system_content, user_content))
        except Exception as e:
            #print(f'Error reading prompt directory {dir}: {e}')            
            pass

    return prompt_args