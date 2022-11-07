@echo off
@echo Django启动程序
@cd  %~dp0

@start /min "获取sis小说" .\venv\Scripts\python.exe .\get_xiaosuo.py