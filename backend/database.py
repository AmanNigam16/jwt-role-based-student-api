from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.getenv("MONGO_URL"))

db = client["studentdb"]

users = db["users"]
students = db["students"]