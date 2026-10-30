# PostgreSQL Composite Indexes and Column Ordering

- **Date:** 2026-10-31 01:41 WIB
- **Category:** `Backend`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### PostgreSQL Composite Indexes and Column Ordering

When creating composite indexes `(col_a, col_b)`, PostgreSQL can use the index for queries filtering on `col_a` alone, or `(col_a, col_b)`, but NOT `col_b` alone (Leftmost Prefix Rule).

```sql
-- Efficient for: WHERE tenant_id = 5 AND created_at > '2026-01-01'
-- Efficient for: WHERE tenant_id = 5
-- Inefficient for: WHERE created_at > '2026-01-01'
CREATE INDEX idx_tenant_created ON orders (tenant_id, created_at DESC);
```

**Rule of Thumb:**
1. Put equality filter columns first (`tenant_id = ?`).
2. Put range filter and ordering columns last (`created_at > ? ORDER BY created_at DESC`).

**Key Takeaway:** Always position highest-cardinality equality columns at the prefix of composite indexes.
