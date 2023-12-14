import asyncio
from tkinter import ttk
import tkinter as tk


class client:
    def __init__(self) -> None:
        self.designer = ''
        self.user = ''
        self.host = "127.0.0.1"
        self.port = 8888
        self.reader = ''
        self.writer = ''

    async def error(self, message):
        print(f"ошибка: {message}")

    async def receive_message(self):
        while True:
            message = await self.reader.read(1024)  # Получаем
            print(f"{message.decode().strip()}")
            await self.designer.receive_message(message.decode().strip())
            if "вы отключены от сервера" in message.decode().strip():
                return

    async def send_message(self, message):
        if message == "":
            self.error("вы ничего не ввели")
            return
        self.writer.write(message.encode())
        await self.writer.drain()
        if message == "exit":
            return

    async def send_message_to_server(self, writer, message):
        writer.write(message.encode())
        await writer.drain()

    async def start_client(self) -> None:
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        print("Подключено к серверу")

        await self.receive_message()
        self.writer.close()


class designer:
    def __init__(self, client):
        self.client = client

        self.root = tk.Tk()
        self.root.title("chat")
        self.root.geometry('620x960')
        self.root.resizable(True, True)

        self.theme = tk.BooleanVar()
        self.theme.set(False)

        self.output_frame = ttk.Frame(self.root)
        self.input_frame = ttk.Frame(self.root)

        self.send_Entry = ttk.Entry(self.input_frame, width=78, justify="left")
        self.send_Entry.grid(row=0, column=0)

        self.send_button = ttk.Button(self.input_frame, command=self.click, text="send")
        self.send_button.grid(row=0, column=1, sticky="ns")

        self.change_theme_button = ttk.Button(self.input_frame, command=self.change_theme, text="Change Theme")
        self.change_theme_button.grid(row=0, column=2, sticky="ns")

        self.input_frame.pack(fill=tk.X, anchor="s")

        self.output_heading = ttk.Label(self.output_frame, text="Chat", anchor="center")
        self.output_heading.pack(fill=tk.X)

        self.history = list()

        self.output_frame.pack(fill=tk.X)

    def change_theme(self):
        if self.theme.get():
            self.root['background'] = "darkgrey"
            self.output_heading.configure(background="darkgray", foreground="white")
            self.send_Entry.configure(background="darkgray")

        else:
            self.root['background'] = "white"
            self.output_heading.configure(background="gray", foreground="black")
            self.send_Entry.configure(background="darkgray")

        self.theme.set(not self.theme.get())

    async def update(self, interval=0.05):
        while True:
            self.root.update()
            await asyncio.sleep(interval)

    def click(self):
        asyncio.create_task(self.send_message())

    async def send_message(self):
        message = self.send_Entry.get()
        await self.client.send_message(message)

    async def receive_message(self, message):
        new_message = ttk.Label(self.output_frame)
        new_message.configure(foreground="black", font=("Arial", 12), background="cyan3", text=message)
        new_message.pack(fill=tk.X, anchor="w")
        self.history.append(new_message)
        self.send_Entry.delete(0, "end")


async def main():
    my_client = client()
    my_des = designer(my_client)
    my_client.designer = my_des
    tasks = [
        asyncio.create_task(my_client.start_client()),
        asyncio.create_task(my_des.update())
    ]

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())