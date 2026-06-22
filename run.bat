@echo off
echo Starting OpenModel.ai Chat...
call venv\Scripts\activate.bat 2>nul || echo Virtual environment not found. Using system Python.
python openmodel.py
pause
