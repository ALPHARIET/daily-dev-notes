# The Satisfies Operator vs Type Annotation

- **Date:** 2026-10-09 21:26 WIB
- **Category:** `TypeScript`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### The Satisfies Operator vs Type Annotation

The `satisfies` operator (TS 4.9+) validates that an expression matches a type contract without widening the inferred type, preserving literal values and specific methods.

```typescript
type Palette = Record<string, string | number[]>;

// With 'satisfies', individual property types are strictly preserved:
const theme = {
  primary: "#3b82f6",
  rgb: [59, 130, 246]
} satisfies Palette;

// Valid: TS knows 'primary' is string, not string | number[]
const hex = theme.primary.toUpperCase();
const r = theme.rgb[0];
```

**Key Takeaway:** Use `satisfies` whenever you want structural validation without losing precise literal autocomplete.
