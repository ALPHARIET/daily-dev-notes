# Implementing Idempotency Keys in Mutation Endpoints

- **Date:** 2026-10-10 17:35 WIB
- **Category:** `Backend`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Implementing Idempotency Keys in Mutation Endpoints

Network drops and client retries can cause duplicate charges if POST requests are not protected by idempotency keys.

**Architecture Workflow:**
1. Client sends header: `Idempotency-Key: <uuid>`.
2. Server validates key in fast cache (Redis) with status `IN_PROGRESS`.
3. If duplicate arrives: return HTTP `409 Conflict` or return cached response once completed.

**Key Takeaway:** Critical transaction mutations must always be protected against client-side retry floods.
