import os
import sys
import json
import random
from datetime import datetime, timezone, timedelta

TOPICS = [
    {
        "category": "Python",
        "title": "Optimizing Memory with Python Generators",
        "slug": "python-generators-memory",
        "content": """### Optimizing Memory with Python Generators

When processing large datasets or reading massive log files, loading everything into a list consumes excessive RAM. Using Python generators (`yield`) computes items on-the-fly with $O(1)$ memory consumption.

```python
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# Memory stays constant regardless of file size
for record in read_large_file("huge_dataset.csv"):
    process(record)
```

**Key Takeaway:** Prefer generator expressions and iterator functions when data does not strictly need random access indexing."""
    },
    {
        "category": "Python",
        "title": "Asyncio TaskGroup vs Gather for Structured Concurrency",
        "slug": "python-asyncio-taskgroup",
        "content": """### Asyncio TaskGroup vs Gather for Structured Concurrency

Python 3.11+ introduced `asyncio.TaskGroup`, bringing structured concurrency. Unlike `asyncio.gather()`, if one task inside a `TaskGroup` fails, all other pending sibling tasks are cleanly cancelled immediately.

```python
import asyncio

async def fetch_user(uid: int):
    await asyncio.sleep(0.1)
    return {"id": uid, "name": f"User_{uid}"}

async def fetch_orders(uid: int):
    await asyncio.sleep(0.1)
    return [{"order_id": 101}]

async def main():
    async with asyncio.TaskGroup() as tg:
        task1 = tg.create_task(fetch_user(42))
        task2 = tg.create_task(fetch_orders(42))
    
    # Both tasks guaranteed finished or cleanly aborted
    print(task1.result(), task2.result())

asyncio.run(main())
```

**Key Takeaway:** Use `asyncio.TaskGroup` for production async workflows to eliminate leaked background tasks on exceptions."""
    },
    {
        "category": "Python",
        "title": "Using __slots__ for Class Memory Optimization",
        "slug": "python-slots-optimization",
        "content": """### Using __slots__ for Class Memory Optimization

By default, Python instances store attributes in a dynamic dictionary (`__dict__`). For millions of small objects, declaring `__slots__` bypasses `__dict__` and reduces memory footprint by 40-60%.

```python
class DataPoint:
    __slots__ = ('x', 'y', 'timestamp')
    
    def __init__(self, x: float, y: float, timestamp: int):
        self.x = x
        self.y = y
        self.timestamp = timestamp
```

**Key Takeaway:** Use `__slots__` on lightweight data transfer objects that are instantiated in large quantities."""
    },
    {
        "category": "Python",
        "title": "Safe Context Managers with contextlib.contextmanager",
        "slug": "python-contextlib-patterns",
        "content": """### Safe Context Managers with contextlib.contextmanager

Writing a full class with `__enter__` and `__exit__` is often overkill for simple resource management. The `@contextmanager` decorator simplifies setup and teardown into a single generator function.

```python
from contextlib import contextmanager
import time

@contextmanager
def execution_timer(label: str):
    start = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - start
        print(f"[{label}] elapsed: {elapsed * 1000:.2f}ms")

with execution_timer("DB Batch Query"):
    time.sleep(0.05)
```

**Key Takeaway:** Always place cleanup logic inside the `finally` block to ensure execution even when exceptions occur."""
    },
    {
        "category": "Python",
        "title": "Functools LRU Cache and Unhashable Arguments Trap",
        "slug": "python-functools-caching",
        "content": """### Functools LRU Cache and Unhashable Arguments Trap

`functools.lru_cache` provides memoization for expensive pure functions, but fails with `TypeError: unhashable type` when receiving lists or dicts.

```python
from functools import lru_cache

# ❌ Fails: func([1, 2, 3])
# ✅ Pass immutable tuples instead:
@lru_cache(maxsize=256)
def calculate_metrics(tags: tuple[str, ...]) -> dict:
    return {"count": len(tags), "score": sum(len(t) for t in tags)}
```

**Key Takeaway:** Convert mutable collections into immutable equivalents (`tuple`, `frozenset`) before caching."""
    },
    {
        "category": "TypeScript",
        "title": "The Satisfies Operator vs Type Annotation",
        "slug": "ts-satisfies-operator",
        "content": """### The Satisfies Operator vs Type Annotation

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

**Key Takeaway:** Use `satisfies` whenever you want structural validation without losing precise literal autocomplete."""
    },
    {
        "category": "TypeScript",
        "title": "Discriminated Unions for Clean State Handling",
        "slug": "ts-discriminated-unions",
        "content": """### Discriminated Unions for Clean State Handling

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

**Key Takeaway:** Replace multiple boolean flags (`isLoading`, `isError`, `isSuccess`) with a single discriminated union."""
    },
    {
        "category": "TypeScript",
        "title": "Branded Nominal Types for Domain Primitive Safety",
        "slug": "ts-branded-nominal-types",
        "content": """### Branded Nominal Types for Domain Primitive Safety

TypeScript uses structural typing, allowing accidental mixing of different string IDs (e.g., passing a `UserId` where an `OrderId` is expected). Branded types enforce nominal safety.

```typescript
type Brand<K, T> = K & { readonly __brand: T };

type UserId = Brand<string, "UserId">;
type OrderId = Brand<string, "OrderId">;

function cancelOrder(userId: UserId, orderId: OrderId) {
  // Logic here
}

const u = "user_123" as UserId;
const o = "order_456" as OrderId;

// cancelOrder(o, u); // ❌ Compile error!
cancelOrder(u, o);    // ✅ Valid
```

**Key Takeaway:** Brand unique string and number primitives to catch semantic logic bugs at compile time."""
    },
    {
        "category": "JavaScript",
        "title": "Event Loop Microtasks vs Macrotasks Execution Order",
        "slug": "js-event-loop-microtasks",
        "content": """### Event Loop Microtasks vs Macrotasks Execution Order

Microtasks (`Promise.then`, `queueMicrotask`, `MutationObserver`) always execute immediately after the current script finishes and before any macrotasks (`setTimeout`, `setInterval`, `I/O`).

```javascript
console.log("1: Synchronous");

setTimeout(() => {
  console.log("4: Macrotask (Timeout)");
}, 0);

Promise.resolve().then(() => {
  console.log("2: Microtask (Promise)");
});

queueMicrotask(() => {
  console.log("3: Microtask (queueMicrotask)");
});

// Output: 1 -> 2 -> 3 -> 4
```

**Key Takeaway:** Use `queueMicrotask` to defer execution asynchronously without waiting for the macrotask timer queue."""
    },
    {
        "category": "JavaScript",
        "title": "AbortController for Fetch Requests and Event Cleanup",
        "slug": "js-abortcontroller-cleanup",
        "content": """### AbortController for Fetch Requests and Event Cleanup

`AbortController` cancels pending HTTP requests and also unregisters DOM event listeners in bulk without manual tracking.

```javascript
const controller = new AbortController();
const { signal } = controller;

fetch("/api/large-dataset", { signal })
  .catch(err => {
    if (err.name === "AbortError") console.log("Request cancelled cleanly");
  });

window.addEventListener("resize", handleResize, { signal });
window.addEventListener("scroll", handleScroll, { signal });

// One single call aborts fetch and removes all bound listeners:
controller.abort();
```

**Key Takeaway:** Pass `{ signal }` into event listener options for clean, memory-safe component unmounting."""
    },
    {
        "category": "Web Dev",
        "title": "CSS Subgrid for Responsive Card Alignments",
        "slug": "css-subgrid-card-layouts",
        "content": """### CSS Subgrid for Responsive Card Alignments

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

**Key Takeaway:** Subgrid removes the need for fixed heights or complex flexbox alignment hacks across responsive grids."""
    },
    {
        "category": "Web Dev",
        "title": "CSS :has() Relational Selector in Production",
        "slug": "css-has-selector-patterns",
        "content": """### CSS :has() Relational Selector in Production

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

**Key Takeaway:** Eliminate JavaScript state toggling for purely visual parent-child relational UI styles."""
    },
    {
        "category": "Backend",
        "title": "PostgreSQL Composite Indexes and Column Ordering",
        "slug": "postgres-composite-indexes",
        "content": """### PostgreSQL Composite Indexes and Column Ordering

When creating composite indexes `(col_a, col_b)`, PostgreSQL can use the index for queries filtering on `col_a` alone, or `(col_a, col_b)`, but NOT `col_b` alone (Leftmost Prefix Rule).

```sql
-- Efficient for: WHERE tenant_id = 5 AND created_at > '2026-01-01'
-- Efficient for: WHERE tenant_id = 5
-- Inefficient for: WHERE created_at > '2026-01-01'
CREATE INDEX idx_tenant_created ON orders (tenant_id, created_at DESC);
```

**Rule of Thumb:**
1. Put equality filter columns first (`tenant_id = ?`).
2. Put range filter and ordering columns last (`created_at > ? ORDER BY created_at DESC`).

**Key Takeaway:** Always position highest-cardinality equality columns at the prefix of composite indexes."""
    },
    {
        "category": "Backend",
        "title": "Mitigating Cache Stampedes with Distributed Mutex",
        "slug": "redis-cache-stampede-mutex",
        "content": """### Mitigating Cache Stampedes with Distributed Mutex

When a heavily requested cache key expires, thousands of concurrent requests hit the database simultaneously (Cache Stampede).

**Mitigation Pattern:**
1. Check cache. If key is missing, attempt to acquire a short-lived Redis lock (`SET lock_key uuid NX EX 5`).
2. If lock acquired: query the primary DB, populate cache with normal TTL, and release lock.
3. If lock fails: sleep briefly (50-100ms) and re-read the cache populated by the winning thread.

**Key Takeaway:** Guard expensive cache repopulation behind a single mutex lock to protect backend databases."""
    },
    {
        "category": "Backend",
        "title": "Cursor-Based vs Offset-Based Pagination for Scalability",
        "slug": "api-cursor-pagination",
        "content": """### Cursor-Based vs Offset-Based Pagination for Scalability

Offset pagination requires the database to scan and discard thousands of rows. Cursor pagination provides constant $O(1)$ indexed lookup.

```sql
SELECT * FROM feed_items 
WHERE (created_at, id) < ('2026-10-01 12:00:00', 'uuid-123')
ORDER BY created_at DESC, id DESC 
LIMIT 20;
```

**Key Takeaway:** Always use cursor-based pagination for infinite feeds and large data export endpoints."""
    },
    {
        "category": "Backend",
        "title": "Implementing Idempotency Keys in Mutation Endpoints",
        "slug": "api-idempotency-keys",
        "content": """### Implementing Idempotency Keys in Mutation Endpoints

Network drops and client retries can cause duplicate charges if POST requests are not protected by idempotency keys.

**Architecture Workflow:**
1. Client sends header: `Idempotency-Key: <uuid>`.
2. Server validates key in fast cache (Redis) with status `IN_PROGRESS`.
3. If duplicate arrives: return HTTP `409 Conflict` or return cached response once completed.

**Key Takeaway:** Critical transaction mutations must always be protected against client-side retry floods."""
    },
    {
        "category": "Git",
        "title": "Git Interactive Rebase for Clean Pull Request History",
        "slug": "git-interactive-rebase",
        "content": """### Git Interactive Rebase for Clean Pull Request History

Before merging a branch into main, interactive rebase squashes noisy WIP commits and formats clean commit messages.

```bash
git rebase -i HEAD~4
```

**Common Directives:**
- `pick`: keep commit as is.
- `squash`: meld commit into previous commit with combined message.
- `fixup`: meld commit into previous commit, discarding its message.

**Key Takeaway:** Keep pull request git history readable with self-contained, descriptive atomic commits."""
    },
    {
        "category": "Git",
        "title": "Git Worktrees for Multi-Branch Parallel Development",
        "slug": "git-worktrees-workflow",
        "content": """### Git Worktrees for Multi-Branch Parallel Development

Switching branches with `git checkout` stashes uncommitted changes. `git worktree` allows checking out multiple branches into separate directories simultaneously.

```bash
git worktree add ../project-hotfix hotfix/critical-patch
cd ../project-hotfix
npm test
cd ../main-project
git worktree remove ../project-hotfix
```

**Key Takeaway:** Use worktrees to tackle urgent hotfixes or code reviews without stashing local work."""
    },
    {
        "category": "Docker",
        "title": "Docker Multi-Stage Builds for Minimal Production Images",
        "slug": "docker-multistage-builds",
        "content": """### Docker Multi-Stage Builds for Minimal Production Images

Multi-stage builds separate the compilation toolchain from the final lean runtime environment.

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine AS runner
WORKDIR /app
COPY --from=builder /app/dist ./dist
CMD ["node", "dist/index.js"]
```

**Key Takeaway:** Multi-stage builds reduce final image size and eliminate build tool attack surfaces."""
    },
    {
        "category": "Docker",
        "title": "Optimizing Docker Layer Caching for Fast Rebuilds",
        "slug": "docker-layer-caching",
        "content": """### Optimizing Docker Layer Caching for Fast Rebuilds

Docker invalidates layer caches as soon as a copied file changes. Ordering instructions by volatility speeds up CI builds dramatically.

```dockerfile
COPY package*.json ./
RUN npm ci
COPY . .
```

**Key Takeaway:** Copy dependency manifests and install packages before copying application source code."""
    },
    {
        "category": "Linux",
        "title": "Inspecting System I/O Bottlenecks with Pidstat and Iotop",
        "slug": "linux-io-inspection-iotop",
        "content": """### Inspecting System I/O Bottlenecks with Pidstat and Iotop

When server load climbs and `top` shows high `%wa` (I/O wait), diagnose the responsible process with `iotop` or `pidstat`.

```bash
sudo iotop -o -P
pidstat -d 2 5
```

**Key Takeaway:** Distinguish between sequential bulk writes and random seek thrashing before re-provisioning disk storage."""
    },
    {
        "category": "Linux",
        "title": "Inspecting Network Listening Sockets with ss",
        "slug": "linux-ss-lsof-network-debug",
        "content": """### Inspecting Network Listening Sockets with ss

The modern `ss` utility is significantly faster than legacy `netstat` for inspecting open ports and network socket states.

```bash
ss -tulpn
ss -tulpn | grep :8080
```

**Key Takeaway:** Replace `netstat` with `ss -tulpn` in debugging scripts for better performance on busy servers."""
    },
    {
        "category": "Security",
        "title": "Preventing Timing Attacks with Constant-Time Comparison",
        "slug": "security-constant-time-comparison",
        "content": """### Preventing Timing Attacks with Constant-Time Comparison

Standard string comparison terminates on the first mismatched byte, allowing attackers to measure execution latency.

```python
import hmac

if hmac.compare_digest(user_token, secret_token):
    grant_access()
```

**Key Takeaway:** Always use constant-time comparison methods (`hmac.compare_digest`) for cryptographic verification."""
    },
    {
        "category": "Algorithms",
        "title": "Sliding Window Pattern for Efficient Subarray Processing",
        "slug": "algo-sliding-window-pattern",
        "content": """### Sliding Window Pattern for Efficient Subarray Processing

Calculating properties over contiguous subarrays using nested loops takes $O(N^2)$ time. The sliding window technique maintains rolling state in $O(N)$ linear time.

```python
def max_subarray_sum(nums: list[int], k: int) -> int:
    if len(nums) < k:
        return 0
    window_sum = sum(nums[:k])
    max_sum = window_sum
    for i in range(k, len(nums)):
        window_sum += nums[i] - nums[i - k]
        max_sum = max(max_sum, window_sum)
    return max_sum
```

**Key Takeaway:** Use sliding window whenever computing metrics over fixed or variable contiguous sequences."""
    },
    {
        "category": "Architecture",
        "title": "Transactional Outbox Pattern for Microservices",
        "slug": "arch-outbox-pattern",
        "content": """### Transactional Outbox Pattern for Microservices

Directly updating a database and publishing an event to a message broker in the same request risks partial failure if the broker is unreachable.

**Outbox Solution:**
1. Save business data and domain event into an `outbox` table within the **same local ACID database transaction**.
2. A separate background worker tails the `outbox` table and publishes messages to the broker.

**Key Takeaway:** The Transactional Outbox pattern guarantees at-least-once message delivery without distributed two-phase commits."""
    }
]

