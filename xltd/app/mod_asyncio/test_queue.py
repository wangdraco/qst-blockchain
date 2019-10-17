import asyncio
import random
import time

#define comsumer or worker
async def worker(name, queue):
    while True:
        # Get a "work item" out of the queue.
        sleep_for = await queue.get()

        # Sleep for the "sleep_for" seconds.
        #await asyncio.sleep(sleep_for)
        #simulate i/o operation using sleep
        await asyncio.sleep(random.random())

        # Notify the queue that the "work item" has been processed.
        queue.task_done()

        print(f'{name} has worked for {sleep_for} ')

#define product method
async def producer(queue,amount):
    for _ in range(amount):
        queue.put_nowait('item-'+str(_))
        print('producer is ===============', 'item-' + str(_))

async def main():
    # Create a queue that we will use to store our "workload".
    queue = asyncio.Queue()

    # Generate random timings and put them into the queue.
    # for _ in range(40):
    #     # sleep_for = random.uniform(0.05, 1.0)
    #     # total_sleep_time += sleep_for
    #     # queue.put_nowait(sleep_for)
    #     queue.put_nowait('item-'+str(_))
    #     print('producer is ===============','item-'+str(_))
    await producer(queue, 40)

    # Create three worker tasks to process the queue concurrently.
    tasks = []
    for i in range(8):
        task = asyncio.create_task(worker(f'worker-{i}', queue))
        tasks.append(task)

    # Wait until the queue is fully processed.
    started_at = time.monotonic()
    await queue.join()
    total_slept_for = time.monotonic() - started_at

    # Cancel our worker tasks.
    for task in tasks:
        print(f'task--{task} will be cancle..............')
        task.cancel()
    # Wait until all worker tasks are cancelled.
    await asyncio.gather(*tasks, return_exceptions=True)

    print('====')
    print(f'all workers slept in parallel for {total_slept_for:.2f} seconds')


asyncio.run(main())