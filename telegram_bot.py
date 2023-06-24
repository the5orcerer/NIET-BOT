# Importing Required Libraries, Imported os Module For Security
import time, threading, telebot
from datetime import datetime
from requests import get, post
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from timepie import get_time

BOT_TOKEN = '__BOT__'

def today():
   return get('__SERVER__').text.lower()

print(f'Bot started on {today()}')
keyboard = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
button1 = KeyboardButton('Help')
button2 = KeyboardButton('Credits')
button3 = KeyboardButton('Tasks')
button4 = KeyboardButton('Notice')
button5 = KeyboardButton('Routine')

tommorrow = KeyboardButton('Tommorrow')
previous = KeyboardButton('Previous')
sub = [tommorrow, previous]

keyboard.add(button1, button2, button3, button4, button5)
keyboard.add(*sub)

bot = telebot.TeleBot(BOT_TOKEN)
markup = telebot.types.InlineKeyboardMarkup()

@bot.message_handler(commands=['start'])
def send_welcome(message):
  markdown = f"""Hey *{message.chat.first_name} {message.chat.last_name}* Welcome To *Were Knights*.\n\nJust a simple and nice bot to help NIET students. :)"""

  bot.reply_to(message, markdown, parse_mode="Markdown", reply_markup=keyboard)
  print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['help'])
def send_help_message(message):
    help_text = "Welcome to the Help Center!\n\n" \
                "Here are some available commands:\n" \
                "/help - Display this help message\n" \
                "/author - Get information about the bot creator and contributors\n" \
                "/routine - To get today class routine\n" \
                "/notice - Latest notices from BETB and NIET\n" \
                "/tasks - Current homwork or practical tasks\n" \
                "Feel free to ask any questions or report issues."
    bot.reply_to(message, help_text)
    print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['author'])
def send_credit_info(message):
  credit_info = f"This bot is designed and created by [Abu Huraira](https://t.me/rootplinix) & *Knight Forever*.\nSpecial thanks to *NIET - Cronicals* for maintain this Bot.\n"
  bot.reply_to(message, credit_info, parse_mode="Markdown", reply_markup=markup)
  print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['routine'])
def send_routine(message):
  command_text = message.text  # Get the full command text
  command_args = command_text.split(' ')
  if len(command_args) == 2:
     routine = get_time(command_args[1].lower())
  else:
     routine = get_time(today())
  bot.reply_to(message, routine)
  print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")

def send_message(message):
    bot.send_message('@niet_cst', message)

# Function to schedule the message
def schedule_message():
    while True:
        current_time = datetime.now().strftime('%H:%M')
        if current_time == '00:05':
            send_message(get_time(today().lower()))
            break
        time.sleep(1)

scheduler = threading.Thread(target=schedule_message)

# Define a handler for channel messages
@bot.channel_post_handler(func=lambda message: True)
def handle_channel_message(message):
    if message.text.startswith('H.W'):
        data = {'data': message.text}
        rot = post('__SERVER__save_data', data=data).status_code
        print(f"Status Code : {rot}")
    elif message.text.startswith('Notice'):
        data = {'data': message.text}
        rot = post('__SERVER__save_notice', data=data).status_code
        print(f"Status Code : {rot}")

@bot.channel_post_handler(content_types=['photo'], func=lambda message: message.chat.username == 'niet_cst')
def handle_channel_photo(message):
    if message.caption == 'Notice':
        photo_file_id = message.photo[-1].file_id
        file_info = bot.get_file(photo_file_id)
        file_path = file_info.file_path
        downloaded_file = bot.download_file(file_path)
        with open('notice.jpg', 'wb') as file:
            file.write(downloaded_file)
        print('Photo downloaded successfully.')
    else:
        print('No photo matching the caption criteria.')
        
@bot.message_handler(commands=['tasks'])
def get_tasks(message):
  opf = open('/__READ__/data.txt', 'r').read()
  bot.reply_to(message, opf)
  print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")

@bot.message_handler(commands=['notice'])
def send_notice(message):
   with open('/__READ__/notice.jpg', 'rb') as image_file:
    # Send the message with the image and caption
    bot.send_photo(message.chat.id, photo=image_file, caption='Notice')
    image_file.close()
    opf = open('/__READ__/notice.txt', 'r').read()
    bot.reply_to(message, opf)
    print(f"[x] Replied To {message.chat.first_name} {message.chat.last_name}")
print("[x] Running\n")


# Button controls

@bot.message_handler(func=lambda message: True)
def handle_message(message):
   match message.text:
      case 'Help':
         send_help_message(message)
      case 'Credits':
         send_credit_info(message)
      case 'Tasks':
         get_tasks(message)
      case 'Routine':
         send_routine(message)
      case 'Tommorrow':
         routine = get_time('t')
         bot.reply_to(message, routine)
      case 'Previous':
         routine = get_time('p')
         bot.reply_to(message, routine)
      case 'Notice':
         send_notice(message)


# Waiting For New Messages
scheduler.start()
bot.infinity_polling()