from telegram_bot import start, search, add_wine, search_flight, help_command
from telegram.ext import Application, CommandHandler
from telegram import Update, ForceReply


def main():
    # Create a bot instance
    application = Application.builder().token("7105985308:AAF_YDpXpO0e-LtyGPU5SWDNbJBciGWKxqE").build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))

    # Searcher
    application.add_handler(CommandHandler("search", search))

    # Add wine
    application.add_handler(CommandHandler("add_wine", add_wine))

    # Search flight
    application.add_handler(CommandHandler("search_flight", search_flight))

    # Help command to test - work this so there's real help
    application.add_handler(CommandHandler("help", help_command))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
