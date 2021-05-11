import asyncio
import time

#The asyncio.create_task() function to run coroutines concurrently as asyncio Tasks.

async def say_after(delay, what):
    await asyncio.sleep(delay)
    print(what)

async def main():
    task1 = asyncio.create_task(
        say_after(1, 'hello'))

    task2 = asyncio.create_task(
        say_after(2, 'world'))

    print(f"started at {time.strftime('%X')}")


    # Wait until both tasks are completed (should take
    # around 2 seconds.)
    #await task1
    #await asyncio.sleep(1)
    task1.cancel()
    try:
        await task1
    except asyncio.CancelledError:
        print("main(): cancel_me is cancelled now")
    await task2

    print(f"finished at {time.strftime('%X')}")

async def factorial(name, number):
    print(f"Task {name}: Compute factorial({number})...")
    if number==0:
        number = 2
    await asyncio.sleep(number)
    print(f"Task {name}: factorial({number}) = ")

async def main_task():
    # Schedule three calls *concurrently*:

    for i in range(3):
        await asyncio.gather(
            factorial("A"+str(i), i),
            say_after(0.1, 'hello world')
        )



# asyncio.run(main())
asyncio.run(main_task())