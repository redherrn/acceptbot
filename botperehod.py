import os
import logging
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение переменных окружения
TOKEN = os.getenv('BOT_TOKEN')
ADMIN_ID = int(os.getenv('ADMIN_ID', '348653863'))  # Ваш ID по умолчанию
CHAT_LINK = os.getenv('CHAT_LINK', 'https://t.me/+Y9dHwT3FTRNhMDcy')

if not TOKEN:
    logger.error("Не задан BOT_TOKEN! Завершаю работу.")
    exit(1)

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect('applications.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS applications (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            comment TEXT,
            status TEXT DEFAULT 'pending'
        )
    ''')
    conn.commit()
    conn.close()

init_db()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        keyboard = [
            [InlineKeyboardButton("📩 Подать заявку", callback_data='apply')],
            [InlineKeyboardButton("🚫 Отказаться", callback_data='decline')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "Привет! Выберите действие:",
            reply_markup=reply_markup
        )
    except Exception as e:
        logger.error(f"Ошибка в start: {e}")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        user_id = query.from_user.id
        username = query.from_user.username or query.from_user.first_name

        if query.data == 'apply':
            conn = sqlite3.connect('applications.db')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO applications (user_id, username) VALUES (?, ?)",
                (user_id, username)
            )
            conn.commit()
            conn.close()
            await query.message.reply_text("Пожалуйста, напишите комментарий (имя, возраст, что-то о себе):")
            return

        if query.data == 'decline':
            await query.message.reply_text("Вы отказались от подачи заявки.")
            return

        if query.data.startswith(("approve_", "reject_")):
            action, target_user_id = query.data.split("_")
            target_user_id = int(target_user_id)
            
            conn = sqlite3.connect('applications.db')
            cursor = conn.cursor()
            
            if action == 'approve':
                cursor.execute(
                    "UPDATE applications SET status = 'approved' WHERE user_id = ?",
                    (target_user_id,)
                )
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"🎉 Ваша заявка одобрена! Добро пожаловать!\nВот ссылка: {CHAT_LINK}"
                )
                await query.edit_message_text("✅ Заявка одобрена.")
            else:
                cursor.execute(
                    "UPDATE applications SET status = 'rejected' WHERE user_id = ?",
                    (target_user_id,)
                )
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text="😞 Ваша заявка отклонена."
                )
                await query.edit_message_text("❌ Заявка отклонена.")
            
            conn.commit()
            conn.close()
    except Exception as e:
        logger.error(f"Ошибка в button_handler: {e}")

async def handle_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_id = update.message.from_user.id
        comment = update.message.text
        
        conn = sqlite3.connect('applications.db')
        cursor = conn.cursor()
        cursor.execute(
            "SELECT username FROM applications WHERE user_id = ?",
            (user_id,)
        )
        result = cursor.fetchone()
        
        if result:
            username = result[0]
            cursor.execute(
                "UPDATE applications SET comment = ? WHERE user_id = ?",
                (comment, user_id)
            )
            conn.commit()
            
            keyboard = [
                [
                    InlineKeyboardButton("✅ Принять", callback_data=f"approve_{user_id}"),
                    InlineKeyboardButton("❌ Отклонить", callback_data=f"reject_{user_id}")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            text = f"📨 Новая заявка от @{username}:\nКомментарий: {comment}"
            await context.bot.send_message(
                chat_id=ADMIN_ID,
                text=text,
                reply_markup=reply_markup
            )
            await update.message.reply_text("Заявка отправлена на рассмотрение.")
        else:
            await update.message.reply_text("Пожалуйста, нажмите '📩 Подать заявку' сначала.")
        
        conn.close()
    except Exception as e:
        logger.error(f"Ошибка в handle_comment: {e}")

def main():
    try:
        app = ApplicationBuilder().token(TOKEN).build()
        
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(button_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment))
        
        logger.info("Бот запущен и работает...")
        app.run_polling()
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")

if __name__ == "__main__":
    main()