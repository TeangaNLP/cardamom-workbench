# debug mode
# ack -g "/code/.*.py" --ignore-dir "env" --ignore-dir "htmlcov" | entr -r python3 flask_app.py
# deploy mode
python3 flask_app.py
