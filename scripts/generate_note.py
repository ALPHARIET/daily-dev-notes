import os
import sys
import random
from datetime import datetime, timezone, timedelta

# Data kumpulan catatan dev berkualitas & realistis
DEV_TOPICS = [
    {
        "category": "Python",
        "title": "Optimizing Memory with Python Generators",
        "slug": "python-generators-memory",
        "content": """### Optimizing Memory with Python Generators

When processing large datasets or reading massive log files, loading everything into a list can quickly consume available RAM. Using Python generators (`yield`) computes items on-the-fly with $O(1)$ memory consumption.

```python
def read_large_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            yield line.strip()

# Memory stays constant regardless of file size
for record in read_large_file("huge_dataset.csv"):
    process(record)
```

**Key Takeaway:** Prefer generator expressions and iterator functions when data does not strictly need random access indexing.
"""
    },
    {
        "category": "TypeScript",
        "title": "Using Discriminated Unions for Strict Type Safety",
        "slug": "typescript-discriminated-unions",
        "content": """### Using Discriminated Unions for Strict Type Safety

Discriminated unions (tagged unions) provide pattern matching-like type safety in TypeScript by sharing a common literal property across shapes.

```typescript
type ApiResponse<T> = 
  | { status: "success"; data: T }
  | { status: "error"; error: string; code: number };

function handleResponse<T>(res: ApiResponse<T>) {
  if (res.status === "success") {
    // TypeScript automatically narrows res to the success object
    console.log(res.data);
  } else {
    // res is safely narrowed to error object
    console.error(`[${res.code}] ${res.error}`);
  }
}
```

**Key Takeaway:** Avoid optional fields for states that are mutually exclusive; use distinct literal tags instead.
"""
    },
    {
        "category": "Git",
        "title": "Useful Git Log Formatting for Clean History",
        "slug": "git-pretty-log-formatting",
        "content": """### Useful Git Log Formatting for Clean History

Instead of scrolling through verbose default `git log` output, an alias with graph and branch decoration makes commit trees readable at a glance.

```bash
git log --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
```

Or configure it permanently in your `.gitconfig`:
```bash
git config --global alias.lg "log --graph --oneline --decorate --all"
```

**Key Takeaway:** Clean log visualizers help catch branch divergence early before complex merges.
"""
    },
    {
        "category": "Web Dev",
        "title": "CSS Subgrid for Consistent Card Layouts",
        "slug": "css-subgrid-card-layouts",
        "content": """### CSS Subgrid for Consistent Card Layouts

With modern CSS `subgrid`, child elements inside a grid item can align seamlessly to the parent grid lines, solving the classic problem of uneven card headers and footers.

```css
.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.card {
  display: grid;
  grid-template-rows: subgrid;
  grid-row: span 3; /* Header, Body, Footer */
}
```

**Key Takeaway:** Subgrid eliminates brittle fixed-height hacks across responsive card grids.
"""
    },
    {
        "category": "Backend",
        "title": "Database Connection Pooling Best Practices",
        "slug": "database-connection-pooling",
        "content": """### Database Connection Pooling Best Practices

Creating a new TCP/TLS connection to PostgreSQL or MySQL on every HTTP request introduces significant latency and exhausts database file descriptors.

**Core Rules:**
1. Maintain an active pool with reasonable min/max connections (e.g., $10 - 20$ workers per node).
2. Set aggressive connection acquisition timeouts ($2-5$ seconds) to fail fast under overload instead of piling up queued requests.
3. Recycle connections periodically to prevent stale state and memory leaks.

**Key Takeaway:** More connections do not equal more throughput; optimal pool size is bounded by CPU core count and disk I/O.
"""
    },
    {
        "category": "Linux",
        "title": "Inspecting High Disk I/O with iotop and pidstat",
        "slug": "linux-io-inspection-iotop",
        "content": """### Inspecting High Disk I/O with iotop and pidstat

When a server feels sluggish and `top` shows high `%wa` (I/O wait), identify the culprit process using `iotop` or `pidstat`.

```bash
# Watch real-time disk read/write per process
sudo iotop -o -P

# Check I/O stats every 2 seconds for 5 intervals
pidstat -d 2 5
```

**Key Takeaway:** Distinguish between sequential bulk writes and random seek thrashing before upgrading storage hardware.
"""
    },
    {
        "category": "React",
        "title": "When to Avoid useEffect in Modern React",
        "slug": "react-avoid-redundant-useeffect",
        "content": """### When to Avoid useEffect in Modern React

A common anti-pattern is using `useEffect` to transform data for rendering or syncing state based on props.

```jsx
// ❌ Anti-pattern: Redundant state + extra render cycle
const [filtered, setFiltered] = useState([]);
useEffect(() => {
  setFiltered(items.filter(i => i.active));
}, [items]);

// ✅ Correct: Derive state directly during render
const filtered = useMemo(() => items.filter(i => i.active), [items]);
```

**Key Takeaway:** If a value can be computed from existing props or state, compute it directly during render.
"""
    },
    {
        "category": "DevOps",
        "title": "Docker Multi-Stage Builds for Minimal Image Size",
        "slug": "docker-multistage-builds",
        "content": """### Docker Multi-Stage Builds for Minimal Image Size

Multi-stage builds separate the compilation environment (SDKs, build tools, package managers) from the final production runtime.

```dockerfile
# Stage 1: Build
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Minimal Runtime
FROM node:20-alpine AS runner
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/dist ./dist
RUN npm ci --omit=dev
USER node
CMD ["node", "dist/index.js"]
```

**Key Takeaway:** Keep build tools out of production containers to reduce attack surface and decrease deployment download times.
"""
    },
    {
        "category": "Security",
        "title": "Preventing Timing Attacks with Constant-Time Comparison",
        "slug": "security-constant-time-comparison",
        "content": """### Preventing Timing Attacks with Constant-Time Comparison

Standard string comparison (`a == b`) terminates as soon as the first mismatched byte is encountered. Attackers can measure response latency to deduce tokens or password hashes byte-by-byte.

```python
import hmac

# ❌ Vulnerable to timing side-channel:
# if user_token == secret_token: ...

# ✅ Safe constant-time comparison:
if hmac.compare_digest(user_token, secret_token):
    grant_access()
```

**Key Takeaway:** Always use constant-time comparison functions for API keys, session signatures, and cryptographic secrets.
"""
    },
    {
        "category": "API Design",
        "title": "Idempotency Keys for Safe Payment & Mutation Endpoints",
        "slug": "api-idempotency-keys",
        "content": """### Idempotency Keys for Safe Payment & Mutation Endpoints

Network drops or client retry logic can cause duplicate transactions if the server does not enforce idempotency.

**Standard Pattern:**
1. Client sends a unique `Idempotency-Key: <uuid>` header on `POST` requests.
2. Server stores the request key in Redis/DB with an expiration TTL (e.g. 24h).
3. If an identical key arrives within the TTL, return the cached previous response without re-executing business logic.

**Key Takeaway:** Critical mutation endpoints should always be idempotent against retries.
"""
    }
]

