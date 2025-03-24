SET "VENV_DIR=.venv"

IF NOT EXIST "%VENV_DIR%" (
    python -m venv %VENV_DIR%
)

CALL %VENV_DIR%\Scripts\activate.bat

python.exe -m pip install --upgrade pip

pip install -r requirements.txt

start pythonw.exe main.py

exit