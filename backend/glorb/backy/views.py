from django.shortcuts import render
from django.http import HttpResponse
import openai

openai.api_key = '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'
messages = [{"role": "system", "content": "You are a genius Artificial Intelligence robot that is akin to Jarvis from the goated Marvel series Iron Man."}]


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
    return reply # will return chat gpt's message

def ai(message):
    # parse through message and look through places that teh ai wants to
    model = "IDK"
    # need to add a way for the ai to make a db call aswell
 
    response = openai.Completion.create(engine=model, prompt=message, maxtokens=100)


