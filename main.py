from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# TOKEN va admin ID
TOKEN = "8035496121:AAFllT7uo-we6QRreYZPj7v6beDqQS4wBmg"
ADMIN_ID = 7824942822

# Majburiy obuna uchun kanal
REQUIRED_CHANNEL = "@instaXsSaver"  # Bu sening kanal havolang

# Obuna tekshiruvi
def check_subscription(user_id, context: CallbackContext):
    try:
        member = context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"Xatolik: {e}")
        return False

# /start komandasi
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id, context):
        button = InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return
    update.message.reply_text("👋 Salom! Menga Instagram link yuboring.")

import requests
from bs4 import BeautifulSoup

def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id, context):
        button = InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text("❗ Avval kanalga obuna bo‘ling:", reply_markup=markup)
        return

    text = update.message.text
    if "instagram.com" in text:
        update.message.reply_text("📥 Yuklanmoqda...")

        try:
            # Yuklab olish uchun ssstik.io ishlatilmoqda
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
            }
            session = requests.Session()
            page = session.get("https://ssstik.io/en", headers=headers)
            soup = BeautifulSoup(page.content, "html.parser")

            token = soup.find("input", {"id": "token"})["value"]
            response = session.post("https://ssstik.io/abc", data={
                "id": text,
                "locale": "en",
                "tt": token
            }, headers=headers)

            soup = BeautifulSoup(response.content, "html.parser")
            video_url = soup.find("a", class_="result__btn")["href"]

            context.bot.send_video(chat_id=update.effective_chat.id, video=video_url, caption="✅ Instagram video yuklandi")
        except Exception as e:
            update.message.reply_text("❌ Videoni yuklab bo‘lmadi. Ehtimol, bu private post yoki link noto‘g‘ri.")
            print(e)
    else:
        update.message.reply_text("❌ Bu Instagram link emas!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# 🔐 TOKEN va ADMIN ID
TOKEN = "8035496121:AAFllT7uo-we6QRreYZPj7v6beDqQS4wBmg"
ADMIN_ID = 7824942822
REQUIRED_CHANNEL = "@instaXsSaver"  # Majburiy obuna kanaling

# ✅ Obuna tekshiruv funksiyasi
def check_subscription(user_id, context: CallbackContext):
    try:
        member = context.bot.get_chat_member(REQUIRED_CHANNEL, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

# 🚀 /start komandasi
def start(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id, context):
        button = InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text("❗ Botdan foydalanish uchun kanalga obuna bo‘ling:", reply_markup=markup)
        return
    update.message.reply_text("👋 Salom! Menga Instagram link yuboring.")

# 📥 Instagram linkni qabul qilish
def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id, context):
        button = InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text("❗ Avval kanalga obuna bo‘ling:", reply_markup=markup)
        return

    text = update.message.text
    if "instagram.com" in text:
        update.message.reply_text("📥 Yuklanmoqda... (Instagram yuklash kodini bu yerga yoziladi)")
    else:
        update.message.reply_text("❌ Bu Instagram link emas!")

# ⚙️ Admin panel funksiyasi
def admin_panel(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        update.message.reply_text("⛔ Siz admin emassiz.")
        return

    text = (
        "👨‍💻 <b>Admin Panel</b>\n\n"
        "1. 📊 Statistika (tez orada)\n"
        f"2. 📎 Obuna kanal: {REQUIRED_CHANNEL}\n"
        "3. 🔄 Kanalni o‘zgartirish (tez orada)\n"
        "4. 📤 Xabar yuborish (tez orada)"
    )
    update.message.reply_text(text, parse_mode="HTML")

# ✅ Barcha handlerlar shu yerda jamlanadi
def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin_panel))  # ← Admin komandasi
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
