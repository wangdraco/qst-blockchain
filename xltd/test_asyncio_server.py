import asyncio,time,concurrent

async def phase(i):
    print('in phase {}'.format(i))
    #await asyncio.sleep(0.1 * i)
    print('done with phase {}'.format(i))
    return 'phase {} result'.format(i)

async def handle_echo(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')

    print(f"Received {message!r} from {addr!r}")

    print(f"Send: {message!r}")
    writer.write(data)
    await writer.drain()

    print("Close the connection")
    writer.close()

async def main_test(num_phases):
    print('starting main')
    phases = [
        phase(i)
        for i in range(num_phases)
    ]
    print('waiting for phases to complete')
    completed, pending = await asyncio.wait(phases)
    print('the pending is {}',completed)
    results = [t.result() for t in completed]
    print('results: {!r}'.format(results))


async def main_server():
    #await asyncio.sleep(1)
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

async def main_server2():
    #await asyncio.sleep(1)
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 9999)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()




#event loop and future is low level api
#gathered_coroutines = asyncio.gather( main_server(),main_test(3),main_server2())
# event_loop = asyncio.get_event_loop()
# try:
#     #event_loop.run_until_complete(main_server())
#     event_loop.run_until_complete(gathered_coroutines)
# finally:
#     event_loop.close()

#beging with asyncio symbol means High level api
#asyncio.run(main_server())

async def main():
    #gathered_coroutines =await asyncio.gather(main_test(3), main_server2())
    #await asyncio.wait_for(main_server(),timeout=5)

    task = asyncio.create_task(main_test(5))
    task2 = asyncio.create_task(main_server())
    task3 = asyncio.create_task(main_server2())
    done, pending = await asyncio.wait([task,task2,task3],timeout=50, return_when=concurrent.futures.ALL_COMPLETED)
    print(done,'--',pending)


    # for f in asyncio.as_completed([task,task2],timeout=5):
    #     earliest_result = await f
    #     print('as complete is ...........',earliest_result)



    # for result in gathered_coroutines:
    #     print('result is ',result)

asyncio.run(main())
