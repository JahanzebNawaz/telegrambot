import telebot
import requests
import json
from telegram.constants import PARSEMODE_HTML, PARSEMODE_MARKDOWN, PARSEMODE_MARKDOWN_V2
from telebot import types
import telebot, requests, json



#########################################################################################

TOKEN = '' #BOT TOKEN

bot = telebot.TeleBot(TOKEN)
#########################################################################################

wrongcall = "Wrong command ! The commands are:\n\n/start \n/help\n\n/support"
debug = 'NO HERE
title = "<b>Your Bot Title</b>"


#########################################################################################
FAQ = types.InlineKeyboardButton(text="FAQ", callback_data="Faq")
GOBACK = types.InlineKeyboardButton(text="🔙 Go Back", callback_data="Start") 
BUY = types.InlineKeyboardButton(text="Buy", callback_data="Buy")
Male = types.InlineKeyboardButton(text="Male", callback_data="Male")
Female = types.InlineKeyboardButton(text="Female", callback_data="Female")
Next1 = types.InlineKeyboardButton(text="Next", callback_data="Next1")
Next2 = types.InlineKeyboardButton(text="Next", callback_data="Next2")

name = None

checks = {
    1: 'Enter your full nam',
    2: 'Enter your Address',
    3: 'Thanks'
}

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.data == "Buy":
                info = "<b>Upload Photo:</b>"
                keyboard = types.InlineKeyboardMarkup(row_width=2)    
                keyboard.add(Male,Female)
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=info, parse_mode=PARSEMODE_HTML,disable_web_page_preview=True)

                @bot.message_handler(content_types=["photo"])
                def any_msg(message):
                    file = message.photo[-1].file_id
                    obj = bot.get_file(file)
                    urll = "https://api.telegram.org/bot"+ TOKEN + "/getFile?file_id=" + file
                    b = requests.get(urll)
                    bc = b.text
                    bb = json.loads(bc)
                    bn = bb["result"]["file_path"]
                    global imgurl
                    imgurl = "https://api.telegram.org/file/bot"+TOKEN+"/"+bn
                    keyboard = types.InlineKeyboardMarkup(row_width=2)
                    
                    keyboard.add(Male,Female)
                    
                    info = f"<b>Choose:</b>" 
                    global cid 
                    cid = message.chat.id
                    global username
                    username = message.from_user.username
                    bot.send_message(message.chat.id,text=info,reply_markup=keyboard,parse_mode=PARSEMODE_HTML)
                    info = f"NEW TEXT"
                    
                    bot.send_message(message.chat.id, text=info)
                    print(call.data)
                    print(message.text, "TEST 1")
                    

    elif call.data == "Male" or call.data =="Female":  #After we choose male or female
        global sex
        sex = call.data
        info = "What is your Name"
        bkl = bot.send_message(cid,text=info,parse_mode=PARSEMODE_HTML)
        bot.register_next_step_handler(bkl, process_age_step)   
	

def process_name_step(message):
    try:
        chat_id = message.chat.id
        name = message.text
        print(name)
        msg = bot.reply_to(message, 'How old are you?')
        bot.register_next_step_handler(msg, process_age_step)
    except Exception as e:
        bot.reply_to(message, 'oooops')

def process_age_step(message):
    try:
        chat_id = message.chat.id
        age = message.text
        if not age.isdigit():
            msg = bot.reply_to(message, 'Age should be a number. How old are you?')
            bot.register_next_step_handler(msg, process_age_step)
            return
        info = f"Thank You"
                    
        bot.send_message(message.chat.id, text=info)
    except Exception as e:
        bot.reply_to(message, 'oooops')

owner = "@your_telegram_bot_name"
ownerid = # owner ide here


@bot.message_handler(commands=["help","start"])
def any_msg(message):
    cid = message.chat.id
    username = message.from_user.username
    if username != None:
        userid = message.from_user.id
        try:      
            keyboard = types.InlineKeyboardMarkup(row_width=2)
            keyboard.add(BUY,FAQ)
            where_am_i = "<b><i>You are in the 'Main Menu' section !</i></b>"   
            info = f"{title}\n\nThis bot was created for the purpose  \n\n{where_am_i}"
            bot.send_message(message.chat.id, info, reply_markup=keyboard, parse_mode=PARSEMODE_HTML)
        except KeyError:
            bot.send_message(message.chat.id, "There is an issue server side.\n@ for support")
    else:
        bot.send_message(cid,"You can't use this bot if you dont have an unique username !\n\nSet up an username and try again !")


bot.polling(none_stop=True)
