import os

from openai import OpenAI


MODEL = "deepseek-v4-flash"


def build_client() -> OpenAI:
    api_key = os.environ["DEEPSEEK_API_KEY"]
    return OpenAI(api_key=api_key, base_url="https://api.deepseek.com")


def query_order_api(user_id: str) -> dict:
    return {"id": "ORD-20260607-001", "user_id": user_id, "amount": 99, "status": "paid"}


def submit_refund(order_id: str) -> None:
    print(f"[系统] 已提交退款申请：{order_id}")


def create_ticket(user_input: str) -> dict:
    return {"id": "TICKET-1001", "content": user_input, "owner": "support-l2"}


def assign_to_team(ticket: dict) -> None:
    print(f"[系统] 工单 {ticket['id']} 已分配给 {ticket['owner']}")


def retrieve_from_knowledge_base(user_input: str) -> str:
    return (
        "退款通常在 1 到 3 个工作日到账；"
        "如为重复扣款，请先确认银行卡短信与订单详情是否一致；"
        f"当前用户问题：{user_input}"
    )


def classify_intent(client: OpenAI, user_input: str) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "将用户消息分类为 refund / complaint / inquiry。"
                    "只返回一个小写类别词。"
                ),
            },
            {"role": "user", "content": user_input},
        ],
    )
    return (resp.choices[0].message.content or "").strip().lower()


def generate_refund_response(client: OpenAI, order: dict) -> str:
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "你是客服助手，请生成简洁、安抚情绪的退款说明。",
            },
            {
                "role": "user",
                "content": f"订单信息：{order}。请生成一段退款通知。",
            },
        ],
    )
    return resp.choices[0].message.content or ""


def handle_refund(client: OpenAI, user_input: str, user_id: str) -> str:
    _ = user_input
    order = query_order_api(user_id)
    reply = generate_refund_response(client, order)
    submit_refund(order["id"])
    return reply


def handle_complaint(user_input: str) -> str:
    ticket = create_ticket(user_input)
    assign_to_team(ticket)
    return f"已创建工单 #{ticket['id']}，会有专人跟进。"


def handle_inquiry(client: OpenAI, user_input: str) -> str:
    docs = retrieve_from_knowledge_base(user_input)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"基于以下资料回答用户问题：\n{docs}"},
            {"role": "user", "content": user_input},
        ],
    )
    return resp.choices[0].message.content or ""


def workflow(client: OpenAI, user_input: str, user_id: str) -> str:
    intent = classify_intent(client, user_input)
    print(f"[路由] 当前意图：{intent}")

    if intent == "refund":
        return handle_refund(client, user_input, user_id)
    if intent == "complaint":
        return handle_complaint(user_input)
    if intent == "inquiry":
        return handle_inquiry(client, user_input)
    return "抱歉，我暂时无法识别你的需求。"


def main() -> None:
    client = build_client()
    user_id = "user-001"
    user_input = input("请输入一条用户消息：").strip()
    if not user_input:
        print("输入不能为空。")
        return
    reply = workflow(client, user_input, user_id)
    print(f"系统回复：{reply}")


if __name__ == "__main__":
    main()
