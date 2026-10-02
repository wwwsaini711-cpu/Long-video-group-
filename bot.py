import threading
import time
from flask import Flask
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo

BOT_TOKEN = "8942479880:AAE_9nn_A_DljZElFOZDCLnWatkrHvw89IY"
ADMIN_CHAT_ID = 8986708946
NEW_UPI_ID = "9983940698-2.wallet@phonepe"

# 👉 आपकी शॉर्ट ग्रुप लिंक
SHORT_GROUP_LINK = "https://t.me/+jJwc2-GtgehhNzhl"

# 👉 बॉट का यूज़रनेम
BOT_USERNAME = "longvideoup_bot"

# 10 डेमो वीडियो File IDs
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

# 12 ऑटो-सेंड वीडियो File IDs
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

user_referrals = {}
referred_by = {}

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
            "🎁 Get 5% Discount (Share)", callback_data="share_discount"
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


def start_auto_sequence(user_id):
    def run_sequence():
        for i, video_id in enumerate(AUTO_VIDEOS):
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
                break

    t = threading.Thread(target=run_sequence)
    t.start()


@bot.message_handler(commands=["start"])
def send_welcome(message):
    user_id = message.chat.id
    user_ids.add(user_id)
    user_demo_count[user_id] = 1

    command_args = message.text.split()
    if len(command_args) > 1:
        referrer_id = command_args[1]
        try:
            referrer_id = int(referrer_id)
            if (
                referrer_id != user_id
                and user_id not in referred_by
                and referrer_id in user_ids
            ):
                referred_by[user_id] = referrer_id
                user_referrals[referrer_id] = (
                    user_referrals.get(referrer_id, 0) + 1
                )
                count = user_referrals[referrer_id]

                bot.send_message(
                    referrer_id,
                    f"🎉 **आपके रेफरल लिंक से 1 नया यूज़र जुड़ा!**\n\nकुल शेयर: **{count}/5**"
                    + (
                        "\n\n🎁 **बधाई हो! 5 लोगों को शेयर करने पर आपको 5% का डिस्काउंट मिल गया है!**"
                        if count >= 5
                        else ""
                    ),
                    parse_mode="Markdown",
                )
        except Exception:
            pass

    video_id, caption_text, markup = get_demo_data(1)
    bot.send_video(
        user_id,
        video=video_id,
        caption=caption_text,
        parse_mode="Markdown",
        reply_markup=markup,
    )
    start_auto_sequence(user_id)


# DIRECT ADMIN BROADCAST
@bot.message_handler(
    func=lambda message: message.chat.id == ADMIN_CHAT_ID,
    content_types=["text", "photo", "video", "document"],
)
def admin_direct_broadcast(message):
    if message.text and message.text.startswith("/start"):
        return

    success, fail = 0, 0
    bot.reply_to(message, "⏳ सभी यूज़र्स को ब्रॉडकास्ट भेजा जा रहा है...")

    for uid in list(user_ids):
        try:
            bot.copy_message(
                chat_id=uid,
                from_chat_id=ADMIN_CHAT_ID,
                message_id=message.message_id,
            )
            success += 1
        except Exception:
            fail += 1

    bot.reply_to(
        message,
        f"📢 **Broadcast Complete!**\n✅ सफलता: {success}\n❌ असफलता: {fail}",
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

    elif call.data == "share_discount":
        ref_link = f"https://t.me/{BOT_USERNAME}?start={user_id}"
        count = user_referrals.get(user_id, 0)

        msg = (
            f"🎁 **5% डिस्काउंट ऑफर!**\n\n"
            f"पेमेंट पर 5% की छूट पाने के लिए अपने **5 दोस्तों** को इस लिंक से जोड़ें:\n\n"
            f"🔗 **आपकी शेयर लिंक:**\n`{ref_link}`\n\n"
            f"📊 **आपके कुल शेयर:** `{count} / 5`"
        )
        if count >= 5:
            msg += "\n\n✅ **5% डिस्काउंट एक्टिवेट हो चुका है! नीचे 'Buy VIP Membership' बटन से डिस्काउंटेड प्राइस में प्लान खरीदें।**"

        bot.send_message(user_id, msg, parse_mode="Markdown")

    elif call.data == "show_plans":
        count = user_referrals.get(user_id, 0)
        has_discount = count >= 5

        p1, p2, p3, p4 = 120, 200, 300, 400

        if has_discount:
            p1 = int(p1 * 0.95)
            p2 = int(p2 * 0.95)
            p3 = int(p3 * 0.95)
            p4 = int(p4 * 0.95)

        markup = InlineKeyboardMarkup()
        disc_text = " (5% OFF 🎉)" if has_discount else ""
        markup.row(
            InlineKeyboardButton(
                f"1️⃣ One month: {p1}₹{disc_text}",
                callback_data=f"pay_{p1}_1 Month",
            )
        )
        markup.row(
            InlineKeyboardButton(
                f"2️⃣ Three months: {p2}₹{disc_text}",
                callback_data=f"pay_{p2}_3 Months",
            )
        )
        markup.row(
            InlineKeyboardButton(
                f"3️⃣ Six months: {p3}₹{disc_text}",
                callback_data=f"pay_{p3}_6 Months",
            )
        )
        markup.row(
            InlineKeyboardButton(
                f"4️⃣ One year: {p4}₹{disc_text}",
                callback_data=f"pay_{p4}_1 Year",
            )
        )

        title_msg = (
            "🎉 **5% डिस्काउंट एक्टिवेटेड प्लान्स:**"
            if has_discount
            else "💎 **अपना प्लान चुनें:**"
        )
        bot.send_message(
            user_id,
            f"{title_msg}\n\nसब्सक्रिप्शन लेने के लिए अपनी पसंद का प्लान चुनें:",
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


app = Flask("")


@app.route("/")
def home():
    return "Bot Alive!"


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = threading.Thread(target=run)
    t.start()


keep_alive()

if __name__ == "__main__":
    bot.infinity_polling()
