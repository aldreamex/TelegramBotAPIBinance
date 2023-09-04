import requests
from datetime import datetime
import telebot
from telebot import types
from auth_data import token


def get_data():
    symbol = 'GALUSDT'
    req = requests.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}')
    response = req.json()
    # print(response)

    bid_Price = response['bidPrice'] #актуальная цена
    print(f" {datetime.now().strftime('Current time and date: %H:%M %d-%m-20%y ')}\n Sell GAL at the bid price: {bid_Price}")


def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, 'Hello friend! See the current price of a pair of GALUSDT!')

    @bot.message_handler(content_types=["text"])
    def sent_messages(message):
        if message.text.lower() == 'price':
            try:
                symbol = 'GALUSDT'
                req = requests.get(f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}')
                response = req.json()
                bid_Price = response['bidPrice']
                bot.send_message(
                    message.chat.id,
                    f" {datetime.now().strftime('Current time and date: %H:%M %d-%m-20%y ')}\nSell GAL at the bid price: {bid_Price}"
                )
            except Exception as ex:
                print(ex)
                bot.send_message(
                    message.chat.id,
                    "Whoops... Something went wrong..."
                )
        else:
            bot.send_message(message.chat.id, 'Whoops... It seems youre asking something I dont know how to:(')

    bot.polling()

if __name__ =='__main__':
    # get_data()
    telegram_bot(token)
