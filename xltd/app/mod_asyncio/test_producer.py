import asyncio
import random,time


async def produce(queue, n):
    for x in range(1, n + 1):
        # produce an item
        print('producing {}/{}'.format(x, n))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())
        item = str(x)
        # put the item in the queue
        await queue.put(item)

    # indicate the producer is done
    await queue.put(None)


async def consume(queue):
    while True:
        # wait for an item from the producer
        item = await queue.get()
        if item is None:
            # the producer emits None to indicate that it is done
            print('No products left................')
            #queue.task_done()
            break

        # process the item
        print('consuming item {}...'.format(item))
        # simulate i/o operation using sleep
        await asyncio.sleep(random.random())

async def main():
    queue = asyncio.Queue()
    begin_time = time.perf_counter()

    p_task = asyncio.create_task(produce(queue, 20))
    c_task = asyncio.create_task(consume(queue))


    try:
        done, pending = await asyncio.wait([p_task, c_task, c_task, c_task], timeout=6)
        # gathered = await asyncio.gather(produce(queue, 10), consume(queue))
        # print('gathered result is ',gathered)
    except Exception as e:
        print('timeout!', e)

    print('final time used---------------', time.perf_counter()-begin_time)

    # print('done task is -----', done)
    # print('pending task is ====', pending)
    # for d in done:
    #     print('finished task is ',d.result())

    # for t in pending:
    #     print(f'cancel task is {t}')
    #     t.cancel()

#high level api
asyncio.run(main())

#low level api :
# loop = asyncio.get_event_loop()
# queue = asyncio.Queue(loop=loop)
# producer_coro = produce(queue, 10)
# consumer_coro = consume(queue)
# loop.run_until_complete(asyncio.gather(producer_coro, consumer_coro))
# loop.close()

