from django.shortcuts import render
from django.http import HttpResponse
import OpenAI
from django.template import loader
import os, json
from other import *


messages = [{"role": "system", "content": "You are an ai tool, you will be used to help users fix things around their computer, you should try to be as usefull as possible,  asnwer questions, explain things, if you want more context on things, you can encase a querry that you want to make to a vector database like **text** if a message contains that , the message will not be sent to the user but the text inside the ** ** will be sent  to query a database, after the database query is done, it will send you new data, that you can use as more context, as the user talks to you more, more context will appear"}]

openai.api_key = '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'



def wants(prompt):
    # make api call rht here
    # it should be text, we can just send that text here to the  open ai thing 
    messages.append({"role": "user", "content": prompt})
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    #save result to the mongodb atlas vector database ;)- not yet

    message = ""
    for char in range(len(reply)-1):
        
        #check if the ai is trying to make a call to the database
        if reply[char] == "*" and reply[char+1] == "*":
            character = char+2
            while character != "*"
                message += reply[character]
            break
    if message = "":
        #nothing special happend so we can just return the reply
        return reply
    else:
        #make it call to the database:
        wants(get(message))
                



    
def home(request):
    response = html


def upload(request):
    if request.method != "POST":
        return HttpResponse("lam you are doing something wrong, it did not send a post request:(")
    try:
        json_object = json.loads(request.body)
    except:
        return HttpResponse(" yeah you send a post request but there was no json response found :(")
    filename  = f'data_something.json'

    try:
        with open(os.path.join(/home/github/project/static/, filename), 'w') as outfile:
            json.dump(json_object, outfile)
            return JsonResponse({'message': f'JSON data saved to: {filename}'})
    except OSError as e:
        return HttpResponse(f'error saving data: {e} you kind of suck dude')


#def take(request):
    #if request != "POST":
       # return HttpResponse("buddy, what are you doing, you didnt send a post request")
    #else:
       # name = 



