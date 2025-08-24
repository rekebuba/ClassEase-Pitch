# --- Stage 1: Builder ---
FROM node:24-alpine AS builder

# Disable Corepack prompt
ENV COREPACK_ENABLE_PROMPT=0

# Enable Corepack and prepare pnpm (auto-accepts download)
RUN corepack enable && corepack prepare pnpm@latest --activate

WORKDIR /app

# Copy package files
COPY package.json pnpm-lock.yaml ./

# Install dependencies (Corepack will auto-use pnpm)
RUN pnpm install

# Copy the rest and build
COPY . ./

# Build the app
RUN pnpm run build

# --- Stage 2: Runtime ---
FROM node:24-alpine

# Install git and other build tools
RUN apk add --no-cache git

# Enable Corepack in runtime
RUN corepack enable

WORKDIR /ClassEase-Pitch

# Copy built files
COPY --from=builder /app ./

EXPOSE 5173
CMD ["pnpm", "run", "dev"]
