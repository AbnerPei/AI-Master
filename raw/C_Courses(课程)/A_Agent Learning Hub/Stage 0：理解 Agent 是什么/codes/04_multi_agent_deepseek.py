import json
import os
from typing import Any

from openai import OpenAI


MODEL = "deepseek-v4-flash"


def build_client() -> OpenAI:
    api_key = os.environ["DEEPSEEK_API_KEY"]
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


class Agent:
    def __init__(self, client: OpenAI, name: str, system_prompt: str):
        self.client = client
        self.name = name
        self.messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]

    def run(self, task: str) -> str:
        self.messages.append({"role": "user", "content": task})
        response = self.client.chat.completions.create(model=MODEL, messages=self.messages)
        reply = response.choices[0].message.content or ""
        self.messages.append({"role": "assistant", "content": reply})
        return reply


def parse_plan(plan_text: str) -> list[dict[str, Any]]:
    start = plan_text.find("[")
    end = plan_text.rfind("]")
    if start == -1 or end == -1:
        raise ValueError(f"未找到 JSON 数组：{plan_text}")
    return json.loads(plan_text[start : end + 1])


def build_agents(client: OpenAI) -> dict[str, Agent]:
    return {
        "researcher": Agent(client, "研究员", "你是一名研究员，擅长搜索和整理信息。"),
        "coder": Agent(client, "程序员", "你是一名 Python 程序员，写清晰、可讲解的示例代码。"),
        "writer": Agent(client, "撰稿人", "你是一名技术撰稿人，善于整理结构化交付物。"),
    }


def create_plan(client: OpenAI, user_task: str) -> str:
    plan_prompt = f"""
任务：{user_task}

请把任务拆成 2 到 4 个步骤，并为每个步骤分配角色。
可用角色：researcher、coder、writer。
只返回 JSON 数组，不要附加解释。

格式示例：
[
  {{"id": "step1", "role": "researcher", "instruction": "先解释需求背景"}},
  {{"id": "step2", "role": "writer", "instruction": "整理成最终输出"}}
]
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": plan_prompt}],
        response_format={"type": "json_object"},
    )
    content = response.choices[0].message.content or ""
    data = json.loads(content)
    if isinstance(data, list):
        return json.dumps(data, ensure_ascii=False)
    if "steps" in data:
        return json.dumps(data["steps"], ensure_ascii=False)
    return content


def orchestrator(client: OpenAI, user_task: str) -> str:
    agents = build_agents(client)
    plan_text = create_plan(client, user_task)
    steps = parse_plan(plan_text)
    print(f"[计划] {json.dumps(steps, ensure_ascii=False)}")

    results: dict[str, str] = {}
    for step in steps:
        role = step["role"]
        instruction = step["instruction"]
        agent = agents[role]
        print(f"[分发] {role}: {instruction}")
        results[step["id"]] = agent.run(instruction)

    writer = agents["writer"]
    summary = writer.run(f"请整合以下各角色的产出，形成最终答复：\n{results}")
    return summary


def main() -> None:
    client = build_client()
    user_task = input("请输入一个需要多角色协作的任务：").strip()
    if not user_task:
        print("输入不能为空。")
        return
    reply = orchestrator(client, user_task)
    print(f"最终交付：{reply}")


if __name__ == "__main__":
    main()
