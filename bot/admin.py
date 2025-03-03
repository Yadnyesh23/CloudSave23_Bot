from bot.database import admins_collection

def add_admin(admin_id):
    """Adds a new admin to the database."""
    if not admins_collection.find_one({"admin_id": admin_id}):
        admins_collection.insert_one({"admin_id": admin_id})

def remove_admin(admin_id):
    """Removes an admin from the database."""
    admins_collection.delete_one({"admin_id": admin_id})

def list_admins():
    """Returns a list of all admin user IDs."""
    return [admin["admin_id"] for admin in admins_collection.find()]

def is_admin(user_id):
    """Checks if a user is an admin."""
    return bool(admins_collection.find_one({"admin_id": user_id}))
