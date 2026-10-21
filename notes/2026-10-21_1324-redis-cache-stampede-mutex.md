# Mitigating Cache Stampedes with Distributed Mutex

- **Date:** 2026-10-21 13:24 WIB
- **Category:** `Backend`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Mitigating Cache Stampedes with Distributed Mutex

When a heavily requested cache key expires, thousands of concurrent requests hit the database simultaneously (Cache Stampede).

**Mitigation Pattern:**
1. Check cache. If key is missing, attempt to acquire a short-lived Redis lock (`SET lock_key uuid NX EX 5`).
2. If lock acquired: query the primary DB, populate cache with normal TTL, and release lock.
3. If lock fails: sleep briefly (50-100ms) and re-read the cache populated by the winning thread.

**Key Takeaway:** Guard expensive cache repopulation behind a single mutex lock to protect backend databases.
