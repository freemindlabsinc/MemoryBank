# Upgrade pip
python.exe -m pip install --upgrade pip

# Packages
pip install gradio
pip install fastapi

pip install transformers
pip install 'transformers[tf-cpu]'
pip install 'transformers[torch]'
pip install 'transformers[flax]'
pip install "python-jose[cryptography]"
pip install "passlib[bcrypt]"
pip install text-generation
pip install torchaudio

pip install streamlit==1.32.1
pip install openai
pip install youtube-transcript-api
pip install bs4
pip install msal_streamlit_authentication