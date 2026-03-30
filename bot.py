import telebot
from telebot import types


TOKEN = '6132474961:AAHsN1fc7JTcW2IKrsEi94BZiYYocmlsAQU'


bot = telebot.TeleBot(TOKEN)


# Клавиатура
def get_main_menu_keyboard():
    """Основное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('📞 Позвонить')
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
    btn3 = types.InlineKeyboardButton('🌐 Google', url='https://google.com')
    markup.add(btn1, btn2, btn3)
    return markup


# 1. Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # message.chat.id — уникальный ID чата
    # message.from_user.first_name — имя пользователя
    bot.send_message(
        message.chat.id,
        f"Привет, {message.from_user.first_name}! Я твой первый бот!!!!",
        reply_markup=get_main_menu_keyboard()
    )


@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        '1',
        reply_markup=get_inline_menu_keyboard()
    )


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    # call — это нажатие, а не сообщение

    if call.data == 'contacts':
        bot.answer_callback_query(call.id)
        bot.send_message(call.message.chat.id, 'Отлично!')
    elif call.data == 'about':
        bot.answer_callback_query(call.id, 'Выбрано: about!')


# 2. Обработка любого текста
@bot.message_handler(content_types=['text'])
def say_hello(message):
    text = message.text.lower()

    if text == 'как дела':
        bot.send_message(message.chat.id, "У меня всё отлично, я же робот! 🤖")
    elif text == 'как вас зовут?':
        bot.send_message(message.chat.id, "Меня зовут Настя!")
    elif message.text == '📞 Позвонить':
        bot.send_message(message.chat.id, '📱 Наш номер: 8-999-000-00-00')
    elif message.text == '📍 Адрес':
        bot.send_message(message.chat.id, '🏢 ул. Пушкина, д. 1')
    else:
        # Эхо-ответ
        bot.send_message(message.chat.id, f"Вы написали: {text}")


print('Запуск бота!')
bot.polling(none_stop=True)
print('Завершение работы!')
