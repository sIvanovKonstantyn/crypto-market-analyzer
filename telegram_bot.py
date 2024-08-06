import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
from crypto_market_analyzer import get_analyze_results

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Read the Telegram bot token from an environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Create a bot instance
bot = Bot(token=TOKEN)

# Define the chat ID of the user to send messages to
CHAT_ID = None


async def send_analysis():
    global CHAT_ID
    logging.info('send analysis...')
    logging.info(f'CHAT_ID: {CHAT_ID}')
    """
    Send the market analysis results to the user.
    """
    if CHAT_ID is None:
        return

    analysis = get_analyze_results()
    await bot.send_message(chat_id=CHAT_ID, text=f"Market Analysis Results:\n{analysis}")


async def start(update, context):
    """
    Start command handler.
    """
    global CHAT_ID
    CHAT_ID = update.effective_chat.id
    logging.info(f'CHAT_ID: {CHAT_ID}')
    await context.bot.send_message(chat_id=CHAT_ID,
                                   text="Bot started! You will receive market analysis updates.")


def main():
    # # Schedule the job
    # # https://apscheduler.readthedocs.io/en/3.x/userguide.html
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_analysis, 'interval', minutes=2)
    scheduler.start()

    # https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
    global TOKEN
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
