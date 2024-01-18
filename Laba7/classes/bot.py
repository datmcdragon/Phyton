""" Bot main"""
import os
import json
from datetime import datetime
from prettytable import PrettyTable

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import Application,CommandHandler,MessageHandler,filters
from telegram.ext import ContextTypes,ConversationHandler
from Data.data import user_data, AGE, HOBBIES, FAVORITE_COLOR , EMAIL
from .validator import Validator
DATA_FOLDER = 'Data'

validator =  Validator()
#bottest = TestBot()

def get_user_history_filename(chat_id):
    """get user history """
    return os.path.join(DATA_FOLDER, f'history_{chat_id}.json')

def get_users_filename():
    """ get user info"""
    return os.path.join(DATA_FOLDER, 'users.json')

def save_history(chat_id, message, answer):
    """ save user history"""
    filename = get_user_history_filename(chat_id)
    try:
        with open(filename, 'r+',encoding = 'UTF-8') as file:
            history_file = json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        history_file = []
    history_file.append({
        'message': message,
        'answer': answer,
        'timestamp': datetime.now().isoformat()
    })

    os.makedirs(DATA_FOLDER, exist_ok=True)

    with open(filename, 'w',encoding = 'UTF-8') as file:
        json.dump(history_file, file, indent=4)
 
# Команда для перегляду історії користувача
async def history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Load user history"""
    chat_id = update.effective_chat.id
    filename = get_user_history_filename(chat_id)
    try:
        with open(filename, 'r',encoding = 'UTF-8') as file:
            history_file = json.load(file)
            message = "Ваша історія запитів:\n\n"
            os.makedirs(DATA_FOLDER, exist_ok=True)
            for item in history_file:
                message += f"{item['timestamp']}: Запит - {item['message']}\nВідповідь - {item['answer']}\n\n"
            await update.message.reply_text(message)
    except FileNotFoundError:
        await update.message.reply_text("Історія запитів відсутня.")


# Команда для початку введення завдань
async def start_task_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Start inpunt option"""
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name

    user_info = {
        'username': username,
        'first_name': first_name,
        'last_name': last_name
    }

    user_data[chat_id] = user_info

    # Ask for the first piece of information
    await update.message.reply_text("Hello! Let's get started. Please tell me your age.")

    return AGE

# Handlers for each state in the conversation
async def age_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ Age input"""
    age = update.message.text
    chat_id = update.effective_chat.id
    if validator.validate_age(age):
        # Якщо вік валідний, запитати улюблений колір
        user_data[chat_id]['age'] = age
        save_history(chat_id, f"Age entered: {age}", "Age is valid and saved.")
        await update.message.reply_text("Вік прийнято. Будь ласка, введіть ваш улюблений колір:")
        return FAVORITE_COLOR
    else:
        # Якщо вік невалідний, попросити ввести знову
        save_history(chat_id, f"Age entered: {age}", "Invalid age format.")
        await update.message.reply_text("Невірний вік. Введіть вік ще раз:")
        return AGE


async def favorite_color_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ color input"""
    chat_id = update.effective_chat.id
    color = update.message.text
    if validator.validate_color(color):

        user_data[chat_id]['fav_color'] = color
        save_history(chat_id, f"Color entered: {color}", "Color is valid and saved.")
        await update.message.reply_text("Interesting! What are your hobbies?")
        return HOBBIES
    else:
        save_history(chat_id, f"Color entered: {color}", "Invalid color format.")
        await update.message.reply_text("Невірна палітра кольорів. Введіть ще раз:")
        return FAVORITE_COLOR

