import io
import os
import random
import sys, tkinter
from textwrap import indent
import tkinter.messagebox
import traceback, import_expression
from contextlib import redirect_stdout
from logging import getLogger
from .ui import show_error
from flogin import ExecuteResponse, Glyph, Query, Result

from .plugin import PyReplPlugin

log = getLogger(__name__)

class RedirectedStdout:
    def __init__(self):
        self._stdout = None
        self._string_io = None

    async def __aenter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._string_io = io.StringIO()
        return self

    async def __aexit__(self, type, value, traceback):
        sys.stdout = self._stdout

    def __str__(self):
        return self._string_io.getvalue()  # type: ignore

class ReplResult(Result):
    plugin: PyReplPlugin  # type: ignore

    def __init__(self, query: Query) -> None:
        self.query = query
        log.info(f"Creating result with {self.query!r}")
        super().__init__("Execute Code?", icon=Glyph("py", "Calibri"))

    def prep_code(self, code: str):
        body = f"x = {code}\nprint(x)"
        return body

    async def callback(self):
        log.info(f"Starting callback")

        env = {
            "random": random,
            "_": self.plugin.last_result,
            "os": os,
            "sys": sys,
            "io": io,
        }

        env.update(globals())

        to_compile = self.prep_code(self.query.text)
        log.info(f"{to_compile!r}")

        async with RedirectedStdout() as otp:
            try:
                import_expression.exec(to_compile, env)
            except Exception as e:
                txt = f"{otp}\n\n{traceback.format_exc()}"
                show_error("PyRepl Error", txt)
                return ExecuteResponse(hide=False)

            tkinter.messagebox.showinfo("PyRepl Result", str(otp))

        return ExecuteResponse(hide=False)
