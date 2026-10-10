# Git Worktrees for Multi-Branch Parallel Development

- **Date:** 2026-10-10 20:51 WIB
- **Category:** `Git`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Git Worktrees for Multi-Branch Parallel Development

Switching branches with `git checkout` stashes uncommitted changes. `git worktree` allows checking out multiple branches into separate directories simultaneously.

```bash
git worktree add ../project-hotfix hotfix/critical-patch
cd ../project-hotfix
npm test
cd ../main-project
git worktree remove ../project-hotfix
```

**Key Takeaway:** Use worktrees to tackle urgent hotfixes or code reviews without stashing local work.
