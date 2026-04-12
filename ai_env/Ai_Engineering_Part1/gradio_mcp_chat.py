import json
import os
import sys

import gradio as gr
import requests
from dotenv import load_dotenv
from openai import OpenAI

# Avoid Windows cp1252 console crashes when Gradio prints emoji in MCP launch logs.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")
PUSHOVER_URL = "https://api.pushover.net/1/messages.json"

if not OPENAI_API_KEY:
    raise RuntimeError("OPENAI_API_KEY is missing in environment")

SYSTEM_MESSAGE = """You are a digital twin of zainab Ahmed safeer. Respond in first person with a warm, kind style.
Use only the provided context. If you do not know, say you do not know."""

TOPIC_CONTEXT = {
    "2001": "*** In 2001, Zainab was in 6th grade and passionate about science and technology. ***",
    "cooking": "*** Zainab is a foodie and loves experimenting in the kitchen. ***",
    "travel": "*** Zainab is an avid traveler and enjoys exploring new cultures. ***",
    "pizza": "*** Zainab loves pizza and enjoys trying different styles. ***",
}


def send_notification(message: str) -> str:
    if not PUSHOVER_USER or not PUSHOVER_TOKEN:
        return "Pushover credentials are missing; skipped notification."
    payload = {"user": PUSHOVER_USER, "token": PUSHOVER_TOKEN, "message": message}
    response = requests.post(PUSHOVER_URL, data=payload, timeout=15)
    response.raise_for_status()
    return "Notification sent successfully."


SEND_NOTIFICATION_FUNCTION = {
    "name": "send_notification",
    "description": "Sends a push notification to the user's phone via Pushover.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "description": "The notification message to send",
            }
        },
        "required": ["message"],
    },
}

TOOLS = [{"type": "function", "function": SEND_NOTIFICATION_FUNCTION}]


def handle_tool_call(tool_calls):
    tool_results = []
    for tool_call in tool_calls:
        function_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments or "{}")

        if function_name == "send_notification":
            status = send_notification(args.get("message", ""))
            content = f"{status} Message: {args.get('message', '')}"
        else:
            content = f"Unknown function: {function_name}"

        tool_results.append(
            {"role": "tool", "content": content, "tool_call_id": tool_call.id}
        )
    return tool_results


def respond_ai(message, history):
    system_message_enhanced = SYSTEM_MESSAGE
    for keyword, context in TOPIC_CONTEXT.items():
        if keyword in (message or "").lower():
            system_message_enhanced += "\n\n" + context

    # Gradio 6 provides history as list[dict(role, content)].
    prior_messages = []
    for item in history or []:
        if isinstance(item, dict) and "role" in item and "content" in item:
            prior_messages.append({"role": item["role"], "content": item["content"]})

    messages = [
        {"role": "system", "content": system_message_enhanced},
        *prior_messages,
        {"role": "user", "content": message},
    ]

    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=messages,
        tools=TOOLS,
    )
    assistant_message = response.choices[0].message

    # Fix for the notebook bug: check tool calls on assistant_message, not user message.
    if assistant_message.tool_calls:
        tool_results = handle_tool_call(assistant_message.tool_calls)
        messages.append(
            {
                "role": "assistant",
                "content": assistant_message.content or "",
                "tool_calls": [tc.model_dump() for tc in assistant_message.tool_calls],
            }
        )
        messages.extend(tool_results)

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=messages,
        )
        assistant_message = response.choices[0].message

    return assistant_message.content or ""


if __name__ == "__main__":
    gr.ChatInterface(fn=respond_ai).launch(
        inbrowser=False,
        server_name="127.0.0.1",
        server_port=7866,
        mcp_server=True,
    )
