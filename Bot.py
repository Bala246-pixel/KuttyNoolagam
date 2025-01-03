from pyrogram import Client, filters
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

# Bot API Token from BotFather
bot = Client("KuttyNoolagamBot", 
             api_id=int(os.getenv("API_ID")), 
             api_hash=os.getenv("API_HASH"), 
             bot_token=os.getenv("BOT_TOKEN"))

# Replace with the Bot Owner's Telegram ID
BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID"))

@bot.on_message(filters.private & ~filters.command("start"))
async def forward_request(_, message):
    # Extract User Details
    user_id = message.from_user.id
    username = message.from_user.username if message.from_user.username else "No username"
    nickname = message.from_user.first_name

    # Forward Request to Bot Owner
    request_message = f"""
📨 *New Book Request*:
👤 User ID: `{user_id}`
🔗 Username: @{username}
📝 Nickname: {nickname}
📖 Requested Book: {message.text}
"""
    forwarded_msg = await bot.send_message(chat_id=BOT_OWNER_ID, text=request_message, parse_mode="markdown")

    # Wait for response from the bot owner (e.g., for 5 minutes)
    try:
        # Here we set a timeout of 5 minutes for the bot owner to reply
        response = await bot.wait_for_message(chat_id=BOT_OWNER_ID, reply_to_message_id=forwarded_msg.message_id, timeout=300)
    except asyncio.TimeoutError:
        # If no response after 5 minutes, notify the user
        await message.reply("✅ Your request has been accepted. We'll get back to you soon!")

    # Acknowledge the User immediately after forwarding the request
    await message.reply("✅ Your request has been forwarded to the admin. We’ll get back to you soon!")

@bot.on_message(filters.command("start"))
async def start(_, message):
    await message.reply("Welcome to Kutty Noolagam 📚! Please send the name of the book you're looking for, and our admin will assist you.")

bot.run()
