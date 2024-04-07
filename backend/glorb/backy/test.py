from other import *
'''this is just a file to run tests in before deploying to the full server'''






uri = "mongodb+srv://rrrenzorodriguez:fl33OHNShKMxpVqQ@cluster0.lt6citz.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Cluster0"]
collection = db["Users w/ chats"]
#insertion to the database 


#testcase passed
#insert_data("hey,how are you doing","this is a test for the embed")

insert_data("vat are you doing bheta")


