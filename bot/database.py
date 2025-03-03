from pymongo import MongoClient
from bot.config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["telegram_bot_db"]

users_collection = db["users"]
admins_collection = db["admins"]
settings_collection = db["settings"]

# Ensure default values exist
if not settings_collection.find_one({"_id": "welcome_message"}):
    settings_collection.insert_one({"_id": "welcome_message", "message": "Hello! Welcome to the bot."})

def add_user(user_id):
    if not users_collection.find_one({"user_id": user_id}):
        users_collection.insert_one({"user_id": user_id})

def get_users():
    return [user["user_id"] for user in users_collection.find()]

def set_welcome_message(message):
    settings_collection.update_one({"_id": "welcome_message"}, {"$set": {"message": message}})

def get_welcome_message():
    return settings_collection.find_one({"_id": "welcome_message"})["message"]

def add_admin(admin_id):
    if not admins_collection.find_one({"admin_id": admin_id}):
        admins_collection.insert_one({"admin_id": admin_id})

def is_admin(user_id):
    return bool(admins_collection.find_one({"admin_id": user_id}))
