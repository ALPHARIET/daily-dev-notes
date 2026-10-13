# Preventing Timing Attacks with Constant-Time Comparison

- **Date:** 2026-10-14 00:47 WIB
- **Category:** `Security`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Preventing Timing Attacks with Constant-Time Comparison

Standard string comparison terminates on the first mismatched byte, allowing attackers to measure execution latency.

```python
import hmac

if hmac.compare_digest(user_token, secret_token):
    grant_access()
```

**Key Takeaway:** Always use constant-time comparison methods (`hmac.compare_digest`) for cryptographic verification.
