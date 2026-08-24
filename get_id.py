import telebot

BOT_TOKEN = "8845638115:AAG_M99pO3u9tFHi9b6duBMsr8BIbk4zLak"
bot = telebot.TeleBot(BOT_TOKEN)

print("--- File ID Generator Started ---")

@bot.message_handler(content_types=['video'])
def get_video_id(message):
    file_id = message.video.file_id
    print(f"\nFile ID: \"{file_id}\"\n")
    bot.reply_to(message, "✅ File ID Termux स्क्रीन पर आ गई है!")

bot.polling(non_stop=True)
