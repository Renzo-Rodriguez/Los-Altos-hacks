from django.shortcuts import render
from django.http import HttpResponse
import openai 
openai.api_key = "key"


# Create your views here.

def wants(request):
    # make api call right here
     # it should be text, we can just send that text here to the  open ai thingy


     return message

def ai(message):
    # parse through message and look through places that teh ai wants to
    model = "IDK"
    # need to add a way for the ai to make a db call aswell
 
    response = openai.Completion.create(engine=model, prompt=message, maxtokens=100)


