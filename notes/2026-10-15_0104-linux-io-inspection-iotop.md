# Inspecting System I/O Bottlenecks with Pidstat and Iotop

- **Date:** 2026-10-15 01:04 WIB
- **Category:** `Linux`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Inspecting System I/O Bottlenecks with Pidstat and Iotop

When server load climbs and `top` shows high `%wa` (I/O wait), diagnose the responsible process with `iotop` or `pidstat`.

```bash
sudo iotop -o -P
pidstat -d 2 5
```

**Key Takeaway:** Distinguish between sequential bulk writes and random seek thrashing before re-provisioning disk storage.
