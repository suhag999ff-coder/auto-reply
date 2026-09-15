import sqlite3
import logging
import asyncio

from telethon import TelegramClient, events, Button
from telethon.errors import (
    ApiIdInvalidError,
    PhoneNumberInvalidError,
    SessionPasswordNeededError,
    FloodWaitError,
)

# =========================================================
#                 TELEGRAM API CONFIG
# =========================================================

API_ID = 35291570
API_HASH = "c61e3095f2047a3c1161d461dc7bfa1c"

SESSION_NAME = "w8_noyon_personal"

# =========================================================
#                    SHOP CONFIG
# =========================================================

SHOP_URL = "https://dark-carding.vercel.app/"

OWNER_NAME = "W8 NOYON"
SHOP_NAME = "DARK CARD SHOP"

# =========================================================
#                    DATABASE
# =========================================================

DB_NAME = "auto_reply_users.db"

conn = sqlite3.connect(DB_NAME, check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY,
    first_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)
""")

conn.commit()

# =========================================================
#                    LOGGING
# =========================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# =========================================================
#                    TELEGRAM CLIENT
# =========================================================

client = TelegramClient(
    SESSION_NAME,
    API_ID,
    API_HASH
)

# =========================================================
#                    AUTO REPLY TEXT
# =========================================================

AUTO_REPLY = """
╭─「 ⚡ 𝗪𝟴 𝗡𝗢𝗬𝗢𝗡 」
│
│ 👋 <b>আসসালামু আলাইকুম!</b>
│
│ 📩 আপনার মেসেজটি সফলভাবে
│    <b>Received</b> হয়েছে। ✅
│
│ ⏳ এই মুহূর্তে আমি হয়তো
│    সরাসরি আপনার মেসেজের
│    উত্তর দিতে পারছি না।
│
│ 📌 চিন্তার কোনো কারণ নেই।
│    আপনার মেসেজটি আমার কাছে
│    পৌঁছে গেছে।
│
│ 🕐 সময় হলে আপনার মেসেজ
│    দেখে প্রয়োজন অনুযায়ী
│    আপনার সাথে যোগাযোগ করা হবে।
│
├─「 👨‍💻 𝗣𝗥𝗢𝗙𝗜𝗟𝗘 」
│
│  ├ 👤 Owner • <b>W8 NOYON</b>
│  ├ 💻 Role • <b>Developer</b>
│  ├ 📁 Service • <b>File Tools</b>
│  ├ 🌐 Service • <b>Web Projects</b>
│  └ 🛒 Brand • <b>DARK CARD SHOP</b>
│
├─「 ⚡ 𝗦𝗘𝗥𝗩𝗜𝗖𝗘𝗦 」
│
│  ├ 📁 Professional File Tools
│  ├ 🌐 Web Development Projects
│  ├ 🛠️ Digital Tools & Projects
│  └ 🛒 Dark Card Shop
│
├─「 📩 𝗔𝗨𝗧𝗢 𝗥𝗘𝗣𝗟𝗬 」
│
│  ├ Status • <b>Received ✅</b>
│  ├ Reply • <b>As Soon As Possible</b>
│  └ Mode • <b>Private Chat</b>
│
├─「 🛒 𝗗𝗔𝗥𝗞 𝗖𝗔𝗥𝗗 𝗦𝗛𝗢𝗣 」
│
│  💎 আমাদের Official Shop-এ গিয়ে
│     available services, projects
│     এবং প্রয়োজনীয় information
│     দেখতে পারবেন।
│
│  🌐 Shop দেখতে নিচের
│     <b>VISIT SHOP</b> button ব্যবহার করুন।
│
├──────────────────────
│
│ 🙏 যোগাযোগ করার জন্য
│    <b>ধন্যবাদ।</b>
│
│ 💙 আপনার Message আমাদের কাছে
│    গুরুত্বপূর্ণ।
│
╰─「 ⚡ 𝗪𝟴 𝗡𝗢𝗬𝗢𝗡 • 𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 」
"""

# =========================================================
#                    SHOP BUTTON
# =========================================================

SHOP_BUTTON = [
    [
        Button.url(
            "🛒 𝗩𝗜𝗦𝗜𝗧 𝗗𝗔𝗥𝗞 𝗖𝗔𝗥𝗗 𝗦𝗛𝗢𝗣",
            SHOP_URL
        )
    ]
]

# =========================================================
#                 PRIVATE MESSAGE HANDLER
# =========================================================

@client.on(events.NewMessage(incoming=True))
async def auto_reply_handler(event):

    # Only private chats
    if not event.is_private:
        return

    # Ignore messages sent by yourself
    if event.out:
        return

    user_id = event.sender_id

    if not user_id:
        return

    try:

        # Check whether user already contacted
        cursor.execute(
            "SELECT user_id FROM users WHERE user_id = ?",
            (user_id,)
        )

        existing_user = cursor.fetchone()

        # Save new user
        if not existing_user:

            cursor.execute(
                "INSERT INTO users (user_id) VALUES (?)",
                (user_id,)
            )

            conn.commit()

            logging.info(
                f"🆕 New private chat detected: {user_id}"
            )

        # Send reply
        await event.respond(
            AUTO_REPLY,
            buttons=SHOP_BUTTON,
            parse_mode="html",
            link_preview=False
        )

        logging.info(
            f"✅ Auto reply sent to: {user_id}"
        )

    except FloodWaitError as e:

        logging.warning(
            f"⏳ Telegram FloodWait: waiting {e.seconds} seconds"
        )

        await asyncio.sleep(e.seconds)

    except Exception as e:

        logging.error(
            f"❌ Auto reply error for {user_id}: {e}"
        )


# =========================================================
#                    STARTUP
# =========================================================

async def main():

    print()
    print("╭──────────────────────────────────╮")
    print("│        ⚡ 𝗪𝟴 𝗡𝗢𝗬𝗢𝗡 ⚡         │")
    print("│                                  │")
    print("│    𝗣𝗘𝗥𝗦𝗢𝗡𝗔𝗟 𝗔𝗨𝗧𝗢 𝗥𝗘𝗣𝗟𝗬     │")
    print("│                                  │")
    print("├──────────────────────────────────┤")
    print("│ 👨‍💻 Developer                    │")
    print("│ 📁 File Tools                    │")
    print("│ 🌐 Web Projects                  │")
    print("│ 🛒 Dark Card Shop                │")
    print("│ 📩 Private Auto Reply            │")
    print("│ 🛒 Shop Button                   │")
    print("├──────────────────────────────────┤")
    print("│          STATUS: ACTIVE          │")
    print("╰──────────────────────────────────╯")
    print()

    try:

        print("🔐 Connecting to Telegram...")

        await client.start()

        me = await client.get_me()

        print()
        print("╭──────────────────────────────────╮")
        print("│       ✅ TELEGRAM CONNECTED       │")
        print("├──────────────────────────────────┤")

        if me:
            username = (
                f"@{me.username}"
                if me.username
                else "No Username"
            )

            print(f"│ 👤 Account • {username:<17}│")
            print(f"│ 🆔 ID      • {str(me.id):<17}│")

        print("│                                  │")
        print("│ 🚀 AUTO REPLY: ACTIVE            │")
        print("│ 📩 PRIVATE CHAT: ENABLED         │")
        print("│ 🛒 SHOP BUTTON: ENABLED          │")
        print("╰──────────────────────────────────╯")
        print()
        print("📩 Waiting for incoming private messages...")
        print("🛒 Shop:", SHOP_URL)
        print()

        await client.run_until_disconnected()

    except ApiIdInvalidError:

        print()
        print("❌ API_ID / API_HASH INVALID")
        print()
        print("➡️ Telegram rejected your API credentials.")
        print("➡️ Check API_ID and API_HASH.")
        print()

    except PhoneNumberInvalidError:

        print()
        print("❌ INVALID PHONE NUMBER")
        print("➡️ Enter your Telegram number with country code.")
        print()

    except SessionPasswordNeededError:

        print()
        print("🔐 TWO-STEP VERIFICATION ENABLED")
        print("➡️ Telegram requires your 2FA password.")
        print()

    except KeyboardInterrupt:

        print()
        print("🛑 Auto Reply stopped.")

    except Exception as e:

        print()
        print("❌ Telegram Login/Connection Error")
        print(f"➡️ {e}")
        print()


# =========================================================
#                    RUN
# =========================================================

if __name__ == "__main__":
    try:
        asyncio.run(main())
    finally:
        conn.close()
