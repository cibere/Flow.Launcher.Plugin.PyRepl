from flogin import Plugin
from .handler import ReplSearchHandler
from .settings import PyReplSettings
import subprocess, asyncio, os
from pathlib import Path

class PyReplPlugin(Plugin[PyReplSettings]):
    def __init__(self) -> None:
        super().__init__()

        self.register_search_handler(ReplSearchHandler())
    
    def show_error(self, msg: str) -> None:
        error_ui_file = os.path.join("pyrepl_error_ui", "pyrepl_error_ui.exe")
        subprocess.Popen([msg], executable=error_ui_file)