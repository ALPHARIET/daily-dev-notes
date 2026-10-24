# Inspecting Network Listening Sockets with ss

- **Date:** 2026-10-24 19:04 WIB
- **Category:** `Linux`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Inspecting Network Listening Sockets with ss

The modern `ss` utility is significantly faster than legacy `netstat` for inspecting open ports and network socket states.

```bash
ss -tulpn
ss -tulpn | grep :8080
```

**Key Takeaway:** Replace `netstat` with `ss -tulpn` in debugging scripts for better performance on busy servers.
