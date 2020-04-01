from email import message

import telebot
from telebot import types
import COVID19Py

covid19 = COVID19Py.COVID19()
bot = telebot.TeleBot('*********************************')

@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
	btn1 = types.KeyboardButton('Во всём мире')
	btn2 = types.KeyboardButton('Украина')
	btn3 = types.KeyboardButton('Россия')
	btn4 = types.KeyboardButton('Беларусь')
	markup.add(btn1, btn2, btn3, btn4)

    send_message = f"<b>Привет {message.from_user.first_name}!</b><br>Чтобы узнать данные про коронавируса напишите название страны, например: США, Украина, Россия и так далее</br>"
	bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)#Тут почему-то ошибка с Bot и markup

# Функция, что сработает при отправке какого-либо текста боту
# Здесь отслеживания данных и вывод статистики по определенной стране
@bot.message_handler(content_types=['text'])
def mess(message):
	final_message = ""
	get_message_bot = message.text.strip().lower()
	if get_message_bot == "сша":
		location = covid19.getLocationByCountryCode("US")
	elif get_message_bot == "украина":
		location = covid19.getLocationByCountryCode("UA")
	elif get_message_bot == "россия":
		location = covid19.getLocationByCountryCode("RU")
	elif get_message_bot == "беларусь":
		location = covid19.getLocationByCountryCode("BY")
	elif get_message_bot == "казакхстан":
		location = covid19.getLocationByCountryCode("KZ")
	elif get_message_bot == "италия":
		location = covid19.getLocationByCountryCode("IT")
	elif get_message_bot == "франция":
		location = covid19.getLocationByCountryCode("FR")
	elif get_message_bot == "германия":
		location = covid19.getLocationByCountryCode("DE")
	elif get_message_bot == "япония":
		location = covid19.getLocationByCountryCode("JP")
	else:
		location = covid19.getLatest()
	final_message = f"<u>Данные по всему миру:</u><br><b>Заболевших: </b>{location['confirmed']:,}<br><b>Сметрей: </b>{location['deaths']:,}"

	if final_message == "":
		date = location[0]['last_updated'].split("T")
		time = date[1].split(".")
		final_message = f"<u>Данные по стране:</u><br>Население: {location[0]['country_population']:,}<br>" \
				f"Последнее обновление: {date[0]} {time[0]}<br>Последние данные:<br><b>" \
				f"Заболевших: </b>{location[0]['latest']['confirmed']:,}<br><b>Сметрей: </b>" \
				f"{location[0]['latest']['deaths']:,}"

	bot.send_message(message.chat.id, final_message, parse_mode='html')

# Это нужно чтобы бот работал всё время
bot.polling(none_stop=True)