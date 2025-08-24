# --- Stage 1: Builder ---
FROM node:24-alpine AS builder

# Disable Corepack prompt and enable Corepack
ENV COREPACK_ENABLE_PROMPT=0
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy package files first to leverage Docker cache
COPY package.json pnpm-lock.yaml ./

# Install dependencies (use --frozen-lockfile for reproducibility)
RUN pnpm install --frozen-lockfile

# Copy the rest of the application
COPY . .

# Build the app
RUN pnpm run build

# --- Stage 2: Runtime ---
FROM node:24-alpine AS runtime

# Install only necessary runtime dependencies
RUN apk add --no-cache tini
ENTRYPOINT ["/sbin/tini", "--"]

# Create a non-root user for security
RUN addgroup -g 1001 -S nodejs && \
    adduser -S class-ease -u 1001

# Enable Corepack in runtime
ENV COREPACK_ENABLE_PROMPT=0
RUN corepack enable

WORKDIR /ClassEase-Pitch

# Copy built files from builder stage with proper ownership
COPY --from=builder --chown=class-ease:nodejs /app .

# Switch to non-root user
USER class-ease

EXPOSE 5173

CMD ["pnpm", "run", "dev"]
