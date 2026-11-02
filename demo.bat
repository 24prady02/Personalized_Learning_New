@echo off
rem Think on the Graph demonstration: asks for a Java program, a question and a student's answer, runs Stage 1 and
rem Stage 2 (Claude CLI, this computer's login) and opens a full-screen page in the browser with every step drawn.
cd /d "%~dp0"
python src\demo.py
echo.
pause
