import threading
import time
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo

BOT_TOKEN = "8942479880:AAE_9nn_A_DljZElFOZDCLnWatkrHvw89IY"
ADMIN_CHAT_ID = 8986708946
NEW_UPI_ID = "9983940698-2.wallet@phonepe"
SHORT_GROUP_LINK = "t.me/vidihkyyjddfh"

# 1. 10 डेमो वीडियो की लिस्ट
DEMO_VIDEOS = [
    "BAACAgUAAxkBAAKGH2q_R1LNT8kCYDXl-cs7_rU97Pr6AAL6IQAC7D_5VXkR60WWQbhoPQQ",
    "BAACAgUAAxkBAAKGHmq_R1I-O8ljRpkbHC4VOoOrTF-_AAL5IQAC7D_5VXDOvjdFlm8EPQQ",
    "BAACAgUAAxkBAAKGIGq_R1IzYEG9SiR1SZXXLeZZ407UAAL8IQAC7D_5VYWxexjuvqQQPQQ",
    "BAACAgUAAxkBAAKGIWq_R1LddFCHcpJReKzstpF3BrlTAAL9IQAC7D_5VX9bCkId5YkCPQQ",
    "BAACAgUAAxkBAAKGI2q_R1KkxED5p_kDJX_B3fNSLJITAAL_IQAC7D_5VWu4KShdLJR3PQQ",
    "BAACAgUAAxkBAAKGImq_R1IuG7en1DG2KoFCIDd9cMK7AAL-IQAC7D_5VUzE0vEJEni_PQQ",
    "BAACAgUAAxkBAAKGJGq_R1I88m9zak9PnUdydfqyJ3vSAAMiAALsP_lV0HIniDxrZbc9BA",
    "BAACAgUAAxkBAAKGJWq_R1LSXBQpwF9uOpUfn4LiMhqaAAIBIgAC7D_5VU7eOgufJXBtPQQ",
    "BAACAgUAAxkBAAKGJmq_R1IIVvwqPBKG8fPDIlJQa96PAAICIgAC7D_5VXOtCZ9l-TD1PQQ",
    "BAACAgUAAxkBAAKGJ2q_R1JfU1tuMBiFopnPBZO4H8PAAAIDIgAC7D_5VYzJ4SFIDGxUPQQ",
]

# 2. 12 ऑटो-सेंड वीडियो की लिस्ट
AUTO_VIDEOS = [
    "BAACAgUAAxkBAAKGMmq_SY2iqhmyPGpAnJoqNpdR-tLqAAIJIgAC7D_5VRUeh62Pj1KtPQQ",
    "BAACAgUAAxkBAAKGM2q_SY0KU1OgQALuL1Rs4-3cNvYYAAIKIgAC7D_5Ve-I5GFdsg6zPQQ",
    "BAACAgUAAxkBAAKGNGq_SY2BNsav1qbQ-kmfUCB0GdbJAAILIgAC7D_5VchlkdLVmlxdPQQ",
    "BAACAgUAAxkBAAKGNWq_SY0DC3xdS0ODLnCQ-HCaJeRoAAIMIgAC7D_5VYjQwefV6D6UPQQ",
    "BAACAgUAAxkBAAKGNmq_SY2ldbmYcs0SeGqwyxJInuVYAAINIgAC7D_5VRpqL5pLUMhFPQQ",
    "BAACAgUAAxkBAAKGN2q_SY0vyZGAjTtjJhls_5AaCeOwAAIOIgAC7D_5VW3li13s3eHJPQQ",
    "BAACAgUAAxkBAAKGOGq_SY2e_GDxuBwZpDd3encYvlQdAAIPIgAC7D_5Vb0LNzWht7wIPQQ",
    "BAACAgUAAxkBAAKGOWq_SY3LJc2luOnc2g0IE8ipaVBkAAIQIgAC7D_5VXWEGsBCBme4PQQ",
    "BAACAgUAAxkBAAKGOmq_SY0vcJ-O4LT1xVidNGo51watAAIRIgAC7D_5Vb6GXkjW9qWMPQQ",
    "BAACAgUAAxkBAAKGO2q_SY3CFZ3urLW-k5vYBW8_0S4vAAISIgAC7D_5VTg1s2dR0OcHPQQ",
    "BAACAgUAAxkBAAKGPGq_SY4Q2LNRZCCtL3GaesObAAFDywACEyIAAuw_-VWhHk817yPlPz0E",
    "BAACAgUAAxkBAAKGPWq_SY5pmkMpmFLxjBSOvHR75QNiAAIUIgAC7D_5VRFCafdwM5cfPQQ",
]

MAX_DEMO = len(DEMO_VIDEOS)
user_demo_count = {}
user_ids = set()

bot = telebot.TeleBot(BOT_TOKEN)


def get_demo_data(count):
    video_id = DEMO_VIDEOS[count - 1]
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("😍 NEXT DEMO 😍", callback_data="next_demo"))
    markup.row(
        InlineKeyboardButton("🎬 Short Video Group 🎬", url=SHORT_GROUP_LINK)
    )
    markup.row(
        InlineKeyboardButton(
            "📹 Long Video Group 📹", callback_data="show_plans"
        )
    )
    markup.row(
        InlineKeyboardButton(
            "🔓 Buy VIP Membership", callback_data="show_plans"
        )
    )

    caption_text = (
        f"⭐ **PREMIUM DEMO MODE** ⭐\n\n"
        f"✨ Demo Video: **{count} / {MAX_DEMO}**\n\n"
        f"🔥 पूरा वीडियो अनलॉक करने के लिए नीचे दिए गए प्लान बटन पर क्लिक करें!"
    )
    return video_id, caption_text, markup


