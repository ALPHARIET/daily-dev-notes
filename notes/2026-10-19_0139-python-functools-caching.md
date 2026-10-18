# Functools LRU Cache and Unhashable Arguments Trap

- **Date:** 2026-10-19 01:39 WIB
- **Category:** `Python`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Functools LRU Cache and Unhashable Arguments Trap

`functools.lru_cache` provides memoization for expensive pure functions, but fails with `TypeError: unhashable type` when receiving lists or dicts.

```python
from functools import lru_cache

# ❌ Fails: func([1, 2, 3])
# ✅ Pass immutable tuples instead:
@lru_cache(maxsize=256)
def calculate_metrics(tags: tuple[str, ...]) -> dict:
    return {"count": len(tags), "score": sum(len(t) for t in tags)}
```

**Key Takeaway:** Convert mutable collections into immutable equivalents (`tuple`, `frozenset`) before caching.
