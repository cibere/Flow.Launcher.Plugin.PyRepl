from typing import Any

from flogin import Plugin


class PyReplPlugin(Plugin):
    last_result: Any | None = None
