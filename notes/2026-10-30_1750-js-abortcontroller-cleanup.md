# AbortController for Fetch Requests and Event Cleanup

- **Date:** 2026-10-30 17:50 WIB
- **Category:** `JavaScript`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### AbortController for Fetch Requests and Event Cleanup

`AbortController` cancels pending HTTP requests and also unregisters DOM event listeners in bulk without manual tracking.

```javascript
const controller = new AbortController();
const { signal } = controller;

fetch("/api/large-dataset", { signal })
  .catch(err => {
    if (err.name === "AbortError") console.log("Request cancelled cleanly");
  });

window.addEventListener("resize", handleResize, { signal });
window.addEventListener("scroll", handleScroll, { signal });

// One single call aborts fetch and removes all bound listeners:
controller.abort();
```

**Key Takeaway:** Pass `{ signal }` into event listener options for clean, memory-safe component unmounting.
