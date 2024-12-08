import io
import os
import random
import sys
import tkinter.messagebox
import traceback
from logging import getLogger

import import_expression
from flogin import ExecuteResponse, Query, Result, SettingNotFound

from .plugin import PyReplPlugin
from .ui import show_error

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
        super().__init__(
            "Execute Code?",
            icon="icon.png",
            auto_complete_text="".join(
                random.choices("qwertyuiopasdfghjklzxcvbnm", k=5)
            ),
            sub=query.text,
        )

    async def callback(self):
        log.info(f"Starting callback")

        try:
            if self.plugin.settings.site_packages_path not in sys.path:
                sys.path.append(self.plugin.settings.site_packages_path)
                log.info(f"Added {self.plugin.settings.site_packages_path!r} to path")
        except SettingNotFound:
            pass

        env = {
            "random": random,
            "_": self.plugin.last_result,
            "os": os,
            "sys": sys,
            "io": io,
        }

        env.update(globals())

        to_compile = self.query.text
        log.info(f"{to_compile!r}")

        async with RedirectedStdout() as otp:
            try:
                res = import_expression.eval(to_compile, env)
            except Exception as e:
                txt = f"{otp}\n\n{traceback.format_exc()}"
                show_error("PyRepl Error", txt)
                return ExecuteResponse(hide=True)
            
            self.plugin.last_result = res

            await self.plugin.api.update_results(
                self.query.raw_text,
                [Result(repr(res), icon="icon.png")] + [Result(line, icon="icon.png") for line in str(otp).splitlines()],
            )

        return ExecuteResponse(hide=False)
