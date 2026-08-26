import telebot
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaVideo

BOT_TOKEN = "8942479880:AAGlJB0I9UVRcpZqN1_0rhAPPSFJVoQWDDI"
ADMIN_CHAT_ID = 8986708946  
NEW_UPI_ID = "9983940698-2.wallet@phonepe"

# 👉 शॉर्ट वीडियो चैनल की लिंक (यह डायरेक्ट खुलेगी)
SHORT_GROUP_LINK = "t.me/vidihkyyjddfh" 

DEMO_VIDEOS = [
    "BAACAgUAAxkBAAMKaopxaRdmduoJBB0gMuepGoAPOXIAAmshAAKZEVhU-aEGhHh72u89BA",
    "BAACAgUAAxkBAAMMaopxb4bhhMe96a1rxLmALAUd7osAAmwhAAKZEVhUAYehV9md_rM9BA",
    "BAACAgUAAxkBAAMOaopxhsFG34Aj3ODYIEIaqhh3RwkAAm0hAAKZEVhUAW7tD_0gfNg9BA",
    "BAACAgUAAxkBAAMQaopxoodGZ8yk6F25VwpIFFHhmOkAAm4hAAKZEVhUp2EEc-buQew9BA",
    "BAACAgUAAxkBAAMSaopxvkMZbA-Tadj1GP3Y8bs3KV4AAm8hAAKZEVhUl0I9VVNjgHI9BA",
    "BAACAgUAAxkBAAMUaopx3SZWAAH1qQkNqfLi2zBEM7XLAAJxIQACmRFYVMvJbcl-1UHAPQQ",
    "BAACAgUAAxkBAAMWaopx7QXHIn_QNJPaepB9pYhzgCAAAnIhAAKZEVhUgbpURfeD85w9BA",
    "BAACAgUAAxkBAAMYaopyEpXiC3bNvrAMv1imgJe8db4AAnMhAAKZEVhUyi11rJObZTM9BA",
    "BAACAgUAAxkBAAMaaopyUTIAAZCN07tDCIE6IFrtrHZbAAJ0IQACmRFYVM9IqmYveEJTPQQ",
    "BAACAgUAAxkBAAMcaopyY7A5ozGvp8XYwy3ZAYYyytAAAnUhAAKZEVhUNAa3-QbZrfc9BA"
]

MAX_DEMO = len(DEMO_VIDEOS)
user_demo_count = {}

bot = telebot.TeleBot(BOT_TOKEN)

def get_demo_data(count):
    video_id = DEMO_VIDEOS[count - 1]
    markup = InlineKeyboardMarkup()
    markup.row(InlineKeyboardButton("😍 NEXT DEMO 😍", callback_data="next_demo"))
    markup.row(InlineKeyboardButton("🎬 Short Video Group 🎬", url=SHORT_GROUP_LINK))
    # लॉन्ग वीडियो ग्रुप बटन अब पेमेंट/प्लान दिखाएगा
    markup.row(InlineKeyboardButton("📹 Long Video Group 📹", callback_data="show_plans"))
    markup.row(InlineKeyboardButton("🔓 Buy VIP Membership", callback_data="show_plans"))

    caption_text = (
        f"⭐ **PREMIUM DEMO MODE** ⭐\n\n"
        f"✨ Demo Video: **{count} / {MAX_DEMO}**\n\n"
        f"🔥 पूरा वीडियो अनलॉक करने के लिए नीचे दिए गए प्लान बटन पर क्लिक करें!"
    )
    return video_id, caption_text, markup

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.chat.id
    user_demo_count[user_id] = 1
    video_id, caption_text, markup = get_demo_data(1)
    bot.send_video(user_id, video=video_id, caption=caption_text, parse_mode="Markdown", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_listener(call):
    user_id = call.message.chat.id
    
    if call.data == "next_demo":
        current_count = user_demo_count.get(user_id, 1)
        new_count = current_count + 1 if current_count < MAX_DEMO else 1
        user_demo_count[user_id] = new_count
        video_id, caption_text, markup = get_demo_data(new_count)
        media = InputMediaVideo(media=video_id, caption=caption_text, parse_mode="Markdown")
        try:
            bot.edit_message_media(chat_id=user_id, message_id=call.message.message_id, media=media, reply_markup=markup)
        except Exception:
            pass

    elif call.data == "show_plans":
        markup = InlineKeyboardMarkup()
        markup.row(InlineKeyboardButton("1️⃣ One month: 120₹📸", callback_data="pay_120_1 Month"))
        markup.row(InlineKeyboardButton("2️⃣ Three months: 200₹⬇️", callback_data="pay_200_3 Months"))
        markup.row(InlineKeyboardButton("3️⃣ Six months: 300₹📸", callback_data="pay_300_6 Months"))
        markup.row(InlineKeyboardButton("4️⃣ One year: 400₹💎", callback_data="pay_400_1 Year"))
        
        bot.send_message(user_id, "💎 **अपना प्लान चुनें:**\n\nलंबी वीडियो ग्रुप का सब्सक्रिप्शन लेने के लिए अपनी पसंद का प्लान चुनें:", parse_mode="Markdown", reply_markup=markup)

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
            bot.send_photo(user_id, photo=qr_url, caption=caption, parse_mode="Markdown")
        except Exception:
            bot.send_message(user_id, caption, parse_mode="Markdown")

@bot.message_handler(content_types=['photo'])
def handle_payment_screenshot(message):
    user = message.from_user
    photo_file_id = message.photo[-1].file_id
    
    admin_caption = (
        f"🔔 **नया पेमेंट स्क्रीनशॉट प्राप्त हुआ!**\n\n"
        f"👤 यूज़र: {user.first_name} (@{user.username})\n"
        f"🆔 User ID: `{user.id}`"
    )
    bot.send_photo(ADMIN_CHAT_ID, photo=photo_file_id, caption=admin_caption, parse_mode="Markdown")
    bot.reply_to(message, "✅ आपका पेमेंट स्क्रीनशॉट प्राप्त हो गया है। एडमिन द्वारा वेरिफिकेशन के बाद आपको तुरंत फुल एक्सेस मिल जाएगा।")

print("Bot Status: ONLINE - Long Video Group set to Subscription Plans")
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I am alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()
bot.infinity_polling(timeout=10, long_polling_timeout=5)
