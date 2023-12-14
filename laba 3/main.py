import sys

from PyQt5.QtWidgets import QApplication

from chat_gui import ChatWindow
import asyncio

async def main_async(chat, reader, writer):
    task_read = asyncio.create_task(read_messages(reader, chat))
    task_write = asyncio.create_task(send_message(writer, chat))

    await asyncio.gather(task_read, task_write)

async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)
    app = QApplication(sys.argv)
    chat = ChatWindow()

    await main_async(chat, reader, writer)

    sys.exit(app.exec_())

asyncio.run(main())