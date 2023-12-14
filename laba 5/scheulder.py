
from main import get_user_reminders, get_user_tasks,delete_user_reminders, delete_user_reminders_test

import telebot
import time
bot = telebot.TeleBot('6707362187:AAFFKmg4z6ag6ZSTWvdmitCdlR6Fc5ixqxs')

def send_daily_tasks():
    times = get_user_reminders()
    tasks = get_user_tasks()

    current_time = time.strftime("%H:%M", time.localtime())
    print(current_time, times)
    for user_i, time_one in times.items():
        print(user_i)
        if current_time in time_one:
            for user_id, task_list in tasks.items():
                if user_id == user_i:
                    for task_info in task_list:
                        bot.send_message(user_id,
                                         f"Ваши задачи на сегодня:\nЗадача: {task_info['task']}\nДедлайн: {task_info['deadline']}")


            #delete_user_reminders(current_time )
            delete_user_reminders_test(user_i, current_time)





if __name__ == "__main__":
    while True:
        send_daily_tasks()
        time.sleep(60)