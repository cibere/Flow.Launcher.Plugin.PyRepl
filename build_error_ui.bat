@echo OFF

pip install --upgrade pip
pip install -U wheel setuptools
pip install -r ./requirements-dev.txt

pyinstaller -w pyrepl_error_ui.py
