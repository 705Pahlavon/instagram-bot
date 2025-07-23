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

# Instagram linklar uchun ishlovchi
def handle_message(update: Update, context: CallbackContext):
    user = update.effective_user
    if not check_subscription(user.id, context):
        button = InlineKeyboardButton("🔗 Obuna bo‘lish", url=f"https://t.me/{REQUIRED_CHANNEL[1:]}")
        markup = InlineKeyboardMarkup([[button]])
        update.message.reply_text("❗ Avval kanalga obuna bo‘ling:", reply_markup=markup)
        return

    text = update.message.text
    if "instagram.com" in text:
        update.message.reply_text("📥 Yuklanmoqda... (Instagram yuklash kodini shu yerga yoziladi)")
    else:
        update.message.reply_text("❌ Bu Instagram link emas!")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))

    updater.start_polling()
    updater.idle()
