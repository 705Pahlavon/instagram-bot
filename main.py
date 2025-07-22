# main.py
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler, CallbackContext
import instaloader

BOT_TOKEN = "8035496121:AAFllT7uo-we6QRreYZPj7v6beDqQS4wBmg"
ADMIN_ID = 7824942822
sub_channels = set()

L = instaloader.Instaloader()

def user_has_subscribed(bot, user_id: int) -> bool:
    for ch in sub_channels:
        try:
            member = bot.get_chat_member(ch, user_id)
            if member.status in ['member', 'creator', 'administrator']:
                return True
        except:
            continue
    return False

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Assalomu alaykum! Instagram video linkini yuboring.")

def admin(update: Update, context: CallbackContext):
    if update.effective_user.id != ADMIN_ID:
        return update.message.reply_text("Siz admin emassiz!")
    keyboard = [
        [InlineKeyboardButton("➕ Kanal qo‘shish", callback_data='add')],
        [InlineKeyboardButton("➖ Kanal o‘chirish", callback_data='remove')],
        [InlineKeyboardButton("📋 Ro‘yxat", callback_data='list')]
    ]
    update.message.reply_text("Admin panel:", reply_markup=InlineKeyboardMarkup(keyboard))

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    uid = query.from_user.id
    if uid != ADMIN_ID:
        return query.answer("Ruxsat yo‘q.")
    if query.data == 'add':
        context.user_data['action'] = 'add'
        query.edit_message_text("Qo‘shiladigan kanal nomini kiriting:")
    elif query.data == 'remove':
        context.user_data['action'] = 'remove'
        query.edit_message_text("O‘chiriladigan kanal nomini kiriting:")
    elif query.data == 'list':
        txt = '\n'.join(sub_channels) or "Hozircha hech narsa yo‘q."
        query.edit_message_text("Majburiy obuna kanallari:\n" + txt)

def text_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    text = update.message.text.strip()

    if context.user_data.get('action') == 'add':
        sub_channels.add(text)
        update.message.reply_text(f"{text} qo‘shildi ✅")
        context.user_data['action'] = None
        return
    elif context.user_data.get('action') == 'remove':
        sub_channels.discard(text)
        update.message.reply_text(f"{text} o‘chirildi ❌")
        context.user_data['action'] = None
        return

    if not user_has_subscribed(context.bot, user.id):
        chlist = '\n'.join(sub_channels) or "Admin hali kanal qo‘shmagan."
        return update.message.reply_text(f"Iltimos, quyidagi kanallarga obuna bo‘ling:\n{chlist}")

    if "instagram.com" not in text:
        return update.message.reply_text("Instagram video link yuboring.")
    try:
        shortcode = text.rstrip('/').split('/')[-1]
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        if post.is_video:
            update.message.reply_video(post.video_url)
        else:
            update.message.reply_text("Bu video emas.")
    except:
        update.message.reply_text("Video yuklanmadi. Linkni tekshiring.")

def main():
    updater = Updater(BOT_TOKEN)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("admin", admin))
    dp.add_handler(CallbackQueryHandler(button))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, text_handler))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
