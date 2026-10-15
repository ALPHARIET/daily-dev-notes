# Cursor-Based vs Offset-Based Pagination for Scalability

- **Date:** 2026-10-15 13:17 WIB
- **Category:** `Backend`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Cursor-Based vs Offset-Based Pagination for Scalability

Offset pagination requires the database to scan and discard thousands of rows. Cursor pagination provides constant $O(1)$ indexed lookup.

```sql
SELECT * FROM feed_items 
WHERE (created_at, id) < ('2026-10-01 12:00:00', 'uuid-123')
ORDER BY created_at DESC, id DESC 
LIMIT 20;
```

**Key Takeaway:** Always use cursor-based pagination for infinite feeds and large data export endpoints.
