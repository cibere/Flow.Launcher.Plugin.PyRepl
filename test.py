from flogin import Query
from flogin.utils import setup_logging

from plugin.result import PyReplPlugin, ReplResult

setup_logging()

code = """
print("hi")#; raise RuntimeError("hi")
""".strip()

q = Query(
    {
        "rawQuery": f"py {code}",
        "search": code,
        "actionKeyword": "py",
        "isReQuery": False,
    }
)
res = ReplResult(q)
res.plugin = PyReplPlugin()


async def main():
    await res.callback()


import asyncio

asyncio.run(main())
