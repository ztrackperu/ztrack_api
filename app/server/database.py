import motor.motor_asyncio
from bson.objectid import ObjectId
from decouple import config


MONGO_DETAILS = config("MONGO_DETAILS")  # read environment variable
BD_DETAILS =config("BD_DETAILS")
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)
#integrado es nombre para la base de datos
#DATA_BASE = config("DATA_BASE")
#database = client.DATA_BASE
#print(DATA_BASE)
database = client[BD_DETAILS]

def collection(data):
    #student_collection = database.get_collection("students_collection")
    data_collection = database.get_collection(data)
    return data_collection

