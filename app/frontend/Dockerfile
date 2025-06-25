# --- Stage 1: Builder ---
FROM node:24-alpine AS builder

# Install git and other build tools
RUN apk add --no-cache git

# Enable pnpm via corepack
RUN corepack enable pnpm

# Set working directory
WORKDIR /app

# Copy only the necessary files for dependency resolution
COPY package.json pnpm-lock.yaml ./

# Install dependencies
RUN pnpm install

# Copy the rest of the frontend source code
COPY . ./

# Build the app
RUN pnpm run build

# --- Stage 2: Runtime ---
FROM node:24-alpine

# Enable pnpm via corepack
RUN corepack enable pnpm

# Set working directory
WORKDIR /ClassEase-Pitch

# Install pnpm globally again (for runtime usage like `pnpm run dev`)
RUN npm install -g pnpm

# Copy only the built output from the builder
COPY --from=builder /app/ ./

# Expose Vite default port
EXPOSE 5173

# Start development server
CMD ["pnpm", "run", "dev"]
