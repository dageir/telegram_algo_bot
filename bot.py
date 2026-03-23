import telebot
from telebot import types


TOKEN = '6132474961:AAEhUY1rQRW-kWBJACKCv4rp3mEN-mQrsbE'


bot = telebot.TeleBot(TOKEN)


# Клавиатура
def get_main_menu_keyboard():
    """Основное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('📞 Контакты')
    btn2 = types.KeyboardButton('ℹ️ О нас')
    btn3 = types.KeyboardButton('📍 Адрес')
    btn4 = types.KeyboardButton('🔙 Назад')
    markup.add(btn1, btn2, btn3, btn4)
    return markup


def get_inline_menu_keyboard():
    """Инлайн-меню"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    btn1 = types.InlineKeyboardButton('📞 Контакты', callback_data='contacts')
    btn2 = types.InlineKeyboardButton('ℹ️ О нас', callback_data='about')
    btn3 = types.InlineKeyboardButton('🌐 Сайт', url='https://example.com')
    markup.add(btn1, btn2, btn3)
    return markup


# 1. Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # message.chat.id — уникальный ID чата
    # message.from_user.first_name — имя пользователя
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я твой первый бот!!!!"
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        'Какой-то текст'
    )


# 2. Обработка любого текста
@bot.message_handler(content_types=['text'])
def say_hello(message):
    text = message.text.lower()

    if text == 'как дела':
        bot.send_message(message.chat.id, "У меня всё отлично, я же робот! 🤖")
    elif text == 'как вас зовут?':
        bot.send_message(message.chat.id, "Меня зовут Настя!")
    else:
        # Эхо-ответ
        bot.send_message(message.chat.id, f"Вы написали: {text}")


print('Запуск бота!')
bot.polling(none_stop=True)
print('Завершение работы!')
