@echo off
@echo Django��������
@cd  %~dp0
@start /min "Django" .\venv\Scripts\python.exe .\manage.py runserver 0.0.0.0:8000