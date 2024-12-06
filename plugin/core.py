from flogin import Query

from .plugin import PyReplPlugin
from .result import ReplResult

plugin = PyReplPlugin()


@plugin.search()
async def handler(query: Query):
    return ReplResult(query)
