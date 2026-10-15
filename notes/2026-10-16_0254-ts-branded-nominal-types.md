# Branded Nominal Types for Domain Primitive Safety

- **Date:** 2026-10-16 02:54 WIB
- **Category:** `TypeScript`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Branded Nominal Types for Domain Primitive Safety

TypeScript uses structural typing, allowing accidental mixing of different string IDs (e.g., passing a `UserId` where an `OrderId` is expected). Branded types enforce nominal safety.

```typescript
type Brand<K, T> = K & { readonly __brand: T };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function cancelOrder(userId: UserId, orderId: OrderId) {
  // Logic here
}

const u = "user_123" as UserId;
const o = "order_456" as OrderId;

// cancelOrder(o, u); // ❌ Compile error!
cancelOrder(u, o);    // ✅ Valid
```

**Key Takeaway:** Brand unique string and number primitives to catch semantic logic bugs at compile time.
