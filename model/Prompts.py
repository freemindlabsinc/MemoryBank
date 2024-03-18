from typing import Optional

class PredefinedPrompt:
    def __init__(self, 
                 id: str, 
                 title: str,
                 system_prompt: str, 
                 user_content: Optional[str] = None,
                 description: Optional[str] = None,
                 icon: Optional[str] = "📜"):
        self.id = id
        self.icon = icon
        self.title = title   
        self.description = description             
        self.system_prompt = system_prompt
        self.user_content = user_content