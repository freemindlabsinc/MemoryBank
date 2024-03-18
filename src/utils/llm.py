from src.utils.prompt_fetcher import PredefinedPrompt
import openai
import os
from openai import Stream
from openai.types.chat import ChatCompletionChunk

# see https://github.com/danielmiessler/fabric?tab=readme-ov-file#just-use-the-patterns     
     
def get_completion_stream(prompt: PredefinedPrompt, input_data: str, openai_key: str = None, model: str = "gpt-3.5-turbo") -> Stream[ChatCompletionChunk]:
     # Build the API call
     openai.api_key = openai_key or os.getenv("OPENAI_API_KEY")
     
     system_message = {"role": "system", "content": prompt.system_prompt}     
     if (prompt.user_content is None):
          prompt.user_content = ""
                    
     user_message = {"role": "user", "content": prompt.user_content + "\n" + input_data}     
     messages = [system_message, user_message]
     #try:
     stream = openai.chat.completions.create(               
          #model="gpt-4-1106-preview",
          #model="gpt-4-32k-0613",
          #model="gpt-3.5-turbo",
          model=model,
          stream=True,
          messages=messages,
          temperature=0.0,
          top_p=1,
          frequency_penalty=0.1,
          presence_penalty=0.1,
     )
     
     for chunk in stream:
          yield chunk
               
     #except Exception as e:
     #     #app.logger.error(f"Error occurred: {str(e)}")
     #     return f"An error occurred while processing the request. {e}"