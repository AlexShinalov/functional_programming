import sqlite3

import requests
import telebot

import time




bot = telebot.TeleBot('token')
tasks = {}
times = []


conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                  (user_id INTEGER, task TEXT, deadline TEXT)''')


cursor.execute('''CREATE TABLE IF NOT EXISTS reminders 
                  (user_id INTEGER, time TEXT)''')

def add_task_to_db(user_id, task, deadline):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO tasks VALUES (?, ?, ?)", (user_id, task, deadline))
    conn.commit()
    conn.close()
def get_user_tasks():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, task, deadline FROM tasks")
    rows = cursor.fetchall()
    conn.close()
    tasks = {}
    for row in rows:
        user_id = row[0]
        task_info = {'task': row[1], 'deadline': row[2]}
        if user_id in tasks:
            tasks[user_id].append(task_info)
        else:
            tasks[user_id] = [task_info]

    return tasks

def add_reminder_to_db(user_id, time):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO reminders VALUES (?, ?)", (user_id, time))
    conn.commit()
    conn.close()


def get_user_reminders():
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()
    cursor.execute("SELECT user_id, time FROM reminders")
    rows = cursor.fetchall()
    reminders_dict = {}
    for row in rows:
        user_id, time = row[0], row[1]
        if user_id in reminders_dict:
            reminders_dict[user_id].append(time)
        else:
            reminders_dict[user_id] = [time]

    conn.close()
    return reminders_dict



def delete_user_reminders_test(user_id, time):
    conn = sqlite3.connect('tasks.db')
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reminders WHERE user_id=? AND time=?", (user_id, time))

    conn.commit()
    conn.close()

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):

    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет, я бот для планирования задач. Для справки напиши /help")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши /addtask для добавления задачи")


@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text == "/addtask":
        bot.send_message(message.from_user.id, "Введите задачу и дедлайн в формате 'Задача; дедлайн'")

    elif ";" in message.text:
        task, deadline = message.text.split(";")
        add_task_to_db(message.from_user.id, task.strip(), deadline.strip())
        bot.send_message(message.from_user.id, f"Задача '{task}' добавлена с дедлайном {deadline}")
    elif message.text == "/tasks":
        tasks = get_user_tasks()
        if tasks:
            for user_id, task_list in tasks.items():
                for task_info in task_list:
                    bot.send_message(user_id,
                                     f"Ваши задачи на сегодня:\nЗадача: {task_info['task']}\nДедлайн: {task_info['deadline']}")
        else:
            bot.send_message(message.from_user.id, "У вас нет задач.")

    elif message.text == "/news":
        news_api_key = 'a6b910a5c09a4d41ad6fa6a0bf80cd8e'
        news_response = requests.get(
            f'https://newsapi.org/v2/everything?q=tesla&from=2023-11-12&sortBy=publishedAt&apiKey={news_api_key}')
        if news_response.status_code == 200:
            news_data = news_response.json()
            articles = news_data['articles'][:5]  # Получаем первые 5 новостей
            for article in articles:
                bot.send_message(message.from_user.id, f"📰 {article['title']}\n🔗 {article['url']}")
        else:
            bot.send_message(message.from_user.id, "Не удалось получить новости.")

    elif message.text == "/remind":
        bot.send_message(message.from_user.id, "Введите когда вам напомнить о задача в формате H:M ")

    elif ":" in message.text and len(message.text)==5:
        houre, mminute = message.text.split(":")
        time = houre +":"+ mminute
        add_reminder_to_db(message.from_user.id, time)
        bot.send_message(message.from_user.id, f"Время '{time}' добавлено")
    else:
        bot.send_message(message.from_user.id, "Не понимаю. Напишите /help для получения инструкций.")



if __name__ == "__main__":
    while True:
        bot.polling()



