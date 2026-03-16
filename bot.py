import telebot


TOKEN = 'token_bot'


bot = telebot.TeleBot(TOKEN)

# 1. Обработка команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    # message.chat.id — уникальный ID чата
    # message.from_user.first_name — имя пользователя
    bot.send_message(
        message.chat.id, 
        f"Привет, {message.from_user.first_name}! Я твой первый бот."
    )

# 2. Обработка любого текста
@bot.message_handler(content_types=['text'])
def say_hello(message):
    text = message.text.lower()

    if text == 'как дела':
        bot.send_message(message.chat.id, "У меня всё отлично, я же робот! 🤖")
    else:
        # Эхо-ответ
        bot.send_message(message.chat.id, f"Вы написали: {text}")


print('Запуск бота!')
bot.polling(none_stop=True)
print('Завершение работы!')
