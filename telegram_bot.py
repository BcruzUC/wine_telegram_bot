import psycopg2
from telegram import Update, ForceReply
from telegram.ext import ContextTypes
from misc_functions import print_result




# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


# Help comand to test replies
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) != 2:
        await update.message.reply_text("Usage: /search <attribute> <attribute_name>\n\n"
                                        "Atributes: \nName\nType\nNotes\nBarrel\nTime\nSugar\nGrapes\n")
        # context.bot.send_message(chat_id=update.effective_chat.id, text="Usage: /search <attribute> <attribute_name>")
        return

    attribute = args[0]
    attribute_name = args[1]

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname='wine_bot',
        user='benjacruz',
        password='bcruz123',
        host='localhost'
    )
    cur = conn.cursor()

    # Execute SQL query to search for wines
    cur.execute("SELECT * FROM wine_description WHERE lower({}) LIKE %s".format(attribute),
                ('%' + attribute_name.lower() + '%',))
    found_wines = cur.fetchall()

    # Close database connection
    cur.close()
    conn.close()

    if found_wines:
        result_text = print_result(found_wines)
        await update.message.reply_text(result_text)
    else:
        await update.message.reply_text("No wines found with the specified attribute.")


async def add_wine(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the user input
    user_input = context.args
    user_input_joined = " ".join(user_input)

    # Check if the user provided enough attributes
    if len(user_input) < 1:
        await update.message.reply_text("Usage: /add_wine <category1>-<content>,<category2>-<content>,...")
        return

    # Parse the attributes provided by the user
    wine_attributes = {}
    user_input_list = user_input_joined.split(',')
    for item in user_input_list:
        category, content = item.split('-')
        wine_attributes[category] = content

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname='wine_bot',
        user='benjacruz',
        password='bcruz123',
        host='localhost'
    )
    cur = conn.cursor()

    # Insert the new wine into the database
    try:
        cur.execute("INSERT INTO wine_description (name, type, notes, barrel, time_barrel, sugar, grapes) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (wine_attributes.get('name', ''), wine_attributes.get('type', ''),
                     wine_attributes.get('notes', ''), wine_attributes.get('barrel', ''),
                     wine_attributes.get('time', ''), wine_attributes.get('sugar', ''),
                     wine_attributes.get('grapes', '')))
        conn.commit()
        await update.message.reply_text("Wine added successfully!")
    except Exception as e:
        conn.rollback()
        await update.message.reply_text(f"An error occurred: {e}")

    # Close database connection
    cur.close()
    conn.close()


async def search_flight(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get the flight_id from user input
    args = context.args
    if len(args) != 1:
        await update.message.reply_text("Usage: /search_flight <flight_id>")
        return

    flight_id = args[0]

    # Connect to PostgreSQL database
    conn = psycopg2.connect(
        dbname='wine_bot',
        user='benjacruz',
        password='bcruz123',
        host='localhost'
    )
    cur = conn.cursor()

    # Execute SQL query to search for wines related to the specified flight
    cur.execute("SELECT wd.* FROM flight_of_fancy ff JOIN wine_description wd ON ff.wine_1_id = wd.id OR ff.wine_2_id = wd.id OR ff.wine_3_id = wd.id "
                "WHERE ff.flight_id = %s AND ff.flight_status = 1", (flight_id,))
    found_wines = cur.fetchall()
    # cur.execute("SELECT flight_name FROM flight_of_fancy WHERE flight_id = %s", (flight_id,))
    # flight_name = cur.fetchall()[0][0]

    # Close database connection
    cur.close()
    conn.close()

    if found_wines:
        result_text = print_result(found_wines)
        await update.message.reply_text(result_text)
    else:
        await update.message.reply_text("No flight of fancy found for the specified number.")

