import asyncio

async def tcp_echo_client(host,port,message):

    for i in range(10000):
        reader, writer = await asyncio.open_connection(
            host, port)
        print(f'Send: {message!r}')
        writer.write(message.encode())

        data = await reader.read(100)
        print(f'Received: {data.decode()!r}')

        print('Close the connection')
        writer.close()


async def main():
    task = asyncio.create_task(tcp_echo_client('127.0.0.1',8888,'To 8888 Hello World!'))
    task2 = asyncio.create_task(tcp_echo_client('127.0.0.1',8888,'==========!'))
    await asyncio.wait([task2,task])

# asyncio.run(tcp_echo_client('127.0.0.1',8888,'To 8888 Hello World!'))
asyncio.run(main())