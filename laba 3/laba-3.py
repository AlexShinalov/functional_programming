import asyncio

clients = []
rooms = {}

async def handle_client(reader, writer):
    client_id = id(writer)
    client_id=str(client_id)
    clients.append(writer)

    if id(writer) not in clients:
        command = ("Введитее свое имя в фомате !name ")
        writer.write(command.encode())
        writer.drain()




    try:
        while True:
            data = await reader.read(100)
            message = data.decode()
            print(message)

            if message.startswith("!name"):
                client_name=message[6:].strip()
                commads = (f"Привет, {client_name}"
                           "Команды:"
                           "!join создать или присоедениться к комнате"
                           "!leave выйти из комнаты")

                writer.write(commads.encode())
                writer.drain()


            if message.startswith('!join'):
                room_name = message[6:].strip()
                if room_name not in rooms:
                    rooms[room_name] = []
                rooms[room_name].append(writer)
            elif message.startswith('!leave'):
                room_name = message[7:].strip()
                if room_name in rooms and writer in rooms[room_name]:
                    rooms[room_name].remove(writer)
            else:
                for room_clients in rooms.values():
                    if writer in room_clients:
                        for client in room_clients:
                            if client != writer:
                                try:
                                    client.write(data)
                                    await client.drain()
                                except:
                                    pass
    except asyncio.CancelledError:
        pass
    finally:
        clients.remove(writer)
        for room_clients in rooms.values():
            if writer in room_clients:
                room_clients.remove(writer)
        writer.close()

async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(main())
