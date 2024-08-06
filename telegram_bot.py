import logging
from telegram import Bot, Update
from telegram.ext import Application, CommandHandler
import os
from trend_analyzer import get_analyze_results
from current_price_taker import get_current_prices

# Configure logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Read the Telegram bot token from an environment variable
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Create a bot instance
bot = Bot(token=TOKEN)


async def start(update, context):
    await bot.send_message(chat_id=update.effective_chat.id,
                           text=f"Available commands:\n"
                                "/prices\n"
                                "/market_trend")


async def send_market_trend(update, context):
    logging.info('send analysis...')
    logging.info(f'CHAT_ID: {update.effective_chat.id}')

    analysis = get_analyze_results()
    await bot.send_message(chat_id=update.effective_chat.id, text=f"Market Analysis Results:\n{analysis}")


async def send_prices(update, context):
    logging.info('send prices...')
    logging.info(f'CHAT_ID: {update.effective_chat.id}')

    prices = get_current_prices()
    await bot.send_message(chat_id=update.effective_chat.id, text=f"Current prices:\n{prices}")


def main():
    # https://github.com/python-telegram-bot/python-telegram-bot/tree/master/examples
    global TOKEN
    application = Application.builder().token(TOKEN).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("market_trend", send_market_trend))
    application.add_handler(CommandHandler("prices", send_prices))

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
