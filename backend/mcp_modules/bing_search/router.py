from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from core.mcp_bridge import bing_mcp
import traceback

router = APIRouter()

class MCPRequest(BaseModel):
    method: str
    params: dict

@router.post("/mcp/bing_search")
async def handle_bing_mcp(payload: MCPRequest):
    if payload.method != "tools/call":
        raise HTTPException(status_code=400, detail="Only 'tools/call' method is supported")
    
    # 兼容 payload 结构（处理前端传来的嵌套 params）
    p = payload.params
    tool_name = p.get("name")
    tool_args = p.get("arguments", {})

    try:
        result = await bing_mcp.call_tool(tool_name, tool_args)
        
        # 如果返回的是 MCP 标准错误格式
        if isinstance(result, dict) and result.get("isError"):
            return result
            
        if "result" in result:
            return result["result"]
        return result
    except Exception as e:
        # 这里的 e 现在会包含 stderr 里的详细报错内容
        traceback.print_exc()
        return {
            "content": [{"type": "text", "text": f"Bridge Error: {str(e)}"}],
            "isError": True
        }