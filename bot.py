import json
from datetime import datetime
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from gpt_recommender import get_movie_recommendation
from tmdb_lookup import search_movie


# توکن باتت رو اینجا بذار
TOKEN = "8113867591:AAGMuS9QpnyXCMdU50mv-d2AqBg7Lt4e7rM"

# فایل ذخیره اشتراک‌ها
SUBSCRIPTION_FILE = "subscribers.json"

# ذخیره کاربران در حالت "پیشنهاد فیلم"
pending_prompt_users = {}

# دکمه‌های کیبورد
keyboard = [
    ["buy/extend Subscription", "start"],
    ["Contact", "about us", "sub status", "Help"]
]
reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# بارگذاری اطلاعات اشتراک از فایل
def load_subscriptions():
    try:
        with open(SUBSCRIPTION_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# ذخیره اطلاعات اشتراک در فایل
def save_subscriptions(data):
    with open(SUBSCRIPTION_FILE, "w") as f:
        json.dump(data, f)

# دستور /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    data = load_subscriptions()

    if user_id not in data:
        data[user_id] = {
            "start_time": datetime.now().isoformat()
        }
        save_subscriptions(data)

    await update.message.reply_text(
        "Welcome! Choose an option below 👇",
        reply_markup=reply_markup
    )

# مدیریت پیام‌ها
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.effective_user.id)
    data = load_subscriptions()

    if text == "start":
        pending_prompt_users[user_id] = True
        await update.message.reply_text("What kind of movie or series are you in the mood for? 🎬")
        return

    if text == "My Subscription":
        user_info = data.get(user_id)
        if user_info:
            start_time = datetime.fromisoformat(user_info["start_time"])
            delta = datetime.now() - start_time
            days = delta.days
            hours = delta.seconds // 3600
            await update.message.reply_text(
                f"Your subscription started on {start_time.strftime('%B %d, %Y at %H:%M')}.\n"
                f"You’ve used {days} days and {hours} hours."
            )
        else:
            await update.message.reply_text("You don’t have an active subscription. Please contact support.")
        return

    if text == "Help":
        await update.message.reply_text("This bot gives you movie or series recommendations based on your mood 🎬")
        return

    if text == "Contact":
        await update.message.reply_text("Email us at support@example.com")
        return

    if text == "sub status":
        await update.message.reply_text("Your subscription is currently unlimited 😉")
        return

    if text == "buy/extend Subscription":
        await update.message.reply_text("This feature is not available yet 😢")
        return

    if text == "about us":
        await update.message.reply_text("🎬 A simple startup focused on smart movie recommendations.")
        return

    # اگر کاربر در حالت ارسال درخواست فیلم هست
    if pending_prompt_users.get(user_id):
        loading_msg = await update.message.reply_text("...")

        gpt_reply = get_movie_recommendation(user_id, text)

        movie_title = gpt_reply.split("\n")[0].split("(")[0].strip()
        movie_info = search_movie(movie_title)

        # حذف پیام "در حال جستجو..."
        await context.bot.delete_message(chat_id=update.effective_chat.id, message_id=loading_msg.message_id)

        if movie_info:
            caption = f"*🎬 {movie_info['title']}*\n\n{movie_info['overview']}"
            await update.message.reply_photo(photo=movie_info['poster_url'], caption=caption, parse_mode='Markdown')
        else:
            await update.message.reply_text(gpt_reply)

        return

    # اگر کاربر خارج از مود درخواست فیلم پیام فرستاد
    await update.message.reply_text("To get movie suggestions, tap *start* first.", parse_mode='Markdown')


# اجرای بات
if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot running with subscription tracking...")
    app.run_polling()

