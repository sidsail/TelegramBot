#!/usr/bin/env python

import os
import requests
import re
import logging
from telegram.ext import Updater, Filters, \
        CommandHandler, MessageHandler, InlineQueryHandler

# @bisv1bot 
BOT_TOKEN = "YOUR OWN BOT TOKEN" 

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - '
                           '%(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

def hi(update, context):
    name = update.message.from_user.first_name
    update.message.reply_text("Hi, " + name + "!")

def help(update, context):
    update.message.reply_text("Help is on the way.\n"
            "/hi\n"
            "/help\n"
            "/reg 1st-CHILD-NAME; CLASS-NAME; 2nd-CHILD-NAME; CLASS-NAME\n"
            "     [;/-] can be the separation marks.")

def welcome(update, contet, member, is_bot):
    msg = "Welcome aboard, " + member + "!\n" 

    if is_bot == False:
        msg += "Please register youself by sending a message " \
               "to the group starting with \n" \
               "'/reg ' followed by the student(s) information: \n" \
               "       1st-CHILD-NAME; CLASS-NAME; "\
               "2nd-CHILD-NAME; CLASS-NAME\n" \
               "       For example: /reg Tom Lee; 8T; Jean Stone; 12"
    update.message.reply_text(msg)

def goodbye(update, contet, member, is_bot):
    msg = "Good-Bye, " + member + "!"
    update.message.reply_text(msg)

def register(update, contet):
    name = update.message.from_user.first_name
    info = update.message.text

    buf = info[5:] 
    # print(buf)
    info = re.split(r'[;/-]', buf)

    txt = ""
    n =  int(len(info) / 2)
    for i in range(0, n):
        student = info[2*i]
        grade = info[2*i + 1]
        txt += str(student) + " @ " + str(grade) + " : "

    if n == 0:
        msg = "Failed to register as: " + name
    else:
        msg = "You have successfully registered as: " + name + " -- " + txt

    update.message.reply_text(msg)

def message(update, context):
    print("\n====\n")
    print(str(update.message))
    print("\n====\n")
    new_member_list = update.message.new_chat_members
    if new_member_list != None:
        for member in new_member_list:
            #print("\n====\n")
            #print(str(member))
            #print("\n====\n")
            welcome(update, context, member.first_name, member.is_bot)
    member = update.message.left_chat_member
    # if member != None and member.is_bot == False:
    if member != None:
        #print("\n====\n")
        #print(str(member))
        #print("\n====\n")
        goodbye(update, context, member.first_name, member.is_bot)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    print("BISV1BOT Starts ...")

    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    # log all errors
    dp.add_error_handler(error)
 
    dp.add_handler(CommandHandler('hi', hi))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('reg', register))

    dp.add_handler(MessageHandler(Filters.all, message))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
