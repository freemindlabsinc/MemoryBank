## How to

- Create a virtual environment
```bash
python -m venv venv
```
- Upgrade pip
```
venv\Scripts\python.exe -m pip install --upgrade pip
```

- *If you get "WARNING: There was an error checking the latest version of pip." on Windows run the following command:*
```
    rm -r $env:LOCALAPPDATA\pip\cache\selfcheck\
```
- Activate the virtual environment
```bash
PS: .\venv\Scripts\activate
Linux: source venv/bin/activate
```

- Install the requirements
```bash
pip install -r requirements.txt
```

## Additional helpful things

python -m venv venv --clear
python -m pip list
python -m pip freeze > requirements.txt

ngrok http http://localhost:7000

## Elasticsearch related

$ openssl x509 -fingerprint -sha256 -noout -in /tmp/ca.crt | awk -F"=" {' print $2 '} | sed s/://g

$ cat /tmp/ca.crt