async def hobbie_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ hobbie input"""
    chat_id = update.effective_chat.id
    hobbies = update.message.text
    # Split the hobbies by comma and remove leading/trailing whitespace
    hobbies_list = [[hobbie.strip()] for hobbie in hobbies.split(',')]
    
    if all(validator.validate_hobbie(hobbie) for hobbie in hobbies_list):
        user_data[chat_id]['hobbies'] = hobbies_list  # Save hobbies as a list
        save_history(chat_id, f"hobbies entered: {hobbies}", "hobbies is valid and saved.")
        await update.message.reply_text("I need to try that! And last one - what is your email?")
        return EMAIL
    else:
        save_history(chat_id, f"Hobbies entered: {hobbies}", "Invalid hobbies format.")
        await update.message.reply_text("There might be a mistake in your hobbies. Please enter them again separated by commas.")
        return HOBBIES


async def email_input(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ email input"""
    chat_id = update.effective_chat.id
    email = update.message.text
    if validator.validate_email(email):
        user_data[chat_id]['email'] = email
        save_history(chat_id, f"Email entered: {email}", "email is valid and saved.")
        save_user_data(user_data[chat_id])

        await update.message.reply_text("Well done,now type /print to see all information!")
        return ConversationHandler.END
    else:
        save_history(chat_id, f"Email entered: {email}", "Invalid email format.")
        await update.message.reply_text("Ви допустили помилку! Спробуйте ще раз")
        return EMAIL

# Зберегти введені дані користувача
def save_user_data(user_data):
    """ save user data"""
    try:
        # Try to open the file and read existing data
        with open(get_users_filename(), 'r+',encoding = 'UTF-8') as file:
            os.makedirs(DATA_FOLDER, exist_ok=True)
            data = json.load(file)
            # Append new user data
            data.append(user_data)
            # Move file pointer to the beginning for overwriting
            file.seek(0)
            # Write updated data
            json.dump(data, file, indent=4)
    except (FileNotFoundError, json.JSONDecodeError):
        # If file doesn't exist or is empty, create it and write the data
        with open(get_users_filename(), 'w',encoding = 'UTF-8') as file:
            json.dump([user_data], file, indent=4)

async def print_user_data(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        with open(get_users_filename(), 'r',encoding = 'UTF-8') as file:
            os.makedirs(DATA_FOLDER, exist_ok=True)
            users = json.load(file)
            message = "<b>User Information:</b>\n<pre>"
            message +="Username | First Name | Last Name | Age | Favorite Color | Hobbies | Email\n"
            message += "-" * 70 + "\n"  # Розділова лінія
            for user in users:
                hobbies_str = ', '.join(hobby for sublist in user['hobbies'] for hobby in sublist)
                message += f"{user['username']} | {user['first_name']} | {user['last_name']} | {user['age']} | {user['fav_color']} | {hobbies_str} | {user['email']}\n"
            message += "</pre>"
            await update.message.reply_text(message, parse_mode=ParseMode.HTML)
    except FileNotFoundError:
        await update.message.reply_text("No user information available.")

def display_data_in_console(users):
    """ display data in console"""
    table = PrettyTable()
    table.field_names=["Username","First Name","Last Name","Age","Favorite Color","Hobbies","Email"]

    for user in users:
        hobbies_str = ', '.join(hobby for hobby_list in user['hobbies'] for hobby in hobby_list)
        table.add_row([user['username'], user['first_name'], user['last_name'], 
        user['age'], user['fav_color'], hobbies_str, user['email']])

    print(table)

async def print_user_data_console(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """ Output user data into console"""
    try:
        with open(get_users_filename(), 'r',encoding = 'UTF-8') as file:
            os.makedirs(DATA_FOLDER, exist_ok=True)
            users = json.load(file)
            display_data_in_console(users)
    except FileNotFoundError:
        print("No user information available.")

# Command to cancel the conversation
async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """ cancel inputing values"""
    await update.message.reply_text('Operation cancelled.')
    return ConversationHandler.END

def main() -> None:
    """ main method"""
    application = Application.builder().token('5655207446:AAFV0v3R8scQtxhuuApOgGCnWkx7Tp1mXAM').build()
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start_task_input)],
        states={
            AGE: [MessageHandler(filters.TEXT & ~filters.COMMAND, age_input)],
            FAVORITE_COLOR: [MessageHandler(filters.TEXT & ~filters.COMMAND, favorite_color_input)],
            HOBBIES: [MessageHandler(filters.TEXT & ~filters.COMMAND, hobbie_input)],
            EMAIL: [MessageHandler(filters.TEXT & ~filters.COMMAND, email_input)]
               },
               fallbacks=[CommandHandler('cancel', cancel)],
    )
    application.add_handler(conv_handler)
    application.add_handler(CommandHandler("print", print_user_data))
    application.add_handler(CommandHandler("print_console", print_user_data_console))
    application.add_handler(CommandHandler('history', history))
    application.run_polling()


if __name__ == '__main__':
    main()
