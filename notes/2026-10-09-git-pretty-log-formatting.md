# Useful Git Log Formatting for Clean History

- **Date:** 2026-10-09
- **Category:** `Git`
- **Source:** Dev Insights & Architecture Practice

---

### Useful Git Log Formatting for Clean History

Instead of scrolling through verbose default `git log` output, an alias with graph and branch decoration makes commit trees readable at a glance.

```bash
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

Or configure it permanently in your `.gitconfig`:
```bash
git config --global alias.lg "log --graph --oneline --decorate --all"
```

**Key Takeaway:** Clean log visualizers help catch branch divergence early before complex merges.

