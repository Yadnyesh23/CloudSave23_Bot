from pyrogram import Client, filters
from bot.config import BOT_TOKEN
from bot.database import add_user, get_users, set_welcome_message, get_welcome_message, add_admin, is_admin

app = Client("my_bot", bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    add_user(user_id)
    welcome_message = get_welcome_message()
    await message.reply_text(welcome_message)

@app.on_message(filters.command("setmessage") & filters.user(lambda user, _: is_admin(user.id)))
async def set_message(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /setmessage <your_message>")
    
    new_message = " ".join(message.command[1:])
    set_welcome_message(new_message)
    await message.reply_text("Welcome message updated!")

@app.on_message(filters.command("broadcast") & filters.user(lambda user, _: is_admin(user.id)))
async def broadcast(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /broadcast <your_message>")

    broadcast_message = " ".join(message.command[1:])
    users = get_users()
    
    for user in users:
        try:
            await client.send_message(user, broadcast_message)
        except:
            pass  # Ignore blocked users

    await message.reply_text("Message broadcasted successfully!")

@app.on_message(filters.command("addadmin") & filters.user(lambda user, _: is_admin(user.id)))
async def add_new_admin(client, message):
    if len(message.command) < 2:
        return await message.reply_text("Usage: /addadmin <user_id>")
    
    new_admin_id = int(message.command[1])
    add_admin(new_admin_id)
    await message.reply_text(f"User {new_admin_id} added as admin!")
