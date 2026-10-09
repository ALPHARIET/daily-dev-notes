# Safe Context Managers with contextlib.contextmanager

- **Date:** 2026-10-09 13:10 WIB
- **Category:** `Python`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Safe Context Managers with contextlib.contextmanager

Writing a full class with `__enter__` and `__exit__` is often overkill for simple resource management. The `@contextmanager` decorator simplifies setup and teardown into a single generator function.

```python
from contextlib import contextmanager
import time

@contextmanager
def execution_timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] elapsed: {elapsed * 1000:.2f}ms")

with execution_timer("DB Batch Query"):
    time.sleep(0.05)
```

**Key Takeaway:** Always place cleanup logic inside the `finally` block to ensure execution even when exceptions occur.
