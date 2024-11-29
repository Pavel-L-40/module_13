import asyncio
import time


async def start_strongman(name, power):
    print(f'Силач {name} начал соревнования.')
    total_balls = [1,2,3,4,5]
    for ball in total_balls:
        await asyncio.sleep(5 / power)
        print(f'Силач {name} поднял {ball}')
    print(f'Силач {name} закончил соревнования.')

async def start_tournament():
    task1 = asyncio.create_task(start_strongman('Pasha', 3))
    task2 = asyncio.create_task(start_strongman('Denis', 4))
    task3 = asyncio.create_task(start_strongman('Apollon', 5))
    await task1
    await task2
    await task3

start = time.time()
asyncio.run(start_tournament())
finish = time.time()
print(round((finish - start), 2), 'sec')
