import asyncio,time,concurrent,threading

async def longtime():
    print('in long time=====')
    result = 0
    #time.sleep(2)
    #await asyncio.sleep(2)
    for i in range(1000000):
        result += i
    print(f'finished long time {result}')
    return f'long time result:{result}'

async def longtime2():
    print('in long time 2----')
    result = 0
    #time.sleep(2)
    #await asyncio.sleep(2)

    for i in range(10000000):
        result += i
    print(f'finished long time2 {result}')
    return f'long time2 result:{result}'

async def longtime3():
    print('in long time 3----')
    result = 0
    #time.sleep(2)

    #await asyncio.sleep(3)
    for i in range(100000000):
        result += i
    print(f'finished long time3 {result}')
    return f'long time3 result:{result}'

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
    results = [t.result() for t in completed]
    print('results: {!r}'.format(results))


async def main_server():
    await asyncio.sleep(0.1)
    server = await asyncio.start_server(
        handle_echo, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()

async def main_server2():
    await asyncio.sleep(0.1)
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
    done, pending = await asyncio.wait([task,task2,task3],timeout=5)
    #or pass through coroutine function directly
    #done, pending = await asyncio.wait([longtime(), longtime2(),longtime3()], timeout=3)
    #
    print('done task is -----',done)
    print('pending task is ====',pending)

    for d in done:
        print('finished task is ',d.result())

    for t in pending:
        print(f'cancel task is {t}')
        t.cancel()


    # for f in asyncio.as_completed([task,task2],timeout=10):
    #     earliest_result = await f
    #     print('as complete is ...........',earliest_result)



    # for result in gathered_coroutines:
    #     print('result is ',result)

async def main_longtime():
    print(f"started at {time.strftime('%X')}")

    # await longtime2()
    # await longtime()
    # await longtime3()
    gathered = await asyncio.gather(longtime2(), longtime(),longtime3())

    print(f"finished at {time.strftime('%X')},and result is {gathered}")


async def main_timeout():
    # Wait for at most 1 second
    try:
        await asyncio.wait_for(longtime3(), timeout=2)
        await asyncio.wait_for(main_server(), timeout=5)
        await asyncio.wait_for(main_server2(), timeout=10)
    except asyncio.TimeoutError:
        print('timeout!')

#asyncio.run(main_timeout())








