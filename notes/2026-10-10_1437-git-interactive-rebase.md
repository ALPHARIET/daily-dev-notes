# Git Interactive Rebase for Clean Pull Request History

- **Date:** 2026-10-10 14:37 WIB
- **Category:** `Git`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Git Interactive Rebase for Clean Pull Request History

Before merging a branch into main, interactive rebase squashes noisy WIP commits and formats clean commit messages.

```bash
git rebase -i HEAD~4
```

**Common Directives:**
- `pick`: keep commit as is.
- `squash`: meld commit into previous commit with combined message.
- `fixup`: meld commit into previous commit, discarding its message.

**Key Takeaway:** Keep pull request git history readable with self-contained, descriptive atomic commits.
