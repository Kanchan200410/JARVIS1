from groq import Groq
import os

# 🔐 Use environment variable (IMPORTANT)
client = Groq(api_key="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")

conversation_history = []

SYSTEM_PROMPT = """
You are JARVIS, an intelligent AI assistant.

- Be clear and concise
- Explain like a teacher when needed
- Help in coding, studies, and real-world understanding
"""

def ask_ai(command):
    global conversation_history

    command = command[:200]

    # Add system prompt only once
    if not any(msg["role"] == "system" for msg in conversation_history):
        conversation_history.insert(0, {"role": "system", "content": SYSTEM_PROMPT})

    conversation_history.append({"role": "user", "content": command})
    conversation_history = conversation_history[-8:]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history,
        max_tokens=300
    )

    reply = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": reply})

    return reply


# 🔥 NEW: Vision Explanation (ADD ONLY, no breaking)
def explain_vision(data):
    prompt = f"""
    Analyze and explain the following visual information:

    {data}

    Explain clearly what is happening.
    """

    return ask_ai(prompt)
#hello