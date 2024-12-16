from flogin import SearchHandler, Query
from .repl_result import ReplResult

class ReplSearchHandler(SearchHandler):
    async def callback(self, query: Query):
        return ReplResult(query)