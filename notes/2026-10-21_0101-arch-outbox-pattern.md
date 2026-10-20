# Transactional Outbox Pattern for Microservices

- **Date:** 2026-10-21 01:01 WIB
- **Category:** `Architecture`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Transactional Outbox Pattern for Microservices

Directly updating a database and publishing an event to a message broker in the same request risks partial failure if the broker is unreachable.

**Outbox Solution:**
1. Save business data and domain event into an `outbox` table within the **same local ACID database transaction**.
2. A separate background worker tails the `outbox` table and publishes messages to the broker.

**Key Takeaway:** The Transactional Outbox pattern guarantees at-least-once message delivery without distributed two-phase commits.
