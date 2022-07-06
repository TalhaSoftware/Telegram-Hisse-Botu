# -*- coding: utf-8 -*-
"""
Created on Sat Jan  2 14:34:39 2021

@author: TalhaSoftware
"""


import requests
from bs4 import BeautifulSoup
import re 
import json

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def telegram_bot_sendtext(bot_message):
    
    bot_token = 'your_token_here'
    bot_chatID = 'chat_id'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)
    print(response.text)
    a =json.loads(response.text)
    return a

def getNumbers(str): 
    array = re.findall(r'[0123456789.]+', str) 
    return array 


def hissebilgicek(hisseadi):
    url = "https://walletinvestor.com/is-stock-forecast/"+hisseadi+"-stock-prediction"
    data = requests.get(url,headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 8.0; Pixel 2 Build/OPD3.170816.012) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Mobile Safari/537.36'}).text
    soup = BeautifulSoup(data,"html.parser")
    tarih = soup.find_all("td",{"class":"w0","data-col-seq":"0"})
    tarih = tarih[0].text
    minimum = soup.find_all("td",{"class":"w0","data-col-seq":"2"})
    minimum = minimum[0].text
    maximum = soup.find_all("td",{"class":"w0","data-col-seq":"3"})
    maximum = maximum[0].text
    
    dosya = open("bilgi.txt","a+")
    dosya.writelines(tarih+"\n")
    dosya.writelines(hisseadi+"\n")
    dosya.writelines(minimum+"\n")
    dosya.writelines(maximum+"\n")
    dosya.writelines("--------------------------------\n")
    
    
    direncler = soup.find_all("div",{"class":"panel-body panel-body-no-padding"})
    sayılar = getNumbers(direncler[3].text)
    
    for i in sayılar:
        if(len(i) == 1):
            sayılar.remove(i)
            
    gdirencler= sayılar[:3]
    gdestekler = sayılar[3:6]
    
    return [minimum,maximum,gdirencler,gdestekler,tarih]




def tahmin(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    hisseadi = update.message.text.replace("/tahmin ","").lower()
    print(hisseadi)
    cevaplar = hissebilgicek(hisseadi)
    cevaplar = hisseadi.upper()+"\n"+cevaplar[4]+"\n"+cevaplar[0]+"\n"+cevaplar[1]
    
    telegram_bot_sendtext(str(cevaplar))

def direnc(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    hisseadi = update.message.text.replace("/direnc ","").lower()
    print(hisseadi)
    cevaplar = hissebilgicek(hisseadi)
    cevaplar = hisseadi.upper()+"\n"+cevaplar[4]+"\n"+str(cevaplar[2])
    telegram_bot_sendtext(str(cevaplar))

def destek(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    hisseadi = update.message.text.replace("/destek ","").lower()
    print(hisseadi)
    cevaplar = hissebilgicek(hisseadi)
    part = cevaplar[3]
    part.pop(0)
    cevaplar = hisseadi.upper()+"\n"+cevaplar[4]+"\n"+str(part)
    telegram_bot_sendtext(str(cevaplar))

def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    #update.message.reply_text(update.message.text)
    pass

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    
    updater = Updater("your_token_here", use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    
    
    dispatcher.add_handler(CommandHandler("tahmin", tahmin))
    dispatcher.add_handler(CommandHandler("direnc", direnc))
    dispatcher.add_handler(CommandHandler("destek", destek))
    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
