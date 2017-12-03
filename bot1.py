import telebot
import telebot.types as types
from engine import process_engine
from engine import get_name

token = "486661624:AAGnAC3G8tPoIb3tbfogi2Ko8oLN32j_iAk"
bot = telebot.TeleBot(token)

@bot.message_handler(content_type=["location"])
def location_handler(message):
    lat = message.location.latitude
    lon = message.location.longitude
    print(message)
    bot.send_message(message.chat.id, "Введенный адрес: " + get_name(lat, lon), {'hide_keyboard': True})
    keyboard = types.ReplyKeyboardRemove()
    bot.send_chat_action(message.chat.id, "typing")
    res = process_engine(lat, lon)
    for i in res:
        bot.send_message(message.chat.id, get_name(i[0], i[1]), {'hide_keyboard': True})
        bot.send_location(message.chat.id, i[0], i[1],  {'hide_keyboard': True})
    bot.send_message(message.chat.id, 'Используй команду start для новой рекомендации.',
                     reply_markup=keyboard)

@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    keyboard.add(button_geo)
    sent = bot.send_message(message.chat.id, 'Привет, я бот. Поделись, пожалуйста, своим местоположением', reply_markup=keyboard)
    bot.register_next_step_handler(sent, location_handler)

@bot.message_handler()
def start2(message):
    print(message)

@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    bot.send_message(message.chat.id, message.text)



if __name__ == '__main__':
    bot.polling(none_stop=True)

