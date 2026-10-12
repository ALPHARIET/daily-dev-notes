# Using __slots__ for Class Memory Optimization

- **Date:** 2026-10-13 02:59 WIB
- **Category:** `Python`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Using __slots__ for Class Memory Optimization

By default, Python instances store attributes in a dynamic dictionary (`__dict__`). For millions of small objects, declaring `__slots__` bypasses `__dict__` and reduces memory footprint by 40-60%.

```python
class DataPoint:
    __slots__ = ('x', 'y', 'timestamp')
    
    def __init__(self, x: float, y: float, timestamp: int):
        self.x = x
        self.y = y
        self.timestamp = timestamp
```

**Key Takeaway:** Use `__slots__` on lightweight data transfer objects that are instantiated in large quantities.
