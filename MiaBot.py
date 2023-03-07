import argparse
import json
import logging
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, CommandHandler

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

class MiaBot:
    def __init__(self, config):
        self.config = config

    def get_telegram_bot(self):
        # get token
        token = self.config['telegram-bot-token']

        # Create bot
        bot = ApplicationBuilder().token(token).build()

        # Add handlers
        bot.add_handler(CommandHandler('start', self.__start))
        bot.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), self.__chat))

        return bot

    def run(self):
        print('Config: {}'.format(self.config))
        print('Running bot')
        bot = self.get_telegram_bot()
        bot.run_polling()

    async def __start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

    async def __chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='MiaBot')
    parser.add_argument('-c', '--config', help='Config file', required=True)
    args = parser.parse_args()
    config = args.config

    # Load config file
    with open(config, 'r') as f:
        config = json.load(f)

    # Create bot
    bot = MiaBot(config)

    # Run bot
    bot.run()