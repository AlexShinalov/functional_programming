import asyncio
import threading
from logging import shutdown


async def read_messages(reader):
    try:
        while True:
            data = await reader.read(100)
            message = data.decode()
            print(f"Received message: {message}")
    except asyncio.CancelledError:
        pass
    except ConnectionResetError:
        print("Сервер закрыл соединение")


async def send_message(writer):
    loop = asyncio.get_event_loop()
    while True:
        command = await loop.run_in_executor(None, input, 'Для выхода введите C:\n')
        if command.lower() == 'c':
            shutdown()  # Отменяем все задачи
            break
        writer.write(command.encode())
        await writer.drain()


async def main():
    reader, writer = await asyncio.open_connection('127.0.0.1', 8888)

    task_read = asyncio.create_task(read_messages(reader))
    task_write = asyncio.create_task(send_message(writer))
    await task_read
    await task_write


asyncio.run(main())
