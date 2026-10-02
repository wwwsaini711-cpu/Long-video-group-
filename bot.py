import os
from flask import Flask
from threading import Thread
import telebot

# 1. Flask Keep-Alive Server
app = Flask('')

@app.route('/')
def home():
    return "File ID Extractor is Running!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# 2. Bot Configuration (आपका नया टोकन)
BOT_TOKEN = "8942479880:AAE_9nn_A_DljZElFOZDCLnWatkrHvw89IY"
bot = telebot.TeleBot(BOT_TOKEN)

# 3. Handle /start command
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(
        message, 
        "👋 **File ID Extractor Bot चालू है!**\n\n"
        "मुझे कोई भी **वीडियो, फोटो या डॉक्यूमेंट** भेजें, मैं तुरंत आपको उसकी **File ID** निकाल कर दे दूँगा।"
    )

# 4. File ID Extractor Handler (वीडियो, फोटो, फाइल की ID देने के लिए)
@bot.message_handler(content_types=['photo', 'video', 'document', 'animation'])
def catch_file_id(message):
    f_id = None
    file_type = ""
    
    if message.video:
        f_id = message.video.file_id
        file_type = "Video"
    elif message.photo:
        f_id = message.photo[-1].file_id
        file_type = "Photo"
    elif message.document:
        f_id = message.document.file_id
        file_type = "Document"
    elif message.animation:
        f_id = message.animation.file_id
        file_type = "GIF/Animation"
        
    if f_id:
        response = (
            f"✅ <b>{file_type} की नई File ID:</b>\n\n"
            f"<code>{f_id}</code>\n\n"
            "<i>(आईडी को कॉपी करने के लिए ऊपर लिखे कोड पर टैप/क्लिक करें)</i>"
        )
        bot.reply_to(message, response, parse_mode="HTML")

# 5. Start Server and Bot
if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling(skip_pending_updates=True)
    
