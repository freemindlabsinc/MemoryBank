from utils.prompt_fetcher import get_predefined_prompts, PredefinedPrompt
import openai

def complete(prompt: PredefinedPrompt, user_text: str) -> str:
     #openai_gpt4_key = st.secrets["OPENAI_API_KEY"]
     #client = OpenAI(api_key=openai_gpt4_key)
     
     system_content = prompt.system_content
     user_file_content = prompt.user_content

     # Build the API call
     system_message = {"role": "system", "content": system_content}     
     user_message = {"role": "user", "content": (user_file_content or "") + "\n" + (user_text or "")}
     messages = [system_message, user_message]
     try:
          response = openai.chat.completions.create(               
               model="gpt-4-1106-preview",
               #model="gpt-4-32k-0613",
               #model="gpt-3.5-turbo",
               messages=messages,
               temperature=0.0,
               top_p=1,
               frequency_penalty=0.1,
               presence_penalty=0.1,
          )
          assistant_message = response.choices[0].message.content
          #return jsonify({"response": assistant_message})
          return assistant_message
     except Exception as e:
          #app.logger.error(f"Error occurred: {str(e)}")
          return f"An error occurred while processing the request. {e}"