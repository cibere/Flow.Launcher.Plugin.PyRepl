import io
import json
import os
import random
import sys
import traceback
from logging import getLogger
from typing import Unpack

import import_expression
import pyperclip
from flogin import ExecuteResponse, Query, Result, SettingNotFound
from flogin.jsonrpc.results import ResultConstructorArgs

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


class ErrorResult(Result):
    plugin: PyReplPlugin  # type: ignore

    def __init__(self, error: Exception, txt: str) -> None:
        self.txt = txt
        super().__init__(
            f"An error has occured: {error.__class__.__name__}: {error}",
            icon="error.png",
            sub="Click to view traceback",
            auto_complete_text="".join(
                random.choices("qwertyuiopasdfghjklzxcvbnm", k=5)
            ),
        )

    async def callback(self):
        log.info(f"Showing error")
        show_error("PyRepl Error", self.txt)
        return ExecuteResponse(hide=True)


class ReplResult(Result):
    plugin: PyReplPlugin  # type: ignore

    def __init__(self, query: Query) -> None:
        self.query = query
        self.use_clipboard = query.raw_text == query.keyword

        log.info(f"Creating result with {self.query!r}")

        super().__init__(
            "Execute Code?",
            icon="icon.png",
            auto_complete_text="".join(
                random.choices("qwertyuiopasdfghjklzxcvbnm", k=5)
            ),
            sub="Use clipboard contents" if self.use_clipboard else query.text,
        )

    async def callback(self):
        log.info(f"Starting callback")

        try:
            if self.plugin.settings.site_packages_path not in sys.path:
                sys.path.append(self.plugin.settings.site_packages_path)
                log.info(f"Added {self.plugin.settings.site_packages_path!r} to path")
        except SettingNotFound:
            pass
        try:
            additional_env = json.loads(self.plugin.settings.env_json)
        except SettingNotFound:
            additional_env = {}
        except (json.JSONDecodeError, TypeError) as e:
            await self.plugin.api.show_error_message(
                "PyRepl",
                f"Additional ENV parameters are not in a valid JSON format: {e!r}",
            )
            await self.plugin.api.open_settings_menu()
            return ExecuteResponse()

        env = {
            "random": random,
            "_": self.plugin.last_result,
            "os": os,
            "sys": sys,
            "io": io,
        } | additional_env

        env.update(globals())

        if self.use_clipboard:
            to_compile = pyperclip.paste()
        else:
            to_compile = self.query.text
        log.info(f"{to_compile!r}")

        async with RedirectedStdout() as otp:
            if self.use_clipboard:
                await self.plugin.api.change_query(self.query.keyword)

            try:
                res = import_expression.eval(to_compile, env)
            except Exception as e:
                txt = f"{otp}\n\n{traceback.format_exc()}"

                if self.plugin.settings.just_show_me_the_tb is True:
                    show_error("PyRepl Error", txt)
                else:
                    res = ErrorResult(e, txt)
                    self.plugin._results[res.slug] = (
                        res  # have to manually register it for the action to work cuz in this version of flogin, `update_results` does not register the results
                    )
                    await self.plugin.api.update_results(self.query.raw_text, [res])
            else:
                self.plugin.last_result = res

                await self.plugin.api.update_results(
                    self.query.raw_text,
                    [Result(repr(res), icon="icon.png")]
                    + [Result(line, icon="icon.png") for line in str(otp).splitlines()],
                )

        return ExecuteResponse(hide=False)
