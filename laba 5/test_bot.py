from telebot.types import Message
from unittest.mock import Mock
from main import echo_all  # Замените на ваше имя файла и функции бота


def test_echo_all():
    # Создаем mock объект для бота
    bot = Mock()

    # Создаем сообщение, которое будет передано в функцию
    message = Message()
    message.text = "/addtask"
    message.from_user.id = 123  # Замените на необходимый ID пользователя

    # Вызываем функцию с созданным сообщением
    echo_all(message, bot)

    bot.send_message.assert_called_once_with(123, "Привет, я бот для планирования задач. Для справки напиши /help")


