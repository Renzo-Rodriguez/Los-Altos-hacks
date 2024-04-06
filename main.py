import openai

openai.api_key = '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'

messages = [{"role": "system", "content": "You are a genius Artificial Intelligence robot that is akin to Jarvis from the goated Marvel series Iron Man."}]

# prompt = input("Would you like to talk to your AI Girlfriend (no to exit): ")
# while prompt != "no":
#     message = input("User: ")
#     messages.append({"role": "user", "content": message})
#     response = openai.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=messages
#     )
#     reply = response.choices[0].message.content
#     messages.append({"role": "assistant", "content": reply})
#     print("AI Girlfriend: " + reply + "\n")

def wants(prompt):
    # make api call right here
     # it should be text, we can just send that text here to the  open ai thingy
     
    messages.append({"role": "user", "content": prompt})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    return reply

prompt = input("Would you like to talk to your AI Girlfriend (no to exit): ")
while prompt != "no":
    check = input("User: ")
    if (check == "no"):
        print("Successfully exited!")
        break
    else: 
        print(wants(check))