import asyncio
import time


async def f1():
    print("process 11111")
    await asyncio.sleep(2)
    print("11111")
    return "11111"

async def f2():
    print("process 22222")
    await asyncio.sleep(1)
    print("22222")
    return "22222"

def get_tasks():
    tasks=[]
    t1 = asyncio.create_task(f1())
    t2 = asyncio.create_task(f2())
    tasks.extend([t1,t2])
    return tasks
    
async def main():
    result = await asyncio.gather(*get_tasks())
    print(f"{result=}")


asyncio.run(main())