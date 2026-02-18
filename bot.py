from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, ContextTypes, filters
import re

TOKEN = "8292780270:AAHkvgElSU5kZlIJfGSHF2cDpZEI03Sq6Fw"
TEACHER_ID = 6081029202

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 KazMathAI іске қосылды! Есеп жіберіңіз.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message is None:
        return

    user = update.message.from_user
    text = update.message.text or "[Мәтінсіз хабарлама]"

    # ✅ Мұғалім Reply жасаса → оқушыға қайта жіберу
    if user.id == TEACHER_ID and update.message.reply_to_message:
        replied_text = update.message.reply_to_message.text or ""

        # Сенің форматқа сай ID табу
        match = re.search(r"\((\d+)\)", replied_text)

        if match:
            student_id = int(match.group(1))

            await context.bot.send_message(
                chat_id=student_id,
                text=f"🤖 KazMathAI жауап берді:\n\n{text}"
            )

            await update.message.reply_text("✅ Жауап оқушыға жіберілді!")
        else:
            await update.message.reply_text("❌ ID табылмады. Дұрыс Reply жасаңыз.")
        return

    # ✅ Оқушыдан келсе → мұғалімге жіберу
    await context.bot.send_message(
        chat_id=TEACHER_ID,
        text=f"Оқушы @{user.username or 'None'} ({user.id}) жіберді:\n{text}"
    )

    await update.message.reply_text("✅ Қабылданды. Жауап күтіңіз...")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, handle_message))

    print("🚀 Бот іске қосылды!")
    app.run_polling()

if __name__ == "__main__":
    main()
