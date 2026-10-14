# Docker Multi-Stage Builds for Minimal Production Images

- **Date:** 2026-10-14 19:55 WIB
- **Category:** `Docker`
- **Source:** Dev Knowledge Base & Systems Architecture

---

### Docker Multi-Stage Builds for Minimal Production Images

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

**Key Takeaway:** Multi-stage builds reduce final image size and eliminate build tool attack surfaces.