def main():
    wib = timezone(timedelta(hours=7))
    today_wib = datetime.now(wib)
    date_str = today_wib.strftime("%Y-%m-%d")
    
    notes_dir = "notes"
    os.makedirs(notes_dir, exist_ok=True)
    
    # Pilih topik berdasarkan hari dalam tahun agar variatif dan deterministik
    day_of_year = today_wib.timetuple().tm_yday
    topic = DEV_TOPICS[day_of_year % len(DEV_TOPICS)]
    
    filename = f"{date_str}-{topic['slug']}.md"
    filepath = os.path.join(notes_dir, filename)
    
    note_content = f"""# {topic['title']}

- **Date:** {date_str}
- **Category:** `{topic['category']}`
- **Source:** Dev Insights & Architecture Practice

---

{topic['content']}
"""
    
    # Tulis / update file note
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(note_content)
        
    print(f"Generated note: {filepath}")
    
    # Update README Recent Notes
    update_readme(notes_dir)
    
    # Siapkan commit message bergaya conventional commit yang meyakinkan
    prefixes = ["docs(notes)", "feat(til)", "chore(notes)", "docs(til)"]
    prefix = random.choice(prefixes)
    commit_msg = f"{prefix}: add {topic['title'].lower()} [{date_str}]"
    
    # Output ke GitHub Actions environment jika berjalan di runner
    github_output = os.environ.get("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"commit_msg={commit_msg}\n")
            
    print(f"Commit message: {commit_msg}")

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
    recent = files[:5]
    
    list_items = []
    for f in recent:
        title = f.replace(".md", "").split("-", 3)[-1].replace("-", " ").title()
        date_part = "-".join(f.split("-")[:3])
        list_items.append(f"- `[{date_part}]` [{title}](notes/{f})")
        
    table_str = "\n" + "\n".join(list_items) + "\n"
    
    before = content.split(start_marker)[0] + start_marker
    after = end_marker + content.split(end_marker)[1]
    
    new_content = before + table_str + after
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)

if __name__ == "__main__":
    main()
