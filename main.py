import openai

openai.api_key = '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'

messages = [{"role": "system", "content": "You are an AI Girlfriend."}]

prompt = input("Would you like to talk to your AI Girlfriend (no to exit): ")
while prompt != "no":
    message = input("User: ")
    messages.append({"role": "user", "content": message})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})
    print("AI Girlfriend: " + reply + "\n")