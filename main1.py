import requests
from datetime import datetime
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from auth_data import token

def get_coin_info(symbol):
    api_key = '****************************************'
    headers = {
        'X-MBX-APIKEY': api_key
    }
    url = f'https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        update_time = datetime.fromtimestamp(data['closeTime'] / 1000).strftime('%H:%M:%S %d-%m-%Y')
        return f"<b>Название:</b> {data['symbol']}\n" \
               f"<b>Цена:</b> {data['lastPrice']}\n" \
               f"<b>Максимальная цена:</b> {data['highPrice']}\n" \
               f"<b>Минимальная цена:</b> {data['lowPrice']}\n" \
               f"<b>Объем торгов:</b> {data['volume']}\n" \
               f"<b>Время/дата обновления:</b>\n{update_time}"
    else:
        return None

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        bot.send_message(message.chat.id, '<b>Привет! Напиши интересующую криптовалюту, чтобы узнать ее текущую цену.</b>\n\n'
                                          '<b>Примеры:</b>\n'
                                          '<b>- GALBTC</b> (Gala/Bitcoin)\n'
                                          '<b>- SOLETH</b> (Solana/Ethereum)\n'
                                          '<b>- XRPUSDT</b> (Ripple/Dollar)\n'
                                          '- ...', parse_mode='HTML')

    @bot.message_handler(content_types=["text"])
    def sent_messages(message):
        symbol = message.text.upper()
        try:
            info_data = get_coin_info(symbol)
            if info_data:
                info_text = "<b>Актуальные данные:</b>\n" + info_data
                keyboard = InlineKeyboardMarkup()
                url_button = InlineKeyboardButton(text="Открыть на BINANCE", url=f"https://www.binance.com/ru/trade/{symbol}")
                keyboard.add(url_button)

                # buy_url = f"https://www.binance.com/ru/trade/{symbol}?type=buy"
                # buy_button = InlineKeyboardButton(text="Купить", url=buy_url)

                # sell_url = f"https://www.binance.com/ru/trade/{symbol}?type=sell"
                # sell_button = InlineKeyboardButton(text="Продать", url=sell_url)
                # keyboard.add(buy_button, sell_button)
                bot.send_message(message.chat.id, info_text, reply_markup=keyboard, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, "Проверьте правильность введенной вами криптовалюты")
        except Exception as ex:
            print(ex)
            bot.send_message(message.chat.id, "....")

    bot.polling()

if __name__ =='__main__':
    telegram_bot(token)