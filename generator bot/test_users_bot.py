# подключение библиотек
import json
from secrets import token_urlsafe

from faker import Faker
from telebot import TeleBot, types

# TODO: вставить свой токен
TOKEN = '6517753197:AAHhQz0UB3_tlPO1CKOAPINeioDQDD5Tbt8'
bot = TeleBot(TOKEN, parse_mode='html')
# библиотека для генерации тестовых ФИО
# указываем язык - русский
faker = Faker('ru_RU') 

# объект клавиаутры
main_menu_reply_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
# первый ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="Лишь 1️⃣"), types.KeyboardButton(text="Всего 2️⃣")
)
# второй ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="Целых 5️⃣"), types.KeyboardButton(text="Аж 🔟")
)
# третий ряд кнопок
main_menu_reply_markup.row(
    types.KeyboardButton(text="Ого, 1️⃣5️⃣"), types.KeyboardButton(text="Ничего себе, 2️⃣0️⃣")
)

# обработчик команды '/start'
@bot.message_handler(commands=['start'])
def start_message_handler(message: types.Message):
    # отправляем ответ на команду '/start'
    # не забываем прикрепить объект клавиатуры к сообщению
    bot.send_message(
        chat_id=message.chat.id,
        text="Привет!\nЭто бот для генерации тестовых пользователей. "\
        "Закончилась фантазия?🤔 Тогда, выбери сколько пользователей тебе нужно 👇🏻",
        reply_markup=main_menu_reply_markup)
    bot.send_video(message.chat.id, 'https://media1.giphy.com/media/nDSlfqf0gn5g4/giphy.gif?cid=6c09b952p8x7a3d1g7cq4zvumhv9267y71izjyq0s355qv4v&ep=v1_gifs_search&rid=giphy.gif&ct=g', None, 'Text')    
        
    


# обработчик всех остальных сообщений
@bot.message_handler()
def message_handler(message: types.Message):
    # определяем количество тестовых пользователей
    # или отправляем ошибку
    payload_len = 0
    if message.text == "Лишь 1️⃣":
        payload_len = 1
    elif message.text == "Всего 2️⃣":
        payload_len = 2
    elif message.text == "Целых 5️⃣":
        payload_len = 5
    elif message.text == "Аж 🔟":
        payload_len = 10
    elif message.text == "Ого, 1️⃣5️⃣":
        payload_len = 15
    elif message.text == "Ничего себе, 2️⃣0️⃣":
        payload_len = 20
    else:
        bot.send_message(chat_id=message.chat.id, text="Чего ты хочешь от меня, друг?🧐")
        return

    # генерируем тестовые данные для выбранного количества пользователей
    # при помощи метода simple_profile
    total_payload = []
    for _ in range(payload_len):
        user_info = faker.simple_profile()
        user_info['phone'] = f'+7{faker.msisdn()[3:]}'
        # при помощи библиотеки secrets генерируем пароль
        user_info['password'] = token_urlsafe(10)
        total_payload.append(user_info)

    # сериализуем данные в строку
    payload_str = json.dumps(
        obj=total_payload,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
        default=str
    )

    # отправляем результат
    bot.send_message(
        chat_id=message.chat.id,
        text=f"Данные {payload_len} тестовых пользователей:\n<code>"\
        f"{payload_str}</code>"
    )
    bot.send_message(
        chat_id=message.chat.id,
        text="Мало пользователей? Пользуйся, сколько нужно 👇🏻",
        reply_markup=main_menu_reply_markup
    )
    

# главная функция программы
def main():
    # запускаем нашего бота
    bot.infinity_polling()


if __name__ == '__main__':
    main()
