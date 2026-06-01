import asyncio
import json
from typing import Any, Callable

from .scheduler import complete_job, create_job, get_job, initialize_database, list_jobs


ToolHandler = Callable[[dict[str, Any]], dict[str, Any]]


def handle_task_create(arguments: dict[str, Any]) -> dict[str, Any]:
    return create_job(content=arguments["content"], due_at=arguments["due_at"])


def handle_task_list(arguments: dict[str, Any]) -> dict[str, Any]:
    return {"jobs": list_jobs(status=arguments.get("status"))}


def handle_task_get(arguments: dict[str, Any]) -> dict[str, Any]:
    job = get_job(int(arguments["id"]))
    if job is None:
        raise ValueError("job not found")
    return job


def handle_task_complete(arguments: dict[str, Any]) -> dict[str, Any]:
    job = complete_job(int(arguments["id"]))
    if job is None:
        raise ValueError("job not found")
    return job


TOOL_REGISTRY: dict[str, ToolHandler] = {
    "task.create": handle_task_create,
    "task.list": handle_task_list,
    "task.get": handle_task_get,
    "task.complete": handle_task_complete,
}


def route_tool_call(tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
    handler = TOOL_REGISTRY.get(tool_name)
    if handler is None:
        raise ValueError(f"Unknown tool: {tool_name}")
    return handler(arguments)


async def run_stdio_server() -> None:
    try:
        from mcp.server import Server
        from mcp.server.stdio import stdio_server
        from mcp.types import TextContent, Tool
    except ImportError as error:
        raise RuntimeError("Install requirements-mcp.txt before running the optional MCP server") from error

    initialize_database()
    server = Server("chatgpt-task-scheduler")

    @server.list_tools()
    async def list_available_tools() -> list[Tool]:
        return [
            Tool(
                name="task.create",
                description="Create a scheduled task.",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "content": {"type": "string"},
                        "due_at": {"type": "string", "description": "ISO datetime"},
                    },
                    "required": ["content", "due_at"],
                },
            ),
            Tool(
                name="task.list",
                description="List scheduled tasks.",
                inputSchema={
                    "type": "object",
                    "properties": {"status": {"type": "string"}},
                },
            ),
            Tool(
                name="task.get",
                description="Get a task by id.",
                inputSchema={
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                    "required": ["id"],
                },
            ),
            Tool(
                name="task.complete",
                description="Mark a task as completed.",
                inputSchema={
                    "type": "object",
                    "properties": {"id": {"type": "integer"}},
                    "required": ["id"],
                },
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any]) -> list[TextContent]:
        result = route_tool_call(name, arguments or {})
        return [TextContent(type="text", text=json.dumps(result, ensure_ascii=False))]

    async with stdio_server() as streams:
        await server.run(streams[0], streams[1], server.create_initialization_options())


def main() -> None:
    asyncio.run(run_stdio_server())


if __name__ == "__main__":
    main()
