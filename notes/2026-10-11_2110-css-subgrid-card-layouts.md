# CSS Subgrid for Responsive Card Alignments

- **Date:** 2026-10-11 21:10 WIB
- **Category:** `Web Dev`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### CSS Subgrid for Responsive Card Alignments

With CSS `subgrid`, child elements inside a grid card align seamlessly to parent grid rows, solving uneven headers, content areas, and footers.

```css
.card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3;
}
```

**Key Takeaway:** Subgrid removes the need for fixed heights or complex flexbox alignment hacks across responsive grids.
