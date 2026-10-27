# Discriminated Unions for Clean State Handling

- **Date:** 2026-10-27 20:22 WIB
- **Category:** `TypeScript`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Discriminated Unions for Clean State Handling

Discriminated unions ensure exhaustive type checking across mutually exclusive states in frontend components and API handlers.

```typescript
type RequestState<T> =
  | { status: "idle" }
  | { status: "loading" }
  | { status: "success"; data: T }
  | { status: "error"; message: string };

function renderState<T>(state: RequestState<T>) {
  switch (state.status) {
    case "success":
      return `Loaded: ${JSON.stringify(state.data)}`;
    case "error":
      return `Error: ${state.message}`;
    default:
      return "Pending...";
  }
}
```

**Key Takeaway:** Replace multiple boolean flags (`isLoading`, `isError`, `isSuccess`) with a single discriminated union.
