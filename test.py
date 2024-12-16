from plugin.repl_result import ReplResult
from flogin import Query
import asyncio
from flogin.testing import PluginTester

class APIClass:
    async def change_query(self, *args):
        print(f"--- change query w/ {args!r} ---")
    
    async def update_results(self, *args):
        print(f'--- update results w/ {args!r} ---')

    async def show_notification(self, *args):
        print(f'--- show_notification w/ {args!r} ---')

async def main():
    from plugin.plugin import PyReplPlugin
    tester = PluginTester(PyReplPlugin(), metadata=None, flow_api_client=APIClass())

    query = Query(raw_text="py print(100)", text="print(100))", keyword="py")
    response = await tester.test_query(query)

    print(response.results)

    res = response.results[0]

    res.plugin = tester.plugin
    await res.callback()

asyncio.run(main())