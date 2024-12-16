from __future__ import annotations
import random, asyncio
from logging import getLogger
from .core import execute_code
import pyperclip
from flogin import ExecuteResponse, Query, Result
from .results import ErrorResult, StdoutLineResult
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from .plugin import PyReplPlugin
else:
    PyReplPlugin = Any

log = getLogger(__name__)

class ReplResult(Result[PyReplPlugin]):
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
        assert self.plugin

        log.info(f"Starting callback")

        site_packages_path = self.plugin.settings.site_packages_path
        site_packages = [site_packages_path] if site_packages_path else []
        
        executable = self.plugin.settings.executable

        if self.use_clipboard:
            to_compile = pyperclip.paste()
        else:
            to_compile = self.query.text

        log.info(f"{to_compile!r}")

        if self.use_clipboard:
            await self.plugin.api.change_query(self.query.keyword)
        
        stderr, stdout = await asyncio.to_thread(execute_code, to_compile, executable, site_packages)

        if stderr:
            if self.plugin.settings.just_show_me_the_tb is True:
                self.plugin.show_error(stderr)
            else:
                res = ErrorResult(f"# Stdout\n\n{stdout}\n\n# Stderr\n\n{stderr}")
                await self.plugin.api.update_results(self.query.raw_text, [res])
        else:
            results = [StdoutLineResult(title=line) for line in str(stdout).splitlines()]
            
            await self.plugin.api.update_results(
                self.query.raw_text,
                results, # type: ignore
            )

        return ExecuteResponse(hide=False)
