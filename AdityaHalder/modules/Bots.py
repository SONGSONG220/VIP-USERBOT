import html

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from config import CMD_HANDLER
from JAPANESE.nxtgenhelper.basic import edit_or_reply
from JAPANESE.nxtgenhelper.parser import mention_html, mention_markdown
from .help import *

@Client.on_message(filters.command(["bots"], cmd) & filters.me)

async def get_list_bots(client: Client, message: Message):
    # Determine the chat to fetch bots from
    if len(message.text.split()) >= 2:
        chat = message.text.split(None, 1)[1]
    else:
        chat = message.chat.id
    
    try:
        grup = await client.get_chat(chat)
    except Exception as e:
        await message.edit(f"Failed to fetch chat information: {str(e)}")
        return
    
    # Determine if there's a reply message
    replyid = message.reply_to_message.id if message.reply_to_message else None
    
    # Fetch all members and filter bots
    try:
        bots = []
        async for member in client.iter_chat_members(chat):
            user = member.user
            name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name
            if not name.strip():
                name = "☠️ Deleted account"
            if user.is_bot:
                bots.append(mention_markdown(user.id, name))
    except Exception as e:
        await message.edit(f"Failed to fetch chat members: {str(e)}")
        return
    
    # Prepare the response text
    sakura = f"**All bots in group {grup.title}**\n"
    sakura += "╒═══「 Bots 」\n"
    
    for bot in bots:
        sakura += f"│ • {bot}\n"
    
    sakura += f"╘══「 Total {len(bots)} Bots 」"
    
    # Send or edit the message based on whether there's a reply
    if replyid:
        await client.send_message(message.chat.id, sakura, reply_to_message_id=replyid)
    else:
        await message.edit(sakura)
