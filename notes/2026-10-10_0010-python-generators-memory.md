# Optimizing Memory with Python Generators

- **Date:** 2026-10-10 00:10 WIB
- **Category:** `Python`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Optimizing Memory with Python Generators

When processing large datasets or reading massive log files, loading everything into a list consumes excessive RAM. Using Python generators (`yield`) computes items on-the-fly with $O(1)$ memory consumption.

```python
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# Memory stays constant regardless of file size
for record in read_large_file("huge_dataset.csv"):
    process(record)
```

**Key Takeaway:** Prefer generator expressions and iterator functions when data does not strictly need random access indexing.
