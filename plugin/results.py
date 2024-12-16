from __future__ import annotations
import random
from logging import getLogger
from typing import Unpack, TYPE_CHECKING, Any
import pyperclip
from flogin import ExecuteResponse, Result, Glyph
from flogin.jsonrpc.results import ResultConstructorArgs

if TYPE_CHECKING:
    from .plugin import PyReplPlugin
else:
    PyReplPlugin = Any

log = getLogger(__name__)

class CopyResult(Result):
    def __init__(self, txt: str, **kwargs: Unpack[ResultConstructorArgs]) -> None:
        self.txt = txt
        super().__init__(**kwargs)
    
    async def callback(self):
        assert self.plugin

        pyperclip.copy(self.txt)
        await self.plugin.api.show_notification("PyRepl", "Successfully copied text", "icon.png")

        return ExecuteResponse(hide=False)

class ErrorResult(Result[PyReplPlugin]):
    def __init__(self, error: str) -> None:
        self.error = error
        super().__init__(
            f"An error has occured: {error.splitlines()[-1]}",
            icon="error.png",
            sub="Click to view traceback",
            auto_complete_text="".join(
                random.choices("qwertyuiopasdfghjklzxcvbnm", k=5)
            ),
        )

    async def callback(self):
        log.info(f"Showing error")
        assert self.plugin

        self.plugin.show_error(self.error)
        return ExecuteResponse(hide=True)

class StdoutLineResult(Result[PyReplPlugin]):
    def __init__(self, **kwargs: Unpack[ResultConstructorArgs]) -> None:
        self.line = kwargs['title']
        if "icon" not in kwargs:
            kwargs['icon'] = "icon.png"
        if "copy_text" not in kwargs:
            kwargs['copy_text'] = self.line

        super().__init__(**kwargs)
    
    async def context_menu(self):
        return CopyResult(self.line, title="Copy Text", sub=self.line, glyph=Glyph("\U0001f4cb", "Calibri"))