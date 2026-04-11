from groq import Groq

client = Groq(api_key="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")

conversation_history = []

def ask_ai(command):
    global conversation_history

    command = command[:200]

    conversation_history.append({"role": "user", "content": command})
    conversation_history = conversation_history[-6:]

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=conversation_history,
        max_tokens=200
    )

    reply = response.choices[0].message.content

    conversation_history.append({"role": "assistant", "content": reply})

    return reply