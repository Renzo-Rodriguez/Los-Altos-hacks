from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from openai import OpenAI


####
###     this section is just for interaction with the database
####


#This is for the connections to the mongodb database, this is for the right thingy
uri = "mongodb+srv://rrrenzorodriguez:fl33OHNShKMxpVqQ@cluster0.lt6citz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Cluster0"]
collection = db["Users w/ chats"]

api_key = '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'

openclient = OpenAI(api_key = api_key)



def embed_text(text, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")  
   return openclient.embeddings.create(input = [text], model=model).data[0].embedding


#insert data into the database
def insert_data(data:str, embed = "")->None:
    if embed == "":
        embed = embed_text(data)
    else:
        embed = "this is just for testing, should not be run  normally"
    object = {
                "background": data,
                "embedded": embed,
            }
    collection.insert_one(object)


def get(data:str)->str:
    # Vector you want to search for (replace with your actual vector)
    query_vector = embed_text(data)

    pipeline = [
        {
            "$search": {
                "knn": {
                    "query": query_vector,
                    "index": "default",  # Replace with the name of your vector index
                    "k": 1  # Number of nearest neighbors to retrieve
                }
            }
        }
    ]

    search_results = collection.aggregate(pipeline).background

    return search_results
    



#openai.api_key = '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'