# --- ऑटोमेटिक वीडियो शेड्यूल थ्रेड ---
def start_auto_sequence(user_id):
    def run_sequence():
        for i, video_id in enumerate(AUTO_VIDEOS):
            # 1 से 12 तक: हर 1 घंटे (3600 सेकंड) बाद
            # 12वें के बाद: हर 24 घंटे (86400 सेकंड) बाद
            delay = 3600 if i < 12 else 86400
            time.sleep(delay)

            try:
                bot.send_video(
                    user_id,
                    video=video_id,
                    caption=f"🔥 **Exclusive Video #{i+1}**\n\nVIP कंटेंट देखने के लिए प्लान अनलॉक करें!",
                    parse_mode="Markdown",
                )
            except Exception:
                break  # अगर यूज़र ने बॉट ब्लॉक कर दिया हो

    t = threading.Thread(target=run_sequence)
    t.start()


# --- कमांड्स और बॉट लॉजिक ---
@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    user_ids.add(user_id)
    user_demo_count[user_id] = 1

    video_id, caption_text, markup = get_demo_data(1)
    bot.send_video(
        user_id,
        video=video_id,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )

    # ऑटो शेड्यूल चालू करें
    start_auto_sequence(user_id)


# एडमिन ब्रॉडकास्ट कमांड (उदाहरण: /broadcast सभी दोस्तों को नमस्कार)
@bot.message_handler(commands=["broadcast"])
def broadcast_message(message):
    if message.chat.id == ADMIN_CHAT_ID:
        msg_text = message.text.replace("/broadcast ", "")
        if not msg_text or msg_text == "/broadcast":
            bot.reply_to(
                message, "कृपया ब्रॉडकास्ट करने के लिए कोई मैसेज लिखें।"
            )
            return

        success, fail = 0, 0
        for uid in list(user_ids):
            try:
                bot.send_message(uid, msg_text)
                success += 1
            except Exception:
                fail += 1
        bot.reply_to(
            message,
            f"📢 **Broadcast Complete!**\n✅ सफल: {success}\n❌ असफल: {fail}",
            parse_mode="Markdown",
        )


@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.message.chat.id

    if call.data == "next_demo":
        current_count = user_demo_count.get(user_id, 1)
        new_count = current_count + 1 if current_count < MAX_DEMO else 1
        user_demo_count[user_id] = new_count

        video_id, caption_text, markup = get_demo_data(new_count)
        media = InputMediaVideo(
            media=video_id, caption=caption_text, parse_mode="Markdown"
        )
        try:
            bot.edit_message_media(
                chat_id=user_id,
                message_id=call.message.message_id,
                media=media,
                reply_markup=markup,
            )
        except Exception:
            pass

    elif call.data == "show_plans":
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton(
                "1️⃣ One month: 120₹📸", callback_data="pay_120_1 Month"
            )
        )
        markup.row(
            InlineKeyboardButton(
                "2️⃣ Three months: 200₹⬇️", callback_data="pay_200_3 Months"
            )
        )
        markup.row(
            InlineKeyboardButton(
                "3️⃣ Six months: 300₹📸", callback_data="pay_300_6 Months"
            )
        )
        markup.row(
            InlineKeyboardButton(
                "4️⃣ One year: 400₹💎", callback_data="pay_400_1 Year"
            )
        )

        bot.send_message(
            user_id,
            "💎 **अपना प्लान चुनें:**\n\nलंबी वीडियो ग्रुप का सब्सक्रिप्शन लेने के लिए अपनी पसंद का प्लान चुनें:",
            parse_mode="Markdown",
            reply_markup=markup,
        )

    elif call.data.startswith("pay_"):
        parts = call.data.split("_")
        amount = parts[1]
        plan_name = parts[2]

        qr_url = f"https://api.qrserver.com/v1/create-qr-code/?size=300x300&data=upi://pay?pa={NEW_UPI_ID}%26pn=PhonePe%26am={amount}%26cu=INR"

        caption = (
            f"⚡ **Payment QR Code** ⚡\n\n"
            f"📌 Plan: **{plan_name}**\n"
            f"💰 Price: **₹{amount}**\n\n"
            "1️⃣ इस QR कोड को स्कैन करके पेमेंट करें।\n"
            "2️⃣ पेमेंट करने के बाद **पेमेंट का स्क्रीनशॉट** इस चैट में भेजें।"
        )
        try:
            bot.send_photo(
                user_id, photo=qr_url, caption=caption, parse_mode="Markdown"
            )
        except Exception:
            bot.send_message(user_id, caption, parse_mode="Markdown")


@bot.message_handler(content_types=["photo"])
def handle_payment_screenshot(message):
    user = message.from_user
    photo_file_id = message.photo[-1].file_id

    admin_caption = (
        f"🔔 **नया पेमेंट स्क्रीनशॉट प्राप्त हुआ!**\n\n"
        f"👤 यूज़र: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`"
    )
    bot.send_photo(
        ADMIN_CHAT_ID,
        photo=photo_file_id,
        caption=admin_caption,
        parse_mode="Markdown",
    )
    bot.reply_to(
        message,
        "✅ आपका पेमेंट स्क्रीनशॉट प्राप्त हो गया है। एडमिन द्वारा वेरिफिकेशन के बाद आपको तुरंत फुल एक्सेस मिल जाएगा।",
    )


# --- Flask keep-alive वेब सर्वर ---
app = Flask("")


@app.route("/")
def home():
    return "Bot is alive!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = threading.Thread(target=run)
    t.start()


keep_alive()

if __name__ == "__main__":
    print("🤖 Bot Online - All Features Active!")
    bot.infinity_polling(timeout=60, long_polling_timeout=30)
