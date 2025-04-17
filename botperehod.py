<<<<<<< HEAD
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = 348653863  # Замени на свой Telegram ID
CHAT_LINK = "https://t.me/+Y9dHwT3FTRNhMDcy"  # Ссылка на твой чат

user_data = {}  # Хранилище заявок

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📩 Подать заявку", callback_data='apply')],
        [InlineKeyboardButton("🚫 Отказаться", callback_data='decline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    if query.data == 'apply':
        user_data[user_id] = {"username": username}
        await query.message.reply_text("Пожалуйста, напишите комментарий (имя, возраст, что-то о себе):")
        return

    if query.data == 'decline':
        await query.message.reply_text("Вы отказались от подачи заявки.")
        return

    if query.data.startswith("approve_") or query.data.startswith("reject_"):
        target_user_id = int(query.data.split("_")[1])
        if query.data.startswith("approve_"):
            await context.bot.send_message(chat_id=target_user_id, text=f"🎉 Ваша заявка одобрена! Добро пожаловать!\nВот ссылка: {CHAT_LINK}")
            await query.edit_message_text("✅ Заявка одобрена.")
        else:
            await context.bot.send_message(chat_id=target_user_id, text="😞 Ваша заявка отклонена.")
            await query.edit_message_text("❌ Заявка отклонена.")

# Получение комментария
async def handle_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    comment = update.message.text
    if user_id in user_data:
        user_data[user_id]["comment"] = comment
        username = user_data[user_id]["username"]

        keyboard = [
            [
                InlineKeyboardButton("✅ Принять", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"📨 Новая заявка от @{username}:\nКомментарий: {comment}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=text, reply_markup=reply_markup)
        await update.message.reply_text("Заявка отправлена на рассмотрение.")
    else:
        await update.message.reply_text("Пожалуйста, нажмите '📩 Подать заявку' сначала.")

# Запуск бота
def main():
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
=======
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

ADMIN_ID = 348653863  # Замени на свой Telegram ID
CHAT_LINK = "https://t.me/+Y9dHwT3FTRNhMDcy"  # Ссылка на твой чат

user_data = {}  # Хранилище заявок

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📩 Подать заявку", callback_data='apply')],
        [InlineKeyboardButton("🚫 Отказаться", callback_data='decline')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Выберите действие:", reply_markup=reply_markup)

# Обработка кнопок
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    username = query.from_user.username or query.from_user.first_name

    if query.data == 'apply':
        user_data[user_id] = {"username": username}
        await query.message.reply_text("Пожалуйста, напишите комментарий (имя, возраст, что-то о себе):")
        return

    if query.data == 'decline':
        await query.message.reply_text("Вы отказались от подачи заявки.")
        return

    if query.data.startswith("approve_") or query.data.startswith("reject_"):
        target_user_id = int(query.data.split("_")[1])
        if query.data.startswith("approve_"):
            await context.bot.send_message(chat_id=target_user_id, text=f"🎉 Ваша заявка одобрена! Добро пожаловать!\nВот ссылка: {CHAT_LINK}")
            await query.edit_message_text("✅ Заявка одобрена.")
        else:
            await context.bot.send_message(chat_id=target_user_id, text="😞 Ваша заявка отклонена.")
            await query.edit_message_text("❌ Заявка отклонена.")

# Получение комментария
async def handle_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    comment = update.message.text
    if user_id in user_data:
        user_data[user_id]["comment"] = comment
        username = user_data[user_id]["username"]

        keyboard = [
            [
                InlineKeyboardButton("✅ Принять", callback_data=f"approve_{user_id}"),
                InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{user_id}")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = f"📨 Новая заявка от @{username}:\nКомментарий: {comment}"
        await context.bot.send_message(chat_id=ADMIN_ID, text=text, reply_markup=reply_markup)
        await update.message.reply_text("Заявка отправлена на рассмотрение.")
    else:
        await update.message.reply_text("Пожалуйста, нажмите '📩 Подать заявку' сначала.")

# Запуск бота
def main():
    TOKEN = os.environ["BOT_TOKEN"]
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment))

    print("Бот запущен...")
    app.run_polling()

if __name__ == "__main__":
    main()
>>>>>>> 7d12e7ac009fdc9e53e895a3cf8d0e12c0fffe35
