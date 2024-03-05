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