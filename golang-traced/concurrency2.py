import asyncio
import time

def cicle(n):
    i = 0
    while True:
        i+=1
        if i > 9000000*n:
            break

async def proc1():
    cicle(8)
    print(1)

async def proc2():
    cicle(2)
    print(2)

def main():
    async def parallel():
        await asyncio.create_task(proc1())
        await asyncio.create_task(proc2())

    print(f"started at {time.strftime('%X')}")
    asyncio.run(parallel())  
    print(f"finished at {time.strftime('%X')}")

main()

