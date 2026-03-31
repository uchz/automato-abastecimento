cd /d %~dp0

echo Iniciando API...
start cmd /k python -m uvicorn main:app --host 0.0.0.0 --port 8000

timeout /t 5

echo Iniciando BOT...
start cmd /k python "tratativa 4.0.py"

timeout /t 3

echo Abrindo dashboard...
start index.html