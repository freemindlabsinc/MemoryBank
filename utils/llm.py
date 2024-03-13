from utils.prompt_fetcher import get_predefined_prompts, PredefinedPrompt
import openai
from openai import Stream
from openai.types.chat import ChatCompletionChunk
     
def get_completion_stream(prompt: PredefinedPrompt, user_text: str) -> Stream[ChatCompletionChunk]:
     system_content = prompt.system_content
     user_file_content = prompt.user_content

     # Build the API call
     system_message = {"role": "system", "content": system_content}     
     user_message = {"role": "user", "content": (user_file_content or "") + "\n" + (user_text or "")}
     messages = [system_message, user_message]
     try:
          stream = openai.chat.completions.create(               
               model="gpt-4-1106-preview",
               #model="gpt-4-32k-0613",
               #model="gpt-3.5-turbo",
               stream=True,
               messages=messages,
               temperature=0.0,
               top_p=1,
               frequency_penalty=0.1,
               presence_penalty=0.1,
          )
          
          for chunk in stream:
               yield chunk
               
     except Exception as e:
          #app.logger.error(f"Error occurred: {str(e)}")
          return f"An error occurred while processing the request. {e}"