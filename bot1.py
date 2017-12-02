import telebot
import telebot.types as types
from engine import process_engine

token = "486661624:AAGnAC3G8tPoIb3tbfogi2Ko8oLN32j_iAk"
bot = telebot.TeleBot(token)

@bot.message_handler(content_type=["location"])
def location_handler(message):
    lat = message.location.latitude
    lon = message.location.longitude
    data_name = message.chat.first_name
    print(message)
    msg = "{0}, your location is ({1};{2})".format(data_name, lat, lon)
    keyboard = types.ReplyKeyboardRemove()
    bot.send_message(message.chat.id, msg, reply_markup=keyboard)
    text, imagepath, newlocation = process_engine(lat, lon)
    if imagepath != "":
        img = open(imagepath, 'rb')
        bot.send_photo(message.chat.id, img)
    bot.send_message(message.chat.id, text, {'hide_keyboard': True})
    bot.send_location(message.chat.id, newlocation[0], newlocation[1],  {'hide_keyboard': True})

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