# Definisi 6 slot waktu sepanjang hari (WIB = UTC + 7)
SLOTS = [
    {"id": 0, "name": "Pagi Hari (~08:30 WIB)", "utc_range": (0, 3)},
    {"id": 1, "name": "Menjelang Siang (~11:15 WIB)", "utc_range": (3, 6)},
    {"id": 2, "name": "Siang Hari (~14:20 WIB)", "utc_range": (6, 9)},
    {"id": 3, "name": "Sore Hari (~17:40 WIB)", "utc_range": (9, 12)},
    {"id": 4, "name": "Malam Hari (~20:25 WIB)", "utc_range": (12, 15)},
    {"id": 5, "name": "Larut Malam (~23:15 WIB)", "utc_range": (15, 18)},
]

TRACKER_FILE = "data/tracker.json"

def get_current_slot(utc_hour):
    for slot in SLOTS:
        start, end = slot["utc_range"]
        if start <= utc_hour < end:
            return slot
    return SLOTS[-1]

def load_or_init_tracker(today_str, force=False):
    os.makedirs("data", exist_ok=True)
    data = {}
    if os.path.exists(TRACKER_FILE):
        try:
            with open(TRACKER_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {}

    current_date = data.get("current_date")
    if current_date != today_str:
        # Hari baru! Roll target acak 3 sampai 5 commit per hari
        target = random.choice([3, 4, 5])
        selected_slots = sorted(random.sample(range(len(SLOTS)), target))
        
        history = data.get("history", [])
        if current_date:
            history.append({
                "date": current_date,
                "commits": data.get("commits_today", 0),
                "target": data.get("daily_target", 0)
            })
            history = history[-30:]
            
        data = {
            "current_date": today_str,
            "daily_target": target,
            "selected_slots": selected_slots,
            "completed_slots": [],
            "commits_today": 0,
            "total_commits": data.get("total_commits", 0),
            "history": history
        }
    return data

def save_tracker(data):
    with open(TRACKER_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

def set_github_output(should_commit, commit_msg=""):
    gh_output = os.environ.get("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a", encoding="utf-8") as f:
            f.write(f"should_commit={'true' if should_commit else 'false'}\n")
            f.write(f"commit_msg={commit_msg}\n")

def get_next_topic(notes_dir):
    os.makedirs(notes_dir, exist_ok=True)
    existing_files = os.listdir(notes_dir)
    used_slugs = set()
    for f in existing_files:
        if f.endswith(".md"):
            parts = f.replace(".md", "").split("-")
            if len(parts) >= 4:
                slug = "-".join(parts[3:])
                used_slugs.add(slug)
                
    available = [t for t in TOPICS if t["slug"] not in used_slugs]
    if available:
        return random.choice(available)
    return random.choice(TOPICS)

def update_readme(notes_dir):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        return

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()

    start_marker = "<!-- RECENT_NOTES_START -->"
    end_marker = "<!-- RECENT_NOTES_END -->"

    if start_marker not in content or end_marker not in content:
        return

    files = sorted([f for f in os.listdir(notes_dir) if f.endswith(".md")], reverse=True)
    recent = files[:10]

    list_items = []
    for f in recent:
        name_no_ext = f.replace(".md", "")
        parts = name_no_ext.split("-", 3)
        date_part = "-".join(parts[:3]).split("_")[0]
        slug_part = parts[-1] if len(parts) >= 4 else "Dev Note"
        title = slug_part.replace("-", " ").title()
        list_items.append(f"- `[{date_part}]` [{title}](notes/{f})")

    table_str = "\n" + "\n".join(list_items) + "\n"
    before = content.split(start_marker)[0] + start_marker
    after = end_marker + content.split(end_marker)[1]

    new_content = before + table_str + after
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    force = "--force" in sys.argv
    status_only = "--status" in sys.argv
    
    wib = timezone(timedelta(hours=7))
    now_wib = datetime.now(wib)
    today_str = now_wib.strftime("%Y-%m-%d")
    time_str = now_wib.strftime("%H%M")
    utc_now = datetime.now(timezone.utc)
    current_slot = get_current_slot(utc_now.hour)

    tracker = load_or_init_tracker(today_str, force=force)
    
    if status_only:
        print(f"Date: {tracker['current_date']}")
        print(f"Daily Target: {tracker['daily_target']} commits")
        print(f"Selected Slots: {[SLOTS[i]['name'] for i in tracker['selected_slots']]}")
        print(f"Completed Slots: {[SLOTS[i]['name'] for i in tracker['completed_slots']]}")
        print(f"Commits Done Today: {tracker['commits_today']}")
        print(f"Current Slot: {current_slot['name']}")
        return

    target = tracker["daily_target"]
    done = tracker["commits_today"]
    selected = tracker["selected_slots"]
    completed = tracker["completed_slots"]
    slot_id = current_slot["id"]

    should_commit = False
    reason = ""

    if force:
        should_commit = True
        reason = "Manual / Force trigger"
    elif done >= target:
        should_commit = False
        reason = f"Target {target} commits already achieved today ({done}/{target})"
    elif slot_id in selected and slot_id not in completed:
        should_commit = True
        reason = f"Slot {current_slot['name']} matched scheduled selection"
    else:
        remaining_slots_count = len([s for s in range(slot_id, len(SLOTS)) if s not in completed])
        needed = target - done
        if remaining_slots_count <= needed and slot_id not in completed:
            should_commit = True
            reason = f"Catch-up mode: needed {needed} commits with {remaining_slots_count} slots remaining"
        else:
            should_commit = False
            reason = f"Slot {current_slot['name']} skipped for natural commit pacing (Done: {done}/{target})"

    print(f"[{today_str} {time_str} WIB] Slot: {current_slot['name']}")
    print(f"Target: {target} | Done: {done} | Reason: {reason}")

    if not should_commit:
        set_github_output(False)
        print(">> No commit required for this run.")
        save_tracker(tracker)
        return

    notes_dir = "notes"
    topic = get_next_topic(notes_dir)
    filename = f"{today_str}_{time_str}-{topic['slug']}.md"
    filepath = os.path.join(notes_dir, filename)

    note_body = f"""# {topic['title']}

- **Date:** {today_str} {now_wib.strftime('%H:%M')} WIB
- **Category:** `{topic['category']}`
- **Source:** Dev Knowledge Base & Systems Architecture

---

{topic['content']}
"""

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(note_body)

    update_readme(notes_dir)

    tracker["commits_today"] += 1
    tracker["total_commits"] = tracker.get("total_commits", 0) + 1
    if slot_id not in tracker["completed_slots"]:
        tracker["completed_slots"].append(slot_id)
    tracker["last_commit_time"] = now_wib.isoformat()
    save_tracker(tracker)

    prefixes = ["feat(til)", "docs(notes)", "docs(til)", "refactor(snippet)", "perf(notes)", "chore(notes)"]
    prefix = random.choice(prefixes)
    commit_msg = f"{prefix}: add {topic['title'].lower()} [{today_str}]"

    print(f">> Generated: {filepath}")
    print(f">> Commit Message: {commit_msg}")
    print(f">> Progress Today: {tracker['commits_today']}/{tracker['daily_target']}")

    set_github_output(True, commit_msg)

if __name__ == "__main__":
    main()
