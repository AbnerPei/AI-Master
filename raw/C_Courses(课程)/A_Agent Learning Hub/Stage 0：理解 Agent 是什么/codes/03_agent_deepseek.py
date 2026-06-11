import contextlib
import io
import json
import os
from typing import Any

from openai import OpenAI


MODEL = "deepseek-v4-flash"


def build_client() -> OpenAI:
    api_key = os.environ["DEEPSEEK_API_KEY"]
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def call_search_api(query: str) -> str:
    knowledge = {
        "agent 是什么": "Agent 的核心是模型在循环里自主决定下一步要不要调用工具。",
        "workflow 是什么": "Workflow 的关键是流程和分支由开发者预定义。",
        "multi-agent 是什么": "Multi-Agent 是多个相对独立的 Agent 协同完成任务。",
    }
    for key, value in knowledge.items():
        if key in query.lower():
            return value
    return f"这是一个模拟搜索结果：未命中知识库，但已收到查询 `{query}`。"


def exec_in_sandbox(code: str) -> str:
    buffer = io.StringIO()
    local_vars: dict[str, Any] = {}
    allowed_builtins = {
        "abs": abs,
        "len": len,
        "min": min,
        "max": max,
        "sum": sum,
        "range": range,
        "print": print,
    }
    try:
        with contextlib.redirect_stdout(buffer):
            exec(code, {"__builtins__": allowed_builtins}, local_vars)
    except Exception as exc:
        return f"Python 执行失败：{exc}"

    stdout = buffer.getvalue().strip()
    if stdout:
        return stdout
    return f"Python 已执行完成，可用变量：{sorted(local_vars.keys())}"


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "搜索资料并返回简短文本结果",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "run_python",
            "description": "执行简短 Python 代码并返回输出",
            "parameters": {
                "type": "object",
                "properties": {"code": {"type": "string"}},
                "required": ["code"],
            },
        },
    },
]


def execute_tool(name: str, arguments: dict[str, Any]) -> str:
    if name == "web_search":
        return call_search_api(arguments["query"])
    if name == "run_python":
        return exec_in_sandbox(arguments["code"])
    return "未知工具"


def agent_run(client: OpenAI, user_input: str, max_steps: int = 8) -> str:
    messages: list[dict[str, Any]] = [
        {
            "role": "system",
            "content": (
                "你是一个会使用工具的助手。"
                "需要时可以调用工具；任务完成后给出最终回答。"
            ),
        },
        {"role": "user", "content": user_input},
    ]

    for step in range(1, max_steps + 1):
        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
        )
        msg = response.choices[0].message
        messages.append(msg.model_dump(exclude_none=True))

        if not msg.tool_calls:
            return f"[总步数 {step}] {msg.content or ''}"

        for tool_call in msg.tool_calls:
            args = json.loads(tool_call.function.arguments)
            result = execute_tool(tool_call.function.name, args)
            print(f"[工具] {tool_call.function.name}({args}) -> {result}")
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": result,
                }
            )

    return "达到最大步数限制，任务未完成。"


def main() -> None:
    client = build_client()
    user_input = input("请输入一个需要工具协助的问题：").strip()
    if not user_input:
        print("输入不能为空。")
        return
    reply = agent_run(client, user_input)
    print(f"最终回答：{reply}")


if __name__ == "__main__":
    main()
