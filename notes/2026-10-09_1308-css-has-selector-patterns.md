# CSS :has() Relational Selector in Production

- **Date:** 2026-10-09 13:08 WIB
- **Category:** `Web Dev`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### CSS :has() Relational Selector in Production

The `:has()` pseudo-class enables parent styling based on child state or sibling conditions without JavaScript DOM queries.

```css
/* Style form group when child input is invalid */
.form-group:has(input:invalid) {
  border-left: 4px solid #ef4444;
}

/* Conditionally style nav when a modal is open */
body:has(dialog[open]) {
  overflow: hidden;
}
```

**Key Takeaway:** Eliminate JavaScript state toggling for purely visual parent-child relational UI styles.
