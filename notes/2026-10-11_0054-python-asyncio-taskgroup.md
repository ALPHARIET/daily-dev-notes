# Asyncio TaskGroup vs Gather for Structured Concurrency

- **Date:** 2026-10-11 00:54 WIB
- **Category:** `Python`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Asyncio TaskGroup vs Gather for Structured Concurrency

Python 3.11+ introduced `asyncio.TaskGroup`, bringing structured concurrency. Unlike `asyncio.gather()`, if one task inside a `TaskGroup` fails, all other pending sibling tasks are cleanly cancelled immediately.

```python
import asyncio

async def fetch_user(uid: int):
    await asyncio.sleep(0.1)
    return {"id": uid, "name": f"User_{uid}"}

async def fetch_orders(uid: int):
    await asyncio.sleep(0.1)
    return [{"order_id": 101}]

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(42))
        task2 = tg.create_task(fetch_orders(42))
    
    # Both tasks guaranteed finished or cleanly aborted
    print(task1.result(), task2.result())

asyncio.run(main())
```

**Key Takeaway:** Use `asyncio.TaskGroup` for production async workflows to eliminate leaked background tasks on exceptions.
