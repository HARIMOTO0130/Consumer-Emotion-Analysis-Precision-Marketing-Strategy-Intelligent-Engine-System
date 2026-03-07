import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
import os
import sys

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

class MCPBridge:
    def __init__(self, command: str, args: list = None):
        self.server_params = StdioServerParameters(
            command=command,
            args=args or [],
            env=os.environ.copy()
        )
        self.session = None
        self._exit_stack = None

    async def _ensure_session(self):
        if self.session:
            return

        from contextlib import AsyncExitStack
        self._exit_stack = AsyncExitStack()
        
        read_stream, write_stream = await self._exit_stack.enter_async_context(
            stdio_client(self.server_params)
        )
        
        self.session = await self._exit_stack.enter_async_context(
            ClientSession(read_stream, write_stream)
        )
        
        await self.session.initialize()
        print(f"MCP Session 建立成功: {self.server_params.command}")

    async def call_tool(self, tool_name: str, arguments: dict):
        try:
            await self._ensure_session()
            
            result = await self.session.call_tool(tool_name, arguments)
            
            return {
                "content": [
                    {"type": "text", "text": item.text if hasattr(item, 'text') else str(item)} 
                    for item in result.content
                ],
                "isError": result.is_error if hasattr(result, 'is_error') else False
            }
        except Exception as e:
            self.session = None
            return {"content": [{"type": "text", "text": f"SDK Error: {str(e)}"}], "isError": True}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mcp_script = os.path.join(BASE_DIR, "mcp_modules", "bing_search", "bing-cn-mcp-server", "build", "index.js")
# 初始化单例
bing_mcp = MCPBridge("node", [mcp_script])