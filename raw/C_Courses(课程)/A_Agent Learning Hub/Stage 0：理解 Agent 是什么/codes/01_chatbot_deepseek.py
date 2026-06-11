import os

from openai import OpenAI


MODEL = "deepseek-v4-flash"


def build_client() -> OpenAI:
    api_key = os.environ["DEEPSEEK_API_KEY"]
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def main() -> None:
    client = build_client()
    messages = [{"role": "system", "content": "你是一个友好的助手。"}]

    print("输入 `exit` 或 `quit` 结束对话。")
    while True:
        user_input = input("你：").strip()
        if not user_input:
            continue
        if user_input.lower() in {"exit", "quit"}:
            print("助手：下次见。")
            break

        messages.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(model=MODEL, messages=messages)
        reply = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": reply})
        print(f"助手：{reply}")


if __name__ == "__main__":
    main()
