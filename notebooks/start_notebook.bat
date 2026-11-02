@echo off
rem Start the Think on the Graph notebook server (detached, fixed address) and open the notebook.
rem Address: http://localhost:8888/notebooks/notebooks/think_on_the_graph.ipynb?token=thinkonthegraph
rem The server keeps running in the background until you end the python process (Task Manager) or restart Windows.
cd /d "%~dp0.."
start "" /b python -m jupyter notebook --no-browser --port=8888 --ServerApp.port_retries=0 --IdentityProvider.token=thinkonthegraph --notebook-dir="%cd%" 2>> experiments\logs\jupyter_server.log
timeout /t 4 /nobreak > nul
start "" "http://localhost:8888/notebooks/notebooks/think_on_the_graph.ipynb?token=thinkonthegraph"
