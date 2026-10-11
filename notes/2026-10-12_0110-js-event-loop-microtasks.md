# Event Loop Microtasks vs Macrotasks Execution Order

- **Date:** 2026-10-12 01:10 WIB
- **Category:** `JavaScript`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Event Loop Microtasks vs Macrotasks Execution Order

Microtasks (`Promise.then`, `queueMicrotask`, `MutationObserver`) always execute immediately after the current script finishes and before any macrotasks (`setTimeout`, `setInterval`, `I/O`).

```javascript
console.log("1: Synchronous");

setTimeout(() => {
  console.log("4: Macrotask (Timeout)");
}, 0);

Promise.resolve().then(() => {
  console.log("2: Microtask (Promise)");
});

queueMicrotask(() => {
  console.log("3: Microtask (queueMicrotask)");
});

// Output: 1 -> 2 -> 3 -> 4
```

**Key Takeaway:** Use `queueMicrotask` to defer execution asynchronously without waiting for the macrotask timer queue.